module encoder_4x2(
    input wire d0, d1, d2, d3,   // 4 input signals
    output wire y0, y1           // 2 output signals
);

// Intermediate wires for the logic gates
wire not_d0, not_d1, not_d2, not_d3;
wire w1, w2, w3, w4;

// Create not gates for each input
not (not_d0, d0);
not (not_d1, d1);
not (not_d2, d2);
not (not_d3, d3);

// For y0: y0 = d1 | d3
or (y0, d1, d3);

// For y1: y1 = d2 | d3
or (y1, d2, d3);

endmodule
