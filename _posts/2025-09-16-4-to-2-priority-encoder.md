---
layout: post
title: "4-to-2 Priority Encoder"
categories: [Verilog]
date: 2025-09-16
---

## 📌 Introduction
A **priority encoder** converts a multi-bit input into the binary index of the highest-priority `1` (or lowest).  
This example converts **4 bits to 2 bits**.

### MSB Priority

| I3   | I2   | I1   | I0   | O0   | O1   |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0    | 0    | 0    | X    | 0    | 0    |
| 0    | 0    | 1    | X    | 0    | 1    |
| 0    | 1    | X    | X    | 1    | 0    |
| 1    | X    | X    | X    | 1    | 1    |

### LSB Priority

| I3   | I2   | I1   | I0   | O0   | O1   |
| :--- | :--- | :--- | :--- | :--- | :--- |
| X    | X    | X    | 1    | 0    | 0    |
| X    | X    | 1    | 0    | 0    | 1    |
| X    | 1    | 0    | 0    | 1    | 0    |
| 1    | 0    | 0    | 0    | 1    | 1    |

## 🧑‍💻 Code Example (LSB Priority)


### Case
```verilog
module top_module (
    input [3:0] in,
    output reg [1:0] pos  );
    
    always@(*) begin
        case(in) 
            4'b0000: pos = 0;
            4'b0001: pos = 0;
            4'b0010: pos = 1;
            4'b0011: pos = 0;
            4'b0100: pos = 2;
            4'b0101: pos = 0;
            4'b0110: pos = 1;
            4'b0111: pos = 0;
            4'b1000: pos = 3;
            4'b1001: pos = 0;
            4'b1010: pos = 1;
            4'b1011: pos = 0;
            4'b1100: pos = 2;
            4'b1101: pos = 0;
            4'b1110: pos = 1;
            4'b1111: pos = 0;
        endcase
    end

endmodule
```

### casez
```verilog
module top_module (
    input [3:0] in,
    output reg [1:0] pos  );
    
    always@(*) begin
        pos = 2'd0; // avoid latch
        casez(in) 
            4'b???1: pos = 0;
            4'b??10: pos = 1;
            4'b?100: pos = 2;
            4'b1000: pos = 3;
        endcase
    end

endmodule
```

### if-else (v1)
```verilog
// 4-bit priority encoder
module top_module (
    input [3:0] in,
    output reg [1:0] pos  );
    
    always@(*) begin
        if (in & 1) pos = 0;
        else if (in & 1<<1) pos = 1;
        else if (in & 1<<2) pos = 2;
        else if (in & 1<<3) pos = 3;
        else pos = 0;
    end

endmodule
```

### if-else (v2)
```verilog
// 4-bit priority encoder
module top_module (
    input [3:0] in,
    output reg [1:0] pos  );
    
    always@(*) begin
        if (in[0]) pos = 0;
        else if (in[1]) pos = 1;
        else if (in[2]) pos = 2;
        else if (in[3]) pos = 3;
        else pos = 0;
    end

endmodule
```

## 📚 Reference
* [HDLBits Problem - Always case2](https://hdlbits.01xz.net/wiki/Always_case2)
