import re
from collections import defaultdict, deque

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

def extract_assignments(data):
    assignments = {}
    for line in data:
        line = line.strip()
        match = re.match(r'assign\s+(\w+)\s*=\s*(\w+);', line)
        if match:
            lhs = match.group(1)
            rhs = match.group(2)
            assignments[lhs] = rhs
    return assignments

def build_dependency_graph(gates_connections):
    graph = defaultdict(list)
    indegree = {gate['gate_name']: 0 for gate in gates_connections}

    for gate in gates_connections:
        gate_name = gate['gate_name']
        connections = gate['connections']
        
        # Check for inputs A and B
        input_a = connections.get('A')
        if input_a:
            graph[input_a].append(gate_name)
            indegree[gate_name] += 1
        
        input_b = connections.get('B')
        if input_b:
            graph[input_b].append(gate_name)
            indegree[gate_name] += 1

    return graph, indegree

def topological_sort(graph, indegree):
    sorted_gates = []
    queue = deque([node for node in indegree if indegree[node] == 0])
    
    while queue:
        current = queue.popleft()
        sorted_gates.append(current)
        
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_gates

def store_and_print_gates_with_io(inputs, outputs, wires, gates_connections, user_inputs, assignments):
    gates_with_io = []
    wire_values = {inputs[i]: user_inputs[i] for i in range(len(inputs))}  # Initialize wire values from user inputs

    # Apply assignments to wire_values
    for lhs, rhs in assignments.items():
        wire_values[lhs] = wire_values.get(rhs, 0)  # Assign RHS value to LHS

    # Define gate functions
    def and_gate(input1, input2):
        return input1 & input2

    def or_gate(input1, input2):
        return input1 | input2

    def not_gate(input1):
        return ~input1 & 1  # Ensuring output is 0 or 1

    # Mapping of gate names to functions
    gate_functions = {
        '$and': and_gate,
        '$or': or_gate,
        '$not': not_gate,
    }

    # Build the dependency graph and perform topological sort
    graph, indegree = build_dependency_graph(gates_connections)
    sorted_gates = topological_sort(graph, indegree)

    # Process gates in sorted order
    for gate_name in sorted_gates:
        # Find the corresponding gate in gates_connections
        gate = next(gate for gate in gates_connections if gate['gate_name'] == gate_name)
        connections = gate['connections']
        input_a = connections.get('A', None)
        input_b = connections.get('B', None)
        output_y = connections.get('Y', None)

        # Assign actual values to input_a_value and input_b_value based on wire_values
        input_a_value = wire_values.get(input_a, 0)  # Get from wire_values, default to 0 if not found
        input_b_value = wire_values.get(input_b, 0) if input_b else None  # Get B value if it exists

        # Evaluate the gate output using the corresponding function
        if gate_name in gate_functions:
            if gate_name == '$not':
                output_value = gate_functions[gate_name](input_a_value)
            else:  # For gates with two inputs
                output_value = gate_functions[gate_name](input_a_value, input_b_value)
        else:
            output_value = None  # If gate name is not recognized

        # Store the wire value if the output is a wire
        if output_y is not None:
            wire_values[output_y] = output_value  # Assign the calculated output to the corresponding wire

        # Store the gate information in a list
        gate_info = [gate_name, input_a_value, input_b_value, output_value]
        gates_with_io.append(gate_info)

        # Print individual gate info including input and output values
        print(f"Gate: {gate_name}, Input A: {input_a_value} (Wire: {input_a}), Input B: {input_b_value} (Wire: {input_b}), Output Y: {output_value if output_y is not None else 'Not Applicable'} (Wire: {output_y})")
        print("-" * 40)

    # Print wire values after processing all gates
    print("Wire values after processing all gates:")
    for wire, value in wire_values.items():
        print(f"Wire: {wire}, Value: {value}")
    print("-" * 40)

    # Calculate the final output for the output gates
    final_outputs = {}
    for output in outputs:
        final_outputs[output] = wire_values.get(output, 0)  # Default to 0 if no wire connected

    # Print final outputs
    print("Final Outputs:")
    for output, value in final_outputs.items():
        print(f"Output {output}: {value}")

    return gates_with_io

# Read data from the file
with open("half.txt", "r") as f:
    data = f.readlines()

# Extract inputs, outputs, and wires
inputs, outputs, wires = extract_io_wires(data)

# Extract assignment statements
assignments = extract_assignments(data)

# Print the extracted IOs
print(f"Inputs: {inputs}")
print(f"Outputs: {outputs}")
print(f"Wires: {wires}")
print("-" * 40)

# User-defined inputs
user_inputs = [1, 0]  # Example inputs for the gates

# Join the lines into a single string and strip whitespace
my_string = ' '.join(map(str.strip, data))

# Updated regex pattern to capture gate definitions and connections
pattern = r'(\$[a-zA-Z0-9_]+)\s+#\((.*?)\)\s+\w+\s+\((.*?)\);'  # Modified pattern

# Find all matches in the text
matches = re.findall(pattern, my_string, re.DOTALL)

# Print the matches to debug
print("Matches found by regex:")
for match in matches:
    print(match)

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

# Print gates connections for debugging
print("Gates connections:")
for gate in gates_connections:
    print(gate)

# Store and print the gates with IO using a list
gates_with_io = store_and_print_gates_with_io(inputs, outputs, wires, gates_connections, user_inputs, assignments)
print("Gates with I/O:")
for gate in gates_with_io:
    print(gate)
