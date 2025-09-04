---
layout: page
title: "Day 5"
categories: [Verilog]
---

## 📌 Module shift + Mux
![alt text](../assets/Module_shift8.png)

## 🧑‍💻 Code Example
```verilog
// 4-to-1, 8-bit mux (combinational)
module mux41(input [7:0] in0, input [7:0] in1, 
             input [7:0] in2, input [7:0] in3, 
             input [1:0]sel, output reg [7:0]out);
    always @(*) begin
        case (sel)
            2'b00: out = in0;
            2'b01: out = in1;
            2'b10: out = in2;
            2'b11: out = in3;
            default: out=8'b0;
        endcase
    end
endmodule

module top_module ( 
    input clk, 
    input [7:0] d, 
    input [1:0] sel, 
    output [7:0] q 
);
    wire [7:0]med1; wire [7:0]med2; wire [7:0]med3;
    my_dff8 mod1(clk, d, med1);
    my_dff8 mod2(clk, med1, med2);
    my_dff8 mod3(clk, med2, med3);
    mux41 sel_mux(d, med1, med2, med3, sel, q);
endmodule
```
> Note: Because ```out``` is in always block, it should be declared by ```output reg``` in verilog.

## 📚 Reference
[HDLBits Problem - Module shift8](https://hdlbits.01xz.net/wiki/Module_shift8)
