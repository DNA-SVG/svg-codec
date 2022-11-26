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
    """传入一个有符号整数，需满足|x| <= 2^30 - 1"""
    """以str形式返回编码dna序列"""
    binary = bin(num).replace('0b', '').replace('-', '')
    value = bin_to_seq(binary)

    if num >= 0:
        sign = 'A'
    else:
        sign = 'T'

    length = bin_to_seq(bin(len(value)).replace('0b', ''))
    if len(length) == 1:
        length = 'A' + length
        
    return sign + length +value

def float_to_seq(num: float) -> str:
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

def str_to_seq(s: str) -> str:
    binary = ''
    if s==None:
        return 'G'+int_to_seq(0)[1:]
    s = s.encode("utf-8")
    for ch in s:
        tmp = bin(ch).replace('0b', '')
        binary += '0' * (8 - len(tmp)) + tmp
    return 'G' + int_to_seq(len(s))[1:] + bin_to_seq(binary)

if __name__ == '__main__':
    #测试用代码，本地随便改
    s = ''
    n = len(s)
    print(int_to_seq(-1))
    # print(float_to_seq(45.0))
    print(str_to_seq('_x34_0-Id_Card'))