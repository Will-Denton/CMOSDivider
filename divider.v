/*

This module preforms the division of two 12-bit floating point numbers with the following format:
    1-bit sign
    5-bit exponent
    6-bit mantissa

Currently we assume that both inputs are normalized and that in1 > in2.
*/

module divider(
    input [11:0] data_input_1, // 12-bit input data in 12 bit floating point format
    input [11:0] data_input_2, // 12-bit input data in 12 bit floating point format
    input clk,                 // 1-bit input clock

    output [11:0] data_output, // 12-bit output data in 12 bit floating point format
    output done                // 1-bit output done signal
    );

    //sign calculation
    wire sign;
    xor(sign, data_input_1[11], data_input_2[11]);

    //exponent calculation
    wire[4:0] out_exp_temp, out_exp_temp_norm;
    assign out_exp_temp = data_input_1[10:6] - data_input_2[10:6] + 5'd15;
    assign out_exp_temp_norm = out_exp_temp - 5'd1;

    //mantissa calculation
    wire[6:0] mantissa_1_leading_1, mantissa_2_leading_1;
    assign mantissa_1_leading_1 = {1'b1, data_input_1[5:0]};
    assign mantissa_2_leading_1 = {1'b1, data_input_2[5:0]};

    wire[13:0] mantissa_1_shifted;
    assign mantissa_1_shifted = {mantissa_1_leading_1, 7'd0}; 

    // wire[13:0] div_mantissa_result;
    // assign div_mantissa_result = mantissa_1_shifted     / mantissa_2_leading_1;

    wire[6:0] div_mantissa_raw;
    wire[6:0] div_mantissa_result;
    wire[4:0] mantissa_correction; //to be subtracted from exponent

    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6] == 1'b1) ? {div_mantissa_raw, 5'b0} : 12'bz;
    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6:5] == 2'b01) ? {div_mantissa_raw[5:0], 1'b0, 5'd1} : 12'bz;
    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6:4] == 3'b001) ? {div_mantissa_raw[4:0], 2'b0, 5'd2} : 12'bz;
    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6:3] == 4'b0001) ? {div_mantissa_raw[3:0], 3'b0, 5'd3} : 12'bz;
    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6:2] == 5'b00001) ? {div_mantissa_raw[2:0], 4'b0, 5'd4} : 12'bz;
    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6:1] == 6'b000001) ? {div_mantissa_raw[1:0], 5'b0, 5'd5} : 12'bz;
    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6:0] == 7'b0000001) ? {div_mantissa_raw[0], 6'b0, 5'd6} : 12'bz;
    assign {div_mantissa_result, mantissa_correction} = (div_mantissa_raw[6:0] == 7'b0) ? {div_mantissa_raw, 5'b0} : 12'bz;


    wire[6:0] out_mantissa_temp;
    assign out_mantissa_temp = div_mantissa_result[6:0];

    wire leading_mantissa_one;
    assign leading_mantissa_one = out_mantissa_temp[6];

    //output data
    assign data_output = (leading_mantissa_one) ? {sign, out_exp_temp, out_mantissa_temp[5:0]} : {sign, out_exp_temp_norm, out_mantissa_temp[4:0] << 1};
endmodule
