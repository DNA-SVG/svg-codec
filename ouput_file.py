import encode_svg
import decode_svg
import xml.etree.ElementTree as ET


def outputDNA(file):
    tree = ET.parse(file)
    root = tree.getroot()
    a=encode_svg.dfs(root,None,0)
    # b = "\n".join(a)
    return a




def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()
# save_to_file('test_output',b)

def outputSVG(file_name:str, DNAseq):
    # 传入要保存的文件名及DNAseq 产生svg文件
    contents=decode_svg.generate_svg(DNAseq)
    save_to_file(file_name,contents)
if __name__ == '__main__':
    # file = '../test1.svg'
    
    file = '../building-construction-education-svgrepo-com.svg'
    # 不能重复会，会影响编号
    a=outputDNA(file)
    print(a)
    outputSVG('test.svg',a)
    # b=decode_svg.generate_svg(a)
    # save_to_file('test1.svg',b)