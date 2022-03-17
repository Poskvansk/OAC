import sys

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

labels_dict = {}
###############################################################
def data_head(file):
    saida = open(file, 'w')
    saida.write('DEPTH = 16384;\n')
    saida.write('WIDTH = 32;\n')
    saida.write('ADDRESS_RADIX = HEX;\n')
    saida.write('DATA_RADIX = HEX;\n')
    saida.write('CONTENT\n')
    saida.write('BEGIN\n\n')
    saida.close()

def text_head(file):
    saida = open(file, 'w')
    saida.write('DEPTH = 4096;\n')
    saida.write('WIDTH = 32;\n')
    saida.write('ADDRESS_RADIX = HEX;\n')
    saida.write('DATA_RADIX = HEX;\n')
    saida.write('CONTENT\n')
    saida.write('BEGIN\n\n')
    saida.close()

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
        not_r_type = not (instruction[0] in type_r_funct or instruction[0] in special_r_type)
        not_i_type = not (instruction[0] in type_i_opcodes)
        not_j_type = not (instruction[0] == 'j' or instruction[0] == 'jal')
        not_sp2 = not (instruction[0] in special2_funct)

        if not_r_type and not_i_type and not_j_type and not_sp2 :
            raise ValueError("Unknown Instruction: " + instruction[0])

    except ValueError as e:
        print(e)
        sys.exit(1)

###############################################################

# retorna o tipo da instrucao J, R, I, COP1 ou PSEUDO
def get_type(instruction):
    
    # check_exceptions(instruction)

    if(instruction[0] == 'j' or instruction[0] == 'jal'):
        return 'j'

    elif(instruction[0] in type_i_opcodes):
        return 'i'

    elif(instruction[0] in type_r_funct or instruction[0] in special_r_type):
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

# RETIRA CARACTERES NÃO DESEJADOS DAS INSTRUÇÕES ( , \n espaços)
def normalize_inst(instruction):
    
    aux = []

    for i in instruction:
        if(i[-1] == ',' or i[-1] == '\n'):
            i = i[:-1]
        aux.append(i)

    return aux

############################################################### INSTRUCOES TIPO J
def hex_to_bin(hex_code):

    bin_code = ''

    for i in hex_code:
        dec = int(i,16)
        bin_code += f'{dec:04b}'

    return bin_code

def get_address(addr):

    if((addr+':') in labels_dict):
        addr = labels_dict[addr+':']

    elif (addr[:1] == '0x'):
        addr = addr[1:]

    else:
        addr = f'{int(addr):08x}'

    return addr

# RETORNA O HEX DOS TIPOS J
def get_j_type_hex(instruction):

    if instruction[0] == 'j': 
        opcode = '000010' 
    else:
        opcode = '000011' 

    address = get_address(instruction[1])

    address = hex_to_bin(address[1:])
           
    bin_code = opcode + address[:-2]

    hex_code = bin_to_hex(bin_code)
    
    return hex_code

############################################################### INSTRUCOES TIPO I
def is_offset(instruction):
    return instruction[-1] == ')'

def get_immediate(imm):
    
    # CORRIGIR PARA NEGATIVOS

    if is_offset(imm):
        imm = imm[:imm.find('(')]
        imm = f'{int(imm):016b}'
    else:
        imm = f'{int(imm):016b}'

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


############################################################### INSTRUCOES TIPO R

# ALGUMAS INSTRUCOES ESPECIAIS
# APESAR DE SEREM DO TIPO R, ELAS TEM UMA ESTRUTURA DIFERENTE
# POR ISSO FOI FEITO UMA FUNCAO PARA CADA UMA
# A FUNCAO APENAS RETORNA OS VALORES DOS CAMPOS SEGUINDO A ESTURTURA DAS FUNCOES
def div(instruction):

    rs = get_register(instruction[1])
    rt = get_register(instruction[2])
    rd = '00000'
    shamt = '00000'
    funct = '011010'

    return rs, rt, rd, shamt, funct

def jr(instruction):

    rs = get_register(instruction[1])
    rt = '00000'
    rd = '00000'
    hint = '00000'
    funct = '001000'

    return rs, rt, rd, hint, funct

def jalr(instruction):

    hint = '00000'
    funct = '001001'
    rt = '00000'

    if(len(instruction) == 2):
        rs = get_register(instruction[1])
        rd = '11111'
    else:
        rs = get_register(instruction[2])
        rd = get_register(instruction[1])

    return rs, rt, rd, hint, funct

