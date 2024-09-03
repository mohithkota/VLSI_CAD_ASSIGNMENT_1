import re

# Initialize global variables
data = []
main_ip = []
main_op = []
wires = []
assign = []
assignments_dict = {}
gates_list = ['and', 'or', 'not', 'nand', 'nor', 'xor', 'xnor']

# Function to extract text from a file
def text_extraction():
    with open("full_adder.txt", "r") as file:
        content = file.read()
        data = content.split()
        return data

data = text_extraction()

# Function to fetch input, output, wires, and assignments from the data
def ip_op_fetch(data):
    for i in range(len(data)):
        if data[i] == 'wire':
            wires.append(data[i + 1].strip(';'))
        if data[i] == 'input':
            main_ip.append(data[i + 1].strip(';'))
        if data[i] == 'output':
            main_op.append(data[i + 1].strip(';'))
        if data[i] == 'assign':
            assign.append(f"{data[i + 1]} {data[i + 2]} {data[i + 3].strip(';')}")

    # Create the assignments dictionary
    for assignment in assign:
        lhs, rhs = assignment.split('=')
        assignments_dict[lhs.strip()] = rhs.strip()

    return wires, main_ip, main_op, assign, assignments_dict

ip_op_fetch(data)

print("wires:", wires)
print("main_ip:", main_ip)
print("main_op:", main_op)
print("assignments_dict:", assignments_dict)
print("-" * 80)

# Process the data to extract gate connections
my_string = ' '.join(map(str.strip, data))
pattern = r'(\$[a-zA-Z0-9_]+)\s+#\((.*?)\)\s+\w+\s+\((.*?)\);'
matches = re.findall(pattern, my_string, re.DOTALL)

# Build the gates connections list
gates_connections = []
for match in matches:
    gate_name = match[0].strip().replace('$', '')
    connections = match[2].strip()

    connection_pattern = r'\.(A|B|Y)\s*\((\w+)\)'
    connection_matches = re.findall(connection_pattern, connections)

    actual_connections = {port: var for port, var in connection_matches}
    gates_connections.append({
        'gate_name': gate_name,
        'connections': actual_connections
    })

print("gate connections without updating")
for gate in gates_connections:
    print(gate)

print('-'*80)

# Update gate connections based on the assignments dictionary
for gate in gates_connections:
    connections = gate['connections']
    for key, value in connections.items():
        if value in assignments_dict:
            connections[key] = assignments_dict[value]

print("gate connections after updating")
for gate in gates_connections:
    print(gate)

print('-'*80)

# Function to levelize the circuit
def levelize_circuit(gates_connections):
    level_dict = {}
    unresolved_gates = gates_connections.copy()

    # Initialize levels for gates with direct main inputs
    level = 0
    while unresolved_gates:
        current_level_gates = []
        for gate in unresolved_gates:
            connections = gate['connections']
            if (connections['A'] in main_ip or connections['A'] in level_dict) and \
               ('B' not in connections or connections['B'] in main_ip or connections['B'] in level_dict):
                level_dict[connections['Y']] = level
                current_level_gates.append(gate)

        for gate in current_level_gates:
            unresolved_gates.remove(gate)
        
        level += 1

    return level_dict

# Levelize the gates
level_dict = levelize_circuit(gates_connections)

# Sort the gates based on their levels
gates_connections.sort(key=lambda x: level_dict.get(x['connections']['Y'], 0))

# Function to calculate gate outputs
def calculate_gate_output(gates_connections, main_ip, main_op):
    results = {}


    def gate_function(gate_name, input1, input2=None):
        if gate_name == 'and':
            return input1 & input2
        elif gate_name == 'or':
            return input1 | input2
        elif gate_name == 'not':
            return ~input1 & 1
        elif gate_name == 'xor':
            return input1 ^ input2 
        elif gate_name == 'xnor':
            return ~(input1 ^ input2)
        elif gate_name == 'nand':
            return ~(input1 & input2)
        elif gate_name == 'nor':
            return ~(input1 | input2)
        return None

    for gate in gates_connections:
        temp_gate_name = gate['gate_name']
        connections = gate['connections']

        input1 = main_ip[connections['A']] if connections['A'] in main_ip else results.get(connections['A'], None)
        input2 = None
        if 'B' in connections:
            input2 = main_ip[connections['B']] if connections['B'] in main_ip else results.get(connections['B'], None)
        
        if input1 is None or (input2 is None and temp_gate_name != 'not'):
            print(f"Error: Missing inputs for gate {temp_gate_name}. Inputs: A={input1}, B={input2}")
            continue

        output = gate_function(temp_gate_name, input1, input2)
        results[connections['Y']] = output

        # Print individual gate information
        print(f"\nGate Name: {temp_gate_name}")
        print(f"Input A ({connections['A']}): {input1}")
        if 'B' in connections:
            print(f"Input B ({connections['B']}): {input2}")
        print(f"Output Y ({connections['Y']}): {output}")

    print("\nFinal Outputs:")
    for output in main_op:
        # Use the assignments_dict to map the main_op to the actual wire that contains the result
        wire = assignments_dict.get(output, None)
        if wire and wire in results:
            final_output = results[wire]
        else:
            final_output = 'N/A'
        print(f"Output {output}: {final_output}")

# Map user inputs to main inputs
def get_user_inputs():
    input_values = {}
    for ip in main_ip:
        val = int(input(f"Enter the value for {ip} (0 or 1): "))
        input_values[ip] = val
    return input_values

# Main execution
main_ip_values = get_user_inputs()
calculate_gate_output(gates_connections, main_ip_values, main_op)
