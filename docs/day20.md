---
layout: page
title: "Combinational for-loop"
categories: [Verilog]
day: 20
date: 2025-10-01
---

## 📌 Introduction

## 🧑‍💻 Code Example

### Vector100r
A for loop (in a combinational always block or generate block) would be useful here. I would prefer a combinational always block in this case because module instantiations (which require generate blocks) aren't needed.
#### Always block - for loop
```verilog
module top_module( 
    input [99:0] in,
    output [99:0] out
);
    integer i;
    always @(*) begin
        for (i=0; i<100; i++) begin
            out[i] = in[99-i];
        end
    end
endmodule
```

#### Genrate block - for loop
```verilog
module top_module( 
    input [99:0] in,
    output [99:0] out
);
    genvar i;
    generate
        for (i=0; i<100; i++) begin: vector100r
            assign out[i] = in[99-i];
        end	
    endgenerate
endmodule
```

### Popcount255
```verilog
module top_module( 
    input [254:0] in,
    output [7:0] out );
    integer i;
    always @(*) begin
        out = 8'b0;
        for (i=0; i<255; i++) begin
            if (in[i])
                out += 1'b1;
        end
    end
endmodule
```

## 📚 Reference
* [HDLBits Problem - Vector100r](https://hdlbits.01xz.net/wiki/Vector100r)
* * [HDLBits Problem - Popcount255](https://hdlbits.01xz.net/wiki/Popcount255)
