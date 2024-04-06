import gzip
str_list = []

def __bytes_to_seq(bytes):
    seq = ''
    for byte in bytes:
        seq += format(byte, '08b')
    return seq

def __seq_to_bytes(seq):
    bytearr = bytearray()
    for i in range(0, len(seq), 8):
        byte = ''
        for j in range(i, i+8):
            byte += seq[j]
        bytearr.append(int(byte, 2))
    return bytes(bytearr)

def str_list_clear():
    str_list.clear()

def str_list_put(s):
    if s not in str_list:
        str_list.append(s)
    return str_list.index(s)

def str_list_get(index):
    return str_list[index]

def str_list_pack():
    packed_data = gzip.compress('\0'.join(str_list).encode())
    return '111111' + __bytes_to_seq(packed_data)

def str_list_unpack(packed_data):
    str_list.clear()
    data = __seq_to_bytes(packed_data)
    str_list.extend(gzip.decompress(data).decode().split('\0'))