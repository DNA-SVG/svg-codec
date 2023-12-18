import struct, re
from decimal import Decimal

nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
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
        sign, digits, exponent = decimal.as_tuple()
        digits = ''.join(map(str, digits))
        return False, sign == 1, int(digits), exponent

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
        if len(data) & 1 == 0:
            data = '0' + data
        data = sign + data
        length = format((len(data) >> 1) - 1, '04b')

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
    length_bin = len(binary_number)
    if length_bin % 4 != 0:
        binary_number = '0' * (4 - length_bin % 4) + binary_number
        length_bin += 4 - length_bin % 4

    ret = sign + format(length_bin // 4, '03b') + format(-exponent, '04b') + binary_number
    return mark + bin_to_seq(ret)

def number_to_seq(number_str):
    '''
    int -> A + length_nt(4 bit) + +/-(1 bit) + codec(max 31bit)
    exsize \in [-1,31) -> G + codec(? nts)
    float -> transfer to scientific notation, coefficient : 24 bit(IEEE float)
    exponent \in [-8, 7] -> T + +/-(1 bit) + length_bytes(3 bit) + exponent(4 bit) + coefficient(max 5 * 4 bit)
    else -> C + Float(32 bit)
    '''
    is_int, sign, number, exponent = __normalize(number_str)
    if is_int:
        return __int_to_seq(sign, number)
    elif number > MAX_SHORT_FLOAT or exponent < -15:
        return __float_to_seq_sys(float(number_str))
    else:
        return __float_to_seq(sign, number, exponent)

def str_to_seq(s):
    binary = ''
    if s == None:
        return number_to_seq(0)
    byte = s.encode("utf-8")
    for ch in byte:
        tmp = bin(ch).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp
    return number_to_seq(len(byte)) + bin_to_seq(binary)