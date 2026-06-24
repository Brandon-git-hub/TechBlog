---
layout: post
title: "U-Boot 和 Kernel 編譯與佈署"
subtitle: "Linux 嵌入式課程 0"
categories: [Linux]
date: 2026-06-22
lang: zh-Hant
---

## 📌 


## VMRun

```
# 1. 更新軟體源並安裝開源版 VMware Tools
sudo apt-get update
sudo apt-get install -y open-vm-tools

# 2. 強制啟動服務，並設定開機自動執行
sudo systemctl enable --now open-vm-tools

# 3. 檢查服務狀態（應該要顯示綠色的 active (running)）
sudo systemctl status open-vm-tools
```

## USB SD CARD
抓出它的 VID 和 PID（硬體身份證）
Device ID                : USB\VID_14CD&PID_1212\121220160204
Hardware IDs             : USB\VID_14CD&PID_1212&REV_0100 USB\VID_14CD&PID_1212

VID_14CD
PID_1212

usb.autoConnect.device0 = "vid:0x55aa pid:0x1234"
usb.autoConnect.device0.flags = "force"

brandon@brandon-VMware-Virtual-Platform:~$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0    60G  0 disk
├─sda1   8:1    0     1M  0 part
└─sda2   8:2    0    60G  0 part /
sdb      8:16   1   7.5G  0 disk
├─sdb1   8:17   1  70.6M  0 part /media/brandon/boot
└─sdb2   8:18   1   7.4G  0 part /media/brandon/rootfs
sr0     11:0    1  97.8M  0 rom  /media/brandon/CDROM
sr1     11:1    1   6.2G  0 rom  /media/brandon/Ubuntu 24.04.4 LTS amd64

## 編譯 Bootloader
注意等號左右不要空格
export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabi-

### 瘦身
# 叫 Git 在本地進行淺層收縮，只保留最後 1 筆 commit 歷史
git fetch --depth=1

# 1. 告訴 Git 所有的操作紀錄（reflog）立刻過期，不要再保留任何備份歷史
git reflog expire --expire=now --all

# 2. 發動積極垃圾資源回收 (Garbage Collection)，並把硬碟空間吐出來
git gc --prune=now --aggressive

# 強制讓本地緩存的遠端分支歷史也收縮到 depth 1
git fetch --depth=1 origin master

# 物理刪除 Git 的各種臨時歷史指針緩存
rm -f .git/FETCH_HEAD .git/ORIG_HEAD .git/packed-refs

# 再次徹底強制回收所有孤兒節點，不留任何情面
git gc --prune=now --aggressive

Developer: Reload Window（重新載入視窗）

# 1. 叫 Git 自動去底層資料夾搜尋那些還沒被徹底抹除的最新 Commit ID
git fsck --lost-found


# 1. 拒絕所有 Tag
git config remote.origin.tagOpt --no-tags

# 2. 限制只抓 master 分支 (可自行替換分支名)
git config remote.origin.fetch "+refs/heads/master:refs/remotes/origin/master"

# 3. 清理目前的雜亂紀錄
git remote prune origin

# 檢查整個 u-boot 資料夾（包含隱藏的 .git）實際佔用的硬碟空間
du -sh .

# 1. 進入 U-Boot 的 CPU 架構目錄
cd arch/

# 2. 除了 arm 之外，其他無關的架構資料夾全部暴力刪除
find . -maxdepth 1 -type d ! -name '.' ! -name 'arm' -exec rm -rf {} +

# 3. 回到 U-Boot 根目錄
cd ..

## Kernel

mkdir -p beaglebone_linux_bsp/u-boot beaglebone_linux_bsp/kernel beaglebone_linux_bsp/rootfs beaglebone_linux_bsp/output

https://github.com/beagleboard/linux
git clone --depth 1 --single-branch --branch v6.6.58-ti-arm32-r15 https://github.com/beagleboard/linux.git

sudo apt-get install -y lzop u-boot-tools

## 📚 Reference
* https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-pro/using-the-vmrun-command-to-control-virtual-machines/running-vmrun-commands/syntax-of-vmrun-commands.html

