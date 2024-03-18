import xml.etree.ElementTree as ET

from .svg_type import *
from .collect import CollectMethod
from .svg_tag import *

nt = tag_nt()
ATTR_CODE = {'number': SVGNumber, 'str': SVGString,
             'enum': SVGEnum, 'pathd': SVGPathD, 'trans': SVGTransform}

STD = '{http://www.w3.org/2000/svg}'

def encode_address(element_num, status):
    return SVGNumber(element_num).encode() + 'AGCT'[status]

def decode_address(seq: str):
    address_seq, end_idx = SVGNumber(seq).decode(call_number=True)
    return [address_seq, 'AGCT'.find(seq[end_idx])], end_idx + 1

def encode_require(node: ET.Element, cur_tag: Tag) -> str:
    seq = ''
    for attr_name, attr_type in cur_tag.get_required().items():
        if attr_name == 'text':
            attr_value = node.text
        else:
            attr_value = node.get(attr_name)
        if attr_type == 'enum':
            seq += SVGEnum(attr_name, attr_value).encode()
        else:
            seq += ATTR_CODE[attr_type](attr_value).encode()
    return seq

def decode_require(seq: str, cur_tag: Tag):
    # 传入以require开头的序列
    # 返回tag属性列表 末尾下标
    ret_list = []
    idx = 0
    for attr_name, attr_type in cur_tag.get_required().items():
        if attr_type == 'enum':
            attr_val, idx = SVGEnum(attr_name, seq, start_idx=idx).decode()
        else:
            attr_val, idx = ATTR_CODE[attr_type](seq, start_idx=idx).decode()
        if attr_val != None:
            ret_list.append([attr_name, attr_val])
    return ret_list, idx

def encode_optional(node: ET.Element, cur_tag: Tag) -> str:
    seq = ''
    total = 0
    attr_optional = []
    for attr_name, _ in node.items():
        if attr_name in cur_tag.get_required():
            continue
        if attr_name.startswith('{http://sodi'):
            continue
        attr_optional.append(attr_name)
        total += 1
    attr_types = cur_tag.get_encode_optional(attr_optional)
    codec_type_value = {k1: (v1, v2, v3) for k1, (v1, v2) in attr_types.items() for k2, v3 in node.items() if k1 == k2}
    for name, (codec, type, value) in codec_type_value.items():
        seq += codec
        if type == 'enum':
            seq += SVGEnum(name, value).encode()
        else:
            seq += ATTR_CODE[type](value).encode()
    return SVGNumber(total).encode() + seq

def decode_optional(seq: str, tag: Tag):
    total, idx = SVGNumber(seq).decode(call_number=True )
    seq = seq[idx:]
    idx = 0
    public_list, public_len = tag.get_decode_public()
    private_list, private_len = tag.get_decode_private()
    ret = []
    for _ in range(total):
        if seq[0] == 'G':
            attr_name, idx = SVGString(seq[1:], start_idx=idx).decode()
            idx = idx + 1
            type = 'str'
        elif seq[:public_len] in public_list.keys():
            attr_name, type = public_list.get(seq[:public_len])
            idx = public_len
        elif private_list != None and seq[:private_len] in private_list.keys():
            attr_name, type = private_list.get(seq[:private_len])
            idx = private_len
        else:
            attr_name = ''
            type = 'str'
        seq = seq[idx:]
        if type == 'enum':
            attr_value, idx = SVGEnum(attr_name, seq).decode()
        else:
            attr_value, idx = ATTR_CODE[type](seq).decode()
        seq = seq[idx:]
        idx = 0
        ret.append([attr_name, attr_value])
    return ret

def encode_tag(node: ET.Element, element_num, status) -> str:
    tag_name = node.tag
    if tag_name.startswith(STD):
        tag_name = tag_name[len(STD):]
    tag_class = globals()[tag_name]
    seq = nt.get_tag_nt(tag_name)
    seq += encode_address(element_num, status)
    seq += encode_require(node, tag_class)
    seq += encode_optional(node, tag_class)
    # CollectMethod.number_collect(len(seq))
    # CollectMethod.number_collect(-len(encode_address(my_counter, first_child, bro)))
    return seq


def decode_tag(seq: str):
    # 传入tag的DNAseq
    tag_name = nt.get_nt_tag(seq[:nt.get_tag_len()])
    tag_class = globals()[tag_name]

    ret_list = [tag_name]
    start = nt.get_tag_len()
    seq = seq[start:]
    address_list, end_idx = decode_address(seq)
    seq = seq[end_idx:]
    require_list, end_idx = decode_require(seq, tag_class)
    seq = seq[end_idx:]
    optional_list = decode_optional(seq, tag_class)
    ret_list += address_list + require_list + optional_list
    return ret_list
