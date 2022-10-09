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
    #获得字节信息
    bs = struct.pack('>f', num)

    #字节转01串
    binary = ''
    for i in bs:
        tmp = bin(i).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp

    return 'C' + bin_to_seq(binary)

def str_to_seq(s: str) -> str:
    binary = ''
    for ch in s:
        tmp = bin(ord(ch)).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp
    return 'G' + int_to_seq(len(s))[1:] + bin_to_seq(binary)

if __name__ == '__main__':
    #测试用代码
    s = 'ajlkadafld'
    n = len(s)
    print(int_to_seq(n), str_to_seq(s))