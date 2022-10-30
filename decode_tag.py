from operator import length_hint
import decode_attr_type
decode_nt_dict = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}
decode_tag_dict = {'AA': "circle", 'AT': "g",  'AC': "path",
                   'AG': "polygon",  'TA': "rect", 'TT': "style"}

# 获取标签


def decode_idclass(seq: str, start=0):
    tottal_len = len(seq)
    ret = []
    # print(start)
    if start >= tottal_len:
        return [None,None]
    if seq[start] == 'A':
        ret += [None, None]
        return ret
    if seq[start] == 'T':
        start += 1
        ret += [None]
        int_length = int(decode_nt_dict[seq[start+1]] +
                         decode_nt_dict[seq[start+2]], 2)
        int_end = start + 1 + 2 + int_length
        length = decode_attr_type.decode('A'+seq[start+1:int_end])
        end = start + 1 + 2 + int_length + length*4
        ret += [decode_attr_type.decode(seq[start:end])]
        return ret
    if seq[start] == 'C':
        start += 1
        int_length = int(decode_nt_dict[seq[start+1]] +
                         decode_nt_dict[seq[start+2]], 2)
        int_end = start + 1 + 2 + int_length
        length = decode_attr_type.decode('A'+seq[start+1:int_end])
        end = start + 1 + 2 + int_length + length*4
        ret += [decode_attr_type.decode(seq[start:end])]
        ret += [None]
        return ret
    if seq[start] == 'G':
        start += 1
        int_length = int(decode_nt_dict[seq[start+1]] +
                         decode_nt_dict[seq[start+2]], 2)
        int_end = start + 1 + 2 + int_length
        length = decode_attr_type.decode('A'+seq[start+1:int_end])
        end = start + 1 + 2 + int_length + length*4
        ret += [decode_attr_type.decode(seq[start:end])]
        start = end

        int_length = int(decode_nt_dict[seq[start+1]] +
                         decode_nt_dict[seq[start+2]], 2)
        int_end = start + 1 + 2 + int_length
        length = decode_attr_type.decode('A'+seq[start+1:int_end])
        end = start + 1 + 2 + int_length + length*4
        ret += [decode_attr_type.decode(seq[start:end])]
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
    ret = []
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


def decode_address(seq: str):
    '''传入以address开头的序列'''
    '''返回[my_counter, first_child, bro, len(address)]'''
    ret = []
    start = 0
    tot_length = 0
    for _ in range(3):
        int_length = int(decode_nt_dict[seq[start+1]] +
                         decode_nt_dict[seq[start+2]], 2)
        end = start + 3 + int_length
        tot_length += 3 + int_length
        cur_counter = decode_attr_type.decode(seq[start:end])
        if cur_counter == -1:
            ret.append(None)
        else:
            ret.append(cur_counter)
        start = end

    ret.append(tot_length)
    return ret


def DNAseq2tag(seq: str):
    '''传入编码一个tag的序列'''
    '''返回[tag, my_counter, first_child, bro, [attrs]]'''
    tag = decode_tag_dict.get(seq[0:2])
    my_counter, first_child, bro, addr_length = decode_address(seq[2:])
    seq = seq[2 + addr_length:]
    DNAseq = [tag, my_counter, first_child, bro] + func(tag, seq)
    return DNAseq


if __name__ == '__main__':

   
    # 编号长度不一定为12位！！！
    # seq = ['ATAATTAATCTATT', 'ATAATCTATTAATGGACGCTTGGTGCAAGAGAGTATTGGAGAAACGTTACTTCTATTGGTAAGTCATTGACTCTA', 'AAAATGTATTAACTACTAACAAAAAAAAAAAACTAATGCGAGAGAGAGTCTAAACAGAGAGAGAGTTGATGTGAGTGTAAGAA', 'TAAACTATATTAACTTCTAAAGGAAAAAAAAAACTAACAGTAAAAAAAAACTAAACAGAGAGAGAGTCTAATAAGAGAGAGAGTTGATGTGAGTGTAAGAT', 'AGAACTTTATTAACTCGAGTCGAGAGAGACACGAAGAGACGCAGTTACAAAGATAGTCACGCAGTCACGAAGATAGTCACGCAGAGACAAAGTAAGTGACGCAGTAACGAAGATAGTCACGCAGAGACAATGATGTGAGTGTAAGAT', 'ACAACTCTATTAACTGGTACTGCTAGTAGATAGACACGCAGATACGAAGACAGCAACGCAGTTTACAAGTGACGCAGTGTCAGACGTAGAAACGCAGTCACGAAGAAACGTAGATACGCAGATACGAAGAAACGCAGTTACGTAGATACGCAGATACGAAGATACGCAGATTGTCAGCAACGCAGCATCAGAGAAACGAAGAAACGCAGTCACGAAGAAACGCAGTTACGAAGATACGCAGATACGAAGATACGCAGATACGAAGATACGCAGATTCCAAGTAACGCAGTATCAGAGAAACGCAGTCACGAAGAAACGAAGATACGCAGATACGTAGAAACGCAGTTACGAAGATACGCAGATACGTAGATACGCAGATTGTCACGTAGCAACGCAGCAACAAACAAACAAACAAACAAACAATAAGAGATAGAGACGCAGACACGAAGACAGCAACGCAGCTACGAAGATAGACACGCAGTGACGAAGACAGCAACGCAGTTACGAAGATAGACACGCAGATACGAAGACAGCAACGCAGTTTGCCACAATAGTAGATAGATACGAAGAGAGTGACGCAGAGTACAAGCAACGCAGCATGTCACGTAGTCACGCAGTCTACAAGATAGATTTTCAGAGAGTGACGCAGAGTGCCTGATGTGAGTGTAAGAG', 'TTAACTGTATTTATTGTAGGTTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGAATGCGTCTCTCCTTCGATCGAAGCCACAGTATCTATCTATTTATTTAATAGCTAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGATTGCGTCTCTCCTTCGATCGAAGCCACAGTATAAGAGAGACAGTAAGAGAGTCAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGACTGCGTCTCTCCTTCGATCGAAGCCACAGAGCATATATATAAGATTATAAGAGAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGAGTGCGTCTCTCCTTCGATCGAAGCCACAGAGAGAGAGAGAATATAAGAAAGAAAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGTATGCGTCTCTCCTTCGATCGAAGCCTCGCTCGGTCGCTCTTAGCGTGAGTGTATGACTCGGTCCGTCTTAGCCACAGAGAGAGAGAGAATATAAGAAAGAAAGCGTGAGTGTATGACTCGGTCCGTCTTACGTTCGATCCTTCGCTCTTTCAGTCATTGAAAGCCTGACTCGGTGTTTCGCTCTAAGCGTGAGTGTATGACTCGGTCCGTCTTACGTTCGATCCTTCGCTCTTTCCCTCGGTCCTTCGCAGCCTGACTCGGTGTTTCGCTCTAAGCGTGAGTGTATGACTCGGTCCGTCTTACGTTCGTTCCTTGTATCTTTGACTCGATCCTTCGTTCCTTGTAAGCCAGATAGAAAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAA']
    # print(DNAseq2tag(seq[1]))
    a='ATAATTAATCTATTA'
    print(DNAseq2tag(a))
# element tree 构建xml
# js write
