from . import encode_svg as encode
from . import decode_svg as decode
from .segment import optimize, restore
import xml.etree.ElementTree as ET
import argparse


def encode_to_DNA(file):
    # 返回以seq列表
    tree = ET.parse(file)
    root = tree.getroot()
    DNAseq = encode.dfs(root, -1,1, 0)
    # b = "\n".join(a)
    return DNAseq


def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()
# save_to_file('test_output',b)

CONST_SEQ_MAX_LEN = 300
CONST_SEQ_MIN_LEN = 150

def regulate_normal_strands(seqs):
    '''
    对于长度正常的序列，为每个 seq 前面加个 A
    '''
    return ['A' + seq for seq in seqs]

def outputDNAseq(infile, outfile):
    # 传入需要encode的文件，输出decode的DNA
    DNAseq = encode_to_DNA(infile) # 得到DNAseq各tag的list

    normal_seq = [len(seq) >= CONST_SEQ_MIN_LEN and len(seq) <= CONST_SEQ_MAX_LEN
                  for seq in DNAseq]
    short_seq = [len(seq) < CONST_SEQ_MIN_LEN for seq for DNAseq]
    long_seq = [len(seq) > CONST_SEQ_MAX_LEN for seq for DNAseq]

    DNAseq = regulate_normal_strands(normal_seq) + \
        split_long_strands(long_seq) + \
        combine_short_strands(short_seq)

    DNAseq = "\n".join(DNAseq)
    save_to_file(outfile, DNAseq)

def decode_short_long_strands(seqs):
    decoded_seqs = []
    for seq in seqs:
        if seq[0] == 'A':
            # handle normal strands
            decode_seq.append(seq[1:])
        elif seq[0] == 'T':
            pass # TODO: handle long strands
        elif seq[0] == 'C':
            pass # TODO: handle short strands
        else:
            raise Error("Unexpected short-long encoding!")
    return decoded_seqs

def outputSVG(infile, outfile):
    # 传入DNAseq的txt文件 产生svg文件
    # 改为返回str
    with open(infile, 'r') as f:
        seq = f.read()

    DNAseq = seq.split('\n')
    # print(DNAseq, len(DNAseq))

    DNAseq = decode_short_long_strands(DNAseq)

    contents = decode.generate_svg(DNAseq)
    save_to_file(outfile, contents)
    

def svg_to_dna(xmlstr):
    # 传入str形式的xml文件 输出decode的DNAseq
    root = ET.fromstring(xmlstr)
    DNAseq = encode.dfs(root, -1, 1, 0)
    DNAseq = optimize(DNAseq)
    return '\n'.join(DNAseq)

def dna_to_svg(DNAseq):
    # 传入DNAseq的str 返回svg的字符串
    DNAseq = DNAseq.split('\n')
    DNAseq = restore(DNAseq)
    svg_str = decode.generate_svg(DNAseq)
    return svg_str


actions = {
    "encode": outputDNAseq,
    "decode": outputSVG
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="action to do:encode or decode?")
    parser.add_argument("infile", help="the input filename")
    parser.add_argument("outfile", help="the output filename")
    args = parser.parse_args()
    if args.action not in actions:
        parser.print_help()
    else:
        actions[args.action](args.infile, args.outfile)


if __name__ == "__main__":
    # file = 'C:\\Users\\ZZ\\Desktop\\DNA\\river.svg'

    file = '../building-construction-education-svgrepo-com.svg'
    # 不能重复，会影响编号
    # a = encode_to_DNA(file)
    # print(a)
    # b = '\n'.join(a)
    outputDNAseq(file, 'After_test2.txt')
    # c = outputSVGstr(b)
    # b=decode_svg.generate_svg(a)
    

    # main()
    outputSVG("After_test2.txt", '4.svg')


