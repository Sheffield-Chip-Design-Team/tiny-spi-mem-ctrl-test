# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge


@cocotb.test()
async def test_spi_read_top(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 20, unit="ns")
    cocotb.start_soon(clock.start())

    dut.ena.value    = 1
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    dut.rst_n.value  = 0

    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    dut.ram.mem[0].value = 0xA5
    dut.ram.mem[1].value = 0x5A

    ui_in  = 0
    ui_in |= 0 << 0      # MODE = 0 (SPI)
    ui_in |= 1 << 1      # SPI_START
    ui_in |= 1 << 2      # SPI_LAST
    ui_in |= 0x0 << 4    # ADDR_HI[0]
    ui_in |= 0x0 << 5    # ADDR_HI[1]
    ui_in |= 0x0 << 6    # ADDR_HI[2]
    ui_in |= 0x0 << 7    # ADDR_HI[3]

    dut.ui_in.value = ui_in
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(1000):
        await RisingEdge(dut.clk)
        valid_bit = dut.uio_out.value[6]
        if valid_bit.is_resolvable and int(valid_bit) == 1:
            break
    else:
        raise TimeoutError("Timeout waiting for SPI valid to assert")
    
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0xA5

    for _ in range(1000):
        await RisingEdge(dut.clk)
        valid_bit = dut.uio_out.value[6]
        if valid_bit.is_resolvable and int(valid_bit) == 1:
            break
    else:
        raise TimeoutError("Timeout waiting for SPI valid to assert")

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x5A
