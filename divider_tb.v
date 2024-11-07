`timescale 1ns / 100ps
module divider_tb();
    reg[11:0] data_input_1; // 12-bit input data in 12 bit floating point format
    reg[11:0] data_input_2; // 12-bit input data in 12 bit floating point format
    wire clk;

    initial begin
        data_input_1 = 12'b110001111000;
        data_input_2 = 12'b010001100000;
    end

    wire[11:0] data_output; // 12-bit output data in 12 bit floating point format
    wire done;        // 1-bit output done signal

    divider divider_inst(
        .data_input_1(data_input_1),
        .data_input_2(data_input_2),
        .clk(1'b0),
        .data_output(data_output),
        .done(done)
    );

    initial begin
        #20
        $display("data_input_1: %b", data_input_1);
        $display("data_input_2: %b", data_input_2);
        $display("data_output:  %b", data_output);
    end

    initial begin
        $dumpfile("divider_tb.vcd");
        $dumpvars(0, divider_tb);
    end

endmodule