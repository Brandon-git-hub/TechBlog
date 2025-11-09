---
layout: page
title: "2-bit Adder with Peripheral Control"
categories: [FPGA]
day: 31
date: 2025-10-22
---

## 📌 Introduction
* **Device**: Intel/Altera Cyclone IV (EP4CE22F17C6, 22K LEs)
* **Board**: Terasic DE0-Nano
* **IDE**: Quartus Prime Lite Edition

This mini project implements a 2-bit adder that the user can trigger with buttons. The operands come from slide switches, and the result is displayed on the LEDs. A single-cycle pulse is generated on the falling edge of the active-low Start button to latch the result.

## 🔧 Pin Mapping (DE0-Nano)
| Function   | Pin (suggested) | Note                       |
| ---------- | --------------- | -------------------------- |
| `KEY1`     | Start           | Active-low, triggers A + B |
| `KEY0`     | Reset           | Active-low reset           |
| `SW[3:2]`  | A               | 2-bit operand A            |
| `SW[1:0]`  | B               | 2-bit operand B            |
| `LED[1:0]` | Sum             | Lower 2 bits of the result |
| `LED[2]`   | Carry           | Carry out                  |

### 🧩 Requirements

1. On Start (press KEY1), capture the current A and B and perform the addition.
2. Show Sum and Carry on LEDs.
3. On Reset (press KEY0), clear the display.

## 🧑‍💻 Code Example

### top.v
```verilog
module top_module (
    input        CLOCK_50,
    input  [1:0] KEY,         // KEY[1]=Start (active-low), KEY[0]=Reset (active-low)
    input  [3:0] SW,          // SW[3:2]=A, SW[1:0]=B
    output reg [7:0] LED
);

    // Active-low buttons
	wire reset_n = KEY[0];
	wire start_n = KEY[1];
    // 2-bit ripple-carry adder wiring
	wire [1:0] sum;
	wire [1:0] cout;
	
	Fadd add0(.a(SW[2]), .b(SW[0]), .cin(1'b0), .cout(cout[0]), .sum(sum[0]));
	Fadd add1(.a(SW[3]), .b(SW[1]), .cin(cout[0]), .cout(cout[1]), .sum(sum[1]));
	
    // Two-flop synchronizer for the Start button + falling-edge detection (active-low press)
	reg start_n_dff1, start_n_dff0;
	always @ (posedge CLOCK_50 or negedge reset_n) begin
		if (!reset_n) begin
			{start_n_dff1, start_n_dff0} <= 2'b11;
		end
		else begin
			{start_n_dff1, start_n_dff0} <= {start_n_dff0, start_n};
		end
	end
	wire start = start_n_dff1 & ~start_n_dff0;
	
    // Display register (latches the result on Start)
	always @ (posedge CLOCK_50 or negedge reset_n) begin
		if (!reset_n) begin
			LED <= 8'h00;
		end
		else begin
			if (start) begin
				LED <= {5'b0, cout[1], sum[1:0]};
			end
		end
	end

endmodule
```

### Fadd.v
```verilog
module Fadd(input a, input b, input cin, output cout, output sum);
	assign sum = a ^ b ^ cin;
	assign cout = (a & b) | (a & cin) | (b & cin);
endmodule
```

### Result
![](../assets/day31/result.jpg)