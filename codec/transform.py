import re
from .encode_attr_type import number_to_seq
from .decode_attr_type import seq_to_number
class ParserTransform:
    encode_table = {'matrix': { 6: '0001'}, 'translate': { 1: '0010', 2: '0011'}, 'scale': { 1: '0100', 2: '0110'}, 'rotate':{ 1: '0111', 3: '1000'}, 'skewX': { 1: '1001'}, 'skewY': { 1: '1011'}}
    decode_table = {'0001': ('matrix', 6), '0010': ('translate', 1), '0011': ('translate', 2), '0100': ('scale', 1), '0110': ('scale', 2), '0111': ('rotate', 1), '1000': ('rotate', 3), '1001': ('skewX', 1), '1011': ('skewY', 1)}
    
    def __encoder_single(self, string):
        ret = re.split(r'\(|\)', string)
        params = re.split(r'[\s,]+', ret[1])
        length = len(params)
        seq = self.encode_table[ret[0]][length]
        for i in range(0, length):
            seq += number_to_seq(params[i])
        return seq
    
    def __decoder_single(self, seq):
        ret = self.decode_table[seq[:4]]
        seq = seq[4:]
        total_nts = 4
        params = []
        for _ in range(0, ret[1]):
            data, idx = seq_to_number(seq, 0, False)
            seq = seq[idx:]
            total_nts += idx
            params.append(str(data))
        return ret[0] + '(' + ','.join(params) + ')', total_nts

    def decoder(self, string, start_idx = 0):
        if start_idx > 0:
            string = string[start_idx:]
        leng, idx = seq_to_number(string, 0, True)
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