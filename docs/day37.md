---
layout: page
title: "DFF with reset"
categories: [Verilog]
day: 37, 38
date: 2025-10-29
---

## 📌 Introduction
This note collects common D-flip-flop coding patterns in Verilog: synchronous reset, synchronous preset (load a constant), asynchronous reset, and byte-enable registers. All examples are synthesis-friendly and use non-blocking assignments.

## 🧑‍💻 Code Example

### 1) Synchronous reset (active-high)
```verilog
module SynR_DFF(input clk, input reset, input d, output reg q);
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

### 2) Synchronous preset / load constant on reset
```verilog
module top_module (
    input clk,
    input reset,
    input [7:0] d,
    output [7:0] q
);
    always @(negedge clk) begin
        if (reset)
            q<=8'h34;
        else
            q<=d;        
    end

endmodule
```

### 3) Asynchronous reset (active-high)
```verilog
module top_module (
    input clk,
    input areset,   // active high asynchronous reset
    input [7:0] d,
    output [7:0] q
);
    always @(posedge clk or posedge areset) begin
        if(areset)
            q<=8'h00;
        else
            q<=d;
    end

endmodule
```
💡 Best practice: Synchronize the de-assertion of asynchronous resets to the clock domain to prevent metastability.

```verilog
// Synchronize external async reset
module reset_sync (
    input  wire clk,
    input  wire areset,       // asynchronous external reset (active high)
    output reg  reset_sync    // synchronized internal reset
);
    reg sync_ff;

    always @(posedge clk or posedge areset) begin
        if (areset)
            {reset_sync, sync_ff} <= 2'b11;
        else
            {reset_sync, sync_ff} <= {sync_ff, 1'b0};
    end
endmodule

// Use synchronized reset inside your main logic
module top_module (
    input  wire clk,
    input  wire areset,       // external async reset
    input  wire [7:0] d,
    output reg  [7:0] q
);
    wire reset_sync;

    // Instantiate reset synchronizer
    reset_sync u_sync (
        .clk(clk),
        .areset(areset),
        .reset_sync(reset_sync)
    );

    // Internal DFF with synchronized reset
    always @(posedge clk) begin
        if (reset_sync)
            q <= 8'h00;
        else
            q <= d;
    end
endmodule

```

### 4) Byte-enable D flip-flops (active-low reset)
```verilog
module top_module (
    input clk,
    input resetn,  // active-low synchronous reset
    input [1:0] byteena, // bit0 controls [7:0], bit1 controls [15:8]
    input [15:0] d,
    output [15:0] q
);
    always @(posedge clk) begin
        if (~resetn)
            q<=16'h0000;
        else begin
            case(byteena)
                2'b01: 
                    q[7:0]<=d[7:0];
                2'b10:
                    q[15:8]<=d[15:8];
                2'b11:
                    q<=d;
                default:
                    q<=q;
            endcase
        end
    end
    
endmodule
```

## 📚 Reference
* [HDLBits Problem - Dff8r](https://hdlbits.01xz.net/wiki/Dff8r)
* [HDLBits Problem - Dff8p](https://hdlbits.01xz.net/wiki/Dff8p)
* [HDLBits Problem - Dff8ar](https://hdlbits.01xz.net/wiki/Dff8ar)
* [HDLBits Problem - Dff16e](https://hdlbits.01xz.net/wiki/Dff16e)