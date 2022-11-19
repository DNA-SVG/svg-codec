import encode_tag
from concurrent.futures.process import BrokenProcessPool
import xml.etree.ElementTree as ET
from svg_code import *

# def visit(root, bro_counter, first_child,my_counter):
#     # if len(root) >= 1:
#     #     first_child = my_counter + 1
#     # else:
#     #     first_child = None
#     return encode_tag.func(root.tag, root, my_counter, first_child, bro_counter)



counter = 1
# 深度遍历


def dfs(root, bro_counter=-1,child_counter=-1, my_counter=-1):
    global counter
    DNA_seq = []
   
    if len(root) == 0:
        # print('结束')
        # print(root.tag,my_counter,bro_counter,child_counter)
        # a = visit(root, bro_counter, None,my_counter)
        a = encode_tag(root, my_counter, -1, bro_counter)
        if a != None:
            DNA_seq += [a]
            
        return DNA_seq
    else:
        length = len(root)
        counters = range(counter, counter+length)
        child_counter = counter  
        counter += length
        
       
        a = encode_tag(root, my_counter, child_counter, bro_counter)
        # print(root.tag,my_counter,bro_counter,child_counter)
        if a != None:
            DNA_seq += [a]
            
        for i in range(length-1):
            DNA_seq += dfs(root[i], counters[i+1], child_counter,counters[i])
        DNA_seq += dfs(root[length-1], -1,child_counter, counters[length-1])
        

    return DNA_seq


if __name__ == '__main__':
    file = '../river.svg'
    tree = ET.parse(file)
    root = tree.getroot()

    a = dfs(root, -1,1, 0)
    print(a)
# print("\n".join(a))
