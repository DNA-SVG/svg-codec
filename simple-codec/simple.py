#!/usr/bin/python3

import re

CONST_PRIMER_LEN = 6
CONST_SEQ_MAX_LEN = 200
CONST_ECC_SEQ_LEN = 4*6

NT_BITS = {
    "A": "00",
    "T": "11",
    "C": "01",
    "G": "10"
};
BITS_NT = {}
for (k, v) in NT_BITS.items():
    BITS_NT[v] = k;


def split(long_seq, max_len):
    """
    Split a long seq into multiple ones within the max_len
    """
    data_len = max_len - CONST_PRIMER_LEN
    def num2nt(num):
        ret = ""
        while num > 0:
            ret += 'ATCG'[num % 4]
            num //= 4
        return (ret + "A" * CONST_PRIMER_LEN)[:CONST_PRIMER_LEN]
    return [(num2nt(i//data_len) + long_seq[i:i+data_len] + 'A'*CONST_ECC_SEQ_LEN)
            for i in range(0, len(long_seq), data_len) ]

def combine(data):
    def nt2num(nts):
        num = 0
        for nt in reversed(nts):
            num *= 4
            num += 'ATCG'.find(nt)
        return num
    kv = {}
    for s in data.split('\n'):
        num = nt2num(s[:CONST_PRIMER_LEN])
        kv[num] = s[CONST_PRIMER_LEN:-CONST_ECC_SEQ_LEN]
    combined = ""
    i = 0
    while i in kv.keys():
        combined += kv[i]
        i += 1
    return combined

def encode(data: bytes):
    """
    Convert a byte array to ATCGs.
    """
    s = ""
    for byte in data:
        binary = "{:08b}".format(byte)
        for twobit in re.findall('..?', binary):
            s += BITS_NT[twobit]
    return s


def decode(seq):
    """
    Convert ATCGS to a byte array.
    """
    assert len(seq) % 4 == 0
    binary = ""
    data = []
    for code in seq:
        binary += NT_BITS[code]
        if len(binary) == 8:
            data.append(int(binary, 2).to_bytes(1, byteorder='big'))
            binary = ""
    assert binary == ""
    return b''.join(data)


def encode_file(infile, outfile):
    with open(infile, "rb") as f:
        data = f.read()
    seq = encode(data)
    seq = "\n".join(split(seq, CONST_SEQ_MAX_LEN))
    with open(outfile, "w") as f:
        f.write(seq)

def decode_file(infile, outfile):
    with open(infile, "r") as f:
        seq = f.read()
    seq = combine(seq)
    data = decode(seq)
    with open(outfile, "wb") as f:
        f.write(data)
