---
layout: post
title: "使用 STM32CubeMX 初始化建立專案"
subtitle: "NUCLEO-F767ZI 開發板學習"
categories: [STM32, CubeMX]
date: 2026-02-17
lang: zh-Hant
---

## 📌 一、 前言

由於 STM32 支援的外設（Peripherals）種類繁多，且不同型號間的硬體配置也存在差異，有一定的開發門檻。雖然意法半導體 (STMicroelectronics) 提供了 **HAL 庫**，讓開發者能以高階（High Level） API 開發應用功能，但對初學者而言，初期手動建立專案與配置暫存器仍具挑戰性。

透過 **STM32CubeMX**，我們可以直接在圖形化介面（GUI）中完成引腳與時鐘配置，並自動生成初始化程式碼。這不僅是目前官方推薦的開發方式，也是新手入門最直覺、方便的首選。

## 🔧 二、 實驗環境與工具

* 開發板: STM32 NUCLEO-F767ZI Board
* 核心 MCU: STM32F767ZI (STM32F7 系列)
* 開發工具：STM32CubeMX
* 輔助工具: 24Mhz 8CH 邏輯分析儀（用於驗證 GPIO 和輸出的通訊訊號）

## 🚀 三、 CubeMX 專案啟動配置步驟

### 1. 選擇開發平台

在啟動畫面中，我們選擇 **「Access to Board Selector」**（或 *Start My project from ST Board*）。對於使用官方開發板的使用者來說，這能自動幫我們定義好板載的 LED、按鈕與調試接口（ST-Link）。

<!-- ![](/assets/26_0217/Board_selector.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/Board_selector.png' | relative_url }}" width="500">
</p>

### 2. 搜尋與確認型號

在跳出的搜尋介面中，選擇 ```NUCLEO-F767ZI```。選定後點擊右上角的 **Start Project**。

<!-- ![](/assets/26_0217/New_Project_from_a_Board_UI.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/New_Project_from_a_Board_UI.png' | relative_url }}" width="800">
</p>

### 3. 初始化外設設定

系統會詢問是否要「Initialize all peripherals with their default Mode?」，點選 Yes。
進入主畫面後，我們就可以開始進行 **Pinout & Configuration**（引腳配置）與 **Clock Configuration**（時鐘樹設定）了！

<!-- ![](/assets/26_0217/STM32F767ZITx_NUCLEO_F767ZI_Project.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/STM32F767ZITx_NUCLEO_F767ZI_Project.png' | relative_url }}" width="800">
</p>

## 🛠️ 四、 外設選擇與設定 (Pinout & Configuration)

在下面範例中，我們將配置 GPIO、ADC1、TIM2 & TIM3、USART3 等外設。

<!-- ![](/assets/26_0217/System_view.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/System_view.png' | relative_url }}" width="800">
</p>

### 1. LED 燈與 GPIO 配置

查看 [UM1974 User Manual](https://www.st.com/resource/en/user_manual/um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf) 的第 7.5 節，確認板載 LED (LD1, LD2, LD3) 所連接的 Pin 腳。

<!-- ![](/assets/26_0217/UM1974_LEDs.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/UM1974_LEDs.png' | relative_url }}" width="700">
</p>

根據文件說明，我們在 STM32CubeMX 的 **Pinout View** 中進行以下設定：

* **PB0**：設定為 `GPIO_Output` (LD1_GREEN)
* **PB7**：設定為 `GPIO_Output` (LD2_BLUE)
* **PB14**：設定為 `GPIO_Output` (LD3_RED)

<!-- ![](/assets/26_0217/Pin_GPIO_setting.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/Pin_GPIO_setting.png' | relative_url }}" width="500">
</p>

<!-- ![](/assets/26_0217/PB0_LD1_GREEN.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/PB0_LD1_GREEN.png' | relative_url }}" width="500">
</p>

<!-- ![](/assets/26_0217/PB7_LD2_BLUE.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/PB7_LD2_BLUE.png' | relative_url }}" width="450">
</p>

<!-- ![](/assets/26_0217/PB14_LD3_RED.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/PB14_LD3_RED.png' | relative_url }}" width="450">
</p>

#### 💡 使用 User Label 的好處

在引腳上點擊右鍵選擇 **"Enter User Label"**，可以為該引腳命名（如 `LD1_GREEN`）。這樣在自動生成的程式碼中，HAL 庫會自動產生的宏（Macro）定義 Port & Pin，這能大幅提高程式碼的可讀性。

### 2. Debug 輔助腳位設定 (PA3)

為了後續方便使用 **邏輯分析儀** 進行調試，我們順手將 **PA3** 也設定為 `GPIO_Output` 模式。

<!-- ![](/assets/26_0217/PA3_GPIO_Output.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/PA3_GPIO_Output.png' | relative_url }}" width="500">
</p>

**此腳位的預期用途：**

* **訊號觸發 (Trigger)**：當程式進入特定中斷或 Function 時，將 PA3 拉高，作為邏輯分析儀的觸發訊號。
* **頻率量測**：透過在迴圈中翻轉（Toggle）此腳位，測量程式執行的實際循環頻率或者是使用 TIM 延遲的時間符不符合預期。
* **軟體模擬 (Bit-banging)**：透過軟體快速切換IO輸出電位，模擬簡單的通訊協定或時鐘訊號。

**GPIO Speed 設定**
應上述對於高頻翻轉的需求，我們將 PA3 的 **Maximum output speed** 調升至 **Medium**。

<!-- ![](/assets/26_0217/PA3_GPIO_Speed.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/PA3_GPIO_Speed.png' | relative_url }}" width="500">
</p>

### 3. ADC 單通道設定 (PA0)

我們選擇 **ADC1** 的 **IN0** 通道，對應引腳為 **PA0**。
在 CubeMX 的選單中，若看到欄位標註警告符號或呈現紅色底色，代表該功能與目前已設定的引腳（如 GPIO 或其他外設）存在 **腳位衝突（Pin Conflict）**，配置時應避開這些選項。


<!-- ![](/assets/26_0217/ADC1_Mode_and_Configuration.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/ADC1_Mode_and_Configuration.png' | relative_url }}" width="500">
</p>

<!-- ![](/assets/26_0217/PA0_ADC1_IN0.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/PA0_ADC1_IN0.png' | relative_url }}" width="500">
</p>

在 **Parameter Settings** 中，可以看到 **Resolution (解析度)** 設定為 **12 Bits**。這是後續撰寫程式時將 ADC 原始數值（0~4095）換算回實際電壓的重要參數。

<!-- ![](/assets/26_0217/ADC_Parameter_Setting.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/ADC_Parameter_Setting.png' | relative_url }}" width="600">
</p>

### 4. TIM 定時器配置與延時邏輯

在本專案中，我計畫將 **TIM2** 作為 `ms` 級延時計數器，**TIM3** 作為 `us` 級延時計數器。 
在配置時，請務必將 **Clock Source** 設定為 **Internal Clock**；其餘通道（Channels）由於本次不需輸出訊號，保持 **Disable** 即可。

<!-- ![](/assets/26_0217/TIM2_Mode.png)-->
<p align="center">
<img src="{{ '/assets/26_0217/TIM2_Mode.png' | relative_url }}" width="800">
</p>

#### 為什麼選擇 TIM2 做長延時？

查閱 [DS11532 Datasheet](https://www.st.com/resource/en/datasheet/stm32f765bi.pdf) 的 **Figure 2 (Block Diagram)** 可以發現：

* **TIM2**：屬於 **32-bit** 定時器，擁有更大的 `Counter Period` (ARR)，適合處理長時間跨度的計數。
* **TIM3**：屬於 **16-bit** 定時器。
因此，選擇位元數較高的 TIM2 作為 `ms` 延時計數器最為合適。

<!-- ![](/assets/26_0217/F767ZI_Block_Diagram.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/F767ZI_Block_Diagram.png' | relative_url }}" width="600">
</p>

#### 頻率與預分頻器 (PSC) 計算

根據 Datasheet **Figure 2 (Block Diagram)** 和後續的 **Clock Configuration** 設定，得知雖然 APB1 匯流排頻率最高為 54MHz，但由於時鐘樹架構，定時器的時鐘輸入（Timer Clock）會經過倍頻，實際運行為 **108 MHz**。

為了達到精確計數，我們透過預分頻器（Prescaler, PSC）來調整計數頻率（減 1 是因為從 0 開始）：

* **TIM2 (10us 計數一次)：**
    公式：$$PSC = \frac{TimerClock}{TargetFrequency} - 1 = \frac{108MHz}{100kHz} - 1 = 1079$$

* **TIM3 (1us 計數一次)：**
    公式：$$PSC = \frac{108MHz}{1MHz} - 1 = 107$$

<!-- ![](/assets/26_0217/TIM2_Configuration.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/TIM2_Configuration.png' | relative_url }}" width="600">
</p>

### 5. USART3 設定 (非同步通訊與 DMA)

接下來配置序列通訊。我們選用 **USART3** 並設定為 **Asynchronous (非同步)** 模式。
考量到未來會實作 **DMA (Direct Memory Access)**，我提前在 **DMA Settings** 分頁中，將 `USART3_TX` 與 `USART3_RX` 加入傳輸通道。

<!-- ![](/assets/26_0217/USART3_Mode_and_Configuration.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/USART3_Mode_and_Configuration.png' | relative_url }}" width="800">
</p>

引腳部分，自動配置 **PB10** 作為 TX，**PB11** 作為 RX。

<!-- ![](/assets/26_0217/PB10_PB11_USART3_TX_RX.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/PB10_PB11_USART3_TX_RX.png' | relative_url }}" width="450">
</p>

### 6. SYS 設定 與 RCC 設定

在完成特定功能外設設定後，最後我們回頭處理 **SYS** 與 **RCC** 的核心配置。

#### SYS (系統調試)

在 SYS 頁面中，將 **Debug** 選擇為 **Serial Wire**。這非常重要，它確保了我們能透過板載的 ST-LINK 進行 SWD 介面的燒錄與除錯。


> **💡 小觀察**：在下方的列表可以看到 `System Wake-Up 1` 標示為紅底。這是因為該功能與我們先前設定的 **ADC1_IN0 (PA0)** 發生了腳位衝突，CubeMX 會主動阻擋重複分配。

<!-- ![](/assets/26_0217/SYS_Mode_and_Configuration.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/SYS_Mode_and_Configuration.png' | relative_url }}" width="800">
</p>

#### RCC (時鐘源設定)

針對時鐘源，我們選擇使用 **HSE (High Speed External)**。
參考 [UM1974 User Manual](https://www.st.com/resource/en/user_manual/um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf) 第 7.8.1 節，NUCLEO 板預設是由 ST-LINK 提供一個固定的 **8MHz MCO 訊號** 給 MCU。

<!-- ![](/assets/26_0217/F767ZI_OSC_Clock_Supply.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/F767ZI_OSC_Clock_Supply.png' | relative_url }}" width="800">
</p>

因此，在 RCC 的 HSE 設定中，必須選擇 **BYPASS Clock Source**。

* **Crystal/Ceramic Resonator**：適用於外部有接石英晶體/陶瓷諧振器（帶電容）的情況。
* **BYPASS Clock Source**：適用於外部直接輸入主動式時鐘訊號（如 ST-LINK 的 MCO）。

<!-- ![](/assets/26_0217/RCC_Mode.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/RCC_Mode.png' | relative_url }}" width="800">
</p>

在 **Parameter Settings** 中維持預設即可，但可留意到系統電壓 **VDD 設定為 3.3V**。

<!-- ![](/assets/26_0217/RCC_Configuration.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/RCC_Configuration.png' | relative_url }}" width="500">
</p>

#### MCO (Main Clock Output) 與時鐘驗證

為了確保 MCU 接收到的 **HSE (外部時鐘源)** 確實如手冊所述為 8MHz，我們可以使用 STM32 的 **MCO (主時鐘輸出)** 功能。透過將內部時鐘訊號除頻後從特定引腳輸出，並搭配 **邏輯分析儀** 進行觀察，即可驗證時鐘頻率的準確性。

<!-- ![](/assets/26_0217/MCO1_2.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/MCO1_2.png' | relative_url }}" width="500">
</p>

在 CubeMX 的 **RCC** 配置頁面中，勾選 **Master Clock Output 1 (或 2)** 即可開啟此功能。開啟後，你可以選擇想要輸出的時鐘源（如 HSE, HSI, PLLCLK 等）以及預分頻係數（Prescaler）。

<!-- ![](/assets/26_0217/RCC_Mode_MCO.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/RCC_Mode_MCO.png' | relative_url }}" width="800">
</p>

**實測結果分享：**
根據實際觀測，**HSE** 輸出確實為 **8MHz**，而內部震盪源 **HSI** 則為 **16MHz**。

## 🕒 五、 Clock Configuration (時鐘樹配置)

完成外設設定後，我們進入時鐘樹頁面進行最後調整。由於 STM32F767ZI 的效能強大，我們目標是將系統時鐘（HCLK）推到最高頻率：

1. **HSE 輸入**：確認 `Input frequency` 設定為 **8MHz**。
2. **時鐘源選擇**：將 `PLL Source Mux` 切換至 **HSE**。
3. **自動配置小技巧**：直接在 `HCLK` 欄位輸入目標頻率 **216 (MHz)** 並按下 Enter，CubeMX 會自動幫你計算出對應的  除頻與倍頻參數，非常方便。

<!-- ![](/assets/26_0217/Clock_Configuration.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/Clock_Configuration.png' | relative_url }}" width="800">
</p>

## 📂 六、 Project Manager (專案管理設定)

對於 Project Manager，這裡的設定由個人需求，下面的範例僅供演示。
實際到這裡設定完成，就可以按下右上角的 GENERATE CODE 按鈕了!
並記得可以儲存成.ioc，之後可以再次開啟並修改。

### 1. Project 區段

* **Project Name**: 為專案取個好辨識的名字。
* **Toolchain / IDE**: 若使用 Keil 則選擇 **MDK-ARM**。

<!-- ![](/assets/26_0217/Project_Manager_Project_Section.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/Project_Manager_Project_Section.png' | relative_url }}" width="800">
</p>

### 2. Code Generator 區段

* **Copy only the necessary library files**: 勾選此項可以讓專案資料夾更精簡，僅包含用到的 HAL 庫檔案。
* **Generate peripheral initialization as a pair of '.c/.h' files per peripheral**: 強烈建議勾選。這會將 GPIO、ADC 等初始化程式碼分開存放在獨立檔案中，避免 `main.c` 變得過於臃腫。

<!-- ![](/assets/26_0217/Project_Manager_Code_Generator_Section.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/Project_Manager_Code_Generator_Section.png' | relative_url }}" width="800">
</p>

### 3. Advanced Settings 區段

* 可以單獨設定各Driver使用 HAL 或者 LL，HAL 相對於來說 HAL 更 High Level 設定調整較少，不過編譯出的 code size 也會較大。

<!-- ![](/assets/26_0217/Project_Manager_Advanced_Settings_Section.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/Project_Manager_Advanced_Settings_Section.png' | relative_url }}" width="800">
</p>

### 🚀 產生程式碼

設定完成後，點擊右上角的 **「GENERATE CODE」** 按鈕，系統就會自動生成專案框架。

> **💡 溫馨提示**：記得將設定存成 `.ioc` 檔。日後若需要新增外設（例如增加更多的 ADC 通道），只要再次開啟該檔案修改並重新產生 Code 即可，這就是使用 CubeMX 開發的最大優勢。

## 🧑‍💻 七、 範例程式以及量測驗證

### 1. LED 燈閃爍與定時器延時實作

以下提供核心邏輯代碼。請注意，STM32CubeMX 僅負責生成定時器的初始化配置，**必須手動呼叫 `HAL_TIM_Base_Start()**` 才能正式啟動計數器。

```c
// TIM_MS   TIM2    32bit timer for MS delay	
#define TM_MS_GET()	    	__HAL_TIM_GET_COUNTER(&htim2)
// TIM_US   TIM3    16bit timer for US delay
#define TM_US_GET()	    	__HAL_TIM_GET_COUNTER(&htim3)

void TM_Delay_MS(__IO U16 ms)
{	
    U32 dly = 100 * ms;
    U32 start = TM_MS_GET();
    while((U32)(TM_MS_GET() - start) < dly) {
        __asm("NOP"); 
    }
}

void TM_Delay_US(__IO U16 us)
{
    U16 start = TM_US_GET();
    while ((U16)(TM_US_GET() - start) < us) {
        __asm("NOP"); 
    }
}

void TM_Init(void) 
{
    HAL_TIM_Base_Start(&htim2);
    HAL_TIM_Base_Start(&htim3);
}

void led_green_toggle(void) {
    HAL_GPIO_TogglePin(LD1_GREEN_GPIO_Port, LD1_GREEN_Pin);  // PB0
}

void led_blue_toggle(void) {
    HAL_GPIO_TogglePin(LD2_BLUE_GPIO_Port, LD2_BLUE_Pin);  // PB7
}

void led_red_toggle(void) {
    HAL_GPIO_TogglePin(LD3_RED_GPIO_Port, LD3_RED_Pin);  // PB14
}

int main(void)
{
    // Start TIM2,3
    TM_Init(); 
    while (1)
    {
        U16 delay_ms = 50;
        led_green_toggle();
        TM_Delay_MS(delay_ms);
        led_blue_toggle();
        TM_Delay_MS(delay_ms);
        led_red_toggle();
        TM_Delay_MS(delay_ms);
    }
}
```

#### 🔍 波形驗證
透過邏輯分析儀觀察 `led_toggle` 的波形，可以確認三個 LED 翻轉的時間間隔是否精確為 50ms。這也是驗證前面 **Clock Configuration** 設定是否正確最直觀的方法。

<!-- ![](/assets/26_0217/LED_Toggle_Waveform.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/LED_Toggle_Waveform.png' | relative_url }}" width="800">
</p>

### 2. ADC 量測電壓與 UART 資料傳輸

在本實作中，我們將讀取 **PA0** 的類比電壓，並透過 **UART3** 將結果輸出。同時，利用 **PA3** 腳位的電位變化，方便透過邏輯分析儀觀察 UART 的傳輸行為。

> **⚠️ 注意**：本範例採用最基礎的 **ADC Polling** 與 **UART Blocking** 模式。在實際專案中，這種方式會導致 CPU 進入等待狀態而造成效能低落。建議一般可使用 **Interrupt** 模式，甚至大量資料傳輸時使用 **DMA** 模式，解放 CPU。

```c
U8 Polling_ADC_Measurement(float *voltage, U8 timeout) {
    if (voltage == NULL) return HAL_ERROR; // avoid null reference
    U8 ret;
    ret = HAL_ADC_Start(&hadc1);
    if (ret != HAL_OK) {return ret;}

    // timeout (ms)
    ret = HAL_ADC_PollForConversion(&hadc1, timeout);
    if (ret == HAL_OK) {
        U32 adc_val = HAL_ADC_GetValue(&hadc1);
        // Vref = 3.3V, Resolution = 12B
        *voltage = ((float)adc_val * 3.3f) / 4095.0f;
    }
    HAL_ADC_Stop(&hadc1);
    return ret;
}

U8 Blocking_UART_Transmit(U8 timeout, const char * format, ... ) {
    U8 ret;
    char msg[64];
    va_list marker;

	va_start(marker, format);
    U16 len = vsnprintf(msg, sizeof(msg), format, marker);
	va_end(marker);
    
    if (len > 0) {
        // (sizeof(msg) - 1) avoid overflow, the last always '\0'
        U16 send_len = (len < sizeof(msg)) ? len : (U16)(sizeof(msg) - 1);
        ret = HAL_UART_Transmit(&huart3, (PU8)msg, send_len, timeout);
    } else {
        ret = HAL_ERROR;
    }
    return ret;
}

void pa3_hi(void) {
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_SET);
}

void pa3_lo(void) {
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_RESET);
}

int main(void)
{
    TM_Init(); 
    while (1)
    {
        float curr_voltage = 0;
        if (Polling_ADC_Measurement(&curr_voltage, 10) == HAL_OK) {
        pa3_hi();
        Blocking_UART_Transmit(100, "Voltage: %.2fV\n", curr_voltage);
        }
        pa3_lo();
        TM_Delay_MS(10);
    }
}
```

#### 📐 ADC 數值換算邏輯

由於 ADC 回傳的是數位量化值，我們需要透過參考電壓比例換算回實際電壓：

$$\frac{V_{input}}{V_{reference}} = \frac{ADC_{val}}{ADC_{max}}$$

已知前面 ADC 設定時解析度為 **12 bits**，且參考電壓是工作電壓 3.3V，因此換算公式如下：

$$V_{input} = \frac{ADC_{val} * V_{reference}}{ADC_{max}} = \frac{ADC_{val} * 3.3}{2^{12} -1} = \frac{ADC_{val} * 3.3}{4095}$$

#### 🔍 波形驗證

**1. 整體週期觀察**
從 Overview 波形可以看到，大約每 **10ms** PA3 會拉高一次，隨即 TX 引腳開始輸出資料。這驗證了我們主迴圈的延時邏輯：先執行 ADC 採樣，隨後立即進行 UART 傳送。

<!-- ![](/assets/26_0217/ADC_UART_Waveform.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/ADC_UART_Waveform.png' | relative_url }}" width="800">
</p>

**2. 資料內容驗證**
解碼 TX 訊號後的 String 結果顯示為 `"Voltage: 3.29V\n"`。這是因為我們將 3.3V 短路接到 PA0 供 ADC 量測。

<!-- ![](/assets/26_0217/hex_to_ascii.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/hex_to_ascii.png' | relative_url }}" width="600">
</p>

**3. UART 時序分析 (Baud Rate 驗證)**
放大觀察單個 Bit 的持續時間約為 **8.6~8.7 us**。
這與我們在 CubeMX 中設定的 BaudRate **115200** 極為接近，誤差在容許範圍內。

<!-- ![](/assets/26_0217/UART_Timing.png) -->
<p align="center">
<img src="{{ '/assets/26_0217/UART_Timing.png' | relative_url }}" width="800">
</p>

此外，從波形可觀察到標準的 UART 協定：

* **Start Bit**：TX 由高電位變為低電位（LO）代表資料開始。
* **Data Bits**：以 Byte 為基本單位，每 8 bits 為一組進行傳送。

## 📚 Reference
* [UM1974 - STM32 Nucleo-144 boards (MB1137)](https://www.st.com/resource/en/user_manual/um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf)
* [DS11532 - STM32F765xx STM32F767xx STM32F768Ax STM32F769xx](https://www.st.com/resource/en/datasheet/stm32f765bi.pdf)
