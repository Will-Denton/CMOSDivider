module conditional_adder_subtractor(
    input A, Din, Pin, Cin;
    output Dout, S, Cout, Pout;
    );

    assign Pout = Pin;
    assign Din = Dout;

    wire w1;
    xor xor1(w1, Pin, Din)

    full_adder fa(.S(S), .Cout(Cout), .A(w1), .B(A), .Cin(Cin));
endmodule