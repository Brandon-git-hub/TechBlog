---
layout: page
title: "Reduction Operators"
categories: [Verilog]
day: 19
---

## 📌 Introduction
The reduction operators can do AND, OR, and XOR of the bits of a vector, producing one bit of output:
``` verilog
& a[3:0]     // AND: a[3]&a[2]&a[1]&a[0]. Equivalent to (a[3:0] == 4'hf)
| b[3:0]     // OR:  b[3]|b[2]|b[1]|b[0]. Equivalent to (b[3:0] != 4'h0)
^ c[2:0]     // XOR: c[2]^c[1]^c[0]
```
These are unary operators that have only one operand (similar to the NOT operators ! and ~). You can also invert the outputs of these to create NAND, NOR, and XNOR gates, e.g., (~& d[7:0]).


## 🧑‍💻 Code Example

### Even Parity
```verilog
module top_module (
    input [7:0] in,
    output parity); 
    assign parity = (~^ in[7:0]) ? 1'b0 : 1'b1;
endmodule
```

### Gates100
```verilog
module top_module( 
    input [99:0] in,
    output out_and,
    output out_or,
    output out_xor 
);
    assign out_and = & in[99:0];
    assign out_or  = | in[99:0];
    assign out_xor = ^ in[99:0];
endmodule
```

## 📚 Reference
* [HDLBits Problem - Reduction](https://hdlbits.01xz.net/wiki/Reduction)
* * [HDLBits Problem - Gates100](https://hdlbits.01xz.net/wiki/Gates100)
