module register #(
    parameter WIDTH = 11
)(
    input [WIDTH-1:0] in,
    input clk,
    input clr,
    input en,
    output wire [WIDTH-1:0] out
);

    genvar i;
    generate
        for (i = 0; i < WIDTH; i = i + 1) begin
            dff flip_flop(.q(out[i]), .d(in[i]), .clk(clk), .clr(clr), .en(en));
        end
    endgenerate

endmodule
