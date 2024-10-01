`timescale 1ns / 100ps
module cla_6bit_tb;
    wire [5:0] A, B;
    wire c0;
    wire [5:0] S;
    wire c_out;

    cla6_bit adder(A, B, c0, S, c_out);
    integer i;
    assign c0 = 1'b0;
    assign {A, B} = i[11:0];
    wire [6:0] total;
    assign total = {c_out, S};

    initial begin
        for(i = 0; i < 4096; i = i+1) begin
            #20
            $display("A:%d, B:%d, => S:%d, Cout:%b, Total:%d", A, B, S, c_out, total);
            if(A+B != S) begin
                $display("Error: %d + %d != %d", A, B, S);
                $stop;
            end
        end
    end

    initial begin
        $dumpfile("cla_6bit_tb.vcd");
        $dumpvars(0, cla_6bit_tb);
    end
endmodule

