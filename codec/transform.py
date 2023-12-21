import re
from .encode_attr_type import number_to_seq
from .decode_attr_type import seq_to_number
class ParserTransform:
    encode_table = {'matrix': { 6: 'AA'}, 'translate': { 1: 'AT', 2: 'AC'}, 'scale': { 1: 'AG', 2: 'TA'}, 'rotate':{ 1: 'TT', 3: 'TC'}, 'skewX': { 1: 'TG'}, 'skewY': { 1: 'CA'}}
    decode_table = {'AA': ('matrix', 6), 'AT': ('translate', 1), 'AC': ('translate', 2), 'AG': ('scale', 1), 'TA': ('scale', 2), 'TT': ('rotate', 1), 'TC': ('rotate', 3), 'TG': ('skewX', 1), 'CA': ('skewY', 1)}
    
    def __encoder_single(self, string):
        ret = re.split(r'\(|\)', string)
        params = re.split(r'[\s,]+', ret[1])
        length = len(params)
        seq = self.encode_table[ret[0]][length]
        for i in range(0, length):
            seq += number_to_seq(params[i])
        return seq
    
    def __decoder_single(self, seq):
        ret = self.decode_table[seq[0:2]]
        seq = seq[2:]
        total_nts = 2
        params = []
        for _ in range(0, ret[1]):
            data, idx = seq_to_number(seq, 0)
            seq = seq[idx:]
            total_nts += idx
            params.append(str(data))
        return ret[0] + '(' + ','.join(params) + ')', total_nts

    def decoder(self, string, start_idx = 0):
        if start_idx > 0:
            string = string[start_idx:]
        leng, idx = seq_to_number(string, start_idx)
        string = string[idx:]
        ret = ''
        for _ in range(0, leng):
            decodec, nts = self.__decoder_single(string)
            ret += decodec
            string = string[nts:]
            idx += nts
        return ret, idx

    def encoder(self, string):
        commands = re.findall(r'[a-zA-Z]+\(.*?\)', string)
        seq = ''
        for command in commands:
            seq += self.__encoder_single(command)
        return number_to_seq(len(commands)) + seq