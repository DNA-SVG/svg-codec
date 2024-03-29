from concurrent.futures.process import BrokenProcessPool
import xml.etree.ElementTree as ET
from .svg_code import *

class Encoder:    
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
    
    def encode_file(self, filename, bro_counter=-1, child_counter=1, my_counter=0):
        with open(filename, 'r', encoding='utf-8') as f:
            root = ET.fromstring(f.read())
            return self.__dfs(root, bro_counter, child_counter, my_counter)