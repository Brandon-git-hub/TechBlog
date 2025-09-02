---
layout: page
title: "Day 3"
categories: [Verilog]
---

## 📌 Hierarchy Module

## 🧑‍💻 Code Example

### By position
```verilog
module top_module ( input a, input b, output out );
    mod_a a_module(a, b, out);
endmodule
```

![alt text](../assets/Modulepos.png)
```verilog
module top_module ( 
    input a, 
    input b, 
    input c,
    input d,
    output out1,
    output out2
);
    mod_a a_module(out1, out2, a, b, c, d);

endmodule
```

### By name
```verilog
module top_module ( input a, input b, output out );
    mod_a a_module(.in1(a), .in2(b), .out(out) );
endmodule
```

Port in ***mod_a***	Port in ***top_module***
- output out1	out1
- output out2	out2
- input in1	a
- input in2	b
- input in3	c
- input in4	d

```verilog
module top_module ( 
    input a, 
    input b, 
    input c,
    input d,
    output out1,
    output out2
);
    mod_a a_module( .in1(a), .in2(b), .in3(c), .in4(d), .out1(out1), .out2(out2) );

endmodule
```

## 📚 Reference
* [HDLBits Problem - Module](https://hdlbits.01xz.net/wiki/Module)
* [HDLBits Problem - Module_pos](https://hdlbits.01xz.net/wiki/Module_pos)
* [HDLBits Problem - Module_name](https://hdlbits.01xz.net/wiki/Module_name)