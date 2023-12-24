import xml.etree.ElementTree as ET
from .svg_code import *
from .str_list import *

class Decoder:
    def get_allDNA(self, Tag_DNAseqlist):
        # 传入编码得到的DNAseq的list 返回解码得到各个
        allDNA = []
        for i in Tag_DNAseqlist:
            allDNA.append(decode_tag(i))
        return allDNA


    def generate_SVGtag(self, tag_list):
        tag_name = tag_list[0]
        line = '<{}'.format(tag_name)
        text_val = ''
        for attr in tag_list[4:]:
            if attr[0] != 'text':
                line += ' {} = "{}"'.format(attr[0], attr[1])
            else:
                text_val = attr[1]
        if tag_name == 'svg':
            line += ' xmlns="http://www.w3.org/2000/svg"'
        line += '>{}</{}>'.format(text_val, tag_name)
        return line


    def add_child(self, root, tag_name, child):
        idx = -1*len(tag_name)-3
        line = '\n'.join([root[:idx], child])
        line += '\n'+root[idx:]
        return line
    # 将并列的后一个标签写入


    def add_bro(self, root, bro):
        line = '\n'.join([root, bro])
        return line


    def dfs_add(self, allDNA, cur=1):
        # 将各个标签拼接
        first_child = int(allDNA[cur][2])
        bro = int(allDNA[cur][3])
        cur_tag_name = allDNA[cur][0]

        if first_child == -1:
            if bro == -1:
                return self.generate_SVGtag(allDNA[cur])
            else:
                return self.add_bro(self.generate_SVGtag(allDNA[cur]), self.dfs_add(allDNA, bro))
        else:
            leaf = self.add_child(self.generate_SVGtag(
                allDNA[cur]), cur_tag_name, self.dfs_add(allDNA, first_child))
            if bro == -1:
                return leaf
            else:
                return self.add_bro(leaf, self.dfs_add(allDNA, bro))


    def generate_svg(self, DNAseq):
        # 传入各个标签及参数的DNA序列list
        for seq in DNAseq:
            if seq[:3] == 'TTT':
                str_list_unpack(seq[15:])
                DNAseq.remove(seq)
                break
        allDNA = self.get_allDNA(DNAseq)  # 将DNAseq转化成各个标签及参数
        allDNA = sorted(allDNA, key=lambda x: int(x[1]))
        file = '<?xml version="1.0" ?>'
        allDNA.insert(0, ['svg', '0', '-1', '-1'])
        file += self.dfs_add(allDNA)
        return file