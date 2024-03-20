import xml.etree.ElementTree as ET
from .svg_code import *
from .str_list import *

class Encoder:
    IGNORE_TAGS = ['sodipodi:nameview', 'metadata']    
    # 深度遍历
    def __init__(self): 
        self.element_num = 0
    
    def __dfs(self, root, is_last = False):
        '''
        tags:
        0 -- no child,  not last
        1 -- no child,  last
        2 -- has child, not last
        3 -- has child, last
        '''
        DNA_seq = []
        status = int(is_last)
        length = len(root)
        if length == 0:
            a = encode_tag(root, self.element_num, status)
            if a != None:
                DNA_seq += [a]
            return DNA_seq
        else:
            status += 2
            a = encode_tag(root, self.element_num, status)
            if a != None:
                DNA_seq += [a]

            for i in range(length-1):
                self.element_num += 1
                DNA_seq += self.__dfs(root[i])
            self.element_num += 1
            DNA_seq += self.__dfs(root[length-1], True)
        return DNA_seq
    
    def __pre_process(self, root):
        for tag in self.IGNORE_TAGS:
            for node in root.iter():
                if tag in node.tag:
                    root.remove(node)
                    break
        return root

    def encode_file(self, filename):
        str_list_clear()
        with open(filename, 'r', encoding='utf-8') as f:
            root = ET.fromstring(f.read())
            root = self.__pre_process(root)
            seqs = self.__dfs(root, True)
            seq_str_list = 'TTT' + str_list_pack()
            seqs.insert(0, seq_str_list)
            return seqs