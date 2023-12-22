import gzip
str_list = []

nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
dict_nt = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}

def __bytes_to_seq(bytes):
    seq = ''
    for byte in bytes:
        binary = format(byte, '08b')
        for i in range(0, 8, 2):
            seq += nt_dict[binary[i:i+2]]
    return seq

def __seq_to_bytes(seq):
    bytearr = bytearray()
    length = len(seq)
    for i in range(0, length, 4):
        byte = ''
        for j in range(i, i+4):
            byte += dict_nt[seq[j]]
        bytearr.append(int(byte, 2))
    return bytes(bytearr)

def str_list_clear():
    str_list.clear()
    str_list.append('')

def str_list_put(s):
    if s not in str_list:
        str_list.append(s)
    return str_list.index(s)

def str_list_get(index):
    return str_list[index]

def str_list_pack():
    packed_data = gzip.compress('\0'.join(str_list).encode())
    return __bytes_to_seq(packed_data)

def str_list_unpack(packed_data):
    str_list.clear()
    str_list.append('')
    data = __seq_to_bytes(packed_data)
    str_list.extend(gzip.decompress(data).decode().split('\0'))