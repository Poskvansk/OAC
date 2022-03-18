from misc import *
############################################################### INSTRUCOES TIPO J
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
