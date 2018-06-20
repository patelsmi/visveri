module adder(
    input  [2:0] add_inp1,
    input  [2:0] add_inp2,
    output [3:0] add_out
);

    assign add_out = add_inp1 + add_inp2;

endmodule
