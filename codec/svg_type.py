from .decode_attr_type import seq_to_number, seq_to_str
from .encode_attr_type import number_to_seq, str_to_seq
import re
from .path_d import ParserPathD as dparser
from .transform import ParserTransform as trparser
from .svg_enum import EnumDict

class SVGType:
    def __init__(self, given_str: str, start_idx=0):
        self.given_str = given_str
        self.start_idx = start_idx
        
# 单个数字：'A'+数字对应编码
# 多个数字：'T'+数字个数(size_t)+数字1+数字2+...
class SVGNumber(SVGType):
    def __init__(self, given_str: str, start_idx=0):
        super().__init__(given_str, start_idx)

    def encode(self):
        value = self.given_str
        if value == None:
            return '00'
        if type(value) != str:
            value = str(value)
        numbers = re.sub(',', ' ', value).strip().split(' ')
        
        if len(numbers) == 1:
            seq = '01'
        else:
            seq = '1' + number_to_seq(len(numbers))
        for number in numbers:
            if number.startswith('.'):
                number = '0' + number
            number = re.sub(r"([^\d])(\.\d+)", r"\g<1>0\g<2>", number)
            if re.match(r'^[+-]?\d+(?:\.\d+)?(?:[eE][-+]\d+)?(px)?$', number) != None:
                if number.endswith('px'):
                    number = number[:-2]
                seq += number_to_seq(number)
            else:
                print('error: value type not supported')
        return seq

    def decode(self, call_number=False):
        sub_seq = self.given_str[self.start_idx:]
        if sub_seq[0] == '1':
            ret = []
            number_length, index = seq_to_number(sub_seq[1:], 1, True)
            for _ in range(0, number_length):
                number, index = seq_to_number(sub_seq[index:], index, call_number)
                ret.append(number)
            return (' '.join(ret), index + self.start_idx)
        elif sub_seq[1] == '1':
            ret, end_idx = seq_to_number(sub_seq[2:], self.start_idx, call_number)
            return ret, end_idx + 2
        else:
            return None, self.start_idx + 2


class SVGString(SVGType):
    def __init__(self, given_str: str, start_idx=0):
        super().__init__(given_str, start_idx)

    def encode(self):
        return str_to_seq(self.given_str)

    def decode(self):
        return seq_to_str(self.given_str[self.start_idx:], self.start_idx)


class SVGEnum(SVGType):
    dict = EnumDict()
    def __init__(self, attr_name, given_str, start_idx=0):
        self.attr_name = attr_name
        super().__init__(given_str, start_idx)

    def encode(self):
        result = self.dict.get_encode_dict(self.attr_name, self.given_str)
        if result != None:
            return result
        return 'G' + SVGString(self.given_str).encode()
    
    def decode(self):
        seq = self.given_str
        if seq[self.start_idx] == 'G':
            self.start_idx += 1
            return SVGString(seq, start_idx=self.start_idx).decode()
        return self.dict.get_decode_dict(self.attr_name, self.given_str, self.start_idx)
    

class SVGPathD(SVGType):
    parser = dparser()
    def __init__(self, given_str: str, start_idx=0):
        super().__init__(given_str, start_idx)

    def encode(self):
        return self.parser.encoder(self.given_str)
    
    def decode(self):
        return self.parser.decoder(self.given_str, self.start_idx)
    

class SVGTransform(SVGType):
    parser = trparser()
    def __init__(self, given_str: str, start_idx=0):
        super().__init__(given_str, start_idx)

    def encode(self):
        return self.parser.encoder(self.given_str)
    
    def decode(self):
        return self.parser.decoder(self.given_str, self.start_idx)

class SVGColorMatrix(SVGType):
    def __init__(self, given_str: str, start_idx=0):
        super().__init__(given_str, start_idx)

    def encode(self):
        numbers = re.split(r'\s+', self.given_str)
        ret_bin = ''
        ret_num = ''
        for number in numbers:
            if number == '0':
                ret_bin += '0'
            else:
                ret_bin += '1'
                ret_num += number_to_seq(number)
        return ret_bin + ret_num
    
    def decode(self):
        sub_seq = self.given_str[self.start_idx:]
        ret_bin = sub_seq[:20]
        ret_num = []
        index = 20
        for i in ret_bin:
            if i == '0':
                ret_num.append('0')
            else:
                number, index = seq_to_number(sub_seq[index:], index, call_number=False)
                ret_num.append(number)
        return  ''.join(ret_num), index + self.start_idx