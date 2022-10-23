#!/usr/bin/python3

import argparse
import re
import sys

NT_BITS = {
    "A": "00",
    "T": "11",
    "C": "01",
    "G": "10"
};
BITS_NT = {}
for (k, v) in NT_BITS.items():
    BITS_NT[v] = k;


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
    with open(outfile, "w") as f:
        f.write(seq)


def decode_file(infile, outfile):
    with open(infile, "r") as f:
        seq = f.read()
    data = decode(seq)
    with open(outfile, "wb") as f:
        f.write(data)


actions = {
    "encode": encode_file,
    "decode": decode_file
};

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="action to do")
    parser.add_argument("infile", help="the input filename")
    parser.add_argument("outfile", help="the output filename")
    args = parser.parse_args()
    if args.action not in actions:
        parser.print_help()
    else:
        actions[args.action](args.infile, args.outfile)

if __name__ == "__main__":
    main()

