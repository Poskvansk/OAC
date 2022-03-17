from misc import *

############################################################### INSTRUCOES TIPO COP1
def get_cop1_hex(instruction):

    # GERANDO ERRADO!

    opcode = '010001'
    
    if instruction[0][-1] == 'd':
        fmt = '10001'
    if instruction[0][-1] == 's':
        fmt = '10000'
    
    ft = get_register(instruction[3])
    fs = get_register(instruction[2])
    fd = get_register(instruction[1])
    funct = cop1_funct[instruction[0][:instruction[0].find('.')]]

    bin = opcode + fmt + fd + fs + ft + funct

    hex_code = bin_to_hex(bin)

    return hex_code

