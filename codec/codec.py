from .encode_svg import Encoder
from .decode_svg import Decoder
from .segment import optimize_seq_len, restore_seq_len
from .error_correction import add_ecc, check_restore
import xml.etree.ElementTree as ET

class Codec:
    def __svg_to_dna(self, filename: str, optimize: bool=True) -> str:
        # 传入str形式的xml文件 输出decode的DNAseq
        enc = Encoder()
        DNAseq = enc.encode_file(filename)
        if optimize:
            DNAseq = optimize_seq_len(DNAseq)
            DNAseq = add_ecc(DNAseq)
        return '\n'.join(DNAseq)

    def __dna_to_svg(self, filename: str, optimize: bool=True) -> str:
        # 传入DNAseq的str 返回svg文件字符串
        dec = Decoder()
        
        with open(filename, 'r', encoding='utf-8') as f:
            seq_str = f.read()
        seq_list = seq_str.split('\n')
        if optimize:
            seq_list = check_restore(seq_list)
            seq_list = restore_seq_len(seq_list)

        svg_str = dec.generate_svg(seq_list)
        return svg_str


    def outputDNAseq(self, infile, outfile):
        # 传入需要encode的文件，输出decode的DNA
        dna = self.__svg_to_dna(infile)
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(dna)


    def outputSVG(self, infile, outfile):
        # 传入DNAseq的txt文件 产生svg文件
        # 改为返回str
        svg = self.__dna_to_svg(infile)
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(svg)
