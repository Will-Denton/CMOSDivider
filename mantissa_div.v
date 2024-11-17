module mantissa_div(
    input [13:0] dividend,
    input [6:0] divisor,
    input ctrl_div,
    input clk,

    output wire [6:0] quotient,
    output ready
);

    wire [15:0] RQ_in, RQ_out;
    register #(.WIDTH(16)) RQ(.out(RQ_out), .in(RQ_in), .clk(clk), .clr(1'b0), .en(1'b1));

    assign RQ_in = ctrl_div ? {2'b00, dividend} : {cla_out[7:0], RQ_out[6:1], ~cla_out[7], 1'b0};
    
    wire [7:0] cla_out, cla_B_in;
    wire c0_in;

    assign {c0_in, cla_B_in} = RQ_out[15] ? {1'b0, 1'b0, divisor} : {1'b1, 1'b1, ~divisor[6:0]};
    cla_8bit cla(.S(cla_out), .A(RQ_out[14:7]), .B(cla_B_in), .c0(c0_in));

    assign quotient = RQ_out[7:1];

    reg [3:0] counter;
    always @(posedge clk) begin
        if (ctrl_div) 
            counter <= 0;
        else 
            counter <= counter + 1;
    end

    assign ready = (counter == 7) ? 1 : 0;

endmodule
