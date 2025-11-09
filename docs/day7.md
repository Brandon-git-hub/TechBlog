---
layout: page
title: "Carry-select adder"
categories: [Verilog]
day: 7
date: 2025-09-07
---

## 📌 Introduction
![alt text](../assets/Module_cseladd.png)

## 🧑‍💻 Code Example
```verilog
module top_module(
    input [31:0] a,
    input [31:0] b,
    output [31:0] sum
);
    wire [15:0]out_lo; wire [15:0]out_hi0; wire [15:0]out_hi1; 
    wire cout_lo, cout_hi0_unused, cout_hi1_unused;
    add16 add_i0(.a(a[15:0]),  .b(b[15:0]),  .cin(1'b0), .sum(out_lo), .cout(cout_lo));
    add16 add_i1(.a(a[31:16]), .b(b[31:16]), .cin(1'b0), .sum(out_hi0), .cout(cout_hi0_unused));
    add16 add_i2(.a(a[31:16]), .b(b[31:16]), .cin(1'b1), .sum(out_hi1), .cout(cout_hi1_unused));

    // --- Option A: direct ternary ---
    assign sum[31:16] = cout_lo ? out_hi1 : out_hi0;

    // --- Option B: use a mux module ---
    //mux_21 sel_mux(out_hi0, out_hi1, cout_lo, sum[31:16]);

    assign sum[15:0] = out_lo;
endmodule

module mux_21(input [15:0]in_1, input [15:0]in_2, input sel, output reg [15:0]out);
    always @(in_1, in_2, sel) begin
        out = sel ? in_2 : in_1;
    end 
endmodule
```
> Note: We can implement either a direct ternary operator or a mux module. The ternary option is pure combinational and avoids introducing a ```reg``` unnecessary.

## 📚 Reference
[HDLBits Problem - Module cseladd](https://hdlbits.01xz.net/wiki/Module_cseladd)
