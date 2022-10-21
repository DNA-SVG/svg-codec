from operator import length_hint
import decode_attr_type
decode_nt_dict = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}
decode_tag_dict = {'AA': "circle", 'AT': "g",  'AC': "path",
                   'AG': "polygon",  'TA': "rect", 'TT': "style"}

# 获取标签

# 目前存在的问题：id class 无法区别
def decode_idclass(seq: str, start=0):
    total_len = len(seq)
    ret = []
    if start < total_len:
        int_length = int(decode_nt_dict[seq[start+1]] +
                         decode_nt_dict[seq[start+2]], 2)
        int_end = start + 1 + 2 + int_length
        length = decode_attr_type.decode('A'+seq[start+1:int_end])
        end = start + 1 + 2 + int_length + length*4
        # print(type(start),type(end))
        ret += [decode_attr_type.decode(seq[start:end])]
        start = end
    else:
        return ret

    while start < total_len:
        int_length = int(
            decode_nt_dict[seq[start+1]] + decode_nt_dict[seq[start+2]], 2)
        int_end = start + 1 + 2 + int_length
        length = decode_attr_type.decode('A'+seq[start+1:int_end])
        end = start + 1 + 2 + int_length + length*4
        ret += [decode_attr_type.decode(seq[start:end])]
        start = end
    return ret


def decode_circle(seq: str):
    # total_len = len(seq)
    start = 0
    ret = []
    for i in range(3):
        end = start+1+16
        ret += [decode_attr_type.decode(seq[start:end])]
        start = end

    ret += decode_idclass(seq, start)
    return ret


def decode_g(seq: str):
    ret = []
    ret += decode_idclass(seq)
    return ret


def decode_path(seq: str, start=0):
    ret = []
    int_length = int(decode_nt_dict[seq[start+1]] +
                     decode_nt_dict[seq[start+2]], 2)
    int_end = start + 1 + 2 + int_length
    length = decode_attr_type.decode('A'+seq[start+1:int_end])
    end = start + 1 + 2 + int_length + length*4
    ret += [decode_attr_type.decode(seq[start:end])]
    start = end
    ret += decode_idclass(seq, start)
    return ret


def decode_polygon(seq: str, start=0):
    ret = []
    int_length = int(decode_nt_dict[seq[start+1]] +
                     decode_nt_dict[seq[start+2]], 2)
    int_end = start + 1 + 2 + int_length
    length = decode_attr_type.decode('A'+seq[start+1:int_end])
    end = start + 1 + 2 + int_length + length*4
    ret += [decode_attr_type.decode(seq[start:end])]
    start = end
    ret += decode_idclass(seq, start)
    return ret


def decode_rect(seq: str, start=0):
    for i in range(4):
        end = start+1+16
        ret += [decode_attr_type.decode(seq[start:end])]
        start = end
    ret += decode_idclass(seq, start)

    return ret


def decode_style(seq: str, start=0):
    ret = []
    int_length = int(decode_nt_dict[seq[start+1]] +
                     decode_nt_dict[seq[start+2]], 2)
    int_end = start + 1 + 2 + int_length
    length = decode_attr_type.decode('A'+seq[start+1:int_end])
    end = start + 1 + 2 + int_length + length*4
    ret += [decode_attr_type.decode(seq[start:end])]
    start = end
    ret += decode_idclass(seq, start)

    return ret


decode_func_dict = {"circle": decode_circle, "g": decode_g, "path": decode_path,
                    "polygon": decode_polygon, "rect": decode_rect, "style": decode_style}


def func_None(seq):
    print('无对应函数')


def func(x, seq):
    return decode_func_dict.get(x, func_None)(seq)


def DNAseq2tag(seq: str):
    tag = decode_tag_dict.get(seq[0:2])
    seq = seq[14:]
    DNAseq = [tag] + func(tag, seq)
    return DNAseq


if __name__ == '__main__':
    # seq = 'AA'+'CTAACAGTAAAAAAAAACTAAACCAAAAAAAAAACTAAACAAAAAAAAAAA' +\
    #     'GATCTGAGTGAG'
    # seq = 'AACTAACAAAAAAAAAAAACTAATGCGAGAGAGAGTCTAAACAGAGAGAGAGTGATGTGAGTGTAAGAA'
    # seq='AACTAACAAAAAAAAAAAACTAATGCGAGAGAGAGTCTAATGCGAGAGAGAGTCTAAACAGAGAGAGAGT'+\
    # 'GATGTGAGTGTAAGAA'
    # seq='ATGATGTGAGTGTAAGAA'
    # 加入编号后测试示例
    seq='AAAATATATTTATTCTAACAAAAAAAAAAAACTAATGCGAGAGAGAGTCTAAACAGAGAGAGAGTGATGTGAGTGTAAGAA'
    # print(decode_circle(seq))
    print(DNAseq2tag(seq))
