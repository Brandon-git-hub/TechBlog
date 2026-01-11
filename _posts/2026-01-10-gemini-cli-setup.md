---
layout: post
title: "Gemini CLI 設定指南"
subtitle: "在命令列介面中與 Gemini 模型互動"
categories: [Gemini CLI]
date: 2026-01-10
lang: zh-Hant
---

## 📌 Gemini CLI 簡單介紹

一般使用者都已經很習慣透過網頁或是APP，來與AI大模型互動。
但有些進階使用者會希望能夠透過命令列介面（CLI）來操作，這樣可以更靈活地整合到自己的工作流程中。
Gemini CLI 就是為了滿足這些需求而設計的工具。

我個人為何會想使用 Gemini CLI 呢？ 
主要是因為希望能夠在本地端的終端機中，快速地與 Gemini 模型互動，不需切換到瀏覽器或是其他應用程式，這樣可以節省時間並提高效率。 
以及使用 ```@file``` 功能來讀取工作區檔案內容，讓我能夠更方便地將資料傳遞給模型進行處理。

<!-- ![alt text](/assets/26_0110/Gemini_CLI_Begin.png) -->

<p align="center">
<img src="{{ '/assets/26_0110/Gemini_CLI_Begin.png' | relative_url }}" width="700">
</p>



## 🧑‍💻 安裝說明

安裝Gemini CLI 需要Node.js環境，我這裡選擇安裝在conda虛擬環境中。
安裝上程序很簡單，請依照以下步驟進行：

```bash
# 建立並啟動conda虛擬環境, 建議使用Python 3.12以上版本
conda create -n gemini-cli -p python=3.14 -y
conda activate gemini-cli
# 安裝Node.js
conda install -c conda-forge nodejs -y
# 安裝Gemini CLI
npm install -g @google/gemini-cli
```

確認安裝成功：

```bash
gemini-cli --version
```

## 🔔 設定API說明

安裝完成後，接下來需要設定我們的API金鑰。
請先前往 [Google AI Studio](https://ai.google.com/studio) 申請並取得你的API金鑰。
在下面圖中的頁面的左側選單中，點擊「Get API Key」選項，進入後右上角會看到「Create API Key」按鈕。

<!-- ![alt text](/assets/26_0110/Google_AI_Studio.png) -->

<p align="center">
<img src="{{ '/assets/26_0110/Google_AI_Studio.png' | relative_url }}" width="700">
</p>

由於建立API金鑰需要導入專案，因此如果你還沒有專案的話，請先建立一個新的專案，然後再點擊「Create API Key」按鈕來生成你的API金鑰。
然後建議設定Billing中的付款方式，升級到```Tier 1```，這樣會有更多的免費額度可以使用，否則```Tier 0```的免費額度非常有限。

不需擔心設定付款方式就會被收費，因為只要在免費額度內使用是完全不會產生費用的。
如果擔心目前的額度使用不夠，可以在API Keys的右側找到view usage按鈕，點擊後可以看到目前的各模型使用狀況以及剩餘額度。

取得API金鑰後，接下來我們需要將它設定到系統的環境變數中。
請依照以下步驟進行：

For windows系統：
```bash
# 永久設定API金鑰, 設定完成另開一個新的終端機視窗才會生效
setx GEMINI_API_KEY "你的API金鑰"
# Windows PowerShell, 可用以下指令確認是否設定成功
echo $env:GEMINI_API_KEY  
```

For Linux系統：
```bash
# 永久設定API金鑰, 將以下指令加入到~/.bashrc或~/.zshrc中
nano ~/.bashrc  # 或 nano ~/.zshrc
# 在檔案末尾加入以下一行
export GEMINI_API_KEY="你的API金鑰"
# 使設定立即生效
source ~/.bashrc  # 或 source ~/.zshrc
# 確認是否設定成功
echo $GEMINI_API_KEY
```

完成設定後，我們就可以開始使用Gemini CLI來與模型互動了！

```bash
gemini "Hello, Gemini!"
```

## ⚙️ 基礎設定與使用

Gemini CLI 透過node.js建立了一個方便的命令列介面，因此我們可以透過```gemini```命令進入互動式模式。

<!-- ![alt text](/assets/26_0110/Gemini_CLI_Begin.png) -->

<p align="center">
<img src="{{ '/assets/26_0110/Gemini_CLI_Begin.png' | relative_url }}" width="700">
</p>

### ```/help```指令

在互動式模式中，我們可以直接輸入指令來與模型互動。
例如，我們可以使用```/help```指令來查看所有可用的命令。

### ```/model```指令

由於撰寫本文時，Gemini 3 模型在CLI中剛推出，因此我們可以需要使用```/settings```進入設定頁面，將```Preview Features (e.g., models) ```選項打開，這樣才能使用最新的模型。
若希望將Gemini 3 模型設為預設模型，可以使用```/model```指令來選擇預設模型。

### ```Gemini CLI Companion```插件

由於我本人主要是使用VS Code作為主要的開發環境，因此我會建議大家可以安裝```Gemini CLI Companion```插件。
這可以幫助Gemini CLI更好地整合到VS Code中，功能如: 得知使用者目前開啟的檔案、生成程式碼後可以直接修改檔案等。

### ```/init``` 和```/memory```指令

接下來介紹一個我很喜歡的功能：```/init```指令。
這個指令可以快速總覽目前工作區中的檔案，並生成一個新的```GEMINI.md```檔案，裡面會包含目前工作區中所有檔案的摘要說明。
這樣我們就可以很方便地讓模型了解我們目前的專案狀況，並且可以直接在互動式模式中引用這些檔案的內容。

生成```GEMINI.md```檔案後，可以使用```/memory list```語法來查看目前的記憶內容，如果沒有剛生成的```GEMINI.md```檔案，請使用```/memory refresh```指令來更新記憶內容。
另外```/memory add```也可以手動新增記憶內容，其內容最好是與所有專案都通用的說明，讓我們省去每次進入互動式模式都要重新說明的麻煩。

### ```/quit```指令

當然如果要退出互動式模式，可以使用```/quit```指令，或者是直接按```Ctrl + C``` 兩次來結束。

## 📝 結語

看到這裡，相信大家已經對Gemini CLI有了一定的了解。
接下來就可以開始探索更多的功能，並將它整合到自己的工作流程中，提升工作效率！


## 📚 Reference
* [Gemini CLI GitHub Repository](https://github.com/google-gemini/gemini-cli)
* [Gemini CLI 官方使用手冊 - CLI 指令](https://gemini-cli.gh.miniasp.com/cli/commands.html)
