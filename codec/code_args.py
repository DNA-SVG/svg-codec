from svg_type import *
ATTR_KEY = {'width': 'AA', 'height': 'AT', 'viewBox': 'AC',
            'style': 'AG', 'id': 'TA', 'class': 'TT',
            'rx': 'TC', 'ry': 'TG', 'version': 'CA', 't': 'CT', 'p-id': 'CG', 'fill': 'GA', 'type': 'GT',
            'transform': 'GC'}
KEY_ATTR = {v: k for k, v in ATTR_KEY.items()}
ATTR_TYPE = {'width': 'number', 'height': 'number',
             'viewBox': 'number', 'style': 'str', 'id': 'str', 'class': 'str',
             'cx': 'number', 'cy': 'number', 'r': 'number',
             'x': 'number', 'y': 'number', 'd': 'str', 'points': 'str',
             'text': 'str', 'ry': 'number', 'rx': 'number', 't': 'str', 'version': 'str', 'p-id': 'str', 'fill': 'str', 'type': 'str', 'transform': 'str'}

ATTR_CODE = {'number': SVGNumber, 'str': SVGString, 'Enum': SVGEnum}
KEY_LENGTH = 2

STD = '{http://www.w3.org/2000/svg}'

TAG_NT = {"circle": 'AA', "g": 'AT', "path": 'AC',
          "polygon": 'AG', "rect": 'TA', "style": 'TT', "ellipse": 'TC', "defs": 'TG', "svg": 'GG'}
NT_TAG = {v: k for k, v in TAG_NT.items()}


# 枚举类型

#  ATTR IN:
IN_ENCODE = {'SourceGraphic': 'AA', 'SourceAlpha': 'AT', 'BackgroundImage': 'AC',
             ' BackgroundAlpha': 'AG', 'FillPaint': 'TA', 'StrokePaint': 'TC', '<filter-primitive-reference>': 'TG'}
IN_DECODE = {v: k for k, v in IN_ENCODE.items()}
IN = [IN_ENCODE, IN_DECODE]
ATTR_DICT = {'in': IN}
