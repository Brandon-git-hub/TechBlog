---
layout: page
title: "D flip-flop"
categories: [Verilog]
day: 36
date: 2025-10-28
---

## 📌 Introduction
A D flip-flop is a circuit that stores a bit and is updated periodically, at the (usually) positive edge of a clock signal.
D flip-flops are created by the logic synthesizer when a clocked always block is used. A D flip-flop is the simplest form of **"blob of combinational logic followed by a flip-flop"** where the combinational logic portion is just a wire.

## 🧑‍💻 Code Example

### D flip-flop
```verilog
module top_module (
    input clk,    // Clocks are used in sequential circuits
    input d,
    output reg q );

    // Use a clocked always block
    always @(posedge clk) begin
    	q <= d;   //non-blocking assignments
    end
    
endmodule
```

### D flip-flops
```verilog
module DFF_mod (
    input clk,
    input d,
    output reg q );

    always @(posedge clk) begin
    	q <= d; 
    end
    
endmodule

module top_module (
    input clk,
    input [7:0] d,
    output [7:0] q
);
    genvar i;
    generate
        for (i=0;i<8;i++) begin: DFFs
            DFF_mod dff(.clk(clk), .d(d[i]), .q(q[i]));
        end
    endgenerate
endmodule
```

## 📚 Reference
* [HDLBits Problem - Dff](https://hdlbits.01xz.net/wiki/Dff)
* [HDLBits Problem - Dff8](https://hdlbits.01xz.net/wiki/Dff8)
