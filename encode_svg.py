from distutils.command.build_scripts import first_line_re
import encode_tag
from concurrent.futures.process import BrokenProcessPool
import xml.etree.ElementTree as ET
# file = '../sample.xml'
# file = '../building-construction-education-svgrepo-com.svg'
file = '../test.svg'
tree = ET.parse(file)
root = tree.getroot()


def visit(root, bro_counter, my_counter):
    if len(root) >= 1:
        first_child = my_counter + 1
    else:
        first_child = None
    return encode_tag.func(root.tag, root, my_counter, first_child, bro_counter)
    # if len(root) >= 1:
    #     if bro == None:
    #         # print(root.tag, '子节点:'+root[0].tag, None)
    #         return get_par.func(root.tag, root, first_child, bro)

    #     else:
    #         # print(root.tag, '子节点:'+root[0].tag, '兄弟节点'+bro.tag)
    #         return get_par.func(root.tag, root, first_child, bro)
    # elif len(root) == 0:
    #     return get_par.func(root.tag, root, None, bro)
    # if bro == None:
    #     # print(root.tag, '无子节点', None)
    #     return get_par.func(root.tag, root, None, bro)

    # else:
    #     return get_par.func(root.tag, root, None, bro)
    #     # print(root.tag, '无子节点', '兄弟节点'+bro.tag)


counter = 1
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


# print(type(dfs(root)))
# print(dfs(root))
print("\n".join(dfs(root[0][0], None, 0)))
