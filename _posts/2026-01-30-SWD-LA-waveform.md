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
<img src="{{ '/assets/26_0130/LA_Inter.png' | relative_url }}" width="400">
</p>

<!-- ![](/assets/26_0130/LA_IC.jpg) -->
<p align="center">
<img src="{{ '/assets/26_0130/LA_IC.png' | relative_url }}" width="200">
</p>

搭配的軟體是 **sigrok** 的 **PulseView**，這是一款開源且跨平台的邏輯分析軟體，支援多種硬體設備。
安裝與使用可以參考 [WeActStudio/LogicAnalyzerV1](https://github.com/WeActStudio/LogicAnalyzerV1) 的教學說明。

### STM32 開發板

使用的是NUCLEO-F767ZI，其上有內建 ST-LINK/V2-1，可以直接透過 USB 連接進行 SWD 調試 STM32F767ZI 微控制器。並且上面有external SWD header，可以方便接線。

<!-- ![](/assets/26_0130/HW_Tools.jpg) -->
<p align="center">
<img src="{{ '/assets/26_0130/HW_Tools.png' | relative_url }}" width="600">
</p>

附上其 Debug Connector 的腳位表:

<!-- ![](/assets/26_0130/Table_5_Debug_connector_CN6.png) -->
<p align="center">
<img src="{{ '/assets/26_0130/Table_5_Debug_connector_CN6.png' | relative_url }}" width="600">
</p>

## 📉 SWD 通訊觀察



## 📝 結語



## 📚 Reference
* [Arm Debug Interface Architecture Specification](https://developer.arm.com/documentation/ihi0031/latest/)
* [JTAG 和 SWD 的優缺點比較](https://knightli.com/zh-tw/2025/04/07/jtag-swd-%E5%84%AA%E7%BC%BA%E9%BB%9E/)
* [sigrok 官方下載頁面](https://sigrok.org/wiki/Downloads)
* [WeActStudio/LogicAnalyzerV1](https://github.com/WeActStudio/LogicAnalyzerV1)
* [芯佰微 - CBM9002A SPEC](https://corebai.com/Data/corebai/upload/file/20240820/03-01-09-CBM9002A8051%E5%86%85%E6%A0%B8%E7%9A%84USB%E5%9E%8B%E5%BE%AE%E6%8E%A7%E5%88%B6%E5%99%A8%E3%80%90%E4%B8%AD%E6%96%87%E6%8E%92%E7%89%88%E3%80%91-202408201400.pdf)
* [NUCLEO-F767ZI_用戶手冊](https://www.st.com.cn/zh/evaluation-tools/nucleo-f767zi.html#documentation)
