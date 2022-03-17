from misc import *
############################################################### INSTRUCOES TIPO I

def is_offset(instruction):
    return instruction[-1] == ')'

def get_immediate(imm):
    
    # CORRIGIR PARA NEGATIVOS


    if is_offset(imm):
        imm = imm[:imm.find('(')]
        imm = f'{int(imm):016b}'
    else:
        if(int(imm) < 0):
            imm = two_complement(imm)
            aux = '1' * (16-len(imm))
            imm = aux + imm
            return imm
        
        else : imm = f'{int(imm):016b}'

    return imm

def get_i_type_hex(instruction) :

    opcode = type_i_opcodes[instruction[0]]

    rt = get_register(instruction[1])

    imm = get_immediate(instruction[-1])

    if instruction[0] == 'lui':
        rs = '00000'

    elif(is_offset(instruction[-1])):

        rs = instruction[2]

        # pega o que está entre parêntese
        # no caso: OFFSET(base) ->  base
        rs = rs[ rs.find('(')+1 : rs.rfind(')')]
        rs = get_register(rs)

    else:
        rs = get_register(instruction[2])

    bin = opcode + rs + rt + imm

    hex_code = bin_to_hex(bin)

    return hex_code

