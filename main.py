#spec2 opcode = 011100
special2_funct = {
    
    'clo'   : '100001',
    'madd'  : '000000',
    'mul'   : '000010',
    'msubu' : '000101',
}

type_i_opcodes = {

    'addi'  :'001000',
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
    'clo'   : '100001',
    'div'   : '011010',
    'jr'    : '001000',
    'jalr'  : '001001',
    'mfhi'  : '010000',
    'mflo'  : '010010',
    'movn'  : '001011',
    'mult'  : '011000',
    'sra'   : '000011',
    'srav'  : '000111',
    'srav'  : '000111',
    'teq'   : '110100',
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

""""
register_dict = {

    '$0'
    '$1'
    '$2'
    '$3'
    '$4'
    '$5'
    '$6'
    '$7'
    '$8'
    '$9'
    '$10'
    '$11'
    '$12'
    '$13'
    '$14'
    '$15'
    '$16'
    '$17'
    '$18'
    '$19'
    '$20'
    '$21'
    '$22'
    '$23'
    '$24'
    '$25'
    '$26'
    '$27'
    '$28'
    '$29'
    '$30'
    '$31'
}

fregister_dict = {
    '$f0': 0
    '$f1': 1
    '$f2': 2
    '$f3': 3
    '$f4': 4
    '$f5': 5
    '$f6': 6
    '$f7': 7
    '$f8': 8
    '$f9': 9
    '$f10': 10
    '$f11': 11
    '$f12': 12
    '$f13': 13
    '$f14': 14
    '$f15': 15
    '$f16': 16
    '$f17': 17
    '$f18': 18
    '$f19': 19
    '$f20': 20
    '$f21': 21
    '$f22': 2
    '$f23': 
    '$f24': 
    '$f25': 
    '$f26': 
    '$f27': 
    '$f28': 
    '$f29': 
    '$f30': 
    '$f31': 
}
"""

def get_type(instruction):

    if(instruction[0] == 'j' or instruction[0] == 'jal'):
        return 'j'

    elif(instruction[-1].isdigit()):
        return 'i'

    else:
        return 'r'

def get_register(mask):
    
    if mask[0] == '$':
        
        if mask in register_mask_dict:
            reg = register_mask_dict[mask]
            reg = f'{reg:05b}'

        else:
            reg = f'{int(mask[1::]):05b}'

    return reg

def bin_to_hex(bin_code):

    hex_code = '0x'
    
    aux = ''
    for i in range(32):

        aux += bin_code[i]
        
        if(len(aux) == 4):
            hex_code += hex((int(aux,2)))[2:]
            aux = ''

    return hex_code

def normalize_inst(instruction):
    
    aux = []

    for i in instruction:
        if(i[-1] == ',' or i[-1] == '\n'):
            i = i[:-1]
        aux.append(i)

    return aux

def get_hex(instruction):

    instruction = normalize_inst(instruction)

    type = get_type(instruction)

    if type == 'j':

        if instruction[0] == 'j': 
            opcode = '000010' 

        else:
            opcode = '000011' 

        address = instruction[1]

        bin = opcode + address
        
        hex_code = bin_to_hex(bin)

    elif type == 'i':

        opcode = type_i_opcodes[instruction[0]]
        rs = get_register(instruction[1])
        rt = get_register(instruction[2])
        imm = f'{int(instruction[3]):016b}'

        bin = opcode + rs + rt + imm

        hex_code = bin_to_hex(bin)

    elif type == 'r':

        opcode = '000000'
        rs = get_register(instruction[2])
        rt = get_register(instruction[3])
        rd = get_register(instruction[1])
        shamt = '00000'
        funct = type_r_funct[instruction[0]]

        bin = opcode + rs + rt + rd + shamt + funct
        
        hex_code = bin_to_hex(bin)

    return hex_code


def main():

    with open('test.txt', 'r') as file:

        line = file.readline() 
        # line = file.readline() 


    print(line)
    
    instruction = line.split(' ')

    print(get_hex(instruction))

main()