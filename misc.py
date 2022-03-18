from misc import *
import sys

type_i_opcodes = {
    'addi'  :'001000',
    'addiu' :'001001',
    'andi'  :'001100',
    'beq'   :'000100',
    'bne'   :'000101',
    'lb'    :'100000',
    'lw'    :'100011',
    'sw'    :'101011',
    'slti'  :'001010',
    'sltiu' :'001011',
    'ori'   :'001101',
    'xori'  :'001110',

    # rever
    'lui':'001111',
}

type_r_funct = {
    'add'   : '100000',
    'addu'  : '100001',
    'and'   : '100100',
    'nor'   : '100111',
    'sub'   : '100010',
    'subu'  : '100011',
    'or'    : '100101',
    'xor'   : '100110',
}

special2_funct = {
    'clo'   : '100001',
    'madd'  : '000000',
    'mul'   : '000010',
    'msubu' : '000101',
}

cop1_funct = {
    'add'   :'000000',
    'sub'   :'000001',
    'div'   :'000011',
    'mul'   :'000010',
    'c.eq'  :'000000',
}

register_mask_dict = {
    '$zero': 0,
    '$at': 1,
    '$v0': 2,
    '$v1': 3,
    '$a0': 4,
    '$a1': 5,
    '$a2': 6,
    '$a3': 7,
    '$t0': 8,
    '$t1': 9,
    '$t2': 10,
    '$t3': 11,
    '$t4': 12,
    '$t5': 13,
    '$t6': 14,
    '$t7': 15,
    '$s0': 16,
    '$s1': 17,
    '$s2': 18,
    '$s3': 19,
    '$s4': 20,
    '$s5': 21,
    '$s6': 22,
    '$s7': 23,
    '$t8': 24,
    '$t9': 25,
    '$k0': 26,
    '$k1': 27,
    '$gp': 28,
    '$sp': 29,
    '$fp': 30,
    '$ra': 31
}
special_r_type2 = {

        'div'   : '1',
        'jr'    : '1',
        'jalr'  : '1',
        'mfhi'  : '1',
        'mflo'  : '1',
        'movn'  : '1',
        'mult'  : '1',
        'sra'   : '1',
        'srav'  : '1',
        'teq'   : '1',
}


pseudo_dict = {

    'li':'1',
}

labels_dict = {}
###############################################################


# CHECA VALIDADE DA INSTRUÇÃO. CHECA SE ENCONTRA O TIPO DA INSTRUÇÃO E OS REGISTRADORES
# CASO HAJA ERRO, ENCERRA A EXECUÇÃO DO PROGRAMA, LEVANTANDO UMA EXCERÃO
def check_register(reg):

    if not reg in register_mask_dict:
        try:
            if(reg.find('.')):
                int(reg[2:])
            else:
                int(reg[1:])
        except:
            print("Register not found: " + reg)
            sys.exit(1)

        try:

            if(reg.find('.')):
                if int(reg[2:]) < 0 or int(reg[2:]) > 31 :
                    raise ValueError("Register out of index: " + reg)
            else:
                if int(reg[1:]) < 0 or int(reg[1:]) > 31 :
                    raise ValueError("Register out of index: " + reg)

        except ValueError as e:
            print(e)
            sys.exit(1)

    return

def check_exceptions(instruction):

    try:
        not_r_type = not (instruction[0] in type_r_funct or instruction[0] in special_r_type2)
        not_i_type = not (instruction[0] in type_i_opcodes)
        not_j_type = not (instruction[0] == 'j' or instruction[0] == 'jal')
        not_sp2 = not (instruction[0] in special2_funct)

        if not_r_type and not_i_type and not_j_type and not_sp2 :
            raise ValueError("Unknown Instruction: " + instruction[0])

    except ValueError as e:
        print(e)
        sys.exit(1)


# retorna o tipo da instrucao J, R, I, COP1 ou PSEUDO
def get_type(instruction):
    
    # check_exceptions(instruction)

    if(instruction[0] == 'j' or instruction[0] == 'jal'):
        return 'j'

    elif(instruction[0] in type_i_opcodes):
        return 'i'

    elif(instruction[0] in type_r_funct or instruction[0] in special_r_type2):
        return 'r'

    elif(instruction[0] in special2_funct):
        return 'sp2'
    
    elif(instruction[0] in pseudo_dict):
        return 'pseudo'
    
    elif(instruction[0][:instruction[0].find('.')] in cop1_funct):
        return 'cop1'

    else: return 'z'

def has_label(instruction):
    return instruction[0][-1] == ':'

# RETORNA O VALOR EM BINÁRIO DO REGISTRADOR
def get_register(mask):
    
    check_register(mask)

    if mask[0] == '$':
        
        if mask in register_mask_dict:
            reg = register_mask_dict[mask]
            reg = f'{reg:05b}'

        else:
            if mask.find('f'):
                reg = f'{int(mask[2:]):05b}'
            else:
                reg = f'{int(mask[1:]):05b}'

    return reg

# CONVERTE O CODIGO DE 32 BITS PARA HEXADECIMAL
def bin_to_hex(bin_code):

    hex_code = ''
    
    aux = ''
    for i in range(32):

        aux += bin_code[i]
        
        if(len(aux) == 4):
            hex_code += hex((int(aux,2)))[2:]
            aux = ''

    return hex_code

def hex_to_bin(hex_code):

    bin_code = ''

    for i in hex_code:
        dec = int(i,16)
        bin_code += f'{dec:04b}'

    return bin_code

# RETIRA CARACTERES NÃO DESEJADOS DAS INSTRUÇÕES ( , \n espaços)
def normalize_inst(instruction):
    
    aux = []

    for i in instruction:
        if(i[-1] == ',' or i[-1] == '\n'):
            i = i[:-1]
        aux.append(i)

    return aux

# FAZ COMPLEMENTO DE 2
def two_complement(num):

    num = int(num)
    num = abs(num)
    num = bin(num)[2:]
    compl = '1'

    for i in num:
        if i =='1': compl += '0'
        else: compl += '1'
    sum = bin(int(compl,2) + 1)[2:]


    return str(sum)
