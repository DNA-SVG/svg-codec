import xml.etree.ElementTree as ET
from .svg_code import *
from .str_list import *
from .segment import split

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

    def generate_element(self, root, array, have_style=False):
        element = ET.SubElement(root, array[0])
        for attr, val in array[3:]:
            if attr == 'text':
                element.text = val
            else:
                element.set(attr, val)
        if have_style:
            element.set('class', 'partial')
        return element

    def dfs_add(self, root):
        '''
        return: True if current tag is last child of its parent, False otherwise
        '''
        array = self.allDNA[self.cur]
        element = self.generate_element(root, array)
        status = array[2]
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

    def dfs_add_partial(self, root, have_style=False):
        root = self.generate_element(root, self.allDNA[0])
        if have_style:
            element = ET.SubElement(root, 'style')
            element.text = r'.partial{fill:none;stroke:#000000;stroke-linecap:round;stroke-linejoin:round;}'
        for array in self.allDNA[1:]:
            self.generate_element(root, array, have_style)

    def generate_svg(self, DNAseq, reserve=None):
        # 传入各个标签及参数的DNA序列list
        DNAseq, have_style = split(DNAseq, reserve)
        for seq in DNAseq:
            if seq[:6] == '111111':
                str_list_unpack(seq[6:])
                DNAseq.remove(seq)
                break
        self.get_allDNA(DNAseq)  # 将DNAseq转化成各个标签及参数
        self.allDNA = sorted(self.allDNA, key=lambda x: int(x[1]))
        if reserve == None:
            self.dfs_add(self.tree.getroot())
        else:
            self.dfs_add_partial(self.tree.getroot(), have_style)
        file = '<?xml version="1.0" ?>' + ET.tostring(self.tree.getroot()[0], encoding='unicode').replace('><', '>\n<')
        return file