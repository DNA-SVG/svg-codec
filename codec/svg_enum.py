class EnumDict:
    dict = {}
    dict['mode'] = {'normal': 'AC', 'multiply': 'AG', 'screen': 'CT', 'darken': 'TC', 'lighten': 'TG'}
    dict['operator'] = {'over': 'AC', 'in': 'AG', 'erode': 'AT', 'out': 'CA', 'atop': 'CG', 'xor': 'CT', 'lighter': 'TA', 'arithmetic': 'TC', 'dilate': 'TG'}
    dict['filterUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['primitiveUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['color-interpolation-filters'] = {'linearRGB': 'A', 'sRGB': 'C'}
    dict['fill-rule'] = {'nonzero': 'A', 'evenodd': 'C'}
    dict['gradientUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['maskUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['maskContentUnits'] = {'userSpaceOnUse': 'A', 'objectBoundingBox': 'C'}
    dict['clip-rule'] = {'nonzero': 'A', 'evenodd': 'C'}
    dict['stroke-linecap'] = {'butt': 'A', 'round': 'C', 'square': 'T'}
    dict['stroke-linejoin'] = {'miter': 'A', 'round': 'C', 'bevel': 'T'}
    dict['in'] = {'SourceGraphic': 'AC', 'SourceAlpha': 'AG', 'BackgroundImage': 'CA', 'BackgroundAlpha': 'CG', 'FillPaint': 'TA', 'StrokePaint': 'TC'}
    dict['in2'] = {'shape': 'AC', 'SourceGraphic': 'AG', 'SourceAlpha': 'AT', 'hardAlpha': 'CA', 'BackgroundImage': 'CG', 'BackgroundAlpha': 'CT', 'BackgroundImageFix': 'TA', 'FillPaint': 'TC', 'StrokePaint': 'TG'}

    def get_encode_dict(self, attr_name, attr_value):
        return self.dict[attr_name].get(attr_value)
    def get_decode_dict(self, attr_name, seq, start_idx):
        decode_dict = {k: v for v, k in self.dict[attr_name].items()}
        length = len(next(iter(decode_dict.keys())))
        if seq[start_idx:start_idx + length] in decode_dict.keys():
            return decode_dict[seq[start_idx:start_idx + length]], start_idx + length
        return None, start_idx