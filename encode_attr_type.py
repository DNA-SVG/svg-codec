import struct

nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}

def bin_to_seq(binSeq: str) -> str:
    n = len(binSeq)
    if n % 2 == 1:
        binSeq = '0' + binSeq
        n += 1
    
    ret = ''
    for i in range(0, n, 2):
        unit = binSeq[i:i+2]
        ret += nt_dict[unit]

    return ret

def int_to_seq(num: int) -> str:
    binary = bin(num).replace('0b', '').replace('-', '')
    value = bin_to_seq(binary)

    if num >= 0:
        sign = 'A'
    else:
        sign = 'T'

    length = bin_to_seq(bin(len(value)).replace('0b', ''))
    if len(length) == 1:
        length = 'A' + length
        
    return sign + length + value

def float_to_seq(num: float) -> str:
    bs = struct.pack('>f', num)
    binary = ''
    for i in bs:
        tmp = bin(i).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp
    return 'C' + bin_to_seq(binary)

def str_to_seq(s: str) -> str:
    new_s = s + '\0'
    binary = ''
    for ch in new_s:
        tmp = bin(ord(ch)).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp
    return 'G' + bin_to_seq(binary)

if __name__ == '__main__':
    #测试用代码
    a, b = 12345, -12345
    c = 1.0
    d = 'c'
    print(int_to_seq(a), int_to_seq(b), float_to_seq(c), str_to_seq(d), sep=' ')