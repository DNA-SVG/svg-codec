from .encode_svg import Encoder
from .decode_svg import Decoder
from .error_correction import add_ecc, check_restore

class Codec:
    def outputDNAseq(self, infile, outfile):
        # 传入需要encode的文件，输出decode的DNA
        enc = Encoder()
        DNAseq = enc.encode_file(infile)
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(DNAseq))

    def outputSVG(self, infile, outfile, reserve=None):
        # 传入DNAseq的txt文件 产生svg文件
        # 改为返回str
        dec = Decoder()
        with open(infile, 'r', encoding='utf-8') as f:
            seq_str = f.read()
        seq_list = seq_str.split('\n')
        
        svg = dec.generate_svg(seq_list, reserve)
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(svg)
