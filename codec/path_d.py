import re
from .encode_attr_type import number_to_seq, bin_to_seq
from .decode_attr_type import decode, seq_to_bin
class ParserPathD:
    nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
    param_table = {'z': 0, 'Z': 0, 'h': 1, 'H': 1, 'v': 1, 'V': 1, 'm': 2, 'M': 2, 'l': 2, 'L': 2, 't': 2, 'T': 2, 's': 4, 'S': 4, 'q': 4, 'Q': 4, 'c': 6, 'C': 6, 'a': 7, 'A': 7}
    dict_nt = {v:k for k, v in nt_dict.items()}

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
        return bin_to_seq(ret)

    def __decode_tag(self, str):
        str = seq_to_bin(str, 3)
        upper = int(str[0])
        str = str[1:]
        offset = int(str, 2)
        ret = chr(offset + ord('a'))
        if upper != 0:
            ret = ret.upper()
        return ret

    def __encoder_single(self, data):
        code_tag = self.__encode_tag(data[0])
        if data[1].startswith('.'):
            data[1] = '0' + data[1]
        data[1] = re.sub(r"([^\d])(\.\d+)", r"\g<1>0\g<2>", data[1])
        number_list = re.findall(r"-?\d+(?:\.\d+)?(?:[eE][-+]\d+)?", data[1])
        ret = ''
        params = self.param_table[data[0]]
        if params == 0:
            return code_tag, 0 
        # offset: if a command followed by N sets of params, then offset = N - 1
        offset = len(number_list) // params - 1
        for _ in range(0, offset + 1):
            ret += code_tag
            for i in range(0, params):
                ret += number_to_seq(number_list[i])
            number_list = number_list[params:]
        return ret, offset

    def __decoder_single(self, ntstr):
        ret = self.__decode_tag(ntstr[0:3])
        ntstr = ntstr[3:]
        times = self.param_table[ret]
        total_nts = 3
        datas = []
        for _ in range(0, times):
            data_str, data_nts = decode(ntstr, 0)
            ntstr = ntstr[data_nts:]
            datas.append(data_str)
            total_nts += data_nts
        ret += ','.join(datas)
        return ret, total_nts

    def encoder(self, string):
        string = re.sub(r'\s+', ' ', string)
        tag_list = re.findall(r"[a-df-zA-DF-Z]", string)
        data_list = re.findall(r"[^a-df-zA-DF-Z\s]+", string)
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
        return number_to_seq(leng, True) + ret

    def decoder(self, string, start_idx = 0):
        # get number of commands
        leng, idx = decode(string, start_idx, is_size=True)
        string = string[idx:]
        ret = ''
        for _ in range(0, leng):
            decodec, nts = self.__decoder_single(string)
            ret += decodec
            string = string[nts:]
            idx += nts
        return ret, idx