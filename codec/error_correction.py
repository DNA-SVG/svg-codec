from reedsolo import RSCodec, ReedSolomonError
from typing import List
from .svg_type import SVGNumber
import re
NT_BITS = {'A':'00', 'T':'01', 'C':'10', 'G':'11'}
BITS_NT = {v:k for k, v in NT_BITS.items()}
CONST_ECC_LEN = 4
rsc = RSCodec(CONST_ECC_LEN)

def seq_to_ba(strand: str) -> bytearray:
    ba = bytearray()
    cur_byte = ''
    for nt in strand:
        cur_byte += NT_BITS[nt]
        if len(cur_byte) == 8:
            ba.append(int(cur_byte, 2))
            cur_byte = ''
    return ba

def ba_to_seq(ba: bytearray) -> str:
    ret = ''
    for byte in ba:
        s = '{:08b}'.format(byte)
        for i in range(0, 8, 2):
            ret += BITS_NT[s[i:i+2]]
    return ret

def add_ecc(strands: List[str]) -> List[str]:
    ret_strands = []
    for strand in strands:
        strand = SVGNumber(str(len(strand)), type='encoder').translate() + strand
        if len(strand) % 4:
            strand += 'A' * (4 - len(strand) % 4)
        ba = seq_to_ba(strand)
        ecc = rsc.encode(ba)[-CONST_ECC_LEN:]
        strand += ba_to_seq(ecc)
        
        ret_strands.append(strand)
    return ret_strands

def error_check(strands: List[str]) -> List[str]:
    ret_strands = []
    for strand in strands:
        ba = seq_to_ba(strand)

        try:
            ba = rsc.decode(ba)[0]
        except ReedSolomonError:
            print('!')
            return []
        init_decode = ba_to_seq(ba)
        rlen, end_idx = SVGNumber(init_decode, type='decoder').translate()
        ret = init_decode[end_idx:end_idx+int(rlen)]
        ret_strands.append(ret)

    return ret_strands