---
layout: post
title: "通訊原理基礎科普"
subtitle: "分享影片【硬核科普】WiFi是怎麼傳遞資訊的？ 把資訊裝進電磁波有多難？ --- 硬體茶談"
categories: [Wifi, Wireless Communication]
date: 2026-05-01
lang: zh-Hant
---

## 📌 前言

今天在B站上，看到介紹Wifi的影片，將通訊原理的基礎整理的非常好，搭配動畫演示，令我欽佩不已。
因此整理下影片的內容。

為了不侵犯到作者的版權，所以自行吸收轉為文字，非常建議去看下原影片:
[【硬核科普】WiFi是怎麼傳遞資訊的？ 把資訊裝進電磁波有多難？](https://www.bilibili.com/video/BV1LS9eBxEGD/?spm_id_from=333.1387)


## 📡 什麼是電磁波?

從導線通電，發現電生磁⚡➡️🧲，發現電磁效應。後到法拉第發現在磁鐵在線圈中移動，產生電流 🧲➡️⚡。
赫茲在實驗室中，發現電磁波的存在，並且測量了電磁波的速度，發現和光速相同，證明了馬克士威的理論。

我們家中的路由器，其天線會透過快速電流變化產生電磁波，這些電磁波在空氣中，電場激發磁場，磁場又維持電場，形成一個自我維持的波動，像水波一樣向四周輻射出去，這就是電磁波。

當天線實際傳送到我們的接收裝置天線時，會驅動天線中的電子做受迫運動，根據電流的變化，產生電壓，這些電壓的變化就可以被解讀為數位訊號，進而還原成我們傳送的資訊。

## 📔 如何把資訊裝進電磁波?

### 調變（Modulation）

電磁波有三個基本的特性：振幅、頻率和相位。這些特性可以用來調變訊號，將資訊編碼進電磁波中。

- 振幅調變（Amplitude Modulation, AM）：通過改變電磁波的振幅來傳遞資訊。例如，振幅大代表1，振幅小代表0。
- 頻率調變（Frequency Modulation, FM）：通過改變電磁波的頻率來傳遞資訊。例如，頻率高代表1，頻率低代表0。
- 相位調變（Phase Modulation, PM）：通過改變電磁波的相位來傳遞資訊。例如，相位改變180度代表1，保持不變代表0。

而所謂的ASK、FSK、PSK，就是分別對應振幅調變、頻率調變和相位調變的技術。

![](/assets/26_0501/ASK_FSK_PSK.jpg)

<p align="center">
<img src="{{ '/assets/26_0501/ASK_FSK_PSK.jpg' | relative_url }}" width="500">
</p>

### QAM（Quadrature Amplitude Modulation）

但是一個波形只能傳達一個bit的資訊，效率實在不夠高。

對於PSK來說，還有一種特殊的調變方式叫做QPSK（Quadrature Phase Shift Keying），以四種不同的初始相位來表示兩個bit的組合，這樣就可以在同一個頻率上傳輸更多的資訊。

這樣還不夠，我們可以相位加振幅，進行排列組合。為了方便可視與轉化為二進制，還創造了星座圖（Constellation Diagram），將不同的相位和振幅組合對應到二進制的點上，這樣就可以在同一個頻率上傳輸更多的資訊。

以16-QAM（Quadrature Amplitude Modulation）為例，使用16個不同的相位和振幅組合，利用了12種相位、3種振幅，可以同時傳輸4個bit的資訊，這樣就大大提高了頻譜效率。

![](/assets/26_0501/QAM_Constellation_Diagram.jpg)

<p align="center">
<img src="{{ '/assets/26_0501/QAM_Constellation_Diagram.jpg' | relative_url }}" width="500">
</p>

QAM 建構了現代高速無線通訊的基礎，從WiFi到4G、5G都在使用這種調變技術來實現高速數據傳輸。
Wifi 4 使用了64-QAM，Wifi 5 使用了256-QAM，而Wifi 6 則使用了1024-QAM，到最新的Wifi 7，則使用了4096-QAM。

![](/assets/26_0501/High_speed_wireless.jpg)

<p align="center">
<img src="{{ '/assets/26_0501/High_speed_wireless.jpg' | relative_url }}" width="500">
</p>

傳送的波形，我們也稱之為符號（Symbol），而當我們將符號一個個序列發送出去，由於多路徑效應（Multipath Effect），會導致符號之間的干擾，這就是所謂的ISI（Inter-Symbol Interference）。因此每個符號間會有保護間隔，稱為循環前綴（Cyclic Prefix），其必須大於多路徑反射的最大時間差，以減少ISI的影響，但這也意味著限制傳輸速率上的受限。

### OFDM（Orthogonal Frequency Division Multiplexing）

為了進一步提高傳輸效率，我們可將不同頻率的波形，每個也都使用QAM，將所有波形疊加合併發射，接收端透過濾波器將各頻率的波形分離出來，數據就像從串行轉換為並行一樣，這就是FDM（Frequency Division Multiplexing）的原理。

每個頻率的波形我們稱為子載波，由於其每個在頻譜空間會占用一小段連續的範圍，因此若要其彼此互不干擾，最簡單的方式是中間加保護間隔，但頻譜資源是有限的，分配給Wifi的資源，2.4GHz Wifi 只有80MHz，5GHz Wifi 從 5.15GHz 到 5.850GHz，這樣的頻譜資源是非常有限的，因此我們需要更有效率的方式來分配子載波。

![](/assets/26_0501/electromagnetic_spectrum.jpg)

<p align="center">
<img src="{{ '/assets/26_0501/electromagnetic_spectrum.jpg' | relative_url }}" width="500">
</p>

當我們將子載波的頻率間隔，等於符號週期的倒數，這樣就會產生正交（Orthogonal）的關係，子載波之間的頻譜重疊，每個子載波在自己的中心頻率上信號強度最高，子載波的頻譜在其他子載波的頻率上剛好為零，因此不會互相干擾，這就是OFDM（Orthogonal Frequency Division Multiplexing）的原理。

![](/assets/26_0501/OFDM.jpg)

<p align="center">
<img src="{{ '/assets/26_0501/OFDM.jpg' | relative_url }}" width="500">
</p>

### MIMO（Multiple Input Multiple Output）

![](/assets/26_0501/MIMO.jpg)

<p align="center">
<img src="{{ '/assets/26_0501/MIMO.jpg' | relative_url }}" width="500">
</p>

為了進一步提高傳輸效率，我們可以使用多天線技術，透過多個發射天線和多個接收天線，利用空間分集（Spatial Diversity）和空間復用（Spatial Multiplexing）的原理，在同一頻率上同時傳輸多條獨立的數據流，這就是MIMO（Multiple Input Multiple Output）的原理。

## 📚 參考資料
[【硬核科普】WiFi是怎麼傳遞資訊的？ 把資訊裝進電磁波有多難？](https://www.bilibili.com/video/BV1LS9eBxEGD/?spm_id_from=333.1387)
