#gates maping and functioning

def store_and_print_gates_with_io(main_ip, main_op, wires, gates_connections, user_inputs):
    gates_with_io = []
    wires_values = {main_ip[i]: user_inputs[i] for i in range(len(main_ip))}  # Initialize wires values from user inputs

    # Define gate functions
    def and_gate(input1, input2):
        return input1 & input2

    def or_gate(input1, input2):
        return input1 | input2

    def not_gate(input1):
        return ~input1 & 1  # Ensuring output is 0 or 1

    def nand_gate(input1, input2):
        return ~(input1 & input2) & 1  # Ensuring output is 0 or 1

    def nor_gate(input1, input2):
        return ~(input1 | input2) & 1  # Ensuring output is 0 or 1

    def xor_gate(input1, input2):
        return input1 ^ input2

    def xnor_gate(input1, input2):
        return ~(input1 ^ input2) & 1  # Ensuring output is 0 or 1

    # Mapping of gate names to functions
    gate_functions = {
        'and': and_gate,
        'or': or_gate,
        'not': not_gate,
        'nand': nand_gate,
        'nor': nor_gate,
        'xor': xor_gate,
        'xnor': xnor_gate,
    }

    # Process each gate connection
    for gate in gates_connections:
        gate_name = gate['gate_name']
        connections = gate['connections']
        input_a = connections.get('A', None)
        input_b = connections.get('B', None)
        output_y = connections.get('Y', None)

        # Get the actual input values from wires_values, defaulting to 0 if not found
        input_a_value = wires_values.get(input_a, 0)  
        input_b_value = wires_values.get(input_b, 0) if input_b else None  # Only fetch input_b if it exists

        # Print inputs to debug
        if gate_name == 'not':
            print(f"Processing Gate: {gate_name}, Input A: {input_a}")
        else:
            print(f"Processing Gate: {gate_name}, Input A: {input_a}, Input B: {input_b}")

        # Evaluate the gate output using the corresponding function
        if gate_name in gate_functions:
            if input_b is not None:  # For gates with two inputs
                output_value = gate_functions[gate_name](input_a_value, input_b_value)
            else:  # For gates with one input (like NOT gate)
                output_value = gate_functions[gate_name](input_a_value)
        else:
            output_value = None  # If gate name is not recognized

        # Store the output if it's a wire
        if output_y is not None:
            wires_values[output_y] = output_value  # Assign the calculated output to the corresponding wire

        # Store the gate information in a list
        gate_info = [gate_name, input_a_value, input_b_value if input_b else None, output_value]
        gates_with_io.append(gate_info)

        # Print individual gate info
        print(f"Gate: {gate_name}, Input A Value: {input_a_value}, Input B Value: {input_b_value if input_b else 'Not Applicable'}, Output Y: {output_value if output_y is not None else 'Not Applicable'}")
        print("-" * 40)

    # Calculate the final output for the output gates
    final_outputs = {}
    for output in main_op:
        if output in wires_values:  # Check if the output wire exists in the wires values
            final_outputs[output] = wires_values[output]
        else:
            final_outputs[output] = 0  # Default to 0 if no wires connected

    # Print final main_op
    print("Final Outputs:")
    for output, value in final_outputs.items():
        print(f"Output {output}: {value}")

    return gates_with_io

# User-defined inputs
user_inputs = [0, 1]  # Example inputs for the gates

# Store and print the gates with IO using a list
gates_with_io = store_and_print_gates_with_io(main_ip, main_op, wires, gates_connections, user_inputs)

# Print the entire gates_with_io list
print("Gates with I/O:")
for gate in gates_with_io:
    print(gate)
