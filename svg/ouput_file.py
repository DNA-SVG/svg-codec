import encode_svg
import decode_svg
import xml.etree.ElementTree as ET
import argparse


def encode_to_DNA(file):
    # 返回以seq列表
    tree = ET.parse(file)
    root = tree.getroot()
    DNAseq = encode_svg.dfs(root, None, 0)
    # b = "\n".join(a)
    return DNAseq


def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()
# save_to_file('test_output',b)


def outputDNAseq(infile, outfile):
    # 传入需要encode的文件，输出decode的DNA
    contents = encode_to_DNA(infile)
    contents = "\n".join(contents)
    save_to_file(outfile, contents)

def output(DNAseq, outfile):
    DNAseq = DNAseq.split('\n')
    contents = decode_svg.generate_svg(DNAseq)
    save_to_file(outfile, contents)
    
def outputSVG(infile, outfile):
    # 传入DNAseq的str文件 产生svg文件

    with open(infile, 'r') as f:
        seq = f.read()

    DNAseq = seq.split('\n')
    # print(DNAseq, len(DNAseq))
    contents = decode_svg.generate_svg(DNAseq)
    save_to_file(outfile, contents)


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
    main()
    # outputSVG("./svg/test_seq.txt", '1.svg')


# if __name__ == '__main__':
    # file = '../test1.svg'

    # file = '../building-construction-education-svgrepo-com.svg'
    # 不能重复，会影响编号
    # a = encode_to_DNA(file)
    # print(a)
    # outputDNAseq(file, 'test_seq.txt')
    # outputSVG('ret.svg', a)
    # b=decode_svg.generate_svg(a)
    # save_to_file('test1.svg',b)
