from .svg_type import SVGNumber
from .svg_tag import tag_nt

def get_merge(ret_list):
    ret_list[0] = format(ret_list[0], '06b') + SVGNumber(len(ret_list) - 1).encode()
    for i in range(1, len(ret_list)):
        ret_list[0] += SVGNumber(len(ret_list[i])).encode()
    return ''.join(ret_list)

def merge(strands):
    for i in range(len(strands)):
        strands[i] = [int(strands[i][:6], 2), strands[i][6:]]
    strands = sorted(strands, key=lambda x: x[0])
    ret = []
    tmp_list = strands[0]
    for i in range(1, len(strands)):
        if strands[i][0] == strands[i-1][0]:
            tmp_list.append(strands[i][1])
        else:
            ret.append(get_merge(tmp_list))
            tmp_list = strands[i]
    ret.append(get_merge(tmp_list))
    return ret

def split_str(strand):
    str_tag = strand[:6]
    strand = strand[6:]
    str_len, idx = SVGNumber(strand).decode(call_number=True)
    strand = strand[idx:]

    lens = []
    for _ in range(str_len):
        length, idx = SVGNumber(strand).decode(call_number=True)
        lens.append(length)
        strand = strand[idx:]
    
    ret = []
    for i in range(str_len):
        ret.append(str_tag + strand[:lens[i]])
        strand = strand[lens[i]:]
    
    return ret

def split(strands, reserve=None):
    ret = []
    have_style = True
    if reserve != None:
        reserve = reserve.split(',')
        if 'svg' not in reserve:
            reserve.append('svg')
        for i in range(len(reserve)):
            if reserve[i] == 'style':
                have_style = False
            reserve[i] = tag_nt().get_tag_nt(reserve[i])
        reserve.append('111111')
        for strand in strands:
            if strand[:6] in reserve:
                ret.append(strand)
        strands = ret.copy()
        ret = []
    for strand in strands:
        ret.extend(split_str(strand))
    return ret, have_style