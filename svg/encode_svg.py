import encode_tag
from concurrent.futures.process import BrokenProcessPool
import xml.etree.ElementTree as ET
# file = '../sample.xml'
# file = '../building-construction-education-svgrepo-com.svg'


def visit(root, bro_counter, first_child,my_counter):
    # if len(root) >= 1:
    #     first_child = my_counter + 1
    # else:
    #     first_child = None
    return encode_tag.func(root.tag, root, my_counter, first_child, bro_counter)


counter = 1
# 深度遍历


def dfs(root, bro_counter=None,child_counter=None, my_counter=None):
    global counter
    DNA_seq = []
    # a = visit(root, bro_counter, my_counter)
    # print(root.tag,my_counter,bro_counter)
 
    # if a != None:
    #     DNA_seq += [a]


    if len(root) == 0:
        # print('结束')
        # print(root.tag,my_counter,bro_counter,None)
        a = visit(root, bro_counter, None,my_counter)
        if a != None:
            DNA_seq += [a]
            
        return DNA_seq
    else:
        length = len(root)
        counters = range(counter, counter+length)
        child_counter = counter  
        counter += length
        
       
        a = visit(root, bro_counter, child_counter,my_counter)
        # print(root.tag,my_counter,bro_counter,child_counter)
        if a != None:
            DNA_seq += [a]
            
        for i in range(length-1):
            DNA_seq += dfs(root[i], counters[i+1], child_counter,counters[i])
        DNA_seq += dfs(root[length-1], None,child_counter, counters[length-1])
        

    return DNA_seq


if __name__ == '__main__':
    file = '../test1.svg'
    tree = ET.parse(file)
    root = tree.getroot()

    a = dfs(root, None,1, 0)
    print(a)
# print("\n".join(a))
