---
layout: post
title: "JTAG"
categories: [Interfaces]
date: 2025-09-21
---

## 📌 Joint Test Action Group

<!-- ![alt text](../assets/day17/Schematic_Diagram_of_a_JTAG_enabled_device.png) -->
<img src="{{ '/assets/day17/Schematic_Diagram_of_a_JTAG_enabled_device.png' | relative_url }}" width="350">

* TCK (Test Clock) – this signal synchronizes the internal state machine operations.
TMS (Test Mode Select) – this signal is sampled at the rising edge of TCK to determine the next state.
* TDI (Test Data In) – this signal represents the data shifted into the device’s test or programming logic. It is sampled at the rising edge of TCK when the internal state machine is in the correct state.
* TDO (Test Data Out) – this signal represents the data shifted out of the device’s test or programming logic and is valid on the falling edge of TCK when the internal state machine is in the correct state.
* TRST (Test Reset) – this is an optional pin which, when available, can reset the TAP controller’s state machine.

## 📚 Reference
<!-- * [JTAG_IEEE-Std-1149.1-2001](/assets/day17/JTAG_IEEE-Std-1149.1-2001.pdf) -->
* [JTAG_IEEE-Std-1149.1-2001]({{ site.baseurl }}/assets/day17/JTAG_IEEE-Std-1149.1-2001.pdf)
* [XJTAG - What is JTAG and how can I make use of it?](https://www.xjtag.com/about-jtag/what-is-jtag/?v=255a5cac7685)
* [XJTAG - Technical Guide to JTAG](https://www.xjtag.com/about-jtag/jtag-a-technical-overview/?v=255a5cac7685)
* [JTAG协议及接口](https://blog.csdn.net/worf1234/article/details/7312184)
* [接口与协议学习笔记-JTAG协议的简单理解（四）](https://blog.csdn.net/uiojhi/article/details/107649230)
