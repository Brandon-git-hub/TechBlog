---
layout: page
title: "DFF with reset"
categories: [Verilog]
day: 37
---

## 📌 Introduction

## 🧑‍💻 Code Example

### Synchronous reset
```verilog
module SynR_DFF(input clk, input reset, input d, output q);
    always @(posedge clk) begin
        if (reset) 
            q <= 1'b0;
        else
            q <= d; 
    end
endmodule

module top_module (
    input clk,
    input reset,            // Synchronous reset
    input [7:0] d,
    output [7:0] q
);
    genvar i;
    generate
        for (i=0;i<8;i++) begin: Dff8r
            SynR_DFF dff(.clk(clk), .reset(reset), .d(d[i]), .q(q[i]));
        end
    endgenerate

endmodule
```

## 📚 Reference
* [HDLBits Problem - Dff8r](https://hdlbits.01xz.net/wiki/Dff8r)
