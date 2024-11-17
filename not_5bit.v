module not5_bit(
    input [4:0] A,
    output [4:0] S
    );

    not not0(S[0], A[0]);
    not not1(S[1], A[1]);
    not not2(S[2], A[2]);
    not not3(S[3], A[3]);
    not not4(S[4], A[4]);
endmodule