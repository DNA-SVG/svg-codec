# tag: circle g path polygon rect style
# optional attibute: id class

# 添加返回序列
from base64 import encode
import xml.etree.ElementTree as ET

import encode_attr_type
nt_dict = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
# '00': 'A', '01': 'c', '10': 'G', '11': 'T'

tag_dict = {"circle": 'AA', "g": 'AT', "path": 'AC',
            "polygon": 'AG', "rect": 'TA', "style": 'TT'}
# 将编号（address）转化成DNA_seq

# 可以优化


def address2DNAseq(my_counter, first_child=None, bro=None):
    # 返回my_counter, first_child, bro的DNAseq
    seq = ''
    # print(first_child,bro)
    seq += encode_attr_type.int_to_seq(my_counter)

    if first_child != None:
        seq += encode_attr_type.int_to_seq(first_child)
    else:
        seq += 'TATT'
    if bro != None:
        seq += encode_attr_type.int_to_seq(bro)
    else:
        seq += 'TATT'
    return seq


def encode_idclass(id, the_class):
    ret = ''
    if id == None:
        if the_class == None:
            ret += 'A'
        else:
            ret += 'T'+encode_attr_type.str_to_seq(the_class)
    else:
        if the_class == None:
            ret += 'C' + encode_attr_type.str_to_seq(id)
            return ret
        else:
            ret += 'G'+encode_attr_type.str_to_seq(id) + \
                encode_attr_type.str_to_seq(the_class)

    return ret
# (root.tag, root,my_counter,first_child, bro_counter)


def get_cicle(node, my_counter, first_child=None, bro=None):
    cx = node.get('cx')
    cy = node.get('cy')
    r = node.get('r')
    id = node.get('id')
    the_class = node.get('class')

    seq = tag_dict['circle']

    # 编号
    seq += address2DNAseq(my_counter, first_child, bro)

    # required attribute
    seq = seq + encode_attr_type.float_to_seq(float(cx)) + encode_attr_type.float_to_seq(
        float(cy)) + encode_attr_type.float_to_seq(float(r))
    # id class
    seq += encode_idclass(id, the_class)
    return seq


def get_g(node, my_counter=None, first_child=None, bro=None):
    id = node.get('id')
    the_class = node.get('class')

    seq = tag_dict['g']

    seq += address2DNAseq(my_counter, first_child, bro)
    seq += encode_idclass(id, the_class)

    return seq


def get_path(node, my_counter, first_child=None, bro=None):
    d = node.get('d')
    id = node.get('id')
    the_class = node.get('class')

    seq = tag_dict['path']
    seq += address2DNAseq(my_counter, first_child, bro)
    seq = seq + encode_attr_type.str_to_seq(d)
    seq += encode_idclass(id, the_class)

    return seq


def get_polygon(node, my_counter, first_child=None, bro=None):
    points = node.get('points')
    id = node.get('id')
    the_class = node.get('class')

    seq = tag_dict['polygon']
    seq += address2DNAseq(my_counter, first_child, bro)
    seq = seq + encode_attr_type.str_to_seq(points)
    seq += encode_idclass(id, the_class)
    return seq


def get_rect(node, my_counter, first_child=None, bro=None):
    x = node.get('x')
    y = node.get('y')
    width = node.get('width')
    height = node.get('height')
    id = node.get('id')
    the_class = node.get('class')

    seq = tag_dict['rect']
    seq += address2DNAseq(my_counter, first_child, bro)
    seq = seq + encode_attr_type.float_to_seq(float(x)) + encode_attr_type.float_to_seq(float(y)) + encode_attr_type.float_to_seq(float(
        width)) + encode_attr_type.float_to_seq(float(height))
    seq += encode_idclass(id, the_class)

    return seq


def get_style(node, my_counter, first_child=None, bro=None):
    text = node.text
    id = node.get('id')
    the_class = node.get('class')

    seq = tag_dict['style']
    seq += address2DNAseq(my_counter, first_child, bro)
    seq = seq + encode_attr_type.str_to_seq(text)
    seq += encode_idclass(id, the_class)

    return seq


std = '{http://www.w3.org/2000/svg}'
func_dict = {std+"circle": get_cicle, std+"g": get_g, std+"path": get_path,
             std+"polygon": get_polygon, std+"rect": get_rect, std+"style": get_style}


def func_None(node, my_counter, first_child, bro):
    print('无对应函数')


def func(x, node, my_counter=None, first_child=None, bro=None):
    # print(x)
    return func_dict.get(x, func_None)(node, my_counter, first_child, bro)


# from concurrent.futures.process import BrokenProcessPool
# file = '../sample.xml'
# file='../building-construction-education-svgrepo-com.svg'
# tree = ET.parse(file)
# root = tree.getroot()

# node = root[0]
# func('g', node, node[0])

# get_g(node, node[0])
# 测试
# print(root[0].get('name'))
# for child in root:
#     print(child.attrib)
# # get返回的是str
# # circle cx cy r
# def getname(node):
#     name=node.get('name')
#     return name
# print(root[0].get('name'))
# print(getname(root[0]))
