from . import encode_svg as encode
from . import decode_svg as decode
from .segment import optimize, restore
import xml.etree.ElementTree as ET
import argparse

def svg_to_dna(xml_str: str, optimize_option: bool=True) -> str:
    # 传入str形式的xml文件 输出decode的DNAseq
    root = ET.fromstring(xml_str)
    DNAseq = encode.dfs(root, -1, 1, 0)
    if optimize_option:
        DNAseq = optimize(DNAseq)
    return '\n'.join(DNAseq)

def dna_to_svg(seq_str: str, optimize_option: bool=True) -> str:
    # 传入DNAseq的str 返回svg文件字符串
    seq_str = seq_str.split('\n')
    if optimize_option:
        seq_str = restore(seq_str)
    svg_str = decode.generate_svg(seq_str)
    return svg_str


def outputDNAseq(infile, outfile):
    # 传入需要encode的文件，输出decode的DNA
    with open(infile, 'r') as f:
        dna = svg_to_dna(f.read())
    with open(outfile, 'w') as f:
        f.write(dna)


def outputSVG(infile, outfile):
    # 传入DNAseq的txt文件 产生svg文件
    # 改为返回str
    with open(infile, 'r') as f:
        svg = dna_to_svg(f.read())
    with open(outfile, 'w') as f:
        f.write(svg)

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


