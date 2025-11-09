---
layout: page
title: "Conditional ternary operator"
categories: [Verilog]
day: 18
date: 2025-09-23
---

## 📌 Introduction
Verilog has a ternary conditional operator ( ? : ) much like C:

(condition ? if_true : if_false)

This can be used to choose one of two values based on condition (a mux!) on one line, without using an if-then inside a combinational always block.

## 🧑‍💻 Code Example

```verilog
module top_module (
    input [7:0] a, b, c, d,
    output [7:0] min);
    
    wire [7:0] r0, r1;
    assign r0 = (a<b) ? a : b;
    assign r1 = (c<d) ? c : d;
    assign min = (r0<r1) ? r0 : r1;

endmodule
```

## 📚 Reference
* [HDLBits Problem - Conditional](https://hdlbits.01xz.net/wiki/Conditional)
