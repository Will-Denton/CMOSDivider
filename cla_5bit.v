module cla5_bit(
    input [4:0] A, B,
    input c0,
    output [4:0] S,
    output c_out
    );

    wire c1, c2, c3, c4, c5;
    wire p0, p1, p2, p3, p4;
    wire g0, g1, g2, g3, g4;

    and And0(g0, A[0], B[0]);
    and And1(g1, A[1], B[1]);
    and And2(g2, A[2], B[2]);
    and And3(g3, A[3], B[3]);
    and And4(g4, A[4], B[4]);

    or Or0(p0, A[0], B[0]);
    or Or1(p1, A[1], B[1]);
    or Or2(p2, A[2], B[2]);
    or Or3(p3, A[3], B[3]);
    or Or4(p4, A[4], B[4]);

    wire c1a1;
    and c1and1(c1a1, p0, c0);
    or  c1or1(c1, c1a1, g0);
    xor s0xor1(S[0], A[0], B[0], c0);

    wire c2a2, c2a1;
    and c2and1(c2a1, p1, g0);
    and c2and2(c2a2, p1, p0, c0);
    or  c2or1(c2, c2a2, c2a1, g1);
    xor s1xor1(S[1], A[1], B[1], c1);

    wire c3a3, c3a2, c3a1;
    and c3and1(c3a1, p2, g1);
    and c3and2(c3a2, p2, p1, g0);
    and c3and3(c3a3, p2, p1, p0, c0);
    or  c3or1(c3, c3a3, c3a2, c3a1, g2);
    xor s2xor1(S[2], A[2], B[2], c2);

    wire c4a4, c4a3, c4a2, c4a1;
    and c4and1(c4a1, p3, g2);
    and c4and2(c4a2, p3, p2, g1);
    and c4and3(c4a3, p3, p2, p1, g0);
    and c4and4(c4a4, p3, p2, p1, p0, c0);
    or  c4or1(c4, c4a4, c4a3, c4a2, c4a1, g3);
    xor s3xor1(S[3], A[3], B[3], c3);

    wire c5a5, c5a4, c5a3, c5a2, c5a1;
    and c5and1(c5a1, p4, g3);
    and c5and2(c5a2, p4, p3, g2);
    and c5and3(c5a3, p4, p3, p2, g1);
    and c5and4(c5a4, p4, p3, p2, p1, g0);
    and c5and5(c5a5, p4, p3, p2, p1, p0, c0);
    or  c5or1(c5, c5a5, c5a4, c5a3, c5a2, c5a1, g4);
    xor s4xor1(S[4], A[4], B[4], c4);

    assign c_out = c5;
endmodule