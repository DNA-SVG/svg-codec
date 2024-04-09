from codec.svg_type import SVGString

class tag_nt:
    __TAG_lENGTH = 6
    __TAG_NT = [
        'circle', 'clipPath', 'defs', 'desc', 'ellipse', 'feBlend', 'feColorMatrix', 'feComposite', 'feFlood', 'feGaussianBlur', 'feMorphology', 'feOffset', 'filter', 'g', 'g1', 'linearGradient', 'mask', 'path', 'polygon', 'polyline', 'radialGradient', 'rect', 'stop', 'style', 'svg', 'title', 'use', 'line'
    ]
    def get_tag_len(self):
        return self.__TAG_lENGTH
    def get_tag_nt(self, tag_name):
        order = self.__TAG_NT.index(tag_name)
        return format(order, '0' + str(self.__TAG_lENGTH) + 'b')
    def get_nt_tag(self, seq):
        order = int(seq, 2)
        return self.__TAG_NT[order]

class Tag:
    required_class = {}
    optional_class = {'id': ('1100', 'str'), 'class': ('1101', 'str'), 'fill': ('1110' ,'str'), 'transform': ('1111', 'trans')}
    class_len = 4

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
                ret[attr_name] = ('10' + SVGString(attr_name).encode(), 'str')
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
    optional_class = {'stroke': ('0010', 'str'), 'stroke-width': ('0011', 'number'), 'stroke-linecap': ('0110', 'enum'), 'stroke-linejoin': ('0111', 'enum')}
    class_len = 4

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
    optional_class = {'opacity': ('00', 'number')}
    class_len = 2

class feBlend(Tag):
    required_class = {'result': 'enum', 'in2': 'enum', 'mode': 'enum'}
    optional_class = {'in': ('00', 'enum')}
    class_len = 2

class feColorMatrix(Tag):
    required_class = {'type': 'enum', 'values': 'colormatrix'}
    optional_class = {'in': ('00', 'enum'), 'result': ('01', 'enum')}
    class_len = 2

class feComposite(Tag):
    required_class = {'in2': 'enum', 'operator': 'enum'}
    optional_class = {'k1': ('0001', 'number'), 'k2': ('0010', 'number'), 'k3': ('0011', 'number'), 'k4': ('0100', 'number'), 'result': ('0110', 'enum'), 'in': ('0111', 'enum')}
    class_len = 4

class feFlood(Tag):
    required_class = {'flood-opacity': 'number', 'result': 'enum'}
    optional_class = {}
    class_len = 0

class feGaussianBlur(Tag):
    required_class = {'stdDeviation': 'number'}
    optional_class = {'in': ('00', 'enum'), 'result': ('01', 'enum')}
    class_len = 2

class feMorphology(Tag):
    required_class = {'in': 'enum', 'operator': 'enum', 'radius': 'number', 'result': 'enum'}
    optional_class = {}
    class_len = 0

class feOffset(Tag):
    required_class = {}  
    optional_class = {'dx': ('00', 'number'), 'dy': ('01', 'number')}
    class_len = 2

class filter(Tag):
    required_class = {'x': 'number', 'y': 'number', 'width': 'number', 'height': 'number', 'filterUnits': 'enum'}
    optional_class = {'filterRes': ('0010', 'number'), 'primitiveUnits': ('0110', 'enum'),  'color-interpolation-filters': ('0111', 'enum')}
    class_len = 4

class g(Tag):
    required_class = {}
    optional_class = {'stroke': ('0001', 'str'), 'filter': ('0010', 'str'), 'clip-path': ('0011', 'str'), 'stroke-width': ('0100', 'number'), 'mask': ('0110', 'str'), 'fill-rule': ('0111', 'enum')}
    class_len = 4

class line(Tag):
    required_class = {'x1': 'number', 'x2': 'number', 'y1': 'number', 'y2': 'number'}
    optional_class = {'stroke': ('0010', 'str'), 'stroke-width': ('0011', 'number'), 'stroke-linecap': ('0100', 'enum'), 'stroke-linejoin': ('0110', 'enum')}
    class_len = 4

class linearGradient(Tag):
    required_class = {'x1': 'number', 'y1': 'number', 'x2': 'number', 'y2': 'number'}
    optional_class = {'gradientTransform': ('0010', 'trans'), 'href': ('0011', 'str'), 'gradientUnits': ('0110', 'enum')}
    class_len = 4

class mask(Tag):
    required_class = {'x': 'number', 'y': 'number', 'width': 'number', 'height': 'number'}
    optional_class = {'maskUnits': ('0010', 'enum'), 'maskContentUnits': ('0110', 'enum'), 'style': ('0111', 'str')}
    class_len = 4

class path(Tag):
    required_class = {'d': 'pathd'}
    optional_class = {'fill-rule': ('0000', 'enum'), 'clip-rule': ('0001', 'enum'), 'stroke': ('0010', 'str'), 'stroke-width': ('0011', 'number'), 'stroke-linecap': ('0100', 'enum'), 'stroke-linejoin': ('0110', 'enum'), 'style': ('0111', 'str')}
    class_len = 4

class polygon(Tag):
    required_class = {'points': 'number'}
    optional_class = {'stroke': ('0010', 'str'), 'stroke-width': ('0011', 'number'), 'stroke-linecap': ('0110', 'enum'), 'stroke-linejoin': ('0111', 'enum')}
    class_len = 4

class polyline(Tag):
    required_class = {'points': 'number'}
    optional_class = {'stroke': ('0010', 'str'), 'stroke-width': ('0011', 'number'), 'stroke-linecap': ('0110', 'enum'), 'stroke-linejoin': ('0111', 'enum')}
    class_len = 4

class radialGradient(Tag):
    required_class = {'cx': 'number', 'cy': 'number', 'r': 'number', 'gradientUnits': 'enum'}  
    optional_class = {'gradientTransform': ('00', 'trans')}
    class_len = 2

class rect(Tag):
    required_class = {'height': 'number', 'width': 'number', 'x': 'number', 'y': 'number'}
    optional_class = {'rx': ('00', 'number'), 'ry': ('01', 'number')}
    class_len = 2

class stop(Tag):
    required_class = {'stop-color': 'str'}
    optional_class = {'offset': ('00', 'number'), 'stop-opacity': ('01', 'number')}
    class_len = 2

class style(Tag):
    required_class = {'text': 'str'}
    optional_class = {'type': ('00', 'str'), 'title': ('01', 'str')}
    class_len = 2

class svg(Tag):
    required_class = {'width': 'number', 'height': 'number', 'viewBox': 'number'}
    optional_class = {'x': ('0010', 'number'), 'y': ('0011', 'number'), 'style': ('0100', 'str'), 'version': ('0110', 'str'), 'xml:space': ('0111', 'str')}
    class_len = 4

class title(Tag):
    required_class = {'text': 'str'}
    optional_class = {}
    class_len = 0

class use(Tag):
    required_class = {}
    optional_class = {'x': ('0001', 'number'), 'width': ('0010', 'number'), 'height': ('0011', 'number'), 'y': ('0100', 'number'), 'fill-rule': ('0110', 'enum'), 'href': ('0111', 'str')}
    class_len = 4