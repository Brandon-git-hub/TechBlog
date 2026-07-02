---
layout: post
title: "U-Boot 與 Linux Kernel 編譯、移植與部署自動化實作筆記"
subtitle: "基於 BeagleBone Black 平台之建立交叉編譯與 AI 輔助開發工作流"
categories: [Linux]
date: 2026-06-25
lang: zh-Hant
---

## 摘要 (Abstract)

本文實作並記錄基於 BeagleBone Black 開發板 (核心為德州儀器 TI Sitara AM3358 處理器) 之嵌入式 Linux 系統建置流程。涵蓋自底層硬體與虛擬化開發主機環境之建構、交叉編譯工具鏈之配置、U-Boot 與 Linux 核心（Kernel）原始碼之編譯，乃至最終開機引導程式與核心映像檔於安全數位卡（SD Card）之部署。 為了提升開發效率節省硬體資源，利用指令行工具 `vmrun` 進行虛擬機無介面（Headless）背景運行管理，並在 Windows 宿主端 (Host) 透過 SSH 連線至虛擬機（Guest）進行遠端開發。 此外，除了搭建傳統 Samba Server 配合 PuTTY 終端機的遠端模式，另外也整合了類 VS Code 的現代人工智慧輔助整合開發環境（AI-Assisted IDE）之工作流，透過一套 `tasks.json` 自動化建構與部署，提升開發效率。

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
至於為何要虛擬機呢? 不能在 Windows 下直接編譯嗎? 原因有三：
1. **交叉編譯工具鏈與 Linux 核心編譯環境**：Linux 核心與 U-Boot 的編譯工具鏈（GCC, Make等）原生支援 Linux 平台。
2. **WSL 對於硬體周邊支援度低**：Windows 現下事實上已有 Windows Subsystem for Linux (WSL2) ，其運行 Microsoft 維護的輕量級 Linux kernl，但其對於 USB devices 的掛載相較麻煩，需要 usbipd 工具手動掛載，對於新手(我)來說，虛擬機的隔離性與穩定性更高，故仍選擇虛擬機。
3. **虛擬機的快照與還原功能**：虛擬機快照功能更方便，可以避免說配置錯誤導致系統混亂，可回到之前保存的狀態。

事實上，還有可以選擇像 Docker 這種容器化的方式，不過其配置麻煩和操作流暢度較低，IO等底層一樣麻煩，未來再挑戰看看。

* **虛擬化管理器（Hypervisor）**：使用VMware Workstation Player ，也可使用開源的 Oracle VM VirtualBox，但聽說 Bug 較多。
* **客體作業系統（Guest OS）**：Ubuntu Linux Desktop 24.04 LTS。
* **資源配置分配原則**：
  * **硬碟空間**：建議配置 **40 GB 以上**之虛擬硬碟空間。Kernel 與 U-Boot 編譯會產生大量中間檔。
  * **記憶體（RAM）**：建議配置 **8 GB 以上**，太少容易 OOM（Out of Memory）。
  * **處理器（CPU）核心數**：建議配置**小於 Host 實體核心數**。由於編譯 Kernel 較久，所以會使用多核心平行編譯。

### 1.3 專案目錄

為了方便管理與維護，所有 BSP（板級支持包）相關的原始碼、編譯產物與根檔案系統皆統一收集於虛擬機使用者目錄下的 `~/beaglebone_linux_bsp`。該目錄下包含這幾個子目錄：

```
beaglebone_linux_bsp/
 ├──u-boot/        # 存放 U-Boot 原始碼
 ├──kernel/        # 存放 Linux Kernel 原始碼
 ├──busybox/       # 存放 BusyBox 原始碼
 ├──output/        # 編譯產物統一收集
 └──rootfs/        # 存放要安裝到 SD 卡 rootfs 分區的資料夾和檔案
```

* **`u-boot/`**：存放 U-Boot 原始碼，負責編譯產出二進位引導負載程式（`MLO` 與 `u-boot.img`）以及引導腳本（`boot.scr`）。
* **`kernel/`**：存放 Linux Kernel 原始碼，負責編譯產出核心映像檔（`uImage`）與硬體設備樹二進位檔（`am335x-boneblack.dtb`）。
* **`busybox/`**：存放 BusyBox 原始碼，負責編譯產出根檔案系統（Root File System）。
* **`output/`**：編譯產物統一收集。各子專案編譯完成後，目標檔案複製至此目錄，以利後續統一部署。
* **`rootfs/`**：存放要安裝到 SD 卡 rootfs 分區的資料夾和檔案。

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
     force directory mode = 777
     force create mode = 777
     force security mode = 777
     force directory security mode = 777
     hide dot file = no
     create mask = 0777
     directory mask = 0777
     delete readonly = yes
     guest ok = yes
     available = yes
     browseable = yes
  ```
  設定 Samba 密碼並重啟服務：
  ```bash
  sudo smbpasswd -a [username]
  sudo /etc/init.d/smbd restart
  ```
  可以在 Windows 系統中，透過「連線網路磁碟機」掛載 `\\<VM_IP>\Share`，查看 IP 可透過 ifconfig (需安裝 net-tools)。 看你的電腦是用乙太網路還是 WiFi，選擇對應的網卡介面訊息，如 Ethernet (en開頭) 或 Wi-Fi (wl開頭)，inet後接的就是 IPv4 地址。
  並且也可以使用 PuTTY 連線至虛擬機之 SSH 伺服器（需在虛擬機Linux那端安裝 `openssh-server`）執行編譯指令。
  ```bash
  sudo apt-get install openssh-server
  sudo /etc/init.d/ssh start
  ```

### 2.2 現代化 IDE 工作流
VSCode 等現代 IDE 透過 Remote-SSH 擴充套件，能直接在 Windows 主機端編輯虛擬機內的檔案，並在虛擬機中執行編譯等等操作指令。 這樣不管是你要使用 Anthrpic 的 Claude code 或者是 Open AI 的 codex，在 VSCode 他們都有支援套件，而本文中是使用 Google 的 Antigravity IDE，其一樣基於 VSCode 開發，操作上相同。選擇使用現代化 IDE 我認為有以下優勢：
1. **單一視窗工作流整合**：代碼編輯、終端調試與 AI 協同皆整合於單一 IDE 介面，大幅降低環境切換，開發上更流暢。
2. **豐富的擴充套件生態**：VSCode 擁有龐大的擴充套件市場，支援語法高亮、程式碼補全、版本控制、遠端開發等功能，可以任意搭配，適配不同的開發需求，不管是 Windows App, MCU Firmware, Linux 嵌入式系統，可以統一在相同的操作介面下進行，省去適應不同專屬 IDE 的學習成本。
3. **AI 輔助開發**：現在寫軟體基本上已經離不開 AI 的輔助，無論是程式碼補全、錯誤偵測、Code 直接生成，AI 能提供即時的協助，提升開發效率。

不需要在虛擬機 Linux 中安裝 IDE，只要在 Windows Host 使用 VSCode (或者是 Google 的 Antigravity IDE)，安裝了 remote-ssh 擴充套件，在介面中的左下角「開啟遠端視窗」點擊後，選擇 `Connect to SSH Host...`，輸入 IP 和密碼等，第一次會在遠端虛擬端自動安裝 SSH server，之後就可以像使用本機一樣在遠端開發了(注意像語法高亮等功能實際上是跑在遠端的，其資訊傳回本地後，IDE 的 UI 渲染才呈現在我們眼前)。

<!-- ![](/assets/26_0625/IDE_Remote_SSH_demo.png) -->

<p align="center">
<img src="{{ '/assets/26_0625/IDE_Remote_SSH_demo.png' | relative_url }}" width="700">
</p>

---

## 3. 虛擬機背景運行控制

為節省虛擬機的系統資源，免去虛擬機圖形介面的額外開銷，可使用 **無介面背景模式（Headless Mode）** 運行。在客體虛擬機內部配置好 `open-vm-tools` 後，即可直接在 Windows 宿主端透過命令列控制虛擬機的運作。

### 3.1 安裝 open-vm-tools
虛擬機內部必須安裝開源版 VMware Tools：
```bash
sudo apt-get install -y open-vm-tools
sudo systemctl enable --now open-vm-tools
```

### 3.2 控制腳本 (Windows PowerShell / Batch)
在 Host（Windows）的 PowerShell 或命令提示字元，可透過 vmrun 相關指令控制虛擬機：
* **無 GUI 背景啟動虛擬機**：
  ```powershell
  # 語法：vmrun -T ws start "虛擬機組態檔路徑.vmx" nogui
  vmrun -T ws start "C:\Users\User\Documents\Virtual Machines\Ubuntu\Ubuntu.vmx" nogui
  ```
* **安全關閉虛擬機（發送關機訊號）**：
  ```powershell
  vmrun -T ws stop "C:\Users\User\Documents\Virtual Machines\Ubuntu\Ubuntu.vmx" soft
  ```
* **列出目前運行中之虛擬機**：
  ```powershell
  vmrun list
  ```
  
這邊分享撰寫的兩個腳本檔案，實現對虛擬機的背景控制或選單化管理。

#### 3.2.1 核心控制指令腳本：[`vm_control.ps1`](../assets/26_0625/vm_control.ps1)
支援命令列參數調用，若無參數則會自動開啟一個互動式選單。預設虛擬機對應為 `"Ubuntu"`，其組態檔路徑指向預設的安裝位置。

#### 3.2.2 宿主端便捷啟動批次檔：[`vm_control.bat`](../assets/26_0625/vm_control.bat)
此批次檔用於在 Windows Command Line 下快速呼叫 PowerShell 腳本，並自動繞過執行原則（Execution Policy）限制與傳遞參數。

透過此雙層腳本，只需在 Windows 中執行 `vm_control.bat` 即可啟動互動式控制面板，下圖是演示畫面，按下`1`可以在背景執行，按下`4`可以列出目前有在執行的虛擬機，更多功能我藏在`7`裡面，裡面會有另外個選單。

<!-- ![](/assets/26_0625/vm_control_batch.png) -->

<p align="center">
<img src="{{ '/assets/26_0625/vm_control_batch.png' | relative_url }}" width="700">
</p>

---

## 4. BeagleBone Black 多階段啟動流程

BeagleBone Black 採用多階段引導機制，解決上電初期硬體資源受限之問題。
下面是透過 AI 撰寫的簡介，若有錯再請指正。
啟動鏈由四個軟硬體階段依次傳遞（如下圖所示）：

<!-- ![](/assets/26_0625/Linux_boot.svg) -->

<p align="center">
<img src="{{ '/assets/26_0625/Linux_boot.svg' | relative_url }}" width="400">
</p>

### 4.1 唯讀記憶體引導階段 (ROM Code / Initial Boot Stage)
* **存放位置**：固化於 AM3358 SoC 內部唯讀記憶體（ROM）中。
* **硬體制約與行為**：上電瞬間，外部 DDR3 DRAM 尚未被初始化，僅有晶片內部之 SRAM 可供使用。ROM Code 會根據硬體引腳電位（例如按住開發板上的 `BOOT` 按鍵）決定引導順序。
* **核心職責**：偵測並引導安全數位卡（SD Card / mmc0）或快閃記憶體（eMMC / mmc1）。ROM Code 會在啟動設備的 FAT32 分區（一般為第一分區）中搜尋名為 **`MLO`** (Secondary Program Loader) 的檔案，並將其搬移至內部 SRAM 中執行。

### 4.2 次級程式引導階段 (U-Boot SPL / MLO)
* **存放位置**：SD 卡第一分區（FAT32，標籤為 `boot`），必須命名為 **`MLO`**。
* **引導動機**：由於完整的 U-Boot 主程式映像檔（`u-boot.img`）體積較大，無法裝入僅有 64KB 的 SRAM 中。因此，需先編譯一個經過高度裁減的先鋒程式 —— SPL（次級程式引導器）。
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
* **根目錄掛載**：核心初始化完畢後，會依據啟動參數（`bootargs`），掛載 SD 卡的第二分區（通常為 Ext3/Ext4 分區，標籤為 **`rootfs`**）作為根目錄 `/`。核心隨後啟動使用者空間的第一個進程 `/sbin/init`，調用各種初始化服務。

---

## 5. 建置開機環境前的硬體準備

### 5.1 清除板載 eMMC
BeagleBone Black 出廠時，其板載 eMMC 已預燒錄作業系統。若未加以清除，系統開機時可能會優先自 eMMC 啟動舊版引導程式，進而干擾我們採用的 SD 卡開機實作測試。因此，在 U-Boot 命令列先將 eMMC 的引導磁區清除（`mmc0` 為 SD 卡，`mmc1` 為 eMMC）：
```bash
# 切換至板載 eMMC 設備
=> mmc dev 1
# 擦除引導區段 (自 Block 0 開始，擦除 0x20000 個區塊)
=> mmc erase 0 20000
```

### 5.2 SD 卡分割與格式化

以下是在 Ubuntu (虛擬機) 上對 SD 卡進行分割與格式化的指令。

```bash
# 建立 FAT32 分區（標籤為 boot，用於存放 MLO、u-boot.img、boot.scr、uImage）
mkfs.vfat -F 32 -n "boot" /dev/sdx
# 建立 Ext3 分區（標籤為 rootfs，用於存放根檔案系統）
mke2fs -j -L "rootfs" /dev/sdx
```

> `sdx` 的 `x` 是需要自行替換為實際的裝置名稱，可能是 sda、sdb、sdc...，可以用 `lsblk` 來查看。

---

## 6. 原始碼和編譯工具 (交叉編譯工具、U-boot&kernel)

### 6.1 交叉編譯工具鏈之原理與部署
由於電腦 CPU 架構（一般為 x86_64）與目標板 CPU 架構（ARMv7-A，32-bit）不同，無法直接編譯為目標板設計的機器碼，因此必須引入**交叉編譯工具鏈（Cross-Compiler Toolchain）**。
在 Ubuntu 系統中，可直接透過進階軟體包工具（APT）安裝適用於 ARM 32-bit 架構的 GCC 編譯器：
```bash
sudo apt-get update
sudo apt-get install -y gcc-arm-linux-gnueabi build-essential
```
此工具鏈的前綴為 `arm-linux-gnueabi-`，gnu 後面的 eabi 是 Embedded Application Binary Interface 的縮寫，ABI 是決定兩個不同的程式或系統之間溝通的規則，例如資料型態大小、暫存器使用方式、函式呼叫慣例等。

### 6.2 U-Boot 與 Linux Kernel 源碼獲取
原始碼可自官方託管倉庫取得：
* **U-Boot 原始碼**：
  ```bash
  git clone --depth 1 git://git.denx.de/u-boot.git
  cd u-boot
  ```
* **Linux Kernel 原始碼**（以 Longterm 分支 v6.6 為例）：
  ```bash
  git clone --depth 1 --single-branch --branch v6.6.58-ti-arm32-r15 https://github.com/beagleboard/linux.git
  ```

大型專案原始碼倉庫（特別是 Linux Kernel）之 Git 歷史記錄與多架構代碼極為龐大，不僅佔用磁碟空間，亦會嚴重降低 IDE 目錄解析與索引建立之速度。因此複製時建議使用限制拉取(Shallow Clone)，僅保留最新一筆 Commit 歷史，避免下載過往數十萬筆歷史變更：
```bash
git clone --depth 1 --branch <branch> <remote_repository>
```
將<branch>替換成想要的branch，<remote_repository>替換成想要拉取的倉庫網址。

---

## 7. U-boot 與 Linux kernel 編譯和打包

### 7.1 U-Boot 編譯流程
1. **宣告環境變數**：
   ```bash
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-gnueabi-
   ```
   可以加到~/.bashrc 中，就不用每次下指令都打。
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

### 7.2 Linux Kernel 編譯流程
1. **配置目標板設定檔**（將編譯中間檔輸出至指定目錄）：
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
   > **LOADADDR=0x80008000 之原理**：
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
   編譯完成後，核心映像檔 `uImage` 將存於 `build_image/build/arch/arm/boot/uImage`；而設備樹二進位檔 `am335x-boneblack.dtb` 則生成於 `build_image/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb` (或舊版 `arch/arm/boot/dts/am335x-boneblack.dtb`)。

---

## 8. 多子專案自動化建置和部署 (VSCode tasks)

基於子專案架構（`u-boot`, `kernel`, `busybox`, `output`, `rootfs`），我們在各工作區目錄下配置對應的 `.vscode/tasks.json`，將各階段之編譯與物理燒錄步驟封裝成自動化任務。

### 8.1 U-Boot 專案自動化任務：[`u_boot_tasks_example.json`](../assets/26_0625/u_boot_tasks_example.json)
此設定檔配置於 `u-boot/` 目錄下。除了提供編譯任務外，亦提供了 SD 卡的自動化掛載（利用 `udisksctl` 輸入密碼後自動掛載）與卸載，並在編譯成功後，將 `MLO` 與 `u-boot.img` 自動複製至上層的 `../output/` 目錄中：

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

### 8.2 Linux 核心專案自動化任務：[`kernel_tasks_example.json`](../assets/26_0625/kernel_tasks_example.json)
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

### 8.3 開機引導元件部署專案自動化任務：[`output_tasks_example.json`](../assets/26_0625/output_tasks_example.json)
此設定檔配置於專案收集目錄 `output/` 中，負責將在此處集齊的所有引導元件（`MLO`、`u-boot.img`、`uImage`、`am335x-boneblack.dtb`、`boot.scr`）一鍵搬移至已掛載的 SD 卡的第一分區中：
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

### 8.4 Busybox 專案自動化任務：[`busybox_tasks_example.json`](../assets/26_0625/busybox_tasks_example.json)
此設定檔配置於 `busybox/.vscode/tasks.json`。
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "📁 BusyBox Proj Size",
            "type": "shell",
            "command": "du -sh .",
            "problemMatcher": []
        },
        {
            "label": "💡 BusyBox Defconfig",
            "type": "shell",
            "command": "make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- defconfig",
            "problemMatcher": []
        },
        {
            "label": "💡 BusyBox Menuconfig",
            "type": "shell",
            "command": "make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- menuconfig",
            "problemMatcher": []
        },
        {
            "label": "🚀 Compile BusyBox",
            "type": "shell",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "command": "make -j$(nproc) ARCH=arm CROSS_COMPILE=arm-linux-gnueabi-",
            "problemMatcher": []
        },
        {
            "label": "🚀 Install BusyBox",
            "type": "shell",
            "command": "make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- install",
            "problemMatcher": []
        }
    ]
}
```

## 9. 建置過程的設置修改

### 9.1 U-boot 的設置修改

U-boot 建置與部署到 SD Card，我實作很順利。 除了上面有提到的舊版映像檔格式支援 (Legacy Image Format)，需要去檢查。由於我是使用 nogui 去操作，外部設備需要手動去將 device 掛載起來，雖然說插上 USB 孔後，我們執行 "🔍 List Device Info" ("lsblk")，可以看到 sda, sdb 的裝置，但此時其實只有底層硬體被電腦辨識，還沒有被掛載到檔案系統中，必須要再執行 "💾 SD: Mount boot & rootfs" ("udisksctl") 將指定的 sdb1, sdb2 掛起來 (依據實際情況調整)。

還有 U-boot 我們可以撰寫開機腳本 (`boot.scr`) 去控制開機過程。 若不用腳本，就須每次進入 U-Boot 命令列介面（`=>`）去一行一行輸入指令，以下為我的範例，位址相對設的很保守:

```cmd
setenv bootargs console=ttyO0,115200 earlyprintk root=/dev/mmcblk0p2 rw rootwait rootdelay=2
fatload mmc 0:1 0x88000000 am335x-boneblack.dtb
fatload mmc 0:1 0x82000000 uImage
bootm 0x82000000 - 0x88000000
```

這裡我有開啟 earlyprintk 進行除錯，因為當初有遇到卡在 `Starting kernel ...` 後沒有後續了，為了尋找問題，開啟後 Log 會比較詳細 (不過問題事實上出在 Kernel 設置那邊)。
還有就是雖然如同 `Documentation/admin-guide/devices.txt` 中，TTY 設備如今都改成如 `/dev/ttyS0` ，但系統開機後會自動轉換從 `/dev/ttyO0` 到 `/dev/ttyS0`，所以 console 直接打 `/dev/ttyO0` 即可。

```txt
4 char	TTY devices
		  0 = /dev/tty0		Current virtual console

		  1 = /dev/tty1		First virtual console
		    ...
		 63 = /dev/tty63	63rd virtual console
		 64 = /dev/ttyS0	First UART serial port
		    ...
		255 = /dev/ttyS191	192nd UART serial port

		UART serial ports refer to 8250/16450/16550 series devices.

		Older versions of the Linux kernel used this major
		number for BSD PTY devices.  As of Linux 2.1.115, this
		is no longer supported.	 Use major numbers 2 and 3.
```


### 9.2 Linux 核心的設置修改

如同上面講到遇到卡在 `Starting kernel ...`，有做了些調整，一是到 kenel 的 menuconfig，搜尋 CONFIG_DEBUG_OMAP2UART1 查找設置位置，將 Debug console port 的輸出從 OMAP 2/3/4 改到 AM33XXUART1。

<!-- ![](/assets/26_0625/CONFIG_DEBUG_OMAP2UART1.png) -->

<p align="center">
<img src="{{ '/assets/26_0625/CONFIG_DEBUG_OMAP2UART1.png' | relative_url }}" width="600">
</p>

進入選單，選到 AM33XX UART1，改完後就可以看到 Kernel Log 跑出來了。

<!-- ![](/assets/26_0625/CONFIG_DEBUG_AM33XXUART1.png) -->

<p align="center">
<img src="{{ '/assets/26_0625/CONFIG_DEBUG_AM33XXUART1.png' | relative_url }}" width="600">
</p>

但後續還有遇到 pinmux 衝突問題，所以去改了 dts (`beaglebone_linux_bsp/kernel/arch/arm/boot/dts/ti/omap/am33xx-l4.dtsi`) 裡面的 #pinctrl-cells 從 <1> 改成 <2>。 

```
            scm: scm@0 {
				compatible = "ti,am3-scm", "simple-bus";
				reg = <0x0 0x2000>;
				#address-cells = <1>;
				#size-cells = <1>;
				#pinctrl-cells = <2>;
				ranges = <0 0 0x2000>;

				am33xx_pinmux: pinmux@800 {
					compatible = "pinctrl-single";
					reg = <0x800 0x238>;
					#pinctrl-cells = <2>;
					pinctrl-single,register-width = <32>;
					pinctrl-single,function-mask = <0x7f>;
				};
```

以上我改完，成功看到 `Trying libraries: m resolv rt`, `Final link with: m resolv` 訊息。然後就開始卡在 init 階段，接下來就剩下 rootfs 的建置了。


### 9.3 Busybox 的設置與建置

同樣 make defconfig，編譯過程有錯，透過訊息去 menuconfig 將 Networking Utilities -> 取消勾選 tc。

<!-- ![](/assets/26_0625/BusyBox_tc_disable.png) -->

<p align="center">
<img src="{{ '/assets/26_0625/BusyBox_tc_disable.png' | relative_url }}" width="600">
</p>

還有我們必須在 Settings -> Destination path for 'make install' 中設定一個絕對路徑，讓 busybox 自動 copy 過去，相對位址會失敗。

<!-- ![](/assets/26_0625/BusyBox_make_install_dir.png) -->

<p align="center">
<img src="{{ '/assets/26_0625/BusyBox_make_install_dir.png' | relative_url }}" width="600">
</p>

make 編譯和 install 完，會發現我們的 `roofts` 裡面資料夾沒有想像中完整，後續我們需要將基本目錄完善，以及創建一些預設的檔案。
這邊我先偷懶，簡單附上所需要執行的步驟，後續有空再細緻整理與筆記。

建立基本目錄和修改權限
```bash
mkdir dev etc home lib proc sys tmp var
mkdir usr/lib
mkdir var/log
sudo chmod 4755 bin/ping
sudo chmod 1777 tmp
```

BusyBox 有些動態連結函數庫，我們需要將他們從工具鏈手動copy到rootfs中，先觀察需要的函數庫，指令如下：

```bash
arm-linux-gnueabi-readelf -a ./bin/busybox | grep "program interpreter"
arm-linux-gnueabi-readelf -a ./bin/busybox | grep "Shared library"
```

得到類似以下訊息：
```
 0x00000001 (NEEDED)                     Shared library: [libm.so.6]
 0x00000001 (NEEDED)                     Shared library: [libresolv.so.2]
 0x00000001 (NEEDED)                     Shared library: [libc.so.6]
 0x00000001 (NEEDED)                     Shared library: [ld-linux.so.3]
```

複製過去
```bash
cp -a /usr/arm-linux-gnueabi/lib/libm.so.6 lib
cp -a /usr/arm-linux-gnueabi/lib/libc.so.6 lib
cp -a /usr/arm-linux-gnueabi/lib/ld-linux.so.3 lib
cp -a /usr/arm-linux-gnueabi/lib/libresolv.so.2 lib
```

建立基本device node
```bash
sudo mknod -m 600 dev/console c 5 1
sudo mknod -m 666 dev/null c 1 3
```

創建/連結init檔案至busybox執行檔
```bash
ln -s bin/busybox init
```

建立inittab
```bash
::sysinit:/etc/init.d/rcS
console::askfirst:-/bin/sh
```

修改inittab的權限
```bash
sudo chmod 644 ./etc/inittab
```

建立init.d目錄 及 rcS
```bash
mkdir ./etc/init.d/
```

撰寫 ./etc/init.d/rcS 內容如下：
```
#! /bin/sh
/bin/mount -a
```

修改./etc/init.d/rcS 的權限
```bash
sudo chmod 755 ./etc/init.d/rcS
```

建立group
```bash
mkdir ./etc/group
```

group 內容如下：
```
root:x:0:
```

修改group的權限
```bash
sudo chmod 644 ./etc/group
```

建立passwd
```bash
mkdir ./etc/passwd
```

passwd 內容如下：
```
root::0:0:root:/root:/bin/sh
```

修改passwd的權限
```bash
sudo chmod 644 ./etc/passwd
```

建立fstab
```bash
mkdir ./etc/fstab
```

fstab 內容如下：
```
proc /proc proc defaults 0 0
none /tmp ramfs defaults 0 0
sysfs /sys sysfs defaults 0 0
```

修改fstab的權限
```bash
sudo chmod 644 ./etc/fstab
```

將rootfs copy到sd card
```bash
sudo cp -rf ./* /media/brandon/rootfs/
```


---

## 10. 感想

能看到 Linux 系統在開發板上啟動，可以透過命令列輸入熟悉的指令，並看到回應，是非常開心的，因為這個系統全部是自己一步一步編譯和部署的，原本眼中神秘的作業系統現在變得真實許多。


## 📚 Reference
* [beagleboard/beaglebone-black GitHub](https://github.com/beagleboard/beaglebone-black/tree/master)

