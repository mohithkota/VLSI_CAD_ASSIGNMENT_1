def and_gate(input1, input2):
    output = input1 & input2
    return output 

def or_gate(input1, input2):
    output = input1 | input2
    return output 

def not_gate(input1):
    output = ~input1 
    return output 

def nand_gate(input1, input2):
    output = ~(input1 & input2)
    return output 

def nor_gate(input1, input2):
    output = ~(input1 | input2)
    return output 

def xor_gate(input1, input2):
    output = input1 ^ input2
    return output 

def xnor_gate(input1, input2):
    output = ~(input1 ^ input2)
    return output  

# List of gate function names
gates_list = [and_gate, or_gate, not_gate, nand_gate, nor_gate, xor_gate, xnor_gate]

# Example gates_with_io list structure
# Assuming gates_with_io contains tuples of (gate_name, input1, input2, output)
gates_with_io = [
    ('and_gate', 1, 1, None),  # Example of and gate
    ('or_gate', 1, 0, None),   # Example of or gate
    ('not_gate', 1, None, None),  # Example of not gate
    # Add more gates as needed
]

# Process each gate in gates_with_io
for gate in gates_with_io:
    gate_name = gate[0]
    input1 = gate[1]
    
    # Check if the gate requires two inputs
    if gate_name in ['and_gate', 'or_gate', 'nand_gate', 'nor_gate', 'xor_gate', 'xnor_gate']:
        input2 = gate[2]
        # Call the corresponding function and print the result
        for g_func in gates_list:
            if g_func.__name__ == gate_name:
                output = g_func(input1, input2)
                print(f"{gate_name}({input1}, {input2}) = {output}")

    # Check if the gate requires only one input
    elif gate_name == 'not_gate':
        # Call the not_gate function
        output = not_gate(input1)
        print(f"{gate_name}({input1}) = {output}")
