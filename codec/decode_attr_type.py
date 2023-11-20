import struct

dict_nt = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}
# XXX: 必须和encode_attr_type.py中的MAX_SIZE_BITS一致
MAX_SIZE_BITS = 7
MAX_SIZE = (1 << MAX_SIZE_BITS) - 2
MAX_SIZE_NTS = (1 + MAX_SIZE_BITS) >> 1

def seq_to_bin(str, x):
    ret = ''
    for i in range(0, x):
        ret += dict_nt[str[i]]
    return ret


def decode(seq, start_idx=-1, is_size=False):
    '''传入一段DNA片段返回对应的值'''
    if is_size:
        return __seq_to_number(seq, is_size, start_idx)
    match seq[0]:
        case 'A' | 'T':
            return __seq_to_number(seq, is_size, start_idx)
        case 'G':
            return __seq_to_str(seq, start_idx)
        case 'C':
            return __seq_to_float(seq[1:17], start_idx)
        case _:
            return '', start_idx


def __seq_to_float(seq, start_idx=-1):
    binstr = seq_to_bin(seq, 16)
    binary = bytes(int(binstr[i:i + 8], 2) for i in range(0, 32, 8))
    ret = struct.unpack('>f', binary)[0]
    ret = str(ret)
    return ret, start_idx + 17


def __seq_to_size(seq, start_idx=-1):
    ret = MAX_SIZE - int(seq_to_bin(seq, MAX_SIZE_NTS)[1:], 2)
    return ret, start_idx + MAX_SIZE_NTS


def __seq_to_number(seq, is_size=False, start_idx=-1):
    '''orders: 0 = use this codec(1 bit)
    sign: 1 = +, 0 = -
    ∵123.4567 = 1234567 * 0.1^4
    ∴len_below1 = 4, 1234567 -> 0x12d687 -> len_total = 6
    '''
    if is_size and (seq[0] == 'G' or seq[0] == 'C'):
        return __seq_to_size(seq, start_idx)
    if is_size:
        orders = seq_to_bin(seq, 2)
        len_total = int(orders[1:4], 2) + 1
        seq = seq[2:]
    else:
        orders = seq_to_bin(seq, 4)
        seq = seq[4:]
        sign = (orders[1] == '1')
        len_total = int(orders[2:5], 2) + 1
        len_below1 = int(orders[5:8], 2)
    number_str = seq_to_bin(seq, len_total * 2)
    num = int(number_str, 2)
    if is_size:
        return num, start_idx + 2 + 2 * len_total
    ret = str(num)
    if len_below1 == len(ret):
        ret = '0.' + ret
    elif len_below1 > 0:
        ret = ret[:-len_below1] + '.' + ret[-len_below1:]
    if not sign:
        ret = '-' + ret
    return ret, start_idx + 4 + 2 * len_total


def __seq_to_str(seq, start_idx=-1):
    ba = bytearray()
    strlen, start_tag = __seq_to_number(seq[1:], True, 1)
    strlen *= 4
    for i in range(start_tag, start_tag + strlen, 4):
        byte = ''
        for j in range(i, i + 4):
            byte += dict_nt[seq[j]]
        ba.append(int(byte, 2))
    ret = ba.decode(encoding='utf-8')
    return ret, start_idx + start_tag + strlen
