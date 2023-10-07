import re
from .encode_attr_type import float_to_seq
from .decode_attr_type import decode as decode_float
class ParserPathD:
    nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
    param_table = {'z': 0, 'Z': 0, 'h': 1, 'H': 1, 'v': 1, 'V': 1, 'm': 2, 'M': 2, 'l': 2, 'L': 2, 't': 2, 'T': 2, 's': 4, 'S': 4, 'q': 4, 'Q': 4, 'c': 6, 'C': 6, 'a': 7, 'A': 7}
    dict_nt = {v:k for k, v in nt_dict.items()}

    def __bits_to_nt(self, str):
        length = len(str)
        if length % 2 == 1:
            str += '0'
        ret = ''
        for i in range(0, length, 2):
            ret += self.nt_dict[str[i:i+2]]
        return ret


    def __nt_to_bits(self, str, x):
        ret = ''
        for i in range(0, x):
            ret += self.dict_nt[str[i]]
        return ret


    def __encode_tag(self, tag):
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
        return self.__bits_to_nt(ret)


    def __decode_tag(self, str):
        str = self.__nt_to_bits(str, 3)
        upper = int(str[0])
        str = str[1:]
        offset = int(str, 2)

        ret = chr(offset + ord('a'))
        if upper != 0:
            ret = ret.upper()
        return ret


    def __encode_number(self, numbers):
        # ∵123.4567 = 1234567 * 0.1^4
        # ∴len_below1 = 4, 1234567 -> 0x12d687 -> len_total = 6
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

        # refill 0s for hexa digits
        delta_zero = 4 - ((numberstrlen - offset) % 4)
        for i in range(0, delta_zero):
            numberstr = '0' + numberstr

        # Hexa digits
        len_total = format(len(numberstr) // 4, '03b')
        ret = '0' + sign + len_total + len_below1 + numberstr
        return self.__bits_to_nt(ret)


    def __encode_object(self, str):
        # hardly uses float_to_seq
        length = len(str)
        if '-' in str:
            length -= 1
        if '.' in str:
            length -= 1
        if length <= 8:
            return self.__encode_number(str)
        else:
            return float_to_seq(float(str))


    def __decode_object(self, ntstr):
        # orders: 0 = use this codec(1 bit)
        # sign: 1 = +, 0 = -
        # ∵123.4567 = 1234567 * 0.1^4
        # ∴len_below1 = 4, 1234567 -> 0x12d687 -> len_total = 6
        orders = self.__nt_to_bits(ntstr, 4)
        if orders[0] == '1':
            return decode_float(ntstr[:17]), 17
        ntstr = ntstr[4:]
        sign = (orders[1] == '1')
        len_total = int(orders[2:5], 2)
        len_below1 = int(orders[5:8], 2)
        
        number_str = ''
        number_str += self.__nt_to_bits(ntstr, len_total * 2)
        ntstr = ntstr[len_total * 2:]
        num = int(number_str, 2)

        ret = str(num)
        if len_total == len_below1:
            ret = '0.' + ret
        elif len_below1 > 0:
            ret = ret[:-len_below1] + '.' + ret[-len_below1:]
        if not sign:
            ret = '-' + ret
        
        return ret, 4 + 2 * len_total


    def __encoder_single(self, data):
        code_tag = self.__encode_tag(data[0])
        number_tuple = re.findall(r"(-?\d+\.\d+)|(-?\d+)|(-?\.\d+)", data[1])
        number_list = []
        for first, second, third in number_tuple:
            number_list.append(first + second + third)

        ret = ''
        params = self.param_table[data[0]]
        if params == 0:
            return code_tag, 0
        
        # offset: if a command followed by N sets of params, then offset = N - 1
        offset = len(number_list) // params - 1
        for k in range(0, offset + 1):
            ret += code_tag
            for i in range(0, params):
                ret += self.__encode_object(number_list[i])
            number_list = number_list[params:]
        return ret, offset


    def __encoder_length(self, length):
        # number of commands in a path.d
        ret = format(length,'08b')
        return self.__bits_to_nt(ret)


    def __decoder_single(self, ntstr):
        ret = self.__decode_tag(ntstr[0:3])
        ntstr = ntstr[3:]
        times = self.param_table[ret]
        total_nts = 3
        datas = []
        for i in range(0, times):
            data_str, data_nts = self.__decode_object(ntstr)
            ntstr = ntstr[data_nts:]
            datas.append(data_str)
            total_nts += data_nts
        ret += ','.join(datas)
        return ret, total_nts


    def encoder(self, string):
        string = re.sub(' ',',',string)
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
            codec, offset_tag = self.__encoder_single(data)
            ret += codec
            leng += offset_tag
        return self.__encoder_length(leng) + ret


    def decoder(self, string):
        # get number of commands
        leng = int(self.__nt_to_bits(string, 4), 2)
        string = string[4:]

        ret = ''
        total_nts = 4
        for i in range(0, leng):
            decodec, nts = self.__decoder_single(string)
            ret += decodec
            string = string[nts:]
            total_nts += nts
        return ret, total_nts