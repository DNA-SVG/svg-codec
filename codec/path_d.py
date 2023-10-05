import cProfile
import re
from codec.encode_attr_type import float_to_seq
nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
param_table = {'z': 0, 'Z': 0, 'h': 1, 'H': 1, 'v': 1, 'V': 1, 'm': 2, 'M': 2, 'l': 2, 'L': 2, 't': 2, 'T': 2, 's': 4, 'S': 4, 'q': 4, 'Q': 4, 'c': 6, 'C': 6, 'a': 7, 'A': 7}

dict_nt = {v:k for k, v in nt_dict.items()}


def bits_to_nt(str):
    length = len(str)
    if length % 2 == 1:
        str += '0'
    ret = ''
    for i in range(0, length, 2):
        ret += nt_dict[str[i:i+2]]
    return ret


def nt_to_bits(str, x):
    ret = ''
    for i in range(0, x):
        ret += dict_nt[str[i]]
    return ret


def encode_tag(tag):
    # 1 bit is a or A
    # 5 bit is a or z
    ret = ''
    if str.isupper(tag):
        ret = '1'
        tag = tag.lower()
    else:
        ret = '0'

    orddiff = ord(tag) - ord('a')
    ret += format(orddiff,'05b')
    return bits_to_nt(ret)


def decode_tag(str):
    str = nt_to_bits(str, 3)
    upper = int(str[0])
    str = str[1:]
    offset = int(str, 2)

    ret = chr(offset + ord('a'))
    if upper != 0:
        ret = ret.upper()
    return ret


def get_codec(numbers):
    # 123.4567 = 1234567 * 0.1^4
    # len_below1 = 4, 1234567 -> 0x12d687 -> len_total = 6
    sign = '1'
    if numbers[0] == '-':
        sign = '0'
        numbers = numbers[1:]
    
    len_below1 = ''
    decs = str.split(numbers, '.')
    if len(decs) > 1:
        len_below1 = format(len(decs[1]),'03b')
    else:
        len_below1 = '000'

    numberstr = format(int(''.join(decs), 10), 'b')

    # clear 0s at the beginning
    offset = 0
    numberstrlen = len(numberstr)
    while numberstr[offset] == '0' and offset < numberstrlen - 1:
        offset += 1
    numberstr = numberstr[offset:]

    # supplement 0s for hexa digits
    delta_zero = 4 - ((numberstrlen - offset) % 4)
    for i in range(0, delta_zero):
        numberstr = '0' + numberstr

    # Hexa digits
    len_total = format(len(numberstr) // 4, '03b')
    ret = '0' + sign + len_total + len_below1 + numberstr
    return bits_to_nt(ret)


def encode_less(str):
    # hardly uses float_to_seq
    length = len(str)
    if '-' in str:
        length -= 1
    if '.' in str:
        length -= 1
    if length <= 8:
        return get_codec(str)
    else:
        return float_to_seq(float(str))


def decode_less(ntstr):
    # orders: 0 = use this codec(1 bit)
    # sign: 1 = +, 0 = -
    # 123.4567 = 1234567 * 0.1^4
    # len_below1 = 4, 1234567 -> 0x12d687 -> len_total = 6
    orders = nt_to_bits(ntstr, 4)
    ntstr = ntstr[4:]
    if orders[0] == '1':
        return
    sign = (orders[1] == '1')
    len_total = int(orders[2:5], 2)
    len_below1 = int(orders[5:8], 2)
    
    number_str = ''
    number_str += nt_to_bits(ntstr, len_total * 2)
    ntstr = ntstr[len_total * 2:]
    num = int(number_str, 2)
    if not sign:
        num = -num
    
    ret = str(num)
    if len_total == len_below1:
        ret = '0.' + ret
    elif len_below1 > 0:
        ret = ret[:-len_below1] + '.' + ret[-len_below1:]
    return ret, 4 + 2 * len_total


def parser_single(data):
    code_tag = encode_tag(data[0])
    number_tuple = re.findall(r"(-?\d+\.\d+)|(-?\d+)|(-?\.\d+)", data[1])
    number_list = []
    for first, second, third in number_tuple:
        number_list.append(first + second + third)

    ret = ''
    params = param_table[data[0]]
    if params == 0:
        return code_tag, 0
    
    # offset: if a command followed by 2 sets of params, then offset = 1
    offset = len(number_list) // params - 1
    while len(number_list) > 0:
        ret += code_tag
        for i in range(0, params):
            ret += encode_less(number_list[i])
        number_list = number_list[params:]
    return ret, offset


def parser_length(length):
    # number of commands in a path.d
    ret = format(length,'08b')
    return bits_to_nt(ret)


def decode_single(ntstr):
    ret = decode_tag(ntstr[0:3])
    ntstr = ntstr[3:]
    times = param_table[ret]
    total_nts = 3
    datas = []
    for i in range(0, times):
        data_str, data_nts = decode_less(ntstr)
        ntstr = ntstr[data_nts:]
        datas.append(data_str)
        total_nts += data_nts
    ret += ','.join(datas)
    return ret, total_nts


def parser(string):
    tag_list = re.findall(r"[a-zA-Z]", string)
    data_list = re.findall(r"[^a-zA-Z\s]+", string)
    leng = len(tag_list)
    b = []
    offset = 0
    for i in range(0, leng):
        b.append([])
        b[i].append(tag_list[i])
        if tag_list[i] == 'z' or tag_list[i] == 'Z':
            b[i].append('')
            offset += 1
        else:
            b[i].append(data_list[i - offset])
    ret = ''
    for data in b:
        codec, offset_tag = parser_single(data)
        ret += codec
        leng += offset_tag
    return parser_length(leng) + ret


def decoder(string):
    # get number of commands
    leng = int(nt_to_bits(string, 4), 2)
    string = string[4:]

    ret = ''
    total_nts = 4
    for i in range(0, leng):
        decodec, nts = decode_single(string)
        ret += decodec
        string = string[nts:]
        total_nts += nts
    return ret, total_nts


def test():
    string = 'M39.7,27.6c0-4.3-3.5-7.7-7.7-7.7s-7.7,3.5-7.7,7.7c0,2.4,1.1,4.5,2.8,5.9c-4.2,1.2-7.3,5-7.3,9.5c0,0.6,0.5,1.1,1.1,1.1H43c0.6,0,1.1-0.5,1.1-1.1c0-4.5-3.1-8.3-7.3-9.5C38.6,32.1,39.7,30,39.7,27.6z M26.5,27.6c0-3,2.5-5.5,5.5-5.5s5.5,2.5,5.5,5.5S35,33.1,32,33.1S26.5,30.6,26.5,27.6z M34.2,35.3c3.9,0,7.1,2.9,7.7,6.6H22.1c0.5-3.7,3.8-6.6,7.7-6.6H34.2z'
    codec = parser(string)
    print(len(codec), 'nts,','{:.2f}'.format(len(string) * 8 / len(codec)), 'bits/nt')
    ret, _ = decoder(codec)
    # print(ret)


if __name__ == "__main__":
    # cProfile.run('test()')
    test()