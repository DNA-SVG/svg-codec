from codec.svg_type import SVGString

class tag_nt:
    __TAG_lENGTH = 3
    __TAG_NT = {
        'circle': 'AAA', 'clipPath': 'AAC', 'defs': 'AAG', 'desc': 'AAT', 'ellipse': 'ACA', 'feBlend': 'ACC', 'feColorMatrix': 'ACG', 'feComposite': 'ACT', 'feFlood': 'AGA', 'feGaussianBlur': 'AGC', 'feMorphology': 'AGG', 'feOffset': 'AGT', 'filter': 'ATA', 'g': 'ATC', 'linearGradient': 'ATG', 'mask': 'ATT', 'path': 'CAA', 'polygon': 'CAC', 'polyline': 'CAG', 'radialGradient': 'CAT', 'rect': 'CCA', 'stop': 'CCC', 'style': 'CCG', 'svg': 'CCT', 'title': 'CGA', 'use': 'CGC'
    }
    __NT_TAG = {v: k for k, v in __TAG_NT.items()}
    def get_tag_len(self):
        return self.__TAG_lENGTH
    def get_tag_nt(self, tag_name):
        return self.__TAG_NT[tag_name]
    def get_nt_tag(self, seq):
        return self.__NT_TAG[seq]

class Tag:
    required_class = {}
    optional_class = {'id': ('TA', 'str'), 'class': ('TC', 'str'), 'fill': ('TG' ,'str'), 'transform': ('TT', 'str')}
    class_len = 2

    @classmethod
    def get_required(cls):
        return cls.required_class

    @classmethod
    def get_encode_optional(cls, attr_list):
        ret = {}
        classes = Tag.optional_class.copy()
        classes.update(cls.optional_class)
        for attr_name in attr_list:
            if classes.get(attr_name) != None:
                ret[attr_name] = classes.get(attr_name)
            else:
                ret[attr_name] = (SVGString(attr_name, type='encoder').translate(), 'str')
        return ret
    
    @classmethod
    def get_decode_public(cls):
        public_ret = {v1: (k, v2) for k, (v1, v2) in Tag.optional_class.items()}
        return public_ret, Tag.class_len
     
    @classmethod
    def get_decode_private(cls):
        if len(cls.optional_class) == 0:
            return None, 0
        private_ret = {v1: (k, v2) for k, (v1, v2) in cls.optional_class.items()}
        return private_ret, cls.class_len

class circle(Tag):
    required_class = {'cx': 'number', 'cy': 'number', 'r': 'number'}
    optional_class = {}
    class_len = 0

class clipPath(Tag):
    required_class = {}
    optional_class = {}
    class_len = 0

class defs(Tag):
    required_class = {}
    optional_class = {}
    class_len = 0

class desc(Tag):
    required_class = {}
    optional_class = {}
    class_len = 0

class ellipse(Tag):
    required_class = {'ry': 'number', 'rx': 'number', 'cy': 'number', 'cx': 'number'}
    optional_class = {}
    class_len = 0

class feBlend(Tag):
    required_class = {'result': 'str', 'in2': 'str', 'mode': 'enum'}
    optional_class = {'in': ('A', 'enum')}
    class_len = 1

class feColorMatrix(Tag):
    required_class = {'type': 'str', 'values': 'number'}
    optional_class = {'in': ('A', 'enum'), 'result': ('C', 'str')}
    class_len = 1

class feComposite(Tag):
    required_class = {'in2': 'str', 'operator': 'enum'}
    optional_class = {'k1': ('AC', 'number'), 'k2': ('AG', 'number'), 'k3': ('AT', 'number'), 'k4': ('CA', 'number'), 'result': ('CG', 'str'), 'in': ('CT', 'enum')}
    class_len = 2

class feFlood(Tag):
    required_class = {'flood-opacity': 'number', 'result': 'str'}
    optional_class = {}
    class_len = 0

class feGaussianBlur(Tag):
    required_class = {'stdDeviation': 'number'}
    optional_class = {'in': ('A', 'enum'), 'result': ('C', 'str')}
    class_len = 1

class feMorphology(Tag):
    required_class = {'in': 'enum', 'operator': 'enum', 'radius': 'number', 'result': 'str'}
    optional_class = {}
    class_len = 0

class feOffset(Tag):
    required_class = {}  
    optional_class = {'dx': ('A', 'number'), 'dy': ('C', 'number')}
    class_len = 1

class filter(Tag):
    required_class = {'x': 'number', 'y': 'number', 'width': 'number', 'height': 'number', 'filterUnits': 'enum'}
    optional_class = {'filterRes': ('AG', 'number'), 'primitiveUnits': ('CG', 'enum'),  'color-interpolation-filters': ('CT', 'enum')}
    class_len = 2

class g(Tag):
    required_class = {}
    optional_class = {'filter': ('AG', 'str'), 'clip-path': ('AT', 'str'), 'mask': ('CG', 'str'), 'fill-rule': ('CT', 'enum')}
    class_len = 2

class linearGradient(Tag):
    required_class = {'x1': 'number', 'y1': 'number', 'x2': 'number', 'y2': 'number', 'gradientUnits': 'enum'}
    optional_class = {'gradientTransform': ('A', 'str'), 'href': ('C', 'str')}
    class_len = 1

class mask(Tag):
    required_class = {}
    optional_class = {'maskUnits': ('AA', 'enum'), 'x': ('AC', 'number'), 'y': ('AG', 'number'), 'width': ('AT', 'number'), 'height': ('CA', 'number'), 'maskContentUnits': ('CC', 'str'), 'style': ('CG', 'str')}
    class_len = 1

class path(Tag):
    required_class = {'d': 'pathd'}
    optional_class = {'fill-rule': ('AA', 'enum'), 'clip-rule': ('AC', 'enum'), 'stroke': ('AG', 'str'), 'stroke-width': ('AT', 'number'), 'stroke-linecap': ('CA', 'enum'), 'stroke-linejoin': ('CG', 'enum'), 'style': ('CT', 'str')}
    class_len = 2

class polygon(Tag):
    required_class = {'points': 'number'}
    optional_class = {'stroke': ('AG', 'str'), 'stroke-width': ('AT', 'number'), 'stroke-linecap': ('CG', 'enum'), 'stroke-linejoin': ('CT', 'enum')}
    class_len = 2

class polyline(Tag):
    required_class = {'points': 'number'}
    optional_class = {'stroke': ('AG', 'str'), 'stroke-width': ('AT', 'number'), 'stroke-linecap': ('CG', 'enum'), 'stroke-linejoin': ('CT', 'enum')}
    class_len = 2

class radialGradient(Tag):
    required_class = {'cx': 'number', 'cy': 'number', 'r': 'number', 'gradientUnits': 'enum'}  
    optional_class = {'gradientTransform': ('A', 'str')}
    class_len = 1

class rect(Tag):
    required_class = {'height': 'number', 'width': 'number'}
    optional_class = {'rx': ('AG', 'number'), 'ry': ('AT', 'number'), 'x': ('CG', 'number'), 'y': ('CT', 'number')}
    class_len = 2

class stop(Tag):
    required_class = {'stop-color': 'str'}
    optional_class = {'offset': ('A', 'str')}
    class_len = 1

class style(Tag):
    required_class = {}
    optional_class = {'type': ('A', 'str'), 'title': ('C', 'str')}
    class_len = 1

class svg(Tag):
    required_class = {'width': 'number', 'height': 'number', 'viewBox': 'str'}
    optional_class = {'x': ('AG', 'number'), 'y': ('AT', 'number'), 'style': ('CA', 'str'), 'version': ('CG', 'str'), 'xml:space': ('CT', 'str')}
    class_len = 2

class title(Tag):
    required_class = {'text': 'str'}
    optional_class = {}
    class_len = 0

class use(Tag):
    required_class = {}
    optional_class = {'x': ('AC', 'number'), 'width': ('AG', 'number'), 'height': ('AT', 'number'), 'y': ('CA', 'number'), 'fill-rule': ('CG', 'enum'), 'href': ('CT', 'str')}
    class_len = 2