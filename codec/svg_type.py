from .decode_attr_type import seq_to_number, seq_to_str
from .encode_attr_type import number_to_seq, str_to_seq
import re
from typing import Tuple
from .path_d import ParserPathD as dparser
from .transform import ParserTransform as trparser
from .svg_enum import EnumDict

class SVGType:
    def __init__(self, given_str: str, start_idx=0) -> None:
        self.given_str = given_str
        self.start_idx = start_idx
        
# 单个数字：'A'+数字对应编码
# 多个数字：'T'+数字个数(size_t)+数字1+数字2+...
class SVGNumber(SVGType):
    def __init__(self, given_str: str, start_idx=0) -> None:
        super().__init__(given_str, start_idx)

    def encode(self):
        value = self.given_str
        if value == None:
            return 'C'
        if type(value) != str:
            value = str(value)
        numbers = re.sub(',', ' ', value).strip().split(' ')
        
        if len(numbers) == 1:
            seq = 'A'
        else:
            seq = 'T' + number_to_seq(len(numbers))
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

    def decode(self):
        sub_seq = self.given_str[self.start_idx:]
        if sub_seq[0] == 'C':
            return None, self.start_idx + 1
        elif sub_seq[0] == 'A':
            ret, end_idx = seq_to_number(sub_seq[1:], self.start_idx)
            end_idx += 1
            return ret, end_idx
        elif sub_seq[0] == 'T':
            ret = []
            index = self.start_idx
            number_length, index = seq_to_number(sub_seq[1:], index + 1)
            for _ in range(0, number_length):
                number, index = seq_to_number(self.given_str[index:], index)
                ret.append(number)
            return (' '.join(str(i) for i in ret), index)
        else:
            print('error: invalid sequence')


class SVGString(SVGType):
    def __init__(self, given_str: str, start_idx=0) -> None:
        super().__init__(given_str, start_idx)

    def encode(self):
        return str_to_seq(self.given_str)

    def decode(self):
        return seq_to_str(self.given_str[self.start_idx:], self.start_idx)


class SVGEnum(SVGType):
    dict = EnumDict()
    def __init__(self, attr_name, given_str, start_idx=0) -> None:
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
    def __init__(self, given_str: str, start_idx=0) -> None:
        super().__init__(given_str, start_idx)

    def encode(self):
        return self.parser.encoder(self.given_str)
    
    def decode(self):
        return self.parser.decoder(self.given_str, self.start_idx)
    

class SVGTransform(SVGType):
    parser = trparser()
    def __init__(self, given_str: str, start_idx=0) -> None:
        super().__init__(given_str, start_idx)

    def encode(self):
        return self.parser.encoder(self.given_str)
    
    def decode(self):
        return self.parser.decoder(self.given_str, self.start_idx)