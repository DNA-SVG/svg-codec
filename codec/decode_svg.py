import xml.etree.ElementTree as ET
from .svg_code import *
from .str_list import *

class Decoder:
    def __init__(self):
        self.tree = ET.ElementTree()
        self.tree._setroot(ET.Element('file'))
        self.cur = 0
        self.allDNA = []

    def get_allDNA(self, Tag_DNAseqlist):
        # 传入编码得到的DNAseq的list 返回解码得到各个
        for i in Tag_DNAseqlist:
            self.allDNA.append(decode_tag(i))

    def dfs_add(self, root):
        '''
        return: True if current tag is last child of its parent, False otherwise
        '''
        array = self.allDNA[self.cur]
        element = ET.SubElement(root, array[0])
        status = array[2]
        for attr, val in array[3:]:
            if attr == 'text':
                element.text = val
            else:
                element.set(attr, val)
        if status == 0:
            return False
        elif status == 1:
            return True
        else:
            while True:
                self.cur += 1
                if self.dfs_add(element):
                    break
            return status == 3

    def generate_svg(self, DNAseq):
        # 传入各个标签及参数的DNA序列list
        for seq in DNAseq:
            if seq[:3] == 'TTT':
                str_list_unpack(seq[3:])
                DNAseq.remove(seq)
                break
        self.get_allDNA(DNAseq)  # 将DNAseq转化成各个标签及参数
        self.allDNA = sorted(self.allDNA, key=lambda x: int(x[1]))
        self.dfs_add(self.tree.getroot())
        file = '<?xml version="1.0" ?>' + ET.tostring(self.tree.getroot()[0], encoding='unicode').replace('><', '>\n<')
        return file