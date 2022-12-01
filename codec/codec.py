import encode_svg as encode
import decode_svg as decode
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

    
def outputDNAseq(infile, outfile):
    # 传入需要encode的文件，输出decode的DNA
    DNAseq = encode_to_DNA(infile) # 得到DNAseq各tag的list
    DNAseq = "\n".join(DNAseq)
    save_to_file(outfile, DNAseq)


def outputSVG(infile, outfile):
    # 传入DNAseq的txt文件 产生svg文件
    # 改为返回str
    with open(infile, 'r') as f:
        seq = f.read()

    DNAseq = seq.split('\n')
    # print(DNAseq, len(DNAseq))
    contents = decode.generate_svg(DNAseq)
    save_to_file(outfile, contents)
    

def svg_to_dna(xmlstr):
    # 传入str形式的xml文件 输出decode的DNAseq
    root = ET.fromstring(xmlstr)
    DNAseq = encode.dfs(root, None, 0)
    DNAseq = "\n".join(DNAseq)
    return DNAseq

def dna_to_svg(DNAseq):
    # 传入DNAseq的str 返回svg的字符串
    DNAseq = DNAseq.split('\n')
    contents = decode.generate_svg(DNAseq)
    return contents
  

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


