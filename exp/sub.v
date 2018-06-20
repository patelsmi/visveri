module(
    input  [2:0] sub_inp1,
    input  [2:0] sub_inp2,
    output [2:0] sub_out
);

    assign sub_out = sub_inp1 - sub_inp2;

endmodule
