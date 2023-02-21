from . import decode_attr_type as decoder
from . import encode_attr_type as encoder
import re
from typing import Tuple

NT_BITS = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}
FLOAT_LENGTH = 16
TYPECODE_LENGTH = 1
INT_SIZE_LENGTH = 2
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
    def __init__(self, given_str: str, type='encoder', start_idx=0) -> None:
        super().__init__(given_str, type, start_idx)

    def encode(self) -> str:
        value = self.given_str
        numbers = value.strip().split(' ')
        if len(numbers) == 1:
            seq = 'A'
        else:
            seq = 'T' + encoder.int_to_seq(len(numbers))[1:]
        for number in numbers:
            if re.match(r'^[+-]?[0-9]*(\.)?[0-9]+(px)?$', number) != None:
                if number.endswith('px'):
                    number = number[:-2]
                eval_number = eval(number)
                if type(eval_number) == int:
                    seq += encoder.int_to_seq(eval_number)
                else:
                    seq += encoder.float_to_seq(eval_number)
            else:
                print('error: value type not supported')
        return seq

    def decode(self) -> Tuple[str, int]:
        sub_seq = self.given_str[self.start_idx:]
        if sub_seq[0] == 'A':
            if sub_seq[1] == 'C':
                end_idx = self.start_idx + 1 + TYPECODE_LENGTH + FLOAT_LENGTH
                ret = decoder.seq_to_float(
                    sub_seq[1:1 + TYPECODE_LENGTH + FLOAT_LENGTH])
            else:
                int_length = int(NT_BITS[sub_seq[2]] + NT_BITS[sub_seq[3]], 2)
                end_idx = self.start_idx + 1 + int_length + TYPECODE_LENGTH + INT_SIZE_LENGTH
                ret = decoder.seq_to_int(
                    sub_seq[1:1 + int_length + TYPECODE_LENGTH + INT_SIZE_LENGTH])
            return (str(ret), end_idx)
        elif sub_seq[0] == 'T':
            tot_int_length = int(NT_BITS[sub_seq[1]] + NT_BITS[sub_seq[2]], 2)
            tot = decoder.seq_to_int(
                'A' + sub_seq[1:tot_int_length + TYPECODE_LENGTH + INT_SIZE_LENGTH])
            ret = []
            idx = tot_int_length + TYPECODE_LENGTH + INT_SIZE_LENGTH
            for _ in range(tot):
                if sub_seq[idx] == 'C':
                    ret.append(decoder.seq_to_float(
                        sub_seq[idx:idx + TYPECODE_LENGTH + FLOAT_LENGTH]))
                    idx += TYPECODE_LENGTH + FLOAT_LENGTH
                else:
                    int_length = int(
                        NT_BITS[sub_seq[idx + 1]] + NT_BITS[sub_seq[idx + 2]], 2)
                    ret.append(decoder.decode(
                        sub_seq[idx:idx + int_length + TYPECODE_LENGTH + INT_SIZE_LENGTH]))
                    idx += int_length + TYPECODE_LENGTH + INT_SIZE_LENGTH
            end_idx = self.start_idx + idx
            return (' '.join(str(i) for i in ret), end_idx)
        else:
            print('error: invalid sequence')


class SVGString(SVGType):
    def __init__(self, given_str: str, type='encoder', start_idx=0) -> None:
        super().__init__(given_str, type, start_idx)

    def encode(self) -> str:
        value = self.given_str
        return encoder.str_to_seq(value)

    def decode(self) -> Tuple[str, int]:
        sub_seq = self.given_str[self.start_idx:]
        size_int_length = int(NT_BITS[sub_seq[1]] + NT_BITS[sub_seq[2]], 2)
        str_length = 4 * \
            decoder.seq_to_int(
                'A' + sub_seq[1:TYPECODE_LENGTH + INT_SIZE_LENGTH + size_int_length])
        tot_length = size_int_length + str_length + TYPECODE_LENGTH + INT_SIZE_LENGTH
        ret = decoder.seq_to_str(sub_seq[:tot_length])
        end_idx = self.start_idx + tot_length
        return (ret, end_idx)


class SVGCoordinate(SVGType):
    def __init__(self, given_str: str, type='encoder', start_idx=0) -> None:
        super().__init__(given_str, type, start_idx)

    def encode(self) -> str:
        value = self.given_str.replace(',', ' ')
        return SVGNumber(value, type='encoder').translate()

    def decode(self) -> Tuple[str, int]:
        init_decode, end_idx = SVGNumber(
            self.given_str, type='decoder', start_idx=self.start_idx).translate()
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

    def encode(self) -> str:
        seq = ''
        seq += self.encode_dict[self.attr_name][self.given_str]
        return seq 
    
    def decode(self) -> str:
        val = self.decode_dict[self.attr_name][self.given_str]
        end_idx = self.start_idx + len(self.given_str)
        return val, end_idx


if __name__ == '__main__':
    n = SVGCoordinate('0,1', type='encoder').translate()
    m = SVGCoordinate(n, type='decoder').translate()[0]
    print(m)
    n = SVGNumber('38.7px .5px 40.83284px 0px', type='encoder').translate()
    print(n)
    m, end = SVGNumber(n, type='decoder', start_idx=0).translate()
    print(m)
    s = SVGString('hello', type='encoder').translate()
    print(s)
    ss, end1 = SVGString(s, type='decoder', start_idx=0).translate()
    print(ss)
