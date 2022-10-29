import encode_tag
from concurrent.futures.process import BrokenProcessPool
import xml.etree.ElementTree as ET
# file = '../sample.xml'
# file = '../building-construction-education-svgrepo-com.svg'


def visit(root, bro_counter, my_counter):
    if len(root) >= 1:
        first_child = my_counter + 1
    else:
        first_child = None
    return encode_tag.func(root.tag, root, my_counter, first_child, bro_counter)


counter = 0
# 深度遍历


def dfs(root, bro_counter=0, my_counter=0):
    global counter
    DNA_seq = []
    a = visit(root, bro_counter, my_counter)
    # print(type(a))
    if a != None:
        DNA_seq += [a]

    # print(DNA_seq)
    if len(root) == 0:
        # print('结束')
        return DNA_seq
    else:
        length = len(root)
        counters = range(counter, counter+length)
        counter += length
        for i in range(length-1):
            DNA_seq += dfs(root[i], counters[i+1], counters[i])
        DNA_seq += dfs(root[length-1], None, counters[length-1])

    return DNA_seq


if __name__ == '__main__':
    file = '../test1.svg'
    tree = ET.parse(file)
    root = tree.getroot()

    a = dfs(root, None, 0)
    print(a)
# print("\n".join(a))
