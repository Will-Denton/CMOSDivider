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

    output [11:0] data_output  // 12-bit output data in 12 bit floating point format
    );

    //sign calculation
    xor(data_output[11], data_input_1[11], data_input_2[11]);

    //exponent calculation
    wire [5:0] in1_exp, in2_exp, out_exp;
    assign in1_exp = {1'b0, data_input_1[10:6]};
    assign in2_exp = {1'b0, data_input_2[10:6]};


endmodule