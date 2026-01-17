---
layout: post
title: "Shift Register (HDLBits)"
subtitle: "SISO Shift Registers with Synchronous Active-Low Reset"
categories: [Verilog]
date: 2026-01-17
---

## 📌 Question

Implement the following circuit:

<!-- ![](/assets/26_0117/Exams_m2014q4k.png) -->

<p align="center">
<img src="{{ '/assets/26_0117/Exams_m2014q4k.png' | relative_url }}" width="600">
</p>

## 🧑‍💻 Code Example

### RTL Code

```verilog
module top_module #(
    parameter WIDTH = 4
) (
    input wire clk,
    input wire resetn,   // synchronous reset
    input wire in,
    output wire out);

    reg [WIDTH-1:0] Q;
    assign out = Q[WIDTH-1];

    always @(posedge clk) begin
        if (~resetn)
            Q <= {WIDTH{1'b0}};
        else
            Q <= {Q[WIDTH-2:0], in};
    end
endmodule
```

### Testbench Code

```verilog
`timescale 1ns/1ps

module tb_top_module;

    reg clk;
    reg resetn;
    reg in;
    wire out;

    top_module dut (
        .clk(clk),
        .resetn(resetn),
        .in(in),
        .out(out)
    );

    initial begin
        resetn = 1;
        clk = 0;
        in = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        $dumpfile("tb_top_module.vcd");
        $dumpvars(0, tb_top_module);

        // Initialize
        #10
        resetn = 0;
        #10;
        resetn = 1;

        in = 1;
        #10;
        in = 0;

        #50;

        in = 1;
        #10;
        in = 0;

        // Reset again
        resetn = 0;
        #10;
        resetn = 1;
        
        #30;

        in = 1;
        #10;
        in = 0;

        #30;
        $finish;
    end
    
    initial begin
        $monitor("Time=%0t resetn=%b out=%b", $time, resetn, out);
    end

endmodule
```

## 🔬 Results

### Simulation Waveform

<!-- ![](/assets/26_0117/Waveform.png) -->

<p align="center">
<img src="{{ '/assets/26_0117/Waveform.png' | relative_url }}" width="800">
</p>


### Synthesis RTL-level Schematic

<!-- ![](/assets/26_0117/schematic_rtl.svg) -->

<p align="center">
<img src="{{ '/assets/26_0117/schematic_rtl.svg' | relative_url }}" width="450">
</p>

### Synthesis Gate-level Schematic

<!-- ![](/assets/26_0117/schematic_gate.svg) -->

<p align="center">
<img src="{{ '/assets/26_0117/schematic_gate.svg' | relative_url }}" width="700">
</p>

## 📚 Reference
* [HDLBits Problem - m2014_q4k](https://hdlbits.01xz.net/wiki/Exams/m2014_q4k)
