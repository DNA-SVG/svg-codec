import struct, re, math
from decimal import Decimal
from .str_list import *
from .collect import CollectMethod

nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
color_words = ['black', 'silver', 'gray', 'white', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua']
# XXX: 必须和decode_attr_type.py中的MAX_SIZE_BITS一致
MAX_SIZE_BITS = 6
MAX_SIZE = (1 << MAX_SIZE_BITS) - 2
MAX_SHORT_FLOAT = (1 << 24) - 1
MAX_INT = (1 << 31) - 1

def bin_to_seq(binSeq):
    n = len(binSeq)
    if n % 2 == 1:
        binSeq = '0' + binSeq
        n += 1

    ret = ''
    for i in range(0, n, 2):
        unit = binSeq[i:i+2]
        ret += nt_dict[unit]

    return ret

def __normalize(number_str):
    decimal = Decimal(number_str)
    if decimal == decimal.to_integral():
        value = decimal.quantize(Decimal(1))
        return True, value < 0, int(value), 0
    else:
        decimal = decimal.normalize()
        sign, digit_tuple, exponent = decimal.as_tuple()
        digits = 0
        for digit in digit_tuple:
            digits = digits * 10 + digit
        return False, sign == 1, digits, exponent

def __int_to_seq(sign, number):
    length = ''
    if number <= MAX_SIZE and number >= -1:
        mark = 'G'
        data = format(number + 1, '0' + str(MAX_SIZE_BITS) + 'b')
    else:
        mark = 'A'
        if sign:
            number = -number
            sign = '1'
        else:
            sign = '0'
        data = format(number, 'b')
        length = math.floor(math.log2(number)) + 1
        if length & 1 == 0:
            data = '0' + data
            length += 1
        data = sign + data
        length = format(((length + 1) >> 1) - 1, '04b')

    return mark + bin_to_seq(length + data)

def __float_to_seq_sys(number):
    binary = format(struct.unpack('>I', struct.pack('>f', number))[0], '032b')
    return 'C' + bin_to_seq(binary)

def __float_to_seq(sign, coefficient, exponent):
    mark = 'T'
    if sign:
        sign = '1'
    else:
        sign = '0'
    binary_number = format(coefficient, 'b')
    length_bin = math.floor(math.log2(coefficient)) + 1
    if length_bin & 1 != 0:
        binary_number = '0' + binary_number
        length_bin += 1

    ret = sign + format(length_bin >> 1, '04b') + format(-exponent-1, '03b') + binary_number
    return mark + bin_to_seq(ret)

def number_to_seq(number_str):
    '''
    int -> A + length_nt(4 bit) + +/-(1 bit) + codec(max 31bit)
    exsize \in [-1,31) -> G + codec(? nts)
    float -> transfer to scientific notation, coefficient : 24 bit(IEEE float)
    exponent >= -8 -> T + +/-(1 bit) + length_nt(4 bit) + exponent(3 bit) + coefficient(max 6 * 4 bit)
    else -> C + Float(32 bit)
    '''
    is_int, sign, number, exponent = __normalize(number_str)
    if is_int:
        return __int_to_seq(sign, number)
    elif number > MAX_SHORT_FLOAT or exponent < -8:
        return __float_to_seq_sys(float(number_str))
    else:
        return __float_to_seq(sign, number, exponent)

def __check_color(s):
    '''
    white, #FFFFFF, #FFF, rgb(255, 255, 255), rgb(100%, 100%, 100%)
    '''
    if s == None:
        return -1, 0, 0, 0
    if s in color_words:
        return 2, color_words.index(s)
    obj = re.match(r'#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$', s)
    if obj != None:
        return 0, int(obj.group(1), 16), int(obj.group(2), 16), int(obj.group(3), 16)
    obj = re.match(r'#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])$', s)
    if obj != None:
        return 0, int(obj.group(1), 16) * 17, int(obj.group(2), 16) * 17, int(obj.group(3), 16) * 17
    obj = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$', s)
    if obj != None:
        return 0, int(obj.group(1), 10), int(obj.group(2), 10), int(obj.group(3), 10)
    obj = re.match(r'rgb\(\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*\)$', s)
    if obj != None:
        return 1, int(obj.group(1), 10), int(obj.group(2), 10), int(obj.group(3), 10)
    return -1, 0, 0, 0

def color_to_seq(s):
    ret = __check_color(s)
    match ret[0]:
        case 0:
            seq = 'TA'
            for i in range(1, 4):
                if ret[i] > 255:
                    ret[i] = 255
                seq += bin_to_seq(format(ret[i], '08b'))
            return seq
        case 1:
            seq = 'TC'
            for i in range(1, 4):
                if ret[i] > 100:
                    ret[i] = 100
                seq += bin_to_seq(format(ret[i], '06b'))
            return seq
        case 2:
            seq = 'TT'
            seq += bin_to_seq(format(ret[1], '04b'))
            return seq
        case _:
            return None

def str_to_seq(s):
    '''
    default: length + code(utf-8)
    color: T + (A + rgb) or (T + word) or (C + %)
    '''
    color_str = color_to_seq(s)
    if color_str != None:
        return color_str
    if s == None:
        return number_to_seq(0)
    return number_to_seq(str_list_put(s))