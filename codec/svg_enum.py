class EnumDict:
    MAX_LENGTH = 2
    dict = {}
    dict['mode'] = {'normal': 'AC', 'multiply': 'CG', 'screen': 'GT', 'darken': 'TA', 'lighten': 'AG'}
    dict['operator'] = {'over': 'AC', 'in': 'AG', 'out': 'CA', 'atop': 'CT', 'xor': 'GA', 'lighter': 'GT', 'arithmetic': 'TC'}
    dict['filterUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['primitiveUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['color-interpolation-filters'] = {'linearRGB': 'A', 'sRGB': 'C'}
    dict['fill-rule'] = {'nonzero': 'A', 'evenodd': 'C'}
    dict['gradientUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['maskUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['clip-rule'] = {'nonzero': 'A', 'evenodd': 'C'}
    dict['stroke-linecap'] = {'butt': 'A', 'round': 'C', 'square': 'G'}
    dict['stroke-linejoin'] = {'miter': 'A', 'round': 'C', 'bevel': 'G'}
    dict['in'] = {'SourceGraphic': 'AC', 'SourceAlpha': 'AG', 'BackgroundImage': 'CA', 'BackgroundAlpha': 'CT', 'FillPaint': 'GA', 'StrokePaint': 'GT', '<filter-primitive-reference>': 'TC'}

    def get_encode_dict(self, attr_name, attr_value):
        return self.dict[attr_name][attr_value]
    def get_decode_dict(self, attr_name, seq, start_idx):
        decode_dict = {k: v for v, k in self.dict[attr_name].items()}
        length = 1
        while(length <= EnumDict.MAX_LENGTH):
            if seq[start_idx:start_idx + length] in decode_dict.keys():
                return decode_dict[seq[start_idx:start_idx + length]], start_idx + length
            length += 1
        return None, start_idx