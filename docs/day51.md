---
layout: page
title: "從零開始使用Esp32開發板"
categories: [Verilog]
day: 51
date: 2025-12-05
---

## 📌 開發環境簡介

### 硬體

* 開發板: ESP32-C3-SuperMini [Datasheet Link](../assets/day51/ESP32-C3%20SuperMini%20datasheet.pdf)
* 配件: USB-TypeC 線 

<img src="../assets/day51/ESP32-C3-SuperMini.png" alt="ESP32-C3-SuperMini" width="200" />

### 軟體

* 開發環境之作業系統: Windows11
* 開發環境之IDE: Visual Studio Code 
* 開發環境之SDK: Esp-idf v5.5.1

<img src="../assets/day51/Software_Enviroment.png" alt="Software Enviroment" width="350" />

> * **Toolchain** to compile code for ESP32 
> * **Build tools** - CMake and Ninja to build a full Application for ESP32 
> * **ESP-IDF** that essentially contains API (software libraries and source code) for ESP32 and scripts to operate the Toolchain


## 📌 第一步: 安裝Esp-idf SDK

### 1. [建議] 建立新的 VS Code設定檔
使用VS Code的一大好處，使用不同的設定檔，可以隔離開不同環境，每個環境下我們可以安裝不同的模組。
版本更迭，我們也可建立新的設定檔，新舊間可快速切換。

### 2. 安裝ESP-IDF 在 VS Code
也可以選擇下載安裝包，手動設定安裝。這邊遵循官方建議，選擇在VS Code下安裝。

[ESP-IDF Extension for VS Code](https://github.com/espressif/vscode-esp-idf-extension/blob/master/README.md)

> 題外話，2025年STM也開始正式發布VS Code之套件的SDK

## 📌 第二步: 嘗試與電腦連線

## 🧑‍💻 Code Example

```verilog

```

## 📚 Reference
* [ESP-IDF v5.5.1 Documentation](https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32/)
* [ESP-IDF v5.5.1 Release Note](https://github.com/espressif/esp-idf/releases/tag/v5.5.1)
* [ESP-IDF Extension for VS Code](https://github.com/espressif/vscode-esp-idf-extension/blob/master/README.md)
