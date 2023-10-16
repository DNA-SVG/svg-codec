from . import decode_attr_type as decoder
from . import encode_attr_type as encoder
import re
from typing import Tuple
from .path_d import ParserPathD as dparser

NT_BITS = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}
# 2020/11/8 封装SVGNumber类和SVGString类


class SVGType:
    def __init__(self, given_str: str, type='encoder', start_idx=0) -> None:
        self.given_str = given_str
        self.start_idx = start_idx
        self.type = type

    def encode(self) -> str:
        pass

    def decode(self) -> Tuple[str, int]:
        pass

    def translate(self):
        if self.type == 'encoder':
            return self.encode()
        elif self.type == 'decoder':
            return self.decode()
        else:
            print('error: wrong codec type')


# 单个数字：'A'+数字对应编码
# 多个数字：'T'+数字个数(size_t)+数字1+数字2+...
class SVGNumber(SVGType):
    def __init__(self, given_str: str, type='encoder', start_idx=0, is_size=False) -> None:
        self.is_size = is_size
        super().__init__(given_str, type, start_idx)

    def encode(self):
        value = self.given_str
        if type(value) != str:
            value = str(value)
        numbers = value.strip().split(' ')
        
        if len(numbers) == 1:
            seq = 'A'
        else:
            seq = 'T' + encoder.number_to_seq(len(numbers), True)
        for number in numbers:
            if re.match(r'^[+-]?[0-9]*(\.)?[0-9]+(px)?$', number) != None:
                if number.endswith('px'):
                    number = number[:-2]
                seq += encoder.number_to_seq(number, is_size=self.is_size)
            else:
                print('error: value type not supported')
        return seq

    def decode(self):
        sub_seq = self.given_str[self.start_idx:]
        if sub_seq[0] == 'A':
            ret, end_idx = decoder.decode(sub_seq[1:], self.start_idx + 1, self.is_size)
            return ret, end_idx
        elif sub_seq[0] == 'T':
            ret = []
            index = self.start_idx
            number_length, index = decoder.decode(sub_seq[1:], index + 1, True)
            for _ in range(0, number_length):
                number, index = decoder.decode(self.given_str[index:], index, self.is_size)
                ret.append(number)
            return (' '.join(str(i) for i in ret), index)
        else:
            print('error: invalid sequence')


class SVGString(SVGType):
    def __init__(self, given_str: str, type='encoder', start_idx=0) -> None:
        super().__init__(given_str, type, start_idx)

    def encode(self):
        return encoder.str_to_seq(self.given_str)

    def decode(self):
        return decoder.decode(self.given_str[self.start_idx:], self.start_idx)


class SVGCoordinate(SVGType):
    def __init__(self, given_str: str, type='encoder', start_idx=0) -> None:
        super().__init__(given_str, type, start_idx)

    def encode(self):
        value = self.given_str.replace(',', ' ')
        return SVGNumber(value, type='encoder').translate()

    def decode(self):
        init_decode, end_idx = SVGNumber(self.given_str, type='decoder', start_idx=self.start_idx).translate()
        start, end = 0, len(init_decode)
        while start < end:
            start = init_decode.find(' ', start, end)
            init_decode = init_decode[:start] + ',' + init_decode[start + 1:]
            start += 1
            start = init_decode.find(' ', start, end)
            if start == -1:
                break
            start += 1
        return (init_decode, end_idx)


class SVGEnum(SVGType):
    encode_dict = {}
    encode_dict['filterUnits'] = {'userSpaceOnUse ': 'A', 'objectBoundingBox': 'T'}
    encode_dict['primitiveUnits'] = {
        'userSpaceOnUse': 'A', 'objectBoundingBox': 'T'}
    encode_dict['gradientUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'T'}
    encode_dict['spreadMethod'] = {'pad': 'A', 'reflect': 'T', 'repeat': 'C'}
    encode_dict['in'] = {'SourceGraphic': 'AA', 'SourceAlpha': 'AT', 'BackgroundImage': 'AC',
                    'BackgroundAlpha': 'AG', 'FillPaint': 'TA', 'StrokePaint': 'TT', '<filter-primitive-reference>': 'TC'}
    encode_dict['in2'] = {'SourceGraphic': 'AA', 'SourceAlpha': 'AT', 'BackgroundImage': 'AC',
                     'BackgroundAlpha': 'AG', 'FillPaint': 'TA', 'StrokePaint': 'TT', '<filter-primitive-reference>': 'TC'}
    encode_dict['operator'] = {'over': 'AA', 'in': 'AT', 'out': 'AC',
                          'atop': 'AG', 'xor': 'TA', 'lighter': 'TT', 'arithmetic': 'TC'}
    decode_dict = {}
    for t in encode_dict:
        decode_dict[t] = {v: k for k, v in encode_dict[t].items()}

    def __init__(self, attr_name, given_str: str, type='encoder', start_idx=0) -> None:
        self.attr_name = attr_name
        super().__init__(given_str, type, start_idx)

    def encode(self):
        seq = ''
        seq += self.encode_dict[self.attr_name][self.given_str]
        return seq 
    
    def decode(self):
        val = self.decode_dict[self.attr_name][self.given_str]
        end_idx = self.start_idx + len(self.given_str)
        return val, end_idx
    

class SVGPathD(SVGType):
    parser = dparser()
    def __init__(self, given_str: str, type='encoder', start_idx=0) -> None:
        super().__init__(given_str, type, start_idx)

    def encode(self):
        return self.parser.encoder(self.given_str)
    
    def decode(self):
        return self.parser.decoder(self.given_str, self.start_idx)