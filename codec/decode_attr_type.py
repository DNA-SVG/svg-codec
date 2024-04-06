import struct
from decimal import Decimal
from .str_list import *

color_words = ['black', 'silver', 'gray', 'white', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua']
# XXX: 必须和encode_attr_type.py中的MAX_SIZE_BITS一致
MAX_SIZE_BITS = 6

def __seq_to_size(seq, start_idx=-1, call_number = False):
    ret = int(seq[:MAX_SIZE_BITS], 2)
    if call_number:
        return ret - 1, start_idx + MAX_SIZE_BITS
    else:
        return str(ret - 1), start_idx + MAX_SIZE_BITS

def __seq_to_int(seq, start_idx=-1, call_number = False):
    length = (int(seq[:4], 2) + 1) * 2
    seq = seq[4:]
    data = seq[:length]
    sign = 1
    if data[0] == '1':
        sign = -1
    data = data[1:]
    number = int(data, 2) * sign
    if call_number:
        return number, start_idx + length + 4
    else:
        return str(number), start_idx + length + 4
    
def __seq_to_short_float(seq, start_idx=-1):
    params = seq[:8]
    seq = seq[8:]
    sign = 0
    if params[0] == '1':
        sign = 1
    binary_nts = int(params[1:5], 2)
    total_nts = binary_nts * 2 + 8
    exponent = -int(params[5:], 2) - 1
    data = seq[:binary_nts* 2]
    data = str(int(data, 2))
    value = tuple(int(char) for char in data)

    decimal = Decimal((sign, value, exponent)).normalize()
    return str(decimal), start_idx + total_nts

def __seq_to_long_float(seq, start_idx=-1):
    binstr = seq[:32]
    binary = bytes(int(binstr[i:i + 8], 2) for i in range(0, 32, 8))
    ret = struct.unpack('>f', binary)[0]
    return str(ret), start_idx + 32

def seq_to_number(seq, start_idx=-1, call_number = False):
    mark = seq[:2]
    seq = seq[2:]
    start_idx += 2
    match mark:
        case '00':
            return __seq_to_int(seq, start_idx, call_number)
        case '01':
            return __seq_to_short_float(seq, start_idx)
        case '10':
            return __seq_to_long_float(seq, start_idx)
        case '11':
            return __seq_to_size(seq, start_idx, call_number)
        case _:
            return 0, start_idx - 2

def seq_to_color(seq, start_idx=-1, stat=0):
    match stat:
        case 0:
            ret = '#'
            for _ in range(1, 4):
                ret += format(int(seq[:8], 2), '02x')
                seq = seq[8:]
            return ret, start_idx + 24
        case 1:
            ret = []
            for i in range(0, 3):
                ret.append(str(int(seq[:6], 2)) + '%')
                seq = seq[6:]
            return 'rgb(' + ','.join(ret) + ')', start_idx + 18
        case 2:
            return color_words[int(seq[:4], 2)], start_idx + 4
        case _:
            return '', start_idx

def seq_to_str(seq, start_idx=-1):
    if seq[0:3] in ['010', '011', '100']:
        stat = int(seq[0:3], 2) - 2
        return seq_to_color(seq[3:], start_idx + 3, stat)
    index, idx = seq_to_number(seq, start_idx, True)
    return str_list_get(index), idx