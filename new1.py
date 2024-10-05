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
    with open("half.txt", "r") as file:
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
print("-" * 100)

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

print("Gates connections:")
for gate in gates_connections:
    print(gate)
print("-" * 100)

# Update gate connections based on the assignments dictionary
for gate in gates_connections:
    connections = gate['connections']
    for key, value in connections.items():
        if value in assignments_dict:
            connections[key] = assignments_dict[value]

print("Updated values of the gate_connections:")
#print(gates_connections)
for gates in gates_connections:
    print(gates)
print("-" * 100)


def getting_ip_from_dict():
    for gate in gates_connections:
        # Step 1: Extract the gate name
        temp_gate_name = gate['gate_name']  # e.g., 'and'

        if temp_gate_name == 'not':
            temp_connections = gate['connections']
            input_a = temp_connections['A']
            output_y = temp_connections['Y']
            print(f"Gate Name: {temp_gate_name}")       #inplace of print statements i need to send these values to the gate function calculation
            print(f"Input A: {input_a}")
            print(f"Output Y: {output_y}")
            # gate_func(input_a,None,output_y)

        else:
        # Step 2: Extract the connections
            temp_connections = gate['connections']
            input_a = temp_connections['A']  # e.g., 'a'
            input_b = temp_connections['B']  # e.g., 'b'
            output_y = temp_connections['Y']  # e.g., '_0_'

        # Step 3: Store them in separate variables
            print(f"Gate Name: {temp_gate_name}")
            print(f"Input A: {input_a}")
            print(f"Input B: {input_b}")
            print(f"Output Y: {output_y}")
            # gate_func(input_a,input_b,output_y)
    return input_a,input_b,output_y

getting_ip_from_dict()


# Function to calculate the functionality of gates and final output


