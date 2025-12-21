---
layout: post
title: "Four-bit binary counter"
categories: [Verilog]
date: 2025-11-20
---

## 📌 Question
Build a 4-bit binary counter that counts from 0 through 15, inclusive, with a period of 16. The reset input is synchronous, and should reset the counter to 0.
<!-- ![alt text](../assets/day46/example.png) -->
<img src="{{ '/assets/day46/example.png' | relative_url }}" width="600">

## 🧑‍💻 Code Example

```verilog
module top_module (
    input clk,
    input reset,      // Synchronous active-high reset
    output reg [3:0] q);
    
    always @ (posedge clk) begin
        if (reset) begin
           q <= 4'b0;
        end
        else begin
           q <= q + 1'b1; 
        end
    end

endmodule
```
<!-- ![alt text](../assets/day46/block_diagram.png) -->
<img src="{{ '/assets/day46/block_diagram.png' | relative_url }}" width="500">

## 📚 Reference
* [HDLBits Problem - Count15](https://hdlbits.01xz.net/wiki/Count15)
* [DigitalJS Online](https://digitaljs.tilk.eu/)
