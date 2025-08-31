# Day1

## 📌 Generate
In the HDLBits *Vectorr* question, the output should be the reverse of the input order.
Although it can be written by:
```verilog
module top_module( 
    input [7:0] in,
    output [7:0] out
);

    assign out = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]};
endmodule
```

However, it's not flexable and becomes troublesome when the bit width is so large.
Hence it can use ```generate endgenerate``` constuct:
```verilog
module top_module( 
    input [7:0] in,
    output [7:0] out
);
    genvar i;
    generate 
        for (i=0; i<8; i++) begin : reverse_vector
        	assign out[i] = in[8-1-i];
    	end
    endgenerate
endmodule
```

## 📚 Reference
[HDLBits Problem - Vectorr](https://hdlbits.01xz.net/wiki/Vectorr)
