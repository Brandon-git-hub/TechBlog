---
layout: post
title: "工具介紹 - Paul Falstad Simulator"
subtitle: "線上免費即時電路模擬工具"
categories: [Analog, Simulation]
date: 2026-03-02
lang: zh-Hant
---

## 📌 Paul Falstad Simulator 簡介

**Falstad** 是一款開源的電路模擬工具，基於 Java 開發（現已有完善的網頁 JavaScript 版本），使用者可直接透過瀏覽器免費操作。
其核心優勢在於**操作直覺**且具備**即時動態回饋**，使用者可以快速佈置元件並組合電路，極適合用於初步概念驗證（Proof of Concept）與教學演示。

### 主要特色：
* **視覺化電流模擬：** 以動態流點具象化電流流向與大小，能直觀地觀察電路行為。
* **即時示波器功能：** 支援將任意導線或元件加入模擬示波器，即時監控電壓與電流的**波形**變化。
* **跨平台與零門檻：** 無須安裝複雜軟體，透過瀏覽器即可快速實踐電路構想。

### 限制與缺點：
由於其元件模型多為理想模型，並非基於特定半導體廠牌的真實元件參數，因此主要適用於**基本邏輯驗證**與**基礎類比電路分析**，若需進行高精度的製程模擬，建議轉用 LTSpice 或 HSPICE。

<!-- ![](/assets/26_0302/faltad_example.png) -->
<p align="center">
<img src="{{ '/assets/26_0302/faltad_example.png' | relative_url }}" width="700">
</p>

## 📚 Reference
* [Paul Falstad](https://www.falstad.com/circuit/circuitjs.html)
* [Reddit - Info on who Paul Falstad is?](https://www.reddit.com/r/AskElectronics/comments/1jvw8zo/info_on_who_paul_falstad_is_needed_for_scientific/)
* [pfalstad/circuitjs1](https://github.com/pfalstad/circuitjs1)
* [下載LTspice](https://www.analog.com/cn/lp/002/tools/ltspice-simulator-tw.html)
