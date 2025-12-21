---
layout: post
title: "Combinational Logic - Multiplexers"
categories: [Verilog]
date: 2025-10-20
---

## 📌 Introduction
Multiplexers (MUX) are fundamental combinational logic circuits used to select one input from multiple signals based on a select line. In Verilog, MUXes can be implemented using conditional operators, case statements, or indexed part selects.


## 🧑‍💻 Code Example

### 2-to-1 multiplexer
```verilog
module top_module( 
    input a, b, sel,
    output out ); 
    assign out = (sel) ? b : a;
endmodule
```

### 2-to-1 bus multiplexer
```verilog
module top_module( 
    input [99:0] a, b,
    input sel,
    output [99:0] out );
    assign out = (sel) ? b: a;
endmodule
```

### 9-to-1 multiplexer
```verilog
module top_module( 
    input [15:0] a, b, c, d, e, f, g, h, i,
    input [3:0] sel,
    output [15:0] out );
    always @ (*) begin
        out = 16'hFFFF;
        case (sel)
            4'd0: out = a;
            4'd1: out = b;
            4'd2: out = c;
            4'd3: out = d;
            4'd4: out = e;
            4'd5: out = f;
            4'd6: out = g;
            4'd7: out = h;
            4'd8: out = i;
            default: out = 16'hFFFF;
        endcase
    end
endmodule
```

### 256-to-1 multiplexer
```verilog
module top_module( 
    input [255:0] in,
    input [7:0] sel,
    output out );
    assign out = in[sel];
endmodule
```

### 256-to-1 4-bit multiplexer
```verilog
module top_module( 
    input [1023:0] in,
    input [7:0] sel,
    output [3:0] out );
    // assign out = {in[sel*4+3], in[sel*4+2], in[sel*4+1], in[sel*4]};
    assign out = in[sel*4 +: 4];
    // assign out = in[sel*4+3 -: 4];
endmodule
```
> * With this many options, a case statement isn't so useful.
> * Vector indices can be variable, as long as the synthesizer can figure out that the width of the bits being selected is constant. It's not always good at this. An error saying "... is not a constant" means it couldn't prove that the select width is constant. In particular, in[ sel*4+3 : sel*4 ] does not work.
> * Bit slicing ("Indexed vector part select", since Verilog-2001) has an even more compact syntax.

## 📚 Reference
* [HDLBits Problem - Mux2to1](https://hdlbits.01xz.net/wiki/Mux2to1)
* [HDLBits Problem - Mux2to1v](https://hdlbits.01xz.net/wiki/Mux2to1v)
* [HDLBits Problem - Mux9to1v](https://hdlbits.01xz.net/wiki/Mux9to1v)
* [HDLBits Problem - Mux256to1](https://hdlbits.01xz.net/wiki/Mux256to1)
* [HDLBits Problem - Mux256to1v](https://hdlbits.01xz.net/wiki/Mux256to1v)
