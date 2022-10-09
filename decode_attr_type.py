import struct
import encode_attr_type as encoder

nt_dict = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}

def decode(seq: str):
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
    for i in range(length):
        binary += nt_dict[seq[i + 3]]
    return sign * int(binary, 2)

def seq_to_float(seq: str) -> float:
    ba = bytearray()
    for i in range(4):
        byte = ''
        for j in range(i*4, i*4 + 4):
            byte += nt_dict[seq[j + 1]]
        ba.append(int(byte, 2))
    return struct.unpack('>f', ba)[0]

def seq_to_str(seq: str) -> str:
    ba = bytearray()
    i = 1
    while True:
        byte = ''
        for j in range(i, i + 4):
            byte += nt_dict[seq[j]]
        if byte == '00000000':
            break
        ba.append(int(byte, 2))
        i += 4
    return ba.decode(encoding='ascii')

if __name__ == '__main__':
    #测试用代码
    print(decode(encoder.int_to_seq(45)))
    print(decode(encoder.float_to_seq(1.0)))
    print(decode(encoder.str_to_seq('acdf')))
