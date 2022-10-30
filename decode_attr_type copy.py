import struct
import encode_attr_type as encoder

nt_dict = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}

def decode(seq: str):
    """传入一段恰编码一个值的DNA片段(否则可能有问题）"""
    """返回对应的值"""
    if seq[0] == 'A' or seq[0] == 'T':
        return seq_to_int(seq)
    elif seq[0] == 'C':
        return seq_to_float(seq)
    else:
        return seq_to_str(seq)

def seq_to_int(seq: str) -> int:
    if seq[0] == 'A':
        sign = 1
    else:
        sign = -1

    length = int(nt_dict[seq[1]] + nt_dict[seq[2]], 2)

    binary = ''
    for i in range(3, length + 3):
        binary += nt_dict[seq[i]]

    return sign * int(binary, 2)

def seq_to_float(seq: str) -> float:
    ba = bytearray()

    #逐字节读取
    for i in range(1, 17, 4):
        byte = ''
        for j in range(i, i + 4):
            byte += nt_dict[seq[j]]
        ba.append(int(byte, 2))

    return struct.unpack('>f', ba)[0]

def seq_to_str(seq: str) -> str:
    ba = bytearray()
    l_length = int(nt_dict[seq[1]] + nt_dict[seq[2]], 2)

    for i in range(l_length + 3, len(seq), 4):
        byte = ''
        for j in range(i, i + 4):
            byte += nt_dict[seq[j]]
        ba.append(int(byte, 2))

    return ba.decode(encoding='ascii')

if __name__ == '__main__':
    #测试用代码
    # print(decode(encoder.int_to_seq(2)))
    # print(decode(encoder.float_to_seq(1.0)))
    # print(decode(encoder.str_to_seq('aasdfasdh')))
    print(decode('GAAAA'))