import re, math
from decimal import Decimal
from .encode_attr_type import int_to_seq, float_to_seq, float_to_seq_sys
from .decode_attr_type import seq_to_number
class ParserPathD:
    param_table = {'z': 0, 'Z': 0, 'h': 1, 'H': 1, 'v': 1, 'V': 1, 'm': 2, 'M': 2, 'l': 2, 'L': 2, 't': 2, 'T': 2, 's': 4, 'S': 4, 'q': 4, 'Q': 4, 'c': 6, 'C': 6, 'a': 7, 'A': 7}
    subsequent_param = {'M': 'L', 'm': 'l'}
    nts = [4, 0, 2, 2, 2, 4, 4, 0]
    bits = [4, 0, 1, 2, 2, 3, 3, 0]
    float_array = []
    '''
    type:
    0 -- normal
    1~6 -- all exponents belongs to 1~6 types
    7 -- exists a number which base >= 1 << 30 or exponent < -6 or blank > 1
    '''
    type = 0
    '''
    offset: smallest exponent in the data
    '''
    offset_num = 0
    '''
    blank: only effective when type is 1~6
    0 -- no blank       e.g.: [-1, 0, 1, 2, 3]
    1 -- exists a blank e.g.: [-1, 0, 2, 3, 4] blank_num = 1
    '''
    blank = 0
    blank_num = 0

    def __encode_tag(self, tag):
        '''
        1 bit is a or A
        5 bit is a or z
        '''
        ret = ''
        if str.isupper(tag):
            ret = '1'
            tag = tag.lower()
        else:
            ret = '0'
        orddiff = ord(tag) - ord('a')
        ret += format(orddiff,'05b')
        return ret

    def __decode_tag(self, str):
        upper = int(str[0])
        str = str[1:]
        offset = int(str, 2)
        ret = chr(offset + ord('a'))
        if upper != 0:
            ret = ret.upper()
        return ret
    
    def __normalize(self, number_str):
        decimal = Decimal(number_str)
        if decimal == decimal.to_integral_value():
            value = decimal.quantize(Decimal(1))
            return True, value < 0, int(value), 0
        else:
            decimal = decimal.normalize()
            sign, digit_tuple, exponent = decimal.as_tuple()
            digits = int(''.join(map(str, digit_tuple)))
            return False, sign == 1, digits, exponent + len(digit_tuple) - 1

    def __get_type(self):
        '''
        DO NOT CHANGE THE ORDER OF THE FOLLOWING CODE
        '''
        self.type = len(self.float_array)
        if self.type == 0:
            return
        
        self.offset_num = min(self.float_array)
        if self.offset_num < -6:
            self.type = 7
            return
        if self.type > 6:
            self.type = 0
            return

        self.blank = max(self.float_array) - self.offset_num - self.type + 1       
        if self.blank > 1:
            self.type = 0
            self.blank = 0
            return
        elif self.blank == 1:
            for i in range(self.offset_num, self.offset_num + self.type):
                if i not in self.float_array:
                    self.blank_num = i
                    return
    
    def __get_exponent(self, exponent):
        if self.type == 0:
            return format(exponent + 6, '04b')
        if self.type == 1:
            return ''
        if self.blank == 1 and exponent > self.blank_num:
            exponent -= (self.offset_num + 1)
        else:
            exponent -= self.offset_num
        return format(exponent, '0' + str(self.bits[self.type]) + 'b')

    def __get_exp_nt_bit(self):
        return self.nts[self.type], self.bits[self.type]

    def __float_to_seq(self, sign, coefficient, exponent):
        if self.type == 7:
            exponent = exponent - int(math.log(coefficient, 10))
            if exponent < -6 or coefficient >= (1 << 30):
                number = coefficient * (10 ** exponent) * (-1 if sign else 1)
                return float_to_seq_sys(number)
            else:
                return float_to_seq(sign, coefficient, exponent)
        
        sign = '1' if sign else '0'
        exponent = self.__get_exponent(exponent)
        binary_number = format(coefficient, 'b')
        length_bin = len(binary_number)

        ret = exponent + binary_number
        if len(ret) & 1 != 0:
            binary_number = '0' + binary_number
            length_bin += 1
        length_bin >>= 1

        ret = sign + format(length_bin >> 1, '03b') + exponent + binary_number
        if length_bin & 1:
            return '01' + ret
        else:
            return '10' + ret
        
    def __seq_to_float(self, seq):
        length_nt = 1 if seq[0] == '0' else 0
        seq = seq[2:]
        params = seq[:4]
        seq = seq[4:]
        sign = int(params[0])
        length_nt += int(params[1:], 2) << 1
        length_nt <<= 1
        exp_nt, exp_bit = self.__get_exp_nt_bit()
        
        if self.type == 0:
            exponent = int(seq[:4], 2) - 6
            seq = seq[4:]
            value = str(int(seq[:length_nt], 2))
            value = ('-' if sign == 1 else '') \
                    + value[0] + '.' + value[1:] \
                    + 'e' + str(exponent)
        else:
            value = seq[:length_nt + exp_nt]
            exponent = self.offset_num
            if exp_bit > 0:
                exponent += int(value[:exp_bit], 2)
            if self.blank and self.blank_num <= exponent:
                exponent += 1
            value = str(int(value[exp_bit:], 2))
            value = value[0] + '.' + value[1:]
            value = ('-' if sign == 1 else '') \
                    + value \
                    + 'e' + str(exponent)
        return str(Decimal(value).normalize()), length_nt + exp_nt + 6

    def __generate_list(self, data):
        data[1] = re.sub(r"([^\d])(\.\d+)", r"\g<1>0\g<2>", data[1])
        number_list = []
        while True:
            if data[1].startswith('.'):
                data[1] = '0' + data[1]
            number = re.search(r"-?\d+(?:\.\d+)?(?:[eE][-+]\d+)?", data[1])
            if number == None:
                break
            number_list.append(number.group())
            data[1] = data[1][number.end():]       

        for i in range(0, len(number_list)):
            is_int, _, digits, exponent = number_list[i] = self.__normalize(number_list[i])
            if is_int:
                continue
            if digits >= (1 << 30):
                self.type = 7
            if exponent not in self.float_array:
                self.float_array.append(exponent)
        
        ret = []
        params = self.param_table[data[0]]
        # offset: if a command followed by N sets of params, then offset = N - 1
        if params == 0:
            offset = 0
        else:
            offset = len(number_list) // params - 1
        for i in range(0, offset + 1):
            if params == 0:
                ret.append([data[0]])
            else:
                if i > 0 and data[0] in self.subsequent_param:
                    ret.append([self.subsequent_param[data[0]]] + number_list[0:params])
                else:
                    ret.append([data[0]] + number_list[0:params])
                number_list = number_list[params:]
        return ret

    def encoder(self, string):
        string = re.sub(r'\s+', ',', string)
        tag_list = re.findall(r"[a-df-zA-DF-Z]", string)
        data_list = re.findall(r"[^a-df-zA-DF-Z\s]+", string)
        for data in data_list:
            if data == ',':
                data_list.remove(data)
        b = []
        offset = 0
        for i in range(0, len(tag_list)):
            b.append([])
            b[i].append(tag_list[i])
            if tag_list[i] == 'z' or tag_list[i] == 'Z':
                b[i].append('')
                offset += 1
            else:
                b[i].append(data_list[i - offset])
        data_list = []
        for data in b:
            data_list += self.__generate_list(data)

        if self.type < 7:
            self.__get_type()
            
        ret = int_to_seq(False, len(data_list)) \
            + format(self.type * 2 + self.blank, '04b')
        if self.type > 0 and self.type < 7:
            ret += format(self.offset_num + 6, '04b')
            if self.blank == 1:
                ret += format(self.blank_num + 6, '04b')
        
        for item in data_list:
            subret = self.__encode_tag(item[0])
            itemlen = len(item)
            if itemlen == 1:
                ret += subret
                continue
            for i in range(1, itemlen):
                if item[i][0]:
                    subret += int_to_seq(item[i][1], item[i][2])
                else:
                    subret += self.__float_to_seq(item[i][1], item[i][2], item[i][3])
            ret += subret
        return ret

    def decoder(self, seq, start_idx = 0):
        length, idx = seq_to_number(seq, start_idx, True)
        seq = seq[idx:]
        type_bin = int(seq[:4], 2)
        seq = seq[4:]
        idx += 4
        self.type = type_bin >> 1
        self.blank = type_bin & 1
        if self.type > 0 and self.type < 7:
            self.offset_num = int(seq[:4], 2) - 6
            seq = seq[4:]
            idx += 4
            if self.blank == 1:
                self.blank_num = int(seq[:4], 2) - 6
                seq = seq[4:]
                idx += 2
    
        ret = ''
        for _ in range(0, length):
            tag = self.__decode_tag(seq[0:6])
            seq = seq[6:]
            params = self.param_table[tag]
            idx += 6
            data = []

            for _ in range(0, params):
                if seq[0] == seq[1] or self.type == 7:
                    data_str, data_nts = seq_to_number(seq, 0, False)
                else:
                    data_str, data_nts = self.__seq_to_float(seq)
                seq = seq[data_nts:]
                idx += data_nts
                data.append(data_str)
            ret += tag + ','.join(data)
            
        return ret, idx