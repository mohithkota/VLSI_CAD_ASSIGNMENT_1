import re

def extract_io_wires(data):
    inputs = []
    outputs = []
    wires = []

    for line in data:
        line = line.strip()
        if line.startswith("input"):
            match = re.findall(r'input\s+(\w+);', line)
            if match:
                inputs.extend(match)
        elif line.startswith("output"):
            match = re.findall(r'output\s+(\w+);', line)
            if match:
                outputs.extend(match)
        elif line.startswith("wire"):
            match = re.findall(r'wire\s+(\w+);', line)
            if match:
                wires.extend(match)

    return inputs, outputs, wires

def store_and_print_gates_with_io(inputs, outputs, wires, gates_connections, user_inputs):
    gates_with_io = []
    wire_values = {inputs[i]: user_inputs[i] for i in range(len(inputs))}  # Initialize wire values from user inputs

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

    last_gate_output = None  # Variable to store the output of the last gate

    # Process each gate connection
    for gate in gates_connections:
        gate_name = gate['gate_name']
        connections = gate['connections']
        input_a = connections.get('A', None)
        input_b = connections.get('B', None)
        output_y = connections.get('Y', None)

        # Assign actual values to input_a_value and input_b_value based on wire_values
        input_a_value = wire_values.get(input_a, 0)  # Get from wire_values, default to 0 if not found
        input_b_value = wire_values.get(input_b, 0)  # Get from wire_values, default to 0 if not found

        # Evaluate the gate output using the corresponding function
        if gate_name in gate_functions:
            if input_b is not None:  # For gates with two inputs
                output_value = gate_functions[gate_name](input_a_value, input_b_value)
            else:  # For gates with one input (like NOT gate)
                output_value = gate_functions[gate_name](input_a_value)
        else:
            output_value = None  # If gate name is not recognized

        # Store the wire value if the output is a wire
        if output_y is not None:
            wire_values[output_y] = output_value  # Assign the calculated output to the corresponding wire
            if gate_name == 'or':  # If the last gate is an OR gate, store its output
                last_gate_output = output_value

        # Store the gate information in a list
        gate_info = [gate_name, input_a_value, input_b_value, output_value]
        gates_with_io.append(gate_info)

        # Print individual gate info
        print(f"Gate: {gate_name}")
        print(f"Input A: {input_a_value}")
        print(f"Input B: {input_b_value}")
        print(f"Output Y: {output_value if output_y is not None else 'Not Applicable'}")
        print("-" * 40)

    # Calculate the final output for the output gates
    final_outputs = {}
    for output in outputs:
        if output == 'y':  # Check if the output is 'y' and assign the last gate output
            final_outputs[output] = last_gate_output
        else:
            final_outputs[output] = wire_values.get(output, 0)  # Default to 0 if no wire connected

    # Print final outputs
    print("Final Outputs:")
    for output, value in final_outputs.items():
        print(f"Output {output}: {value}")

    return gates_with_io

# Read data from the file
with open("sample_net.txt", "r") as f:
    data = f.readlines()

# Extract inputs, outputs, and wires
inputs, outputs, wires = extract_io_wires(data)

# Print the extracted IOs
print(f"Inputs: {inputs}")
print(f"Outputs: {outputs}")
print(f"Wires: {wires}")
print("-" * 40)

# User-defined inputs
user_inputs = [1, 1, 0]  # Example inputs for the gates

# Join the lines into a single string and strip whitespace
my_string = ' '.join(map(str.strip, data))

# Updated regex pattern to capture gate definitions and connections
pattern = r'(\\\$[a-zA-Z0-9_]+)\s+#\((.*?)\)\s+_\d+_\s+\((.*?)\);'

# Find all matches in the text
matches = re.findall(pattern, my_string, re.DOTALL)

# Process each match and build the gates connections list
gates_connections = []
for match in matches:
    gate_name = match[0].strip().replace('\\$', '')  # Remove the leading backslash
    connections = match[2].strip()  # Extract connections

    # Find .A, .B, and .Y connections using regex
    connection_pattern = r'\.(A|B|Y)\s*\((\w+)\)'
    connection_matches = re.findall(connection_pattern, connections)

    # Build a dictionary for actual connections
    actual_connections = {port: var for port, var in connection_matches}

    # Append the gate connection to the list
    gates_connections.append({
        'gate_name': gate_name,
        'connections': actual_connections
    })

# Store and print the gates with IO using a list
gates_with_io = store_and_print_gates_with_io(inputs, outputs, wires, gates_connections, user_inputs)

# Print the entire gates_with_io list
print("Gates with I/O:")
for gate in gates_with_io:
    print(gate)
