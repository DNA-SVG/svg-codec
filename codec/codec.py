from . import encode_svg as encoder
from . import decode_svg as decoder
from .segment import optimize_seq_len, restore_seq_len
from .error_correction import add_ecc, check_restore
import xml.etree.ElementTree as ET
import argparse

def svg_to_dna(xml_str: str, optimize: bool=True) -> str:
    # 传入str形式的xml文件 输出decode的DNAseq
    root = ET.fromstring(xml_str)
    encoder.init_counter()
    DNAseq = encoder.dfs(root, -1, 1, 0)
    if optimize:
        DNAseq = optimize_seq_len(DNAseq)
        DNAseq = add_ecc(DNAseq)
    return '\n'.join(DNAseq)

def dna_to_svg(seq_str: str, optimize: bool=True) -> str:
    # 传入DNAseq的str 返回svg文件字符串
    seq_list = seq_str.split('\n')
    if optimize:
        seq_list = check_restore(seq_list)
        seq_list = restore_seq_len(seq_list)

    svg_str = decoder.generate_svg(seq_list)
    return svg_str


def outputDNAseq(infile, outfile):
    # 传入需要encode的文件，输出decode的DNA
    with open(infile, 'r', encoding='utf-8') as f:
        dna = svg_to_dna(f.read())
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(dna)


def outputSVG(infile, outfile):
    # 传入DNAseq的txt文件 产生svg文件
    # 改为返回str
    with open(infile, 'r', encoding='utf-8') as f:
        svg = dna_to_svg(f.read())
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(svg)
