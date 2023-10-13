import struct

nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}

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

def float_to_seq(num):
    """传入float,对应c标准的float(8 bit)"""
    """以str形式返回编码dna序列"""
    #获得字节信息
    bs = struct.pack('>f', num)

    #字节转01串
    binary = ''
    for i in bs:
        tmp = bin(i).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp

    return 'C' + bin_to_seq(binary)

def get_shrink_offset(str):
    offset = -1
    while str[offset] == '0':
        offset -= 1
    if str[offset] == '.':
        offset -= 1
    offset += 1
    if offset < 0:
        return str[:offset], -offset
    else:
        return str, 0
    
def number_split(number_str, is_size):
    if is_size:
        return format(int(number_str), 'b'), '000'
    len_below1 = ''
    decs = str.split(number_str, '.')
    if len(decs) > 1:
        len_below1 = format(len(decs[1]),'03b')
    else:
        len_below1 = '000'
    return format(int(''.join(decs), 10), 'b'), len_below1

def number_to_seq(number_str, is_size=False):
    ''' components:
    Float(123456789): 'C'(10) + float_to_seq
    Number(1234567.8): '0' + sign(1) + total(3) + below1(3) + binary(max 32)
    Size_t(<8 bytes, positive int or 0): '0' + total(3) + binary(max 32)

    ∵123.4567 = 1234567 * 0.1^4
    ∴len_below1 = 4, 1234567 -> 0x12d687 -> len_total = 6
    '''
    if type(number_str) != str:
        number_str = str(number_str)
    if is_size and number_str == '-1':
        return 'G'
    length = len(number_str)
    if '-' in number_str:
        length -= 1
    if '.' in number_str:
        number_str, offset = get_shrink_offset(number_str)
        length -= (offset + 1)
    if length >= 8:
        return float_to_seq(number_str)
    
    sign = '1'
    if number_str[0] == '-':
        sign = '0'
        number_str = number_str[1:]
    number_str, len_below1 = number_split(number_str, is_size)
    # clear 0s at the beginning
    offset = 0
    numberstrlen = len(number_str)
    while number_str[offset] == '0' and offset < numberstrlen - 1:
        offset += 1
    number_str = number_str[offset:]
    numberstrlen -= offset

    # refill 0s for hexa digits
    if numberstrlen % 4 == 0:
        delta_zero = 0
    else:
        delta_zero = 4 - numberstrlen % 4
    number_str = '0' * delta_zero + number_str

    # Hexa digits
    len_total = format(len(number_str) // 4, '03b')
    if is_size:
        ret = '0' + len_total + number_str
    else:
        ret = '0' + sign + len_total + len_below1 + number_str    
    return bin_to_seq(ret)

def str_to_seq(s):
    binary = ''
    if s == None:
        return 'G' + number_to_seq(0, True)
    byte = s.encode("utf-8")
    for ch in byte:
        tmp = bin(ch).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp
    return 'G' + number_to_seq(len(byte), True) + bin_to_seq(binary)
