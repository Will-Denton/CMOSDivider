module dff(
    input d,
    input en,
    input clr,
    input clk,
    output reg q
);

    always @(posedge clk or posedge clr) begin
        if (clr)
            q <= 0;
        else if (en)
            q <= d;
    end


endmodule
