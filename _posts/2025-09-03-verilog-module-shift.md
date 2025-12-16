---
layout: post
title: "Module shift"
categories: [Verilog]
date: 2025-09-03
---

## 📌 Introduction

<img src="{{ '/assets/day4/Module_shift.png' | relative_url }}" width="700">

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
