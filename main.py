from itype import *
from jtype import *
from rtype import *
from specialtype import *
from cop1 import *
from misc import *

###############################################################
def produce_data(input_file, output_file):
    entrada = open(input_file, 'r')
    saida   = open(output_file, 'a')

    linha = entrada.readline() # pula a primeira linha que é a .data
    linha = entrada.readline()
    teste = (linha == '\n' or linha == ' ' or linha == '.text')
    linha = linha.replace(',', '').split(' ')

    address = 0
    while not teste: # para cada linha da secao .data
        quantidade = len(linha) - 2 # ve a quantidade de declaracoes, tira 2 do nome da variavel e do .word

        for i in range(quantidade):
            address_hex = hex(address)
            saida.write((str(address_hex).replace('0x', '')).zfill(8) + ' : ')
            saida.write((str(hex(int(linha[i + 2]))).replace('0x', '').zfill(8) + ';' + '\n'))
            print(linha[i+2]) # 0 é o nome da variavel, 1 é o '.word', os valores comecam a partir de 2
            address = address + 1

        linha = entrada.readline()
        teste = (linha == '\n' or linha == ' ' or linha == '.text')
        linha = linha.replace(',', '').split(' ')

    saida.write('\nEND;')
    entrada.close()
    saida.close()

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
# IEE 754 FLOATING POINT
def get_mantissa(num):

    mantissa = ''

    for i in range(52):
        mantissa += str(int(num*2))
        num *= 2   
        num -= int(num)

        if num == 0:
            break

    if len(mantissa) < 52:
        aux = '0'*(52-len(mantissa))
        new = mantissa + aux
        return new

    else:
        return mantissa

def iee754(num):

    if(num > 100):
        return
    
    else:
        int_part = int(num)
        dec_part = num - int_part

        if num > 0: 
            sign = '0'
        else: 
            sign = '1'

        int_part = bin(int_part)[2:]
        print(int_part)

        mantissa = get_mantissa(dec_part)
        print(mantissa)

        exponent = '0'*11


    return sign + exponent + mantissa

############################################################### PSEUDO-INSTRUCOES
def li(instruction):

    return

def get_pseudo(instruction):

    if instruction[0] == 'li':
        li(instruction)

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
    text_head('output.mif')
    assembled = []
    inst_list = []
    
    # print(get_mantissa(.9))

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

    output = open('output.mif', 'a')

    for i in range(len(assembled)):
        output.write( '{:08x}'.format(i) + ' : ' + assembled[i] + ';\n')

    output.write( '\nEND;\n')
    output.close()


if __name__ == '__main__':

    main()