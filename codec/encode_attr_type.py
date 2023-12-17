import struct, re

nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
# XXX: 必须和decode_attr_type.py中的MAX_SIZE_BITS一致
MAX_SIZE_BITS = 6
MAX_SIZE = (1 << MAX_SIZE_BITS) - 2
MAX_SHORT_FLOAT_BITS = 24
MAX_SHORT_FLOAT = (1 << MAX_SHORT_FLOAT_BITS) - 1

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

def __erase_zero(number_str):
    if type(number_str) != str:
        number_str = str(number_str)
    tmp_str = number_str
    sign = ''
    if number_str.startswith('-'):
        tmp_str = number_str[1:]
        sign = '-'
    
    exponent = 0
    if 'e' in tmp_str or 'E' in tmp_str:
        tmp_str, exponent = re.split(r'e|E', tmp_str)
        exponent = int(exponent, 10)
    
    while tmp_str.startswith('0') and len(tmp_str) > 1 and tmp_str[1] != '.':
        tmp_str = tmp_str[1:]
    if '.' in tmp_str:
        while tmp_str.endswith('0'):
            tmp_str = tmp_str[:-1]
        if tmp_str.endswith('.'):
            tmp_str = tmp_str[:-1]

    return sign, tmp_str, exponent

def __int_to_seq(number):
    length = ''
    if number <= MAX_SIZE and number >= -1:
        mark = 'G'
        data = format(number + 1, '0' + str(MAX_SIZE_BITS) + 'b')
    else:
        mark = 'A'
        data = format(number, 'b')
        sign = '0'
        if data.startswith('-'):
            sign = '1'
            data = data[1:]
        if len(data) & 1 == 0:
            data = '0' + data
        data = sign + data
        length = format(len(data) // 2 - 1, '04b')

    return mark + bin_to_seq(length + data)

def __float_to_seq_sys(number):
    binary = format(struct.unpack('>I', struct.pack('>f', number))[0], '032b')
    return 'C' + bin_to_seq(binary)

def __float_to_seq(sign, coefficient, exponent):
    mark = 'T'
    if sign == '-':
        sign = '1'
    else:
        sign = '0'
    binary_number = format(int(coefficient, 10), 'b')
    length_bin = len(binary_number)
    if length_bin % 4 != 0:
        binary_number = '0' * (4 - length_bin % 4) + binary_number
        length_bin += 4 - length_bin % 4

    ret = sign + format(length_bin // 4, '03b') + format(exponent + 8, '04b') + binary_number
    return mark + bin_to_seq(ret)

def number_to_seq(number_str, is_size=False):
    '''
    int -> A + length_nt(4 bit) + +/-(1 bit) + codec(max 31bit)
    exsize \in [-1,31) -> G + codec(? nts)
    float -> transfer to scientific notation, coefficient : 24 bit(IEEE float)
    exponent \in [-8, 7] -> T + +/-(1 bit) + length_bytes(3 bit) + exponent(4 bit) + coefficient(max 5 * 4 bit)
    else -> C + Float(32 bit)
    '''
    sign, number_str, exponent = __erase_zero(number_str)
    if not '.' in number_str and exponent == 0:
        return __int_to_seq(int(sign + number_str, 10))
    orginal_float = float(sign + number_str) * (10 ** exponent)
    integer = ''
    decimal = ''
    if '.' in number_str:
        integer, decimal = re.split(r'\.', number_str)
    else:
        integer = number_str
    
    if exponent == len(decimal):
        return __int_to_seq(int(sign + integer + decimal, 10))
    coefficient = integer + decimal
    coefficient_value = int(coefficient, 10)
    coefficient = str(coefficient_value)
    if coefficient_value > MAX_SHORT_FLOAT:
        return __float_to_seq_sys(orginal_float)
    exponent -= (len(decimal) - (len(coefficient) - 1))
    if exponent > 7 or exponent < -8:
        return __float_to_seq_sys(orginal_float)

    return __float_to_seq(sign, coefficient, exponent)

def str_to_seq(s):
    binary = ''
    if s == None:
        return number_to_seq(0)
    byte = s.encode("utf-8")
    for ch in byte:
        tmp = bin(ch).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp
    return number_to_seq(len(byte), True) + bin_to_seq(binary)