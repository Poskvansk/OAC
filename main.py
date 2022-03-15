from dis import Instruction
import sys
from turtle import pen
#spec2 opcode = 011100
special2_funct = {
    
    'clo'   : '100001',
    'madd'  : '000000',
    'mul'   : '000010',
    'msubu' : '000101',
}

type_i_opcodes = {

    'addi'  :'001000',
    'addiu' :'001001',
    'andi'  :'001100',
    'beq'   :'000100',
    'bne'   :'000101',
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

    # rever

    # 'clo'   : '100001',
    'div'   : '011010',
    'jr'    : '001000',
    'jalr'  : '001001',
    'mfhi'  : '010000',
    'mflo'  : '010010',
    'movn'  : '001011',
    'mult'  : '011000',
    'sra'   : '000011',
    'srav'  : '000111',
    # 'teq'   : '110100',
}

type_r_has_shamt = {

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

def data_head():
    saida = open('example_saida_data.mif', 'w')
    saida.write('DEPTH = 16384;\n')
    saida.write('WIDTH = 32;\n')
    saida.write('ADDRESS_RADIX = HEX;\n')
    saida.write('DATA_RADIX = HEX;\n')
    saida.write('CONTENT\n')
    saida.write('BEGIN\n\n')
    saida.close()

def text_head():
    saida = open('example_saida_text.mif', 'w')
    saida.write('DEPTH = 4096;\n')
    saida.write('WIDTH = 32;\n')
    saida.write('ADDRESS_RADIX = HEX;\n')
    saida.write('DATA_RADIX = HEX;\n')
    saida.write('CONTENT\n')
    saida.write('BEGIN\n')
    saida.close()

###############################################################

# retorna o tipo da instrucao J, R, I
def get_type(instruction):

    if(instruction[0] == 'j' or instruction[0] == 'jal'):
        return 'j'

    elif(instruction[0] in type_i_opcodes):
        return 'i'

    elif(instruction[0] in type_r_funct):
        return 'r'
    
    else: return 'z'

# RETORNA O VALOR EM BINÁRIO DO REGISTRADOR
def get_register(mask):
    
    if mask[0] == '$':
        
        if mask in register_mask_dict:
            reg = register_mask_dict[mask]
            reg = f'{reg:05b}'

        else:
            reg = f'{int(mask[1:]):05b}'

    return reg

# CONVERTE O CODIGO DE 32 BITS PARA HEXADECIMAL
def bin_to_hex(bin_code):

    # hex_code = '0x'
    hex_code = ''
    
    aux = ''
    for i in range(32):

        aux += bin_code[i]
        
        if(len(aux) == 4):
            hex_code += hex((int(aux,2)))[2:]
            aux = ''

    return hex_code

# RETIRA CARACTERES NÃO DESEJADOS DAS INSTRUÇÕES ( , \n espaços)
def normalize_inst(instruction):
    
    aux = []

    for i in instruction:
        if(i[-1] == ',' or i[-1] == '\n'):
            i = i[:-1]
        aux.append(i)

    return aux

# CHECA VALIDADE DA INSTRUÇÃO. CHECA SE ENCONTRA O TIPO DA INSTRUÇÃO E OS REGISTRADORES
# CASO HAJA ERRO, ENCERRA A EXECUÇÃO DO PROGRAMA, LEVANTANDO UMA EXCERÇÃO
def check_exceptions(instruction):

    try:
        not_r_type = not (instruction[0] in type_r_funct)
        not_i_type = not (instruction[0] in type_i_opcodes)
        not_j_type = not (instruction[0] == 'j' or instruction[0] == 'jal')

        if not_r_type and not_i_type and not_j_type :
            raise ValueError("Unknown Instruction: " + instruction[0])

    except ValueError as e:
        print(e)
        sys.exit(1)

    for reg in instruction[1:] :

        if not reg in register_mask_dict:
            try:
                int(reg[1:])
            except:
                print("Register not found: " + reg)
                sys.exit(1)

            try:
                if int(reg[1:]) < 0 or int(reg[1:]) > 31 :
                    raise ValueError("Register out of index: " + reg)

            except ValueError as e:
                print(e)
                sys.exit(1)


def get_j_type_hex(instruction):

    if instruction[0] == 'j': 
        opcode = '000010' 

    else:
        opcode = '000011' 

    address = instruction[1]

    bin = opcode + address
    
    hex_code = bin_to_hex(bin)

    return hex_code


def is_offset(instruction):
    return instruction[-1][-1] == ')'


def get_i_type_hex(instruction) :

    opcode = type_i_opcodes[instruction[0]]

    rt = get_register(instruction[1])

    if(is_offset(instruction)):

        rs = instruction[2]

        # pega o que está entre parêntese
        # no caso: OFFSET(base) ->  base
        rs = rs[ rs.find('(')+1 : rs.rfind(')')]
        rs = get_register(rs)

        # pega o que está antes do primeiro parêntese
        # no caso: OFFSET(base) ->  OFFSET
        imm = instruction[2][:instruction[2].find('(')]
        imm = f'{int(imm):016b}'
        

    else:
        rs = get_register(instruction[2])

        imm = f'{int(instruction[3]):016b}'

    bin = opcode + rs + rt + imm

    hex_code = bin_to_hex(bin)

    return hex_code

def get_r_type_hex(instruction):

    opcode = '000000'
    rs = get_register(instruction[2])
    rt = get_register(instruction[3])
    rd = get_register(instruction[1])
    shamt = '00000'
    funct = type_r_funct[instruction[0]]

    bin = opcode + rs + rt + rd + shamt + funct
    
    hex_code = bin_to_hex(bin)

    return hex_code

# GERA O HEX DA INSTRUÇÃO
def get_hex(instruction):

    instruction = normalize_inst(instruction)

    type = get_type(instruction)

    # check_exceptions(instruction)

    if type == 'j':
        return get_j_type_hex(instruction)
       
    elif type == 'i':
        return get_i_type_hex(instruction)
        
    elif type == 'r':

        return get_r_type_hex(instruction)
    
    else: return 'ERROR'


def main():

    assembled = []
    with open('test.txt', 'r') as file:
        for line in file:

            instruction = line.split(' ')

            assembled.append( (get_hex(instruction)) )

    output = open('output.txt', 'w')

    for i in assembled:
        output.write(i + '\n') 

main()