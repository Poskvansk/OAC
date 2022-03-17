from misc import *


############################################################### INSTRUCOES SPECIAL2
def get_special2_hex(instruction):

    opcode = '011100'
    funct = special2_funct[instruction[0]]
    shamt = '00000'

    if instruction[0] == 'clo':

        rd = get_register(instruction[1])
        rs = get_register(instruction[2])
        rt = '00000'
        
    elif instruction[0] == 'mul':

        rd = get_register(instruction[1])
        rs = get_register(instruction[2])
        rt = get_register(instruction[3])

    else:        
        rs = get_register(instruction[1])
        rt = get_register(instruction[2])
        rd = '00000'

    bin = opcode + rs + rt + rd + shamt + funct
    
    hex_code = bin_to_hex(bin)

    return hex_code
