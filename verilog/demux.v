module demux_1x8(
    input wire din,           // 1 input data signal
    input wire s0, s1, s2,    // 3 select lines
    output wire d0, d1, d2, d3, d4, d5, d6, d7  // 8 output signals
);

// Intermediate signals for inverted select lines
wire not_s0, not_s1, not_s2;

// Invert the select lines
not (not_s0, s0);
not (not_s1, s1);
not (not_s2, s2);

// Output logic for each output bit (AND gates for each combination of select lines and input)
and (d0, din, not_s2, not_s1, not_s0);  // 000
and (d1, din, not_s2, not_s1, s0);      // 001
and (d2, din, not_s2, s1, not_s0);      // 010
and (d3, din, not_s2, s1, s0);          // 011
and (d4, din, s2, not_s1, not_s0);      // 100
and (d5, din, s2, not_s1, s0);          // 101
and (d6, din, s2, s1, not_s0);          // 110
and (d7, din, s2, s1, s0);              // 111

endmodule
