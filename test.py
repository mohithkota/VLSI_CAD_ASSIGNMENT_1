import re

# this to get the inputs and outputs from the textfile
def get_inputs():
    with open("sample_net.txt", "r") as f:
        data = f.readlines()

    inputs = []
    outputs = []

    for line in data:
        if "input" in line:
            inputs.append(line.strip())
        elif "output" in line:
            outputs.append(line.strip())

    return inputs, outputs
    

# this to get the gates from the textfile 

def get_gates_io():
    gates = []
    gate_io = {}

    with open("sample_net.txt", "r") as f:
        data = f.readlines() #data means textfile matter

    gate_keywords = ["and", "or", "not", "xor", "xnor", "nand", "nor"]

    current_gate = None
    for line in data:
        for gate in gate_keywords:
               if f"${gate}" in line.lower():
                current_gate = gate.upper()
                gates.append(current_gate)
                print(current_gate)
                gate_io[current_gate] = {'inputs': [], 'outputs': []}
                break

        # If we are inside a gate definition, extract its inputs/outputs
        if current_gate:
            inputs = re.findall(r'\.(A|B)\s*\(([^)]+)\)', line)
            outputs = re.findall(r'\.(Y)\s*\(([^)]+)\)', line)

            input_names = [input_name.strip() for _, input_name in inputs]
            output_names = [output_name.strip() for _, output_name in outputs]

            gate_io[current_gate]['inputs'].extend(input_names)
            gate_io[current_gate]['outputs'].extend(output_names)

        # Reset current_gate if the line ends the gate definition
        if ");" in line:
            current_gate = None

    return gates, gate_io
    

#counting the no.of gates occured 
temp  = get_gates_io()

from collections import Counter


my_list = temp[0] # type: ignore

# Use Counter to count occurrences
counts = Counter(my_list)
print("Counts:", counts)


# Calling the function and printing the results
gates, gate_io = get_gates_io()
print("Gates:", gates)
      
# Calling the function and printing the results
inputs, outputs = get_inputs()
print("Inputs:", inputs)
print("Outputs:", outputs)

#for printing each gate inputs from the textfile
for gate in gates:
    if gate in gate_io:  # Check if gate exists in the dictionary
        print(f"{gate} - Inputs: {gate_io[gate]['inputs']}, Outputs: {gate_io[gate]['outputs']}")
