module wrapper(
);

reg [2:0] inp1;
reg [2:0] inp2;
reg [3:0] out1;
reg [3:0] out2;

assign inp1 = 3'b110;
assign inp2 = 3'b011;

adder inst_adder(
    .add_inp1(inp1),
    .add_inp2(inp2),
    .add_out(out1)
);

sub inst_sub(
    .sub_inp1(inp1),
    .sub_inp2(inp2),
    .sub_out(out2)
);

endmodule
