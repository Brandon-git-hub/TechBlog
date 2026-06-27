---
layout: post
title: "U-Boot 與 Linux Kernel 編譯、移植與部署自動化實作筆記"
subtitle: "基於 BeagleBone Black 平台之建立交叉編譯與 AI 輔助開發工作流"
categories: [Linux]
date: 2026-06-25
lang: zh-Hant
---

## 摘要 (Abstract)

本文實作並記錄基於 BeagleBone Black 開發板 (核心為德州儀器 TI Sitara AM3358 處理器) 之嵌入式 Linux 系統建置流程。涵蓋自底層硬體與虛擬化開發主機環境之建構、交叉編譯工具鏈之配置、U-Boot 與 Linux 核心（Kernel）原始碼之編譯，乃至最終開機引導程式與核心映像檔於安全數位卡（SD Card）之部署。 為了提升開發效率節省硬體資源，利用指令行工具 `vmrun` 進行虛擬機無介面（Headless）背景運行管理，並在 Windows 宿主端 (Host) 透過 SSH 連線至虛擬機（Guest）進行遠端開發。 此外，除了搭建傳統 Samba Server 配合 PuTTY 終端機的遠端模式，另外也整合了類 VS Code 的現代人工智慧輔助整合開發環境（AI-Assisted IDE）之工作流，透過一套 `tasks.json` 自動化建構與部署，提升嵌入式 BSP（板級支持包）開發效率。

---

## 1. 開發環境 (硬體、虛擬機、專案目錄)


### 1.1 硬體與序列埠除錯工具
* **開發板**： **TI AM335x BeagleBone Black (BBB)** 。核心為 Sitara™ AM335x ARM® Cortex®-A8 處理器，配備 512MB DDR3 RAM、4GB 8 位元 eMMC 板載 flash 儲存，有 USB Host、Ethernet、HDMI 等介面。
* **序列埠除錯工具**：為了接收系統啟動 Log，使用 USB 轉 UART 除錯模組（如 FT232, CP2102, CH340 等）。
  * 板子上的 **J1 Header**：原理圖可以到官方 Github 獲取，[beagleboard/beaglebone-black GitHub](https://github.com/beagleboard/beaglebone-black/tree/master)，第 1 腳位為 `GND`，第 4 腳位為 `RX`，第 5 腳位為 `TX`。
  * 參數配置：波特率（Baud Rate）設為 **115200 bps、資料位元 8-bit、無校驗位、停止位元 1-bit，無硬體流控制（8N1）**。

<!-- ![](/assets/26_0625/BBB_J1_header.png) -->

<p align="center">
<img src="{{ '/assets/26_0625/BBB_J1_header.png' | relative_url }}" width="600">
</p>

### 1.2 虛擬機
本實作之編譯工作完全在宿主機（Host）的虛擬機 Linux 環境（Ubuntu）下進行。
至於為何要虛擬機呢? 不能在 Windows 下直接編譯嗎? 主要原因有三：
1. **交叉編譯工具鏈與 Linux 核心編譯環境**：Linux 核心與 U-Boot 的編譯工具鏈（GCC, Make等）原生支援 Linux 平台。
2. **WSL 對於硬體周邊支援度低**：Windows 現下事實上已有 Windows Subsystem for Linux (WSL2) ，其運行 Microsoft 維護的輕量級 Linux kernl，但其對於 USB devices 的掛載相較麻煩，需要 usbipd 工具手動掛載，考量到我是新手，虛擬機的隔離性與穩定性更高，故仍選擇虛擬機。
3. **虛擬機的快照與還原功能**：虛擬機快照功能更方便，可以避免說配置錯誤導致系統混亂，可回到之前保存的狀態。

事實上，還有可以選擇像 Docker 這種容器化的方式，不過其配置麻煩和操作流暢度較低，未來再挑戰看看。

* **虛擬化管理器（Hypervisor）**：使用VMware Workstation Player ，也可使用開源的 Oracle VM VirtualBox，但聽說 Bug 較多。
* **客體作業系統（Guest OS）**：Ubuntu Linux Desktop 24.04 LTS。
* **資源配置分配原則**：
  * **硬碟空間**：建議配置 **40 GB 以上**之虛擬硬碟空間。Kernel 與 U-Boot 編譯會產生大量中間檔。
  * **記憶體（RAM）**：建議配置 **8 GB 以上**，太少容易 OOM（Out of Memory）。
  * **處理器（CPU）核心數**：建議配置**小於 Host 實體核心數**。由於編譯 Kernel 較久，所以會使用多核心平行編譯。

### 1.3 專案目錄

為了方便管理與維護，所有 BSP（板級支持包）相關的原始碼、編譯產物與根檔案系統皆統一收集於虛擬機使用者目錄下的 `~/beaglebone_linux_bsp`。該目錄下包含四個平行子專案：

* **`u-boot/`**：存放 U-Boot 原始碼，負責編譯產出二進位引導負載程式（`MLO` 與 `u-boot.img`）以及引導腳本（`boot.scr`）。
* **`kernel/`**：存放 Linux 核心原始碼，負責編譯產出核心映像檔（`uImage`）與硬體設備樹二進位檔（`am335x-boneblack.dtb`）。
* **`output/`**：編譯產物統一收集。各子專案編譯完成後，目標檔案複製至此目錄，以利後續統一部署。
* **`rootfs/`**：為後續用於建置與掛載根檔案系統（Root File System）。

---

## 2. 遠端連線虛擬機（包含傳統 Samba + PuTTY 與現代 AI IDE）

### 2.1 傳統 Samba + PuTTY 工作流
在過去嵌入式 Linux 開發中，會在虛擬機內架設 Samba 伺服器，將客體機 Linux 之檔案系統掛載至 Windows 主機端作為網路磁碟，以及使用像 PuTTY 這類的 SSH 終端機連線至虛擬機，手動執行編譯與燒錄指令。
* **Samba 伺服器核心配置**：
  在客體虛擬機（Ubuntu）中安裝 Samba：
  ```bash
  sudo apt-get install -y samba cifs-utils smbclient
  ```
  並編輯 `/etc/samba/smb.conf`。為防止 Windows 與 Linux 字元編碼不一致而導致編譯源碼檔名混亂，須在 `[global]` 中配置：
  ```ini
  [global]
     workgroup = WORKGROUP
     display charset = UTF-8
     unix charset = UTF-8
     dos charset = cp936 (或者繁體中文可使用 cp950)
  ```
  並於設定檔最底端加入對根目錄的共享配置：
  ```ini
  [Share]
     comment = VM Shared Directory
     path = /
     public = yes
     writable = yes
     read only = no
     force directory mode = 0777
     force create mode = 0777
     create mask = 0777
     directory mask = 0777
     guest ok = yes
     available = yes
     browseable = yes
  ```
  設定 Samba 密碼並重啟服務：
  ```bash
  sudo smbpasswd -a username
  sudo systemctl restart smbd
  ```
  在 Windows 系統中，透過「連線網路磁碟機」掛載 `\\<VM_IP>\Share`，並使用 PuTTY 連線至虛擬機之 SSH 伺服器（需安裝 `openssh-server`）執行編譯指令。

### 2.2 現代化 IDE 工作流
VSCode 等現代 IDE 透過 Remote-SSH 擴充套件，能直接在 Windows 主機端編輯虛擬機內的檔案，並在虛擬機中執行編譯等等操作指令。 這樣不管是你要使用 Anthrpic 的 Claude code 或者是 Open AI 的 codex，在 VSCode 他們都有支援套件，而本文中是使用 Google 的 Antigravity IDE，其一樣基於 VSCode 開發，操作上相同。選擇使用現代化 IDE 我認為有以下優勢：
1. **單一視窗工作流整合**：代碼編輯、終端調試與 AI 協同皆整合於單一 IDE 介面，大幅降低環境切換，開發上更流暢。
2. **豐富的擴充套件生態**：VSCode 擁有龐大的擴充套件市場，支援語法高亮、程式碼補全、版本控制、遠端開發等功能，可以任意搭配，適配不同的開發需求，不管是 Windows App, MCU Firmware, Linux 嵌入式系統，可以統一在相同的操作介面下進行，省去適應不同專屬 IDE 的學習成本。
3. **AI 輔助開發**：現在寫軟體基本上已經離不開 AI 的輔助，無論是程式碼補全、錯誤偵測、Code 直接生成，AI 能提供即時的協助，提升開發效率。

---

## 3. 虛擬機背景運行控制

為節省宿主機之系統資源並免去虛擬機圖形介面（GUI）之額外開銷，可將虛擬機配置為 **無介面背景模式（Headless Mode）** 運行。開發人員在客體虛擬機內部配置好 `open-vm-tools` 後，即可直接在 Windows 宿主端透過命令列控制虛擬機之運作。

### 3.1 客體端守護進程配置
虛擬機內部必須安裝開源版 VMware Tools，以配合宿主機發送之管理指令：
```bash
sudo apt-get install -y open-vm-tools
sudo systemctl enable --now open-vm-tools
```

### 3.2 宿主主機雙層控制腳本 (PowerShell / Batch)
在宿主主機（Windows）之 PowerShell 或命令提示字元中，可透過以下指令控制虛擬機：
* **無 GUI 背景啟動虛擬機**：
  ```powershell
  # 語法：vmrun -T ws start "虛擬機組態檔路徑.vmx" nogui
  vmrun -T ws start "C:\Users\User\Documents\Virtual Machines\Ubuntu\Ubuntu.vmx" nogui
  ```
* **安全關閉虛擬機（發送 ACPI 關機訊號）**：
  ```powershell
  # 語法：vmrun -T ws stop "虛擬機組態檔路徑.vmx" soft
  vmrun -T ws stop "C:\Users\User\Documents\Virtual Machines\Ubuntu\Ubuntu.vmx" soft
  ```
* **列出目前運行中之虛擬機**：
  ```powershell
  vmrun list
  ```
另外在此處建立以下兩個腳本檔案，即可實現對虛擬機的一鍵背景控制或選單化管理。

#### 3.2.1 核心控制指令腳本：[`vm_control.ps1`](file:///c:/Users/User/Documents/TechBlog/assets/26_0625/vm_control.ps1)
本腳本支援命令列參數調用，若無參數則會自動開啟一個互動式選單。預設虛擬機對應為 `"Ubuntu"`，其組態檔路徑指向預設的安裝位置。

#### 3.2.2 宿主端便捷啟動批次檔：[`vm_control.bat`](file:///c:/Users/User/Documents/TechBlog/assets/26_0625/vm_control.bat)
此批次檔用於在 Windows Command Line 下快速呼叫 PowerShell 腳本，並自動繞過執行原則（Execution Policy）限制與傳遞參數。
透過此雙層腳本，開發人員只需在 Windows 中執行 `vm_control.bat` 即可啟動互動式控制面板，或執行 `vm_control.bat start Ubuntu nogui` 將虛擬機於背景掛載，隨後即可使用 VS Code 透過 Remote-SSH 直接連入進行無縫開發。

---

## 4. BeagleBone Black 多階段啟動流程

BeagleBone Black 採用複雜的多階段引導機制，以解決上電初期硬體資源極度受限之問題。啟動鏈由四個軟硬體階段依次傳遞（如下圖所示）：

<!-- ![](/assets/26_0625/Linux_boot.svg) -->

<p align="center">
<img src="{{ '/assets/26_0625/Linux_boot.svg' | relative_url }}" width="400">
</p>

### 4.1 唯讀記憶體引導階段 (ROM Code / Initial Boot Stage)
* **存放位置**：固化於 AM3358 SoC 內部唯讀記憶體（ROM）中。
* **硬體制約與行為**：上電瞬間，外部 DDR3 DRAM 尚未被初始化，僅有晶片內部約 64KB 之 SRAM 可供使用。ROM Code 會根據硬體引腳電位（例如按住開發板上的 `BOOT` 按鍵）決定引導順序。
* **核心職責**：偵測並引導安全數位卡（SD Card / mmc0）或快閃記憶體（eMMC / mmc1）。ROM Code 會在啟動設備的 FAT32 分區（一般為第一分區）中搜尋名為 **`MLO`** (Secondary Program Loader) 的檔案，並將其搬移至內部 SRAM 中執行。

### 4.2 次級程式引導階段 (U-Boot SPL / MLO)
* **存放位置**：SD 卡第一分區（FAT32，標籤為 `boot`），必須命名為 **`MLO`**。
* **引導動機**：由於完整的 U-Boot 主程式映像檔（`u-boot.img`）體積達數百 KB，無法裝入僅有 64KB 的 SRAM 中。因此，需先編譯一個經過高度裁減的先鋒程式 —— SPL（次級程式引導器）。
* **核心職責**：**初始化板載的 512MB DDR3 DRAM 記憶體**，使其可用。隨後，MLO 會從 SD 卡中讀取完整的引導映像檔 **`u-boot.img`**，將其搬移至 DDR3 記憶體中，並將執行權交出。

### 4.3 引導加載程式主階段 (U-Boot Main / u-boot.img)
* **存放位置**：SD 卡第一分區，檔名為 **`u-boot.img`**。
* **交互機制**：U-Boot 主程式啟動後，會透過序列埠輸出倒數計時（例如 `Hit any key to stop autoboot`）。此時，**在偵錯終端按下鍵盤任意鍵（如空白鍵），即可攔截引導程序**，進入 U-Boot 命令列介面（`=>`）。此互動介面由 `u-boot.img` 提供，而非底層 ROM Code。
* **自動引導劇本**：若未被攔截，U-Boot 會依序加載以下三個關鍵檔案：
  1. **開機腳本 (`boot.scr`)**：由純文字腳本 `boot.cmd` 透過 `mkimage` 工具封裝而成之二進位引導腳本。其內容指示 U-Boot 將核心與設備樹撈取至指定記憶體位址，並發動引導。
  2. **設備樹二進位檔 (`am335x-boneblack.dtb`)**：提供給核心的**硬體結構說明書**。由於 Linux 核心不包含硬編碼的硬體暫存器位址，核心必須依賴此設備樹檔案（DTB）來辨識板載的硬體資源（如序列埠、乙太網路控制器、GPIO 腳位等）。
  3. **核心映像檔 (`uImage`)**：封裝有 U-Boot 標頭（64 位元組）之 Linux 核心本體。
  * U-Boot 將上述檔案成功搬移至記憶體後，會呼叫 `bootm` 指令，將處理器控制權轉移至核心入口，隨後 U-Boot 退出記憶體並下班。

### 4.4 核心初始化與根檔案系統掛載階段 (Linux Kernel & Rootfs)
* **核心行為**：Linux 核心獲取控制權後，輸出 `Starting kernel ...` 訊息。核心透過設備樹初始化晶片之時鐘、驅動周邊控制器，並偵測儲存媒介。
* **根目錄掛載**：核心初始化完畢後，會依據啟動參數（`bootargs`），掛載 SD 卡的第二分區（通常為 Ext3/Ext4 分區，標籤為 **`rootfs`**）作為根目錄 `/`。核心隨後啟動使用者空間的第一個進程 `/sbin/init`，調用各種初始化服務，最終透過序列埠終端拋出使用者登入提示字元（`beaglebone login:`）。

### 4.5 清除板載 eMMC 防止開機干擾 (eMMC Content Erasing)
BeagleBone Black 出廠時，其板載 eMMC 已預燒錄 Debian 作業系統。若未加以清除，系統開機時可能會優先自 eMMC 啟動舊版引導程式，進而干擾 SD 卡之移植測試。因此，建議在 U-Boot 命令列下強制擦除 eMMC 的引導磁區（`mmc0` 為 SD 卡，`mmc1` 為 eMMC）：
```bash
# 切換至板載 eMMC 設備
=> mmc dev 1
# 擦除引導區段 (自 Block 0 開始，擦除 0x20000 個區塊)
=> mmc erase 0 20000
```

---

## 5. 原始碼和編譯工具 (交叉編譯工具、U-boot&kernel)

### 5.1 交叉編譯工具鏈之原理與部署
由於宿主機 CPU 架構（一般為 x86_64）與目標板 CPU 架構（ARMv7-A，32-bit）不同，宿主機無法直接執行為目標板設計的機器碼，因此必須引入**交叉編譯工具鏈（Cross-Compiler Toolchain）**。
在 Ubuntu 系統中，可直接透過進階軟體包工具（APT）安裝適用於 ARM 32-bit 架構之 GCC 編譯器：
```bash
sudo apt-get update
sudo apt-get install -y gcc-arm-linux-gnueabi build-essential
```
此工具鏈之前綴為 `arm-linux-gnueabi-`，主要針對無硬體浮點協處理器或使用軟浮點（Soft-float）ABI 之 ARM 設備；若目標平台支援硬體浮點運算，亦可採用 `arm-linux-gnueabihf-`。

### 5.2 U-Boot 與 Linux Kernel 源碼獲取
引導負載程式與作業系統核心原始碼可自官方託管倉庫取得：
* **U-Boot 原始碼**：
  ```bash
  git clone git://git.denx.de/u-boot.git
  cd u-boot
  ```
* **Linux Kernel 原始碼**（以 BeagleBoard 官方維護且長期維護之穩定分支 v6.6 為例）：
  ```bash
  git clone --depth 1 --single-branch --branch v6.6.58-ti-arm32-r15 https://github.com/beagleboard/linux.git
  ```

### 5.3 版本倉庫之物理瘦身與編譯最佳化 (Repository Pruning)
大型專案原始碼倉庫（特別是 Linux Kernel）之 Git 歷史記錄與多架構代碼極為龐大，不僅佔用磁碟空間，亦會嚴重降低 IDE 目錄解析與索引建立之速度。本報告提出以下物理瘦身策略：
1. **深度限制拉取 (Shallow Clone)**：使用 `--depth 1` 參數拉取源碼，僅保留最新一筆 Commit 歷史，避免下載過往數十萬筆歷史變更。
2. **清除 Git 冗餘快取與積極垃圾回收**：
   對於已存在的完整 Git 倉庫，可執行以下指令強制物理刪除歷史指針快取並回收硬碟空間：
   ```bash
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   rm -f .git/FETCH_HEAD .git/ORIG_HEAD .git/packed-refs
   git gc --prune=now --aggressive
   git fsck --lost-found
   # 停用 Tag 自動抓取並限定分支
   git config remote.origin.tagOpt --no-tags
   git config remote.origin.fetch "+refs/heads/master:refs/remotes/origin/master"
   git remote prune origin
   ```
3. **物理剔除無關之 CPU 架構目錄**：
   Linux 核心與 U-Boot 支援數十種處理器架構。對於 ARM 開發，除了 `arch/arm` 外的其餘架構目錄（如 `mips`, `powerpc`, `x86`, `riscv` 等）皆可安全物理刪除，以大幅縮減原始碼體積：
   ```bash
   cd arch/
   find . -maxdepth 1 -type d ! -name '.' ! -name 'arm' -exec rm -rf {} +
   cd ..
   ```

---

## 6. U-boot 與 Linux kernel 編譯和打包

### 6.1 U-Boot 編譯流程
1. **宣告環境變數與清除快取**：
   ```bash
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-gnueabi-
   make distclean
   ```
2. **配置目標板設定檔**：
   ```bash
   make am335x_evm_config
   ```
3. **啟用舊版映像檔格式支援 (Legacy Image Format)**：
   執行 `make menuconfig` 進入選單介面，依循以下路徑：
   `Boot options` ---> `Boot images` ---> 勾選 `[*] Enable support for the legacy image format`。存檔後退出。此項設定極為關鍵，否則 U-Boot 後續將無法辨識核心產出之 `uImage` 格式。
4. **平行編譯**：
   ```bash
   make -j$(nproc)
   ```
   編譯成功後，根目錄下將產生次級引導映像檔 `MLO` 與引導程式主映像檔 `u-boot.img`。

### 6.2 Linux Kernel 編譯流程
1. **配置目標板設定檔**（將編譯中間檔輸出至專屬目錄，以保持原始碼樹潔淨）：
   ```bash
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-gnueabi-
   make O=build_image/build omap2plus_defconfig
   ```
2. **編譯核心映像檔與設定載入位址**：
   編譯 `uImage` 時，必須顯式指定實體記憶體載入位址 `LOADADDR=0x80008000`。
   ```bash
   make -j$(nproc) O=build_image/build LOADADDR=0x80008000 uImage
   ```
   > [!IMPORTANT]
   > **LOADADDR=0x80008000 之科學原理**：
   > 核心映像檔 `uImage` 實質上是由壓縮後之核心 `zImage` 加上由 `mkimage` 產生之 64 位元組（40H）標頭封裝而成。該標頭紀錄了引導參數、校驗和以及核心在記憶體中的預期載入位址（Load Address，即 `0x80008000`）與入口位址（Entry Point，即 `0x80008040`）。
   > 在 ARM 架構中，系統實體記憶體（DDR DRAM）之物理起始位址通常映射於 `0x80000000`。依據 Linux 核心之啟動規範，前 32KB（即 `0x8000` 位址偏移，亦即 `0x00008000`）必須保留給內核頁表、零頁異常向量與開機參數塊（Agress Parameter Block / ATags）。因此，核心之載入位址必須設為 `0x80000000 + 0x8000 = 0x80008000`。
   若編譯過程中拋出 `lzop: not found` 錯誤，需執行 `sudo apt-get install lzop`；若提示 `mkimage` 命令行不存在，則需將 U-Boot 編譯生成之 `tools/mkimage` 複製至系統執行路徑下：
   ```bash
   sudo cp <u-boot-directory>/tools/mkimage /usr/local/bin/
   ```
3. **編譯設備樹二進位檔 (DTB)**：
   ```bash
   make O=build_image/build dtbs
   ```
   編譯完成後，核心映像檔 `uImage` 將存於 `build_image/build/arch/arm/boot/uImage`；而設備樹二進位檔 `am335x-boneblack.dtb` 則生成於 `build_image/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb` (或舊版核心之 `arch/arm/boot/dts/am335x-boneblack.dtb`)。

---

## 7. 多子專案自動化建置和部屬 (VSCode tasks)

基於平行子專案架構（`u-boot`, `kernel`, `output`, `rootfs`），我們在各工作區目錄下配置對應的 `.vscode/tasks.json`，將各階段之編譯與物理燒錄步驟封裝成自動化任務。

### 7.1 U-Boot 引導專案自動化任務：[`u_boot_tasks_example.json`](file:///c:/Users/User/Documents/TechBlog/assets/26_0625/u_boot_tasks_example.json)
此設定檔配置於 `u-boot/` 目錄下。除了提供編譯任務外，亦封裝了 SD 卡的自動化掛載（利用 `udisksctl` 進行無密碼掛載）與卸載，並在編譯成功後，將 `MLO` 與 `u-boot.img` 複製至平行的 `../output/` 目錄中：

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "🔍 List Device Info",
            "type": "shell",
            "command": "lsblk",
            "problemMatcher": []
        },
        {
            "label": "💾 SD: Mount boot & rootfs",
            "type": "shell",
            "command": "echo '==== Auto Mounting partitions via udisksctl ====' && udisksctl mount -b /dev/sdb1 && udisksctl mount -b /dev/sdb2",
            "problemMatcher": []
        },
        {
            "label": "💾 SD: Unmount & Eject",
            "type": "shell",
            "command": "echo '==== Syncing & Unmounting safely ====' && sync && udisksctl unmount -b /dev/sdb1 && udisksctl unmount -b /dev/sdb2 && echo '==== [SUCCESS] Safe to physical eject SD Card! ===='",
            "problemMatcher": []
        },
        {
            "label": "📁 Boot Proj Size",
            "type": "shell",
            "command": "du -sh .",
            "problemMatcher": []
        },
        {
            "label": "🚀 Compile U-boot",
            "type": "shell",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "command": "export ARCH=arm && export CROSS_COMPILE=arm-linux-gnueabi- && make am335x_evm_config && make && echo '==== Copying Build Artifacts to Output ====' && cp MLO u-boot.img ../output/ && echo '==== DONE! Files safely placed in output/ ===='",
            "problemMatcher": []
        },
        {
            "label": "📚 U-boot Menu",
            "type": "shell",
            "command": "export ARCH=arm && export CROSS_COMPILE=arm-linux-gnueabi- && make menuconfig",
            "problemMatcher": []
        },
        {
            "label": "📜 Boot Script",
            "group": "build",
            "type": "shell",
            "command": "mkimage -C none -A arm -T script -n '@BrandonEmbedded boot scr'  -d boot.cmd boot.scr && echo '==== Copying Script to Output ====' && cp boot.scr ../output/ && echo '==== DONE! Files safely placed in output/ ===='",
            "problemMatcher": []
        }
    ]
}
```

### 7.2 Linux 核心專案自動化任務：[`kernel_tasks_example.json`](file:///c:/Users/User/Documents/TechBlog/assets/26_0625/kernel_tasks_example.json)
此設定檔配置於 `kernel/` 目錄下。它定義了預設的建置配置、`menuconfig` 互動選單，並在平行編譯完成後，將 `uImage` 與 `am335x-boneblack.dtb` 轉移至 `../output/` 目錄：
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "📁 Kernel Proj Size",
            "type": "shell",
            "command": "du -sh .",
            "problemMatcher": []
        },
        {
            "label": "💡 Kernel Defconfig",
            "type": "shell",
            "command": "mkdir -p build_image/build && make O=build_image/build ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- omap2plus_defconfig",
            "problemMatcher": []
        },
        {
            "label": "💡 Kernel Menuconfig",
            "type": "shell",
            "command": "make O=build_image/build ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- menuconfig",
            "problemMatcher": []
        },
        {
            "label": "🚀 Complete Build Kernel & DTB",
            "type": "shell",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "command": "echo '==== [Step 1] Compiling Kernel Image (uImage) ====' && make -j$(nproc) O=build_image/build ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- LOADADDR=0x80008000 uImage && echo '==== [Step 2] Compiling Device Tree (DTB) ====' && make O=build_image/build ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- dtbs && echo '==== [Step 3] Safely Copying Build Artifacts to Project Output ==== ' && mkdir -p ../output && cp build_image/build/arch/arm/boot/uImage ../output/ && cp build_image/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb ../output/ && echo '==== [SUCCESS] uImage and am335x-boneblack.dtb are ready in beaglebone_linux_bsp/output/ ===='",
            "problemMatcher": []
        },
        {
            "label": "📦 Clean Kernel Build",
            "type": "shell",
            "command": "rm -rf build_image/ && make mrproper",
            "problemMatcher": []
        }
    ]
}
```
> [!IMPORTANT]
> **核心編譯之 LOADADDR 科學原理**：
> 核心映像檔 `uImage` 包含了由 U-Boot `mkimage` 產生之 64 位元組（40H）標頭。該標頭紀錄了引導參數與核心在 DDR 記憶體中的預期載入位址。
> 由於 BeagleBone Black 上的實體記憶體映射起點為 `0x80000000`，且前 32KB（`0x8000` 位址偏移，亦即 `0x00008000`）必須保留給內核頁表、零頁異常向量與開機參數塊（ATags/DTB），因此核心之載入位址必須設為 `0x80008000`。編譯時指明 `LOADADDR=0x80008000` 即是為了在 `uImage` 檔頭寫入正確的引導位址資訊。

### 7.3 物理部署專案自動化任務：[`output_tasks_example.json`](file:///c:/Users/User/Documents/TechBlog/assets/26_0625/output_tasks_example.json)
此設定檔配置於專案收集目錄 `output/` 中，負責將在此處集齊的所有引導元件（`MLO`、`u-boot.img`、`uImage`、`am335x-boneblack.dtb`、`boot.scr`）一鍵燒錄至已掛載之安全數位卡的第一分區中：
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "📥 Copy to SD Card",
            "type": "shell",
            "command": "cp uImage am335x-boneblack.dtb MLO u-boot.img boot.scr /media/brandon/boot/ && sync && echo '==== [SUCCESS] All files safely copied to SD Card! ===='",
            "problemMatcher": []
        }
    ]
}
```

---

## 8. 結論 (Conclusion)

本技術報告透過理論解析與實務指令之整合，系統性地梳理了基於 TI AM335x 平台之嵌入式 Linux 建置與移植流程。在系統啟動方面，深刻剖析了 ROM Code、MLO (SPL)、U-Boot 主程式與 Linux 核心四階段引導之本質與資源傳遞協定。同時，藉由對比傳統 Samba + PuTTY 與現代 AI IDE 開發流，揭示了現代工具在消除 I/O 延遲、上下文感知與自動除錯上之顯著優勢。最後，透過背景運行虛擬機之 `vmrun` 管理指令，以及自動化 `tasks.json` 編譯部署任務之設計，建構了一套高效且易於維護之 BSP 開發體系，為後續之字元裝置驅動開發與硬體控制奠定了堅實之基礎。

## 📚 Reference
* [beagleboard/beaglebone-black GitHub](https://github.com/beagleboard/beaglebone-black/tree/master)

