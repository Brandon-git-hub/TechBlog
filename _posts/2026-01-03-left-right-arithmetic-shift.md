---
layout: post
title: "Left/right arithmetic shift by 1 or 8"
categories: [Verilog]
date: 2026-01-04
---

## 📌 Question
Build a 64-bit arithmetic shift register, with synchronous load. The shifter can shift both left and right, and by 1 or 8 bit positions, selected by amount.

An arithmetic right shift shifts in the sign bit of the number in the shift register (q[63] in this case) instead of zero as done by a logical right shift. Another way of thinking about an arithmetic right shift is that it assumes the number being shifted is signed and preserves the sign, so that arithmetic right shift divides a signed number by a power of two.

There is no difference between logical and arithmetic left shifts.

* load: Loads shift register with data[63:0] instead of shifting.
* ena: Chooses whether to shift.
* amount: Chooses which direction and how much to shift.
  * 2'b00: shift left by 1 bit.
  * 2'b01: shift left by 8 bits.
  * 2'b10: shift right by 1 bit.
  * 2'b11: shift right by 8 bits.
* q: The contents of the shifter.

### Hint
A 5-bit number 11000 arithmetic right-shifted by 1 is 11100, while a logical right shift would produce 01100.
Similarly, a 5-bit number 01000 arithmetic right-shifted by 1 is 00100, and a logical right shift would produce the same result, because the original number was non-negative.


## 🧑‍💻 Code Example

```verilog
module top_module (
    input wire clk,
    input wire rst_n,
    input wire load,
    input wire ena,
    input wire [1:0] amount,
    input wire [63:0] data,
    output reg [63:0] q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 64'd0;
        else if (load)
            q <= data;
        else if (ena)
            case(amount)
                2'b00: q <= {q[62:0], 1'b0}; // ASL 1
                2'b01: q <= {q[55:0], 8'd0}; // ASL 8
                2'b10: q <= {q[63], q[63:1]}; // ASR 1
                2'b11: q <= { {8{q[63]}}, q[63:8]}; // ASR 8
            endcase
    end
endmodule
```

## 📐 Diagram
<!-- ![Diagram](/assets/26_0103/top_module.svg) -->
<img src="{{ '/assets/26_0103/top_module.svg' | relative_url }}" width="450">

### Ports

| Port name | Direction | Type        | Description                |
| --------- | --------- | ----------- | -------------------------- |
| clk       | input     | wire        | System Clock               |
| rst_n     | input     | wire        | Asynchronous Reset (Active Low) |
| load      | input     | wire        | Synchronous Load Enable    |
| ena       | input     | wire        | Shift Enable Signal        |
| amount    | input     | wire [1:0]  | Shift Amount and Direction |
| data      | input     | wire [63:0] | Data to be loaded          |
| q         | output    | reg [63:0]  | Shift Register Output      |



## 🔬 Results

<!-- ![](/assets/26_0103/schematic.svg) -->
<img src="{{ '/assets/26_0103/schematic.svg' | relative_url }}" width="700">

<!-- ![](/assets/26_0103/Shifting.svg) -->
<img src="{{ '/assets/26_0103/Shifting.svg' | relative_url }}" width="700">

<!-- ![](/assets/26_0103/Arithmetic_right_shift.svg) -->
<img src="{{ '/assets/26_0103/Arithmetic_right_shift.svg' | relative_url }}" width="700">

<!-- ![](/assets/26_0103/Arithmetic_right_shift_2.svg) -->
<img src="{{ '/assets/26_0103/Arithmetic_right_shift_2.svg' | relative_url }}" width="700">

## 📚 Reference
* [HDLBits Problem - Shift18](https://hdlbits.01xz.net/wiki/Shift18)
