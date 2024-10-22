module full_adder(S, Cout, A, B, Cin);
    input A, B, Cin;
    output Cout, S;
    wire w1, w2, w3;

    xor S_result(S, A, B, Cin);
    and A_and_B(w1, A, B);
    and A_and_C(w2, A, Cin);
    and B_and_C(w3, B, Cin);

    or Cout_result(Cout, w1, w2, w3);
endmodule