import xml.etree.ElementTree as ET
from .svg_type import SVGNumber, SVGString, SVGCoordinate, SVGEnum
from .svg_tag import *


ATTR_KEY = {'width': 'AAA', 'height': 'AAT', 'viewBox': 'AAC',
            'style': 'AAG', 'id': 'ATA', 'class': 'ATT',
            'rx': 'ATC', 'ry': 'ATG', 'filterRes': 'ACA', 'filterUnits': 'ACT', 'x1': 'ACC', 'x2': 'ACG',
            'y1': 'AGA', 'y2': 'AGT', 'gradientUnits': 'AGC', 'gradientTransform': 'AGG', 'spreadMethod': 'TAA',
            'xlink:href': 'TAT', 'offset': 'TAC', 'stop-color': 'TAG', 'stop-opacity': 'TTA',
            'in': 'TTT', 'dx': 'TTC', 'dy': 'TTG', 'result': 'TCA', 'in2': 'TCT', 'operator': 'TCC', 'k1': 'TCG',
            'k2': 'TGA', 'k3': 'TGT', 'k4': 'TGC', 'values': 'TGG', 'type': 'CAA','stdDeviation':'CAT','edgeNode':'CAC'}

KEY_ATTR = {v: k for k, v in ATTR_KEY.items()}

ATTR_TYPE = {'width': 'number', 'height': 'number',
             'viewBox': 'number', 'style': 'str', 'id': 'str', 'class': 'str',
             'cx': 'number', 'cy': 'number', 'r': 'number',
             'x': 'number', 'y': 'number', 'd': 'str', 'points': 'str',
             'text': 'str', 'ry': 'number', 'rx': 'number',
             'filterRes': 'number', 'filterUnits': 'enum', 'x1': 'number', 'x2': 'number',
             'y1': 'number', 'y2': 'number', 'gradientUnits': 'enum', 'gradientTransform': 'str',
             'spreadMethod': 'enum', 'xlink:href': 'str', 'offset': 'number',
             'stop-color': 'str', 'stop-opacity': 'number', 'in': 'str', 'dx': 'number', 'dy': 'number','result':'str',
             'in2': 'str', 'operator': 'enum', 'k1': 'number', 'k2': 'number', 'k3': 'number',
             'k4': 'number', 'values': 'number', 'type': 'str','stdDeviation':'number','edgeNode':'str'}

ATTR_CODE = {'number': SVGNumber, 'str': SVGString,
             'enum': SVGEnum, 'coordinate': SVGCoordinate}
KEY_LENGTH = 3  # TODO:没确认

STD = '{http://www.w3.org/2000/svg}'

TAG_lENGTH = 3
TAG_NT = {"circle": 'AAA', "g": 'AAT', "path": 'AAC',
          "polygon": 'AAG', "rect": 'ATA', "style": 'ATT', "ellipse": 'ATC', "defs": 'ATG', "svg": 'ACA', 
          'title': 'ACT', 'filter': 'ACC', 'linearGradient': 'ACG', 'stop': 'AGA',
          'feOffset': 'AGT', 'feComposite': 'AGC', 'feColorMatrix': 'AGG', 'feMerge': 'TAA', 'feMergeNode': 'TAT',
          'feGaussianBlur':'TAC'}
TAG_lENGTH = 3
TAG_NT = {"circle": 'AAA', "g": 'AAT', "path": 'AAC',
          "polygon": 'AAG', "rect": 'ATA', "style": 'ATT', "ellipse": 'ATC', "defs": 'ATG', "svg": 'ACA', 
          'title': 'ACT', 'filter': 'ACC', 'linearGradient': 'ACG', 'stop': 'AGA',
          'feOffset': 'AGT', 'feComposite': 'AGC', 'feColorMatrix': 'AGG', 'feMerge': 'TAA', 'feMergeNode': 'TAT',
          'feGaussianBlur':'TAC'}
NT_TAG = {v: k for k, v in TAG_NT.items()}



def encode_optional(node: ET.Element, cur_tag: Tag) -> str:
    seq = ''
    total = 0
    for attr_name, attr_value in node.items():
        if attr_name in cur_tag.get_required():
            continue
        if attr_name not in cur_tag.get_optional():
            print('error: attribute {} not supported in {}'.format(
                attr_name, cur_tag.__name__))
            continue
            print('error: attribute {} not supported in {}'.format(
                attr_name, cur_tag.__name__))
            continue
        total += 1
        key = ATTR_KEY[attr_name]
        type = ATTR_TYPE[attr_name]
        seq += key

        if type == 'enum':
            seq += SVGEnum(attr_name, attr_value, type='encoder').translate()
        else:
            seq += ATTR_CODE[type](attr_value, type='encoder').translate()

        if type == 'enum':
            seq += SVGEnum(attr_name, attr_value, type='encoder').translate()
        else:
            seq += ATTR_CODE[type](attr_value, type='encoder').translate()

    return SVGNumber(str(total), type='encoder').translate()[2:] + seq

# TODO: get 返回none情况


def encode_require(node: ET.Element, cur_tag: Tag) -> str:


def encode_require(node: ET.Element, cur_tag: Tag) -> str:
    seq = ''
    for attr_name in cur_tag.get_required():
        if attr_name == 'text':
            attr_val = node.text
        else:
            attr_val = node.get(attr_name)

        type = ATTR_TYPE[attr_name]
        if type == 'enum':
            seq += SVGEnum(attr_name, attr_val, type='encoder').translate()
        else:
            seq += ATTR_CODE[type](attr_val, type='encoder').translate()

    return seq


def decode_require(seq: str, cur_tag: Tag):
def decode_require(seq: str, cur_tag: Tag):
    # 传入以require开头的序列
    # 返回tag属性列表 末尾下标
    ret_list = []
    idx = 0
    for attr_name in cur_tag.get_required():


        type = ATTR_TYPE[attr_name]
        if type == 'enum':
            attr_val, end_idx = SVGNumber(
                attr_name, seq, type='decoder', start_idx=idx).translate()
        else:
            attr_val, end_idx = ATTR_CODE[type](
                seq, type='decoder', start_idx=idx).translate()
        if type == 'enum':
            attr_val, end_idx = SVGNumber(
                attr_name, seq, type='decoder', start_idx=idx).translate()
        else:
            attr_val, end_idx = ATTR_CODE[type](
                seq, type='decoder', start_idx=idx).translate()
        ret_list.append([attr_name, attr_val])
        idx = end_idx

    return ret_list, idx


def encode_address(my_counter, first_child=-1, bro=-1):
    # 返回my_counter, first_child, bro的DNAseq
    seq = ''
    # '0 1 2'
    address_str = str(my_counter) + ' '+str(first_child) + ' '+str(bro)
    seq += SVGNumber(address_str, type='encoder').translate()
    return seq


def decode_address(seq: str):
    '''传入以address开头的序列'''
    '''返回[my_counter, first_child, bro],end_idx'''
    address_seq, end_idx = SVGNumber(seq, type='decoder').translate()
    return address_seq.split(' '), end_idx


def decode_optional(seq: str):
    total, idx = SVGNumber('AA'+seq, type='decoder').translate()
    ret_list = []
    idx -= 2
    for _ in range(int(total)):
        key = seq[idx:idx + KEY_LENGTH]
        key = seq[idx:idx + KEY_LENGTH]
        idx += KEY_LENGTH
        attr_name = KEY_ATTR[key]
        type = ATTR_TYPE[attr_name]

        if type == 'enum':
            attr_value, end_idx = SVGNumber(
                attr_name, seq, type='decoder', start_idx=idx).translate()
        else:
            attr_value, end_idx = ATTR_CODE[type](
                seq, type='decoder', start_idx=idx).translate()

        if type == 'enum':
            attr_value, end_idx = SVGNumber(
                attr_name, seq, type='decoder', start_idx=idx).translate()
        else:
            attr_value, end_idx = ATTR_CODE[type](
                seq, type='decoder', start_idx=idx).translate()
        ret_list.append([attr_name, attr_value])
        idx = end_idx
    return ret_list



def encode_tag(node: ET.Element, my_counter, first_child=-1, bro=-1) -> str:
    tag_name = node.tag
    if tag_name.startswith(STD):
        tag_name = tag_name[len(STD):]
    tag_class = globals()[tag_name]
    seq = TAG_NT[tag_name]
    seq += encode_address(my_counter, first_child, bro) + \
        encode_require(node, tag_class) + \
        encode_optional(node, tag_class)
    seq += encode_address(my_counter, first_child, bro) + \
        encode_require(node, tag_class) + \
        encode_optional(node, tag_class)
    return seq



def decode_tag(seq: str):
    # 传入tag的DNAseq
    tag_name = NT_TAG[seq[0:TAG_lENGTH]]
    tag_name = NT_TAG[seq[0:TAG_lENGTH]]
    tag_class = globals()[tag_name]


    ret_list = [tag_name]
    start = TAG_lENGTH
    start = TAG_lENGTH
    address_list, end_idx = decode_address(seq[start:])
    start += end_idx
    require_lsit, end_idx = decode_require(seq[start:], tag_class)
    require_lsit, end_idx = decode_require(seq[start:], tag_class)
    start += end_idx
    optional_list = decode_optional(seq[start:])
    ret_list += address_list + require_lsit + optional_list
    return ret_list




if __name__ == '__main__':
    root = ET.fromstring(
        '<svg width="64px" height="64px" viewBox="0 0 64px 64px" style="enable-background:new 0 0 64 64;"/>')
    root = ET.fromstring(
        '<svg width="64px" height="64px" viewBox="0 0 64px 64px" style="enable-background:new 0 0 64 64;"/>')
    s = encode_optional(root, svg)
    print(s)
    ss = decode_optional(s)
    # for t in ss:
    #     print('{0}="{1}"'.format(t[0], t[1]))

    # a = 'AATTAATCTATT'

    # 测试address
    # b = SVGNumber('1 2 3', type = 'encoder').translate()
    # # b = SVGNumber(b, type='decoder').translate()
    # print(b)
    # a = encode_address(0,1,-1)
    # decode_address(a)

    # 测试require
    root = ET.fromstring(
        '<svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" id="1"/>')
    op = encode_optional(root, svg)
    op = encode_optional(root, svg)
    deop = decode_optional(op)
    # s = encode_require(root,circle)
    # print(s)
    # sl = 'GG' +encode_address(0,1,-1)
    # Tag_ = encode_tag(root,0,1,-1)
    # print(Tag_)
    # seq ='GGTATGAATAAATTTATTATCACTACTAAATAAATAATCTAAAAAATCTAAAAATAGACTACCGTGGGTTGATAACTTGGAGAT'

    # print(decode_tag(''))
    # ss = decode_tag('GGTATGTATTAATTATCACTACTAAATAAATAATCTAAAAAATCTAAAAATAGACTACCGTGGGTTGATAACTTGGAGAT')
    # print(ss)
