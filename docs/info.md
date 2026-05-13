<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This design combines two simple IP blocks:

- SPI memory controller (`spi_mem_ctrl_core`): A small FSM that reads bytes from an external SPI RAM using command `0x03` (read) plus a 16-bit address. It drives `cs_n`, `sck`, and `mosi`, samples `miso`, and exposes `busy`/`valid` along with `data_out`. In sequential mode, it keeps `cs_n` low and continues clocking to fetch subsequent bytes until `last` is asserted.
- VGA timing core (`vga_core`): Generates 640x480 @ 60 Hz timing using a 25.175 MHz pixel clock. It produces `hsync`, `vsync`, `display_on`, and current pixel coordinates (`screen_hpos`, `screen_vpos`).

The top-level ties both cores to the shared `clk`/reset domains and exposes their signals on the Tiny Tapeout IOs (exact pin mapping depends on the top-level wiring).

## How to test

1. Provide a stable clock and active-low reset.
2. For SPI: drive `start` with a one-cycle pulse, set `addr`, and optionally set `last` high on the final byte. Monitor `busy` and capture `data_out` when `valid` pulses.
3. For VGA: feed a 25.175 MHz pixel clock and observe `hsync`, `vsync`, and `display_on`. Use `screen_hpos`/`screen_vpos` to verify timing counts.

If you use the included testbench, run it from the `test/` folder per its README.

## External hardware

- SPI RAM compatible with 23LC512 read protocol (or a simulator providing `miso`).
- VGA connector or display interface to observe `hsync`/`vsync` timing (optional for simulation).
