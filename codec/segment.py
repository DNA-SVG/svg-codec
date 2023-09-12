from typing import List
from . import svg_code
from .svg_type import SVGNumber
CONST_NORMAL_IDN = 'A'
CONST_LONG_IDN = 'T'
CONST_SHORT_IDN = 'C'
CONST_SEQ_MIN_LEN = 100
CONST_SEQ_MAX_LEN = 2 * CONST_SEQ_MIN_LEN
CONST_TAG_SEQ_LEN = 3

def split_long_strands(strands: List[str]) -> List[str]:
    '''传入长链列表, 将每条长链拆分并打标记'''
    ret_strands = []
    for strand in strands:
        tail = len(strand) % CONST_SEQ_MAX_LEN
        addr = SVGNumber(str(svg_code.decode_address(strand[CONST_TAG_SEQ_LEN:])[0][0]), type='encoder').translate()
        # addr = strand[CONST_TAG_SEQ_LEN:svg_code.decode_address(strand[CONST_TAG_SEQ_LEN:])[1] + CONST_TAG_SEQ_LEN]
        l = len(strand)
        cnt = 0
        for i in range(0, l - tail - CONST_SEQ_MAX_LEN, CONST_SEQ_MAX_LEN):
            substrand = strand[i:i + CONST_SEQ_MAX_LEN]
            substrand = CONST_LONG_IDN + addr + SVGNumber(str(cnt), type='encoder').translate() + substrand
            cnt += 1
            ret_strands.append(substrand)

        if (tail >= CONST_SEQ_MIN_LEN):
            for i in range (l - tail - CONST_SEQ_MAX_LEN, l, CONST_SEQ_MAX_LEN):
                substrand = strand[i:i + CONST_SEQ_MAX_LEN]
                substrand = CONST_LONG_IDN + addr + SVGNumber(str(cnt), type='encoder').translate() + substrand
                cnt += 1
                ret_strands.append(substrand)
        else:
            cur_pos = l - tail - CONST_SEQ_MAX_LEN
            len_left2 = (tail + CONST_SEQ_MAX_LEN) // 2
            left2_1 = strand[cur_pos:cur_pos+len_left2]
            left2_1 = CONST_LONG_IDN + addr + SVGNumber(str(cnt), type='encoder').translate() + left2_1
            ret_strands.append(left2_1)

            left2_2 = strand[cur_pos+len_left2:]
            left2_2 = CONST_LONG_IDN + addr + SVGNumber(str(cnt+1), type='encoder').translate() + left2_2
            ret_strands.append(left2_2)

    return ret_strands

def merge_short_strands(strands: List[str]) -> List[str]:
    '''传入短链列表, 将合并短链并打标记'''
    ret_strands = []
    cur_strand = CONST_SHORT_IDN
    cur_valid_len = 0

    for strand in strands:
        l = len(strand)
        if cur_valid_len + l > CONST_SEQ_MAX_LEN:
            ret_strands.append(cur_strand)
            cur_strand = CONST_SHORT_IDN
            cur_valid_len = 0
        cur_strand += SVGNumber(str(l), type='encoder').translate() + strand
        cur_valid_len += l

    # 最后可能多出一条短链
    if len(cur_strand) > 1:
        ret_strands.append(cur_strand)

    return ret_strands
        

def restore_long_strands(strands: List[str]) -> List[str]:
    '''传入带'T'标记的长链列表'''
    '''返回长链合并后的链列表'''
    ret_strands = []
    addr_substrs = {}
    for strand in strands:
        addr, id_start_idx = SVGNumber(strand, type='decoder', start_idx=1).translate()
        id, content_start_idx = SVGNumber(strand, type='decoder', start_idx=id_start_idx).translate()
        if addr not in addr_substrs:
            addr_substrs[addr] = []
        addr_substrs[addr].append((int(id), strand[content_start_idx:]))
    
    for addr, substr_list in addr_substrs.items():
        substr_list.sort(key=lambda t:t[0])
        ret_strands.append(''.join(t[1] for t in substr_list))

    return ret_strands

def restore_short_strands(strands: List[str]) -> List[str]:
    '''传入带'C'标记的短链列表'''
    '''返回短链拆分后的链列表'''
    ret_strands = []
    for strand in strands:
        idx = 1
        while idx < len(strand):
            seq_len, seq_start_idx = SVGNumber(strand, type='decoder', start_idx=idx).translate()
            seq_end_idx = seq_start_idx + int(seq_len)
            ret_strands.append(strand[seq_start_idx:seq_end_idx])
            idx = seq_end_idx

    return ret_strands

def regulate_normal_strands(strands: List[str]) -> List[str]:
    return [CONST_NORMAL_IDN + strand for strand in strands]

def restore_normal_strands(strands: List[str]) -> List[str]:
    return [strand[1:] for strand in strands]

def optimize_seq_len(strands: List[str]) -> List[str]:
    long_strands = [strand for strand in strands if len(strand) > CONST_SEQ_MAX_LEN]
    short_strands = [strand for strand in strands if len(strand) < CONST_SEQ_MIN_LEN]
    normal_strands = [strand for strand in strands if CONST_SEQ_MIN_LEN <= len(strand) <= CONST_SEQ_MAX_LEN]

    return  regulate_normal_strands(normal_strands) + \
            split_long_strands(long_strands) + \
            merge_short_strands(short_strands)

def restore_seq_len(strands: List[str]) -> List[str]:
    long_strands = [strand for strand in strands if strand[0] == CONST_LONG_IDN]
    short_strands = [strand for strand in strands if strand[0] == CONST_SHORT_IDN]
    normal_strands = [strand for strand in strands if strand[0] == CONST_NORMAL_IDN]

    return  restore_normal_strands(normal_strands) + \
            restore_long_strands(long_strands) + \
            restore_short_strands(short_strands)
                   