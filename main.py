from itype import *
from jtype import *
from rtype import *
from specialtype import *
from cop1 import *
from misc import *

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

def produce_data(input_file, output_file):

    data_head(output_file)

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
            address = address + 1

        linha = entrada.readline()
        teste = (linha == '\n' or linha == ' ' or linha == '.text')
        linha = linha.replace(',', '').split(' ')

    saida.write('\nEND;')
    entrada.close()
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
# IEEE 754 FLOATING POINT
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

def get_exponent(num):

    exponent = ''

    return exponent

def ieee_normalize(num):

    return

def ieee754(num):
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
        mantissa = get_mantissa(dec_part)
        mantissa = int_part + mantissa
        print(mantissa)

        exponent = '0'*11

    return sign + exponent + mantissa

############################################################### PSEUDO-INSTRUCOES
def li(instruction):
    inst1 = get_hex(['lui', '$at', '0x'+instruction[2][2:6]])
    inst2 = get_hex(['ori', instruction[1], '$at', '0x'+instruction[2][6:]])
    return inst1, inst2


def get_pseudo(instruction):

    if instruction[0] == 'li':
        inst1, inst2 = li(instruction)

    return inst1, inst2

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

    elif type == 'pseudo':
        return get_pseudo(instruction)
    
    else: return 'ERROR'

def main():

    # INSIRA O NOME DO ARQUIVO EM file:
    # file = nome_do_arquivo
    if len(sys.argv) == 1:
        file = 'example_saida.asm'
    else:
        file = sys.argv[1]

    out_data = file[:file.rfind('.')]+'_data.mif'
    out_text = file[:file.rfind('.')]+'_text.mif'

    produce_data(file, out_data)
    text_head(out_text)

    assembled = []
    inst_list = []

    with open(file, 'r') as file:
        flag = False
        while(flag == False):
            line = file.readline()
            if(line[:-1] == '.text'):
                flag = True

        for line in file:
            instruction = line.split(' ')
            inst_list.append( instruction )
        file.close()

    for i in range(len(inst_list)):
        if (has_label(inst_list[i])):
            labels_dict[inst_list[i][0]] = '{:08x}'.format(i)
            inst_list[i] = inst_list[i][1:]

        hex_code = get_hex(inst_list[i])

        if(isinstance(hex_code,tuple)):
            assembled.append(hex_code[0])
            assembled.append(hex_code[1])
        else:
            assembled.append(get_hex(inst_list[i]))

    output = open(out_text, 'a')

    for i in range(len(assembled)):
        output.write( '{:08x}'.format(i) + ' : ' + assembled[i] + ';\n')

    output.write( '\nEND;\n')
    output.close()

if __name__ == '__main__':

    main()