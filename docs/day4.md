---
layout: page
title: "Module shift"
categories: [Verilog]
day: 4
date: 2025-09-03
---

## 📌 Introduction
![alt text](../assets/Module_shift.png)

## 🧑‍💻 Code Example
```verilog
module top_module ( input clk, input d, output q );
    wire q1_out;
    wire q2_out;
    my_dff dff1(.clk(clk), .d(d), .q(q1_out));
    my_dff dff2(.clk(clk), .d(q1_out), .q(q2_out));
    my_dff dff3(.clk(clk), .d(q2_out), .q(q));
endmodule
```

## 📚 Reference
[HDLBits Problem - Module shift](https://hdlbits.01xz.net/wiki/Module_shift)
