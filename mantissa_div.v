module mantissa_div(
    input [13:0] dividend,
    input [6:0] divisor,
    input ctrl_div,
    input clk,

    output [6:0] wire quotient
);

    wire [14:0] RQ_in;
    reg #(.WIDTH(15)) RQ(.out(), .in(RQ_in), .clk(clk), .clr(0), .en(1));

    assign RQ_in = ctrl_div ? {1'b0, dividend} : 

endmodule
