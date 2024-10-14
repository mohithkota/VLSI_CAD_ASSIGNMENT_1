module decoder_3x8(
    input wire y0, y1, y2,   // 3 input signals
    output wire d0, d1, d2, d3, d4, d5, d6, d7  // 8 output signals
);

// Intermediate signals for inverted inputs
wire not_y0, not_y1, not_y2;

// Invert each input
not (not_y0, y0);
not (not_y1, y1);
not (not_y2, y2);

// Output logic for each output bit (AND gates for each combination of inputs)
and (d0, not_y2, not_y1, not_y0);  // 000
and (d1, not_y2, not_y1, y0);      // 001
and (d2, not_y2, y1, not_y0);      // 010
and (d3, not_y2, y1, y0);          // 011
and (d4, y2, not_y1, not_y0);      // 100
and (d5, y2, not_y1, y0);          // 101
and (d6, y2, y1, not_y0);          // 110
and (d7, y2, y1, y0);              // 111

endmodule
