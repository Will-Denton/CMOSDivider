`timescale 1ns / 100ps
module cla_tb;
    wire [4:0] A, B;
    wire c0;
    wire [4:0] S;
    wire c_out;

    cla5_bit adder(A, B, c0, S, c_out);
    integer i;
    assign c0 = 1'b0;
    assign {A, B} = i[7:0];
    wire [5:0] total;
    assign total = {c_out, S};

    initial begin
        for(i = 0; i < 1024; i = i+1) begin
            #20
            $display("A:%d, B:%d, => S:%d, Cout:%b, Total:%d", A, B, S, c_out, total);
            if(A+B != S) begin
                $display("Error: %d + %d != %d", A, B, S);
                $stop;
            end
        end
    end

    initial begin
        $dumpfile("cla_tb.vcd");
        $dumpvars(0, cla_tb);
    end
endmodule

