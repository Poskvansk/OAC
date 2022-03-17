from misc import *
############################################################## INSTRUCOES TIPO R
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
    sa = f'{int(instruction[3]):05b}'
    sa = bin(int(instruction[3]))[2:].zfill(5)
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