def mfhi(instruction):

    rs = '00000'
    rt = '00000'

    rd = get_register(instruction[1])

    shamt = '00000'
    funct = '010000'

    return rs, rt, rd, shamt, funct

def mflo(instruction):

    rs = '00000'
    rt = '00000'

    rd = get_register(instruction[1])

    shamt = '00000'
    funct = '010010'
    
    return rs, rt, rd, shamt, funct

def movn(instruction):

    rs = get_register(instruction[2])
    rt = get_register(instruction[3])
    rd = get_register(instruction[1])
    shamt = '00000'
    funct = '001011'

    return rs, rt, rd, shamt, funct

def mult(instruction):

    rs = get_register(instruction[1])
    rt = get_register(instruction[2])
    rd = '00000'
    shamt = '00000'
    funct = '011000'

    return rs, rt, rd, shamt, funct

def sra(instruction):

    rs = '00000'
    rt = get_register(instruction[2])
    rd = get_register(instruction[1])
    sa = get_register(instruction[3])
    funct = '000011'

    return rs, rt, rd, sa, funct

def srav(instruction):

    rs = get_register(instruction[3])
    rt = get_register(instruction[2])
    rd = get_register(instruction[1])
    shamt = '00000'
    funct = '000111'

    return rs, rt, rd, shamt, funct

def teq(instruction):

    rs = get_register(instruction[1])
    rt = get_register(instruction[2])
    rd = '00000'
    shamt = '00000'
    funct = '110100'

    return rs, rt, rd, shamt, funct

# DICTIONARY TO FUNCTION CALLS
# FUCNTIONS ABOVE
special_r_type = {

        'div'   : div,
        'jr'    : jr,
        'jalr'  : jalr,
        'mfhi'  : mfhi,
        'mflo'  : mflo,
        'movn'  : movn,
        'mult'  : mult,
        'sra'   : sra,
        'srav'  : srav,
        'teq'   : teq,
}
def get_r_type_hex(instruction):

    opcode = '000000'

    # se a instrucao é do tip o R, mas um dos casos em que nao segue a estrutura padrao
    # (referidos aqui como special R type)
    # entao vai chamar a funcao que trata a instrucao especifica
    # a chamada é administrada pelo dictionary special_r_type
    if(instruction[0] in special_r_type):
        rs, rt, rd, shamt, funct = special_r_type[instruction[0]](instruction)

    # caso siga a estrutura padrao do tipo R, entao:
    else:
        rs = get_register(instruction[2])
        rt = get_register(instruction[3])
        rd = get_register(instruction[1])
        shamt = '00000'
        funct = type_r_funct[instruction[0]]

    bin = opcode + rs + rt + rd + shamt + funct
    
    hex_code = bin_to_hex(bin)

    return hex_code

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


############################################################### PSEUDO-INSTRUCOES
def li(instruction):

    return

pseudo_dict = {

    'li':li,
}
def get_pseudo(instruction):

    pseudo_dict[instruction[0]](instruction)

    return

###############################################################
# GERA O HEX DA INSTRUÇÃO
def get_hex(instruction):

    instruction = normalize_inst(instruction)

    type = get_type(instruction)

    if type == 'j':
        return get_j_type_hex(instruction)
       
    elif type == 'i':
        return get_i_type_hex(instruction)
        
    elif type == 'r':
        return get_r_type_hex(instruction)
    
    elif type == 'sp2':
        return get_special2_hex(instruction)
    
    elif type == 'cop1':
        return get_cop1_hex(instruction)
    
    else: return 'ERROR'

def main():

    # data_head()
    text_head('output.txt')
    assembled = []
    inst_list = []
    with open('test2.txt', 'r') as file:
        for line in file:

            instruction = line.split(' ')
            inst_list.append( instruction )
        file.close()

    for i in range(len(inst_list)):
        if (has_label(inst_list[i])):
            labels_dict[inst_list[i][0]] = '{:08x}'.format(i)
            inst_list[i] = inst_list[i][1:]
        assembled.append(get_hex(inst_list[i]))

    output = open('output.txt', 'a')

    for i in range(len(assembled)):
        output.write( '{:08x}'.format(i) + ' : ' + assembled[i] + ';\n')

    output.write( '\nEND;\n')
    output.close()


if __name__ == '__main__':

    main()