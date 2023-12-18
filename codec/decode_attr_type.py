import struct
from decimal import Decimal

dict_nt = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}
# XXX: 必须和encode_attr_type.py中的MAX_SIZE_BITS一致
MAX_SIZE_BITS = 6
MAX_SIZE_NTS = MAX_SIZE_BITS >> 1

def seq_to_bin(str, x):
    ret = ''
    for i in range(0, x):
        ret += dict_nt[str[i]]
    return ret

def __seq_to_size(seq, start_idx=-1):
    ret = int(seq_to_bin(seq, MAX_SIZE_NTS), 2)
    return ret - 1, start_idx + MAX_SIZE_NTS

def __seq_to_int(seq, start_idx=-1):
    length = int(seq_to_bin(seq, 2), 2) + 1
    seq = seq[2:]
    data = seq_to_bin(seq, length)
    sign = 1
    if data[0] == '1':
        sign = -1
    data = data[1:]
    number = int(data, 2) * sign
    return number, start_idx + length + 2
    
def __seq_to_short_float(seq, start_idx=-1):
    params = seq_to_bin(seq, 4)
    seq = seq[4:]
    sign = 0
    if params[0] == '1':
        sign = 1
    binary_nts = int(params[1:4], 2) * 2
    total_nts = binary_nts + 4
    exponent = -int(params[4:], 2)
    data = seq_to_bin(seq, binary_nts)
    data = str(int(data, 2))
    value = tuple(int(char) for char in data)

    decimal = Decimal((sign, value, exponent)).normalize()
    return str(decimal), start_idx + total_nts

def __seq_to_long_float(seq, start_idx=-1):
    binstr = seq_to_bin(seq, 16)
    binary = bytes(int(binstr[i:i + 8], 2) for i in range(0, 32, 8))
    ret = struct.unpack('>f', binary)[0]
    ret = str(ret)
    return ret, start_idx + 16

def seq_to_number(seq, start_idx=-1):
    mark = seq[0]
    seq = seq[1:]
    start_idx += 1
    match mark:
        case 'A':
            return __seq_to_int(seq, start_idx)
        case 'T':
            return __seq_to_short_float(seq, start_idx)
        case 'C':
            return __seq_to_long_float(seq, start_idx)
        case 'G':
            return __seq_to_size(seq, start_idx)
        case _:
            return 0, start_idx - 1

def seq_to_str(seq, start_idx=-1):
    ba = bytearray()
    strlen, start_tag = seq_to_number(seq, 0)
    strlen *= 4
    for i in range(start_tag, start_tag + strlen, 4):
        byte = ''
        for j in range(i, i + 4):
            byte += dict_nt[seq[j]]
        ba.append(int(byte, 2))
    ret = ba.decode(encoding='utf-8')
    return ret, start_idx + start_tag + strlen