---
layout: page
title: "Combinational Logic - Adders"
categories: [Verilog]
day: 30, 32
---

## 📌 Introduction
In digital logic design, **adders** are fundamental building blocks used for performing binary addition.  
A *half adder* adds two single-bit inputs, while a *full adder* also includes a carry-in input.  
By cascading full adders, we can construct a **ripple-carry adder** to handle multi-bit operations.

## 🧑‍💻 Code Example

### Half Adder
```verilog
module top_module( 
    input a, b,
    output cout, sum );
	assign cout = a & b;
    assign sum  = a ^ b;
endmodule
```

### Full Adder
```verilog
module top_module( 
    input a, b, cin,
    output cout, sum );
    assign cout = (a & b) | (a & cin) | (b & cin);
    assign sum  = a ^ b ^ cin;
endmodule
```

### 3-bit Binary Ripple-Carry Adder
```verilog
module Fadd( 
    input a, b, cin,
    output cout, sum );
    assign cout = (a & b) | (a & cin) | (b & cin);
    assign sum  = a ^ b ^ cin;
endmodule

module top_module( 
    input [2:0] a, b,
    input cin,
    output [2:0] cout,
    output [2:0] sum );
    
    Fadd Add0(.a(a[0]), .b(b[0]), .cin(cin), .cout(cout[0]), .sum(sum[0]));
    Fadd Add1(.a(a[1]), .b(b[1]), .cin(cout[0]), .cout(cout[1]), .sum(sum[1]));
    Fadd Add2(.a(a[2]), .b(b[2]), .cin(cout[1]), .cout(cout[2]), .sum(sum[2]));
	
endmodule
```

### 4-bit Binary Ripple-Carry Adder
![alt text](../assets/day32/4-bit.png)
```verilog
module FA(input a, input b, input cin, output sum, output cout);
	assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (a & cin) | (b & cin);
endmodule

module top_module (
    input [3:0] x,
    input [3:0] y, 
    output [4:0] sum);
    wire [2:0] cout;
    FA add0(.a(x[0]), .b(y[0]), .cin(1'b0), .sum(sum[0]), .cout(cout[0]));
    FA add1(.a(x[1]), .b(y[1]), .cin(cout[0]), .sum(sum[1]), .cout(cout[1]));
    FA add2(.a(x[2]), .b(y[2]), .cin(cout[1]), .sum(sum[2]), .cout(cout[2]));
    FA add3(.a(x[3]), .b(y[3]), .cin(cout[2]), .sum(sum[3]), .cout(sum[4]));
endmodule
```

## 📚 Reference
* [HDLBits Problem - Hadd](https://hdlbits.01xz.net/wiki/Hadd)
* [HDLBits Problem - Fadd](https://hdlbits.01xz.net/wiki/Fadd)
* [HDLBits Problem - Adder3](https://hdlbits.01xz.net/wiki/Adder3)
* [HDLBits Problem - m2014_q4j](https://hdlbits.01xz.net/wiki/Exams/m2014_q4j)
