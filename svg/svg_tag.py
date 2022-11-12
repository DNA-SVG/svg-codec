# 章程
# 2022/11/7
import xml.etree.ElementTree as ET
from svg_type import SVGNumber, SVGString

ATTR_KEY = {'width':'AA', 'height':'AT', 'viewBox':'AC', 'style':'AG', 'id':'TA', 'class':'TT'}
KEY_ATTR = {v:k for k, v in ATTR_KEY.items()}
ATTR_TYPE = {'width':'number', 'height':'number', 'viewBox':'number', 'style':'str', 'id':'str', 'class':'str'}
KEY_LENGTH = 2

class Tag:
    required_attrs = []
    optional_attrs = set()
    @classmethod
    def get_required(cls):
        return cls.required_attrs
    @classmethod
    def get_optional(cls):
        return cls.optional_attrs

class Circle(Tag):
    required_attrs = ['cx', 'cy']

class Svg(Tag):
    optional_attrs = {'width', 'height', 'viewBox', 'id', 'class', 'style'}

def encode_optional(node: ET.Element, cur_tag: Tag) -> str:
    seq = ''
    total = 0
    for attr_name, attr_value in node.items():
        if attr_name in cur_tag.get_required():
            continue
        if attr_name not in cur_tag.get_optional():
            print('error: attribute not supported')
            continue
        total += 1
        key = ATTR_KEY[attr_name]
        type = ATTR_TYPE[attr_name]
        seq += key
        if type == 'number':
            seq += SVGNumber(attr_value, type='encoder').translate()
        elif type == 'str':
            seq += SVGString(attr_value, type='encoder').translate()
    
    return SVGNumber(str(total), type='encoder').translate()[2:] + seq

def decode_optional(seq: str, cur_tag: Tag):
    total, idx = SVGNumber('AA'+seq, type='decoder').translate()
    ret_list = []
    idx -= 2
    for i in range(total):
        key = seq[idx:idx + 2]
        idx += KEY_LENGTH
        attr_name = KEY_ATTR[key]
        type = ATTR_TYPE[attr_name]
        if type == 'number':
            attr_value, end_idx = SVGNumber(seq, type='decoder', start_idx=idx).translate()
        else:
            attr_value, end_idx = SVGString(seq, type='decoder', start_idx=idx).translate()
        ret_list.append([attr_name, attr_value])
        idx = end_idx
    return ret_list

if __name__ == '__main__':
    root = ET.fromstring('<svg width="64px" height="64px" viewBox="0 0 64px 64px" style="enable-background:new 0 0 64 64;"/>')
    s = encode_optional(root, Svg)
    print(s)
    ss = decode_optional(s, Svg)
    for t in ss:
        print('{0}="{1}"'.format(t[0], t[1]))