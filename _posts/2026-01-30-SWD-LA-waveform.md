---
layout: post
title: "使用邏輯分析儀初探SWD協定"
subtitle: "實際量測 ARM Debug Interface (ADI) 波型"
categories: [Interfaces, SWD, ADI]
date: 2026-01-30
lang: zh-Hant
---

## 📌 SWD/JTAG Debug Port(DP) 基本理解

*  **JTAG-DP (JTAG Debug Port):**
   基於 IEEE 1149.1 標準，使用 **DBGTAP 掃描鏈 (Scan Chains)** 來讀寫暫存器資訊。這是一種傳統且廣泛使用的標準介面。
*  **SW-DP (Serial Wire Debug Port):**
   這是一種 **雙腳位 (Two-pin)** 的序列介面，使用 **封包傳輸協定 (Packet-based protocol)** 來進行暫存器的讀寫。


| 特性 | JTAG (IEEE 1149.1) | SWD (Serial Wire Debug) |
| :--- | :--- | :--- |
| **訊號腳位** | 需要較多腳位，包含 **TDI, TDO, TMS, TCK** (以及可選的 nTRST),。 | 僅需 **2 個腳位**：雙向資料線 **SWDIO** 與時脈線 **SWCLK**,。 |
| **傳輸機制** | 透過 **狀態機 (State Machine)** 與 **掃描鏈** 進行序列位移操作。 | 透過 **封包 (Packet)** 進行通訊，包含請求(Request)、回應(Acknowledge)與資料傳輸階段,。 |
| **主要優勢** | 廣泛支持以及豐富調試功能。 | 腳位需求少，讀取效率更高。 |

## 🔧 工具平台選擇

單純讀文件資料會比較枯燥乏味，因此決定使用實際的硬體工具來觀察 SWD 協定的運作。
使用的工具包含 STM32 開發板與邏輯分析儀。

### 邏輯分析儀

