---
layout: page
title: "Combinational Logic - 3-bit population"
categories: [Verilog]
day: 26
date: 2025-10-15
---

## 📌 Introduction
A "population count" circuit counts the number of '1's in an input vector. Build a population count circuit for a 3-bit input vector.

## 🧑‍💻 Code Example
```verilog
module top_module( 
    input [2:0] in,
    output [1:0] out );
    integer i;
    always @(*) begin
        out = 0;
        for  (i=0;i<3;i++) begin
            out = in[i] + out;
        end
    end
endmodule
```
> **Without initializing `out = 0;`, the addition uses an unknown (X) value, causing the simulation result to float or remain undefined.**


## 📚 Reference
* [HDLBits Problem - Popcount3](https://hdlbits.01xz.net/wiki/Popcount3)
