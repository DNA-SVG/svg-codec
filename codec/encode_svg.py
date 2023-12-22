import xml.etree.ElementTree as ET
from .svg_code import *
from .str_list import *

class Encoder:
    IGNORE_TAGS = ['sodipodi:nameview', 'metadata']    
    # 深度遍历
    def __init__(self): 
        self.counter = 1
        

    def __dfs(self, root, bro_counter=-1, child_counter=1, my_counter=0):
        DNA_seq = []

        if len(root) == 0:
            a = encode_tag(root, my_counter, -1, bro_counter)
            if a != None:
                DNA_seq += [a]
            return DNA_seq
        else:
            length = len(root)
            counters = range(self.counter, self.counter+length)
            child_counter = self.counter
            self.counter += length

            a = encode_tag(root, my_counter, child_counter, bro_counter)
            if a != None:
                DNA_seq += [a]
            for i in range(length-1):
                DNA_seq += self.__dfs(root[i], counters[i+1], child_counter, counters[i])
            DNA_seq += self.__dfs(root[length-1], -1, child_counter, counters[length-1])

        return DNA_seq
    
    def __pre_process(self, root):
        for tag in self.IGNORE_TAGS:
            for node in root.iter():
                if tag in node.tag:
                    root.remove(node)
                    break
        return root

    def encode_file(self, filename, bro_counter=-1, child_counter=1, my_counter=0):
        # str_list_clear()
        with open(filename, 'r', encoding='utf-8') as f:
            root = ET.fromstring(f.read())
            root = self.__pre_process(root)
            seqs = self.__dfs(root, bro_counter, child_counter, my_counter)
            # seq_str_list = str_list_pack()
            # seqs.insert(0, seq_str_list)
            return seqs