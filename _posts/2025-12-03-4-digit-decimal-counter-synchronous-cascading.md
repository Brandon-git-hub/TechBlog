---
layout: post
title: "4-Digit Decimal Counter (Synchronous Cascading)"
categories: [Verilog]
date: 2025-12-03
---

## 📌 Question
Build a 4-digit BCD (binary-coded decimal) counter. Each decimal digit is encoded using 4 bits: q[3:0] is the ones digit, q[7:4] is the tens digit, etc. For digits [3:1], also output an enable signal indicating when each of the upper three digits should be incremented.

## 🧑‍💻 Code Example

```verilog
module BCD(input clk, input reset, input enable, output carry, output reg [3:0] Q);
    always @ (posedge clk) begin
        if (reset)
            Q <= 4'b0;
        else if (enable) begin
            if (Q==4'h9)
                Q <= 4'b0;
            else
           		Q <= Q + 4'b1; 
        end
    end
    assign carry = (Q==4'h9) && enable;
endmodule

module top_module (
    input clk,
    input reset,   // Synchronous active-high reset
    output [3:1] ena,
    output [15:0] q);
    
    wire [3:1] internal_wire;
    assign ena = internal_wire;
    wire dummy_wire;
    BCD counter0(.clk(clk), .reset(reset), .enable(1'b1), .carry(internal_wire[1]), .Q(q[3:0]));
    BCD counter1(.clk(clk), .reset(reset), .enable(internal_wire[1]), .carry(internal_wire[2]), .Q(q[7:4]));
    BCD counter2(.clk(clk), .reset(reset), .enable(internal_wire[2]), .carry(internal_wire[3]), .Q(q[11:8]));
    BCD counter3(.clk(clk), .reset(reset), .enable(internal_wire[3]), .carry(dummy_wire), .Q(q[15:12]));
	
endmodule
```
> ```ena```由於作為輸出，最好不要又做為內部的集聯，另外宣告```wire```供內部使用。

<img src="{{ '/assets/day50/Counting.png' | relative_url }}" width="700">

<img src="{{ '/assets/day50/100_rollover_1.png' | relative_url }}" width="700">

<img src="{{ '/assets/day50/100_rollover_2.png' | relative_url }}" width="700">

## 📚 Reference
* [HDLBits Problem - Countbcd](https://hdlbits.01xz.net/wiki/Countbcd)
