`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a FST file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  reg        clk;
  reg        rst_n;
  reg        ena;
  reg  [7:0] ui_in;
  wire [7:0] uo_out;
  wire [7:0] uio_in;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;
  
  wire [7:0] uio_in_to_dut;
  wire       spi_miso;
`ifdef GL_TEST
  wire      VPWR = 1'b1;
  wire      VGND = 1'b0;
`endif

  assign uio_in_to_dut = {uio_in[7:4], spi_miso, uio_in[2:0]};

  spi_ram_model #(.MEM_BYTES(256)) ram (
      .cs_n (uio_out[0]),
      .sck  (uio_out[1]),
      .mosi (uio_out[2]),
      .miso (spi_miso)
  );

  // Replace tt_um_example with your module name:
  tt_um_enjimneering_spi_mem user_project (
      // Include power ports for the Gate Level test:
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in_to_dut),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );

endmodule