使用的是便宜的 24Mhz 8CH 邏輯分析儀，其應是來自開源的 WeAct LogicAnalyzer V1 的設計(仿製cypress)。
<!-- ![](/assets/26_0130/VC0008_LOGIC_8.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/VC0008_LOGIC_8.png' | relative_url }}" width="380">
</p>

拆開其外殼後，可以看到其內部使用的是 **芯佰微 (CoreBai)** 的 **CBM9002A** 晶片，這是一款基於 8051 核心的 USB 微控制器。
<!-- ![](/assets/26_0130/LA_Inter.jpg) -->
<p align="center">
<img src="{{ '/assets/26_0130/LA_Inter.jpg' | relative_url }}" width="400">
</p>

<!-- ![](/assets/26_0130/LA_IC.jpg) -->
<p align="center">
<img src="{{ '/assets/26_0130/LA_IC.jpg' | relative_url }}" width="200">
</p>

搭配的軟體是 **sigrok** 的 **PulseView**，這是一款開源且跨平台的邏輯分析軟體，支援多種硬體設備。
安裝與使用可以參考 [WeActStudio/LogicAnalyzerV1](https://github.com/WeActStudio/LogicAnalyzerV1) 的教學說明。

### STM32 開發板

使用的是NUCLEO-F767ZI，其上有內建 ST-LINK/V2-1，可以直接透過 USB 連接進行 SWD 調試 STM32F767ZI 微控制器。並且上面有external SWD header，可以方便接線。

<!-- ![](/assets/26_0130/HW_Tools.jpg) -->
<p align="center">
<img src="{{ '/assets/26_0130/HW_Tools.jpg' | relative_url }}" width="600">
</p>

附上其 Debug Connector 的腳位表:

<!-- ![](/assets/26_0130/Table_5_Debug_connector_CN6.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/Table_5_Debug_connector_CN6.png' | relative_url }}" width="600">
</p>

而操作上，使用 STM32CubeProgrammer ，在 GUI 介面命令 ST-LINK 進行 SWD 通訊，並且在 PulseView 上觀察 SWD 波型。

<!-- ![](/assets/26_0130/Cube_programmer.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/Cube_programmer.png' | relative_url }}" width="700">
</p>


## 📈 SWD 通訊觀察

透過 CubeProgrammer 連接 STM32F767ZI 後，按下 Connect 按鈕，ST-LINK 會自動透過 SWD 協定與目標 MCU 進行通訊。
此次觀察的重點在於 SWD 協定的初始化過程，以及讀取 DPIDR (Debug Port ID Register) 的操作。

<!-- ![](/assets/26_0130/Overview_waveform.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/Overview_waveform.png' | relative_url }}" width="800">
</p>

### JTAG 轉 SWD 序列

<!-- ![](/assets/26_0130/JTAG_to_SWD_sequence_timing.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/JTAG_to_SWD_sequence_timing.png' | relative_url }}" width="800">
</p>

<!-- ![](/assets/26_0130/JTAG_to_SWD_sequence_waveform.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/JTAG_to_SWD_sequence_waveform.png' | relative_url }}" width="800">
</p>

經過NRST 重置後，由於 JTAG interface 必須在 TLR state 才能偵測 16-bit JTAG-to-SWD sequence，因此套過 Line Reset (至少 50 個 TCK 並且 TMS HIGH) 後，接著會送出 JTAG-to-SWD sequence。
> Note: 我的疑問，為何假設此時初始狀態是在JTAG的某state下，其software reset 明明只要5個TCK就可以了?
> 參考文件的解釋 ```The sequence that is shown in the figure has been chosen to ensure that the SWJ-DP switches to SWD, independent of whether it was previously expecting JTAG or SWD.``` ，由於此時無法確定處於的狀態，因此使用了較長的序列來確保切換成功。

而 JTAG-to-SWD sequence 為 16-bit 的固定序列 `0x79E7` (大多是MSB first)，其二進位為 `0b0111 1001 1110 0111`。

### SWD 讀 IDCODE (DPIDR)

<!-- ![](/assets/26_0130/SWD_successful_read_operation.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/SWD_successful_read_operation.png' | relative_url }}" width="700">
</p>

SWD 不同於 JTAG 有 IDCODE instrunction，其走的是封包概念，所以當我們要讀取 Chip ID 時，會透過 SWD 讀取 DPIDR (Debug Port ID Register) 來取得，而其位址為 `0x00`。

我們的 STLink 調適器作為 Host 端，會先送出一個讀取 DPIDR 的 8-bit 請求封包 (Request Packet)，然後等待目標IC回應，在讀DPIDR此操作上，其部會回應 WAIT 或 FAULT，而是會直接回應 OK (0b001) by LSB first。

Parity bit 看傳送封包的資料位元數量來決定其值，若資料中 1 的數量為奇數，則 Parity bit 為 1 (使得總數為偶數)，反之亦然。
Park bit 為 1，事先將資料線拉高，表示傳輸結束，且確保 Trn 期間資料線為高電位。
Trn (Turnaround) 為雙向資料線切換方向的時間，讀取操作時，Host 端在送出請求封包後，需要釋放資料線，讓目標 IC 可以回應資料，因此會有一個 Trn 週期。

<!-- ![](/assets/26_0130/SWD_read_op_DPIDR.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/SWD_read_op_DPIDR.png' | relative_url }}" width="800">
</p>

在上圖中，IDCODE 傳送8-bit 後，看起來少了一個 Trn cycle，尚不確定原因，懷疑 LA 取樣率不夠高導致少觀察到。

<!-- ![](/assets/26_0130/DPIDR_value.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/DPIDR_value.png' | relative_url }}" width="800">
</p>

傳送回來的 DPIDR 資料為 `0x5BA02477`，其二進位為 `0101 1011 1010 0000 0010 0100 0111 0111`，符合 ARM DPIDR 的格式說明:
| Bits      | Name               | Value    |Description                                 |
|-----------|--------------------|----------|---------------------------------------------|
| [31:28]   | Revision           | 0x5      |**修訂版本號 (Revision code)** 表示此 DP 設計的修訂版本為 r5。  |
| [27:20]   | Part Number        | 0xBA     |**零件編號 (Part Number)** 由設計者 (Designer) 分配的編號。`0xBA` 通常對應 Arm CoreSight SoC-400 系列的 SW-DP。 |
| [19:17]   | Reserved           | 0x0      |保留位，應設為零。                           |
| [16]      | Min                | 0x0      |**最小化實作 (Minimal DP)** `0`表示此 DP **不是** MINDP。 |
| [15:12]   | Version            | 0x2      |**DP 架構版本 (DP Version)** `0x2` 表示此 DP 符合 **DPv2** 規範。|
| [11:1]    | Designer ID        | 0x23B    |**設計者代碼 (Designer ID)** 這是 JEDEC JEP106 代碼，代表 **Arm Limited**。|
| [0]       | RAO                | 0x1      |**Read As One** 此位元永遠為 1。               |

在資料後面，同樣在下個操作前，會有一個 Parity bit 和 Trn 週期。

## 📝 結語

由於 ARM 架構的細節相當多，因此在了解 SWD 協定時，必須同時補充相關的背景知識。
在使用新買的邏輯分析儀並操作 PulseView ，發現其操作介面相當直觀，且支援多種協定解碼器 (Protocol Decoder)，對於我後續學習與工作上debug 相關會有很大幫助。
原本想學習到至少讀出 IC UID ，不過後續發現還需要對 Access Port (AP) 操作等等，暫時先擱置，未來有機會再繼續深入研究。


## 📚 Reference
* [Arm Debug Interface Architecture Specification](https://developer.arm.com/documentation/ihi0031/latest/)
* [JTAG 和 SWD 的優缺點比較](https://knightli.com/zh-tw/2025/04/07/jtag-swd-%E5%84%AA%E7%BC%BA%E9%BB%9E/)
* [sigrok 官方下載頁面](https://sigrok.org/wiki/Downloads)
* [WeActStudio/LogicAnalyzerV1](https://github.com/WeActStudio/LogicAnalyzerV1)
* [芯佰微 - CBM9002A SPEC](https://corebai.com/Data/corebai/upload/file/20240820/03-01-09-CBM9002A8051%E5%86%85%E6%A0%B8%E7%9A%84USB%E5%9E%8B%E5%BE%AE%E6%8E%A7%E5%88%B6%E5%99%A8%E3%80%90%E4%B8%AD%E6%96%87%E6%8E%92%E7%89%88%E3%80%91-202408201400.pdf)
* [NUCLEO-F767ZI_用戶手冊](https://www.st.com.cn/zh/evaluation-tools/nucleo-f767zi.html#documentation)
