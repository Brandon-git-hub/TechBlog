---
layout: page
title: "Combinational Logic - Basic Gates"
categories: [Verilog]
day: 22
---

## 📌 Introduction

### Wire
```verilog
module top_module (
    input in,
    output out);
	assign out = in;
endmodule
```

### GND
```verilog
module top_module (
    output out);
	assign out = 1'b0;
endmodule
```

### XOR
```verilog
module top_module (
    input in1,
    input in2,
    output out);
    assign out = !(in1 | in2);
endmodule
```

### And-not Gate
```verilog
module top_module (
    input in1,
    input in2,
    output out);
	assign out = in1 & !in2;
endmodule
```

### Two Gates
```verilog
module top_module (
    input in1,
    input in2,
    input in3,
    output out);
    assign out = !(in1 ^ in2) ^ in3;
endmodule
```

### More Gates
```verilog
module top_module( 
    input a, b,
    output out_and,
    output out_or,
    output out_xor,
    output out_nand,
    output out_nor,
    output out_xnor,
    output out_anotb
);
	assign out_and = a & b;
    assign out_or  = a | b;
    assign out_xor = a ^ b;
    assign out_nand = !(a & b);
    assign out_nor  = !(a | b);
    assign out_xnor = !(a ^ b);
    assign out_anotb = a & !b;
endmodule
```



## 📚 Reference
* [HDLBits Problem - Wire](https://hdlbits.01xz.net/wiki/Exams/m2014_q4h)
* [HDLBits Problem - GND](https://hdlbits.01xz.net/wiki/Exams/m2014_q4i)
* [HDLBits Problem - XOR](https://hdlbits.01xz.net/wiki/Exams/m2014_q4e)
* [HDLBits Problem - And-not Gate](https://hdlbits.01xz.net/wiki/Exams/m2014_q4f)
* [HDLBits Problem - Two Gates](https://hdlbits.01xz.net/wiki/Exams/m2014_q4g)
* [HDLBits Problem - More Gates](https://hdlbits.01xz.net/wiki/Gates)
