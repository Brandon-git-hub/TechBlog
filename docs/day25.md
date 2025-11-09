---
layout: page
title: "Think Backwards: Designing Hardware from Outputs to Inputs"
categories: [Verilog]
day: 25
date: 2025-10-12
---

## 📌 Introduction
When designing circuits, one often has to think of the problem "backwards", starting from the outputs then working backwards towards the inputs. This is often the opposite of how one would think about a (sequential, imperative) programming problem, where one would look at the inputs first then decide on an action (or output). For sequential programs, one would often think "If (inputs are ___ ) then (output should be ___ )". On the other hand, hardware designers often think "The (output should be ___ ) when (inputs are ___ )".

## 🧑‍💻 Code Example

```verilog
module top_module (
    input ring,
    input vibrate_mode,
    output ringer,       // Make sound
    output motor         // Vibrate
);
    assign ringer = (~vibrate_mode & ring)? 1'b1 : 1'b0;
    assign motor = (vibrate_mode & ring)? 1'b1 : 1'b0;
endmodule
```

```verilog
module top_module (
    input too_cold,
    input too_hot,
    input mode,
    input fan_on,
    output heater,
    output aircon,
    output fan
); 
    assign heater = (mode & too_cold)? 1'b1 : 1'b0;
    assign aircon = (~mode & too_hot)?1'b1 : 1'b0;
    assign fan = (fan_on | heater | aircon);
endmodule
```

## 📚 Reference
* [HDLBits Problem - Ringer](https://hdlbits.01xz.net/wiki/Ringer)
* [HDLBits Problem - Thermostat](https://hdlbits.01xz.net/wiki/Thermostat)
