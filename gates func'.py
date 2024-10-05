def and_gate (input1,input2,output):

    output = input1 & input2

    return output 

def or_gate (input1,input2,output):

    output = input1 | input2

    return output 

def not_gate (input1,output):

    output = ~input1 

    return output 


def nand_gate (input1,input2,output):

    output = ~(input1 & input2)

    return output 
def nor_gate (input1,input2,output):

    output = ~(input1 | input2)

    return output 
def xor_gate (input1,input2,output):

    output = input1 ^ input2

    return output 
def xnor_gate (input1,input2,output):

    output = ~(input1 ^ input2)

    return output  