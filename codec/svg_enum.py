class EnumDict:
    dict = {}
    dict['mode'] = {'normal': '000', 'multiply': '001', 'screen': '010', 'darken': '011', 'lighten': '100'}
    dict['operator'] = {'over': '0001', 'in': '0010', 'erode': '0011', 'out': '0100', 'atop': '0110', 'xor': '0111', 'lighter': '1000', 'arithmetic': '1001', 'dilate': '1011'}
    dict['filterUnits'] = {'userSpaceOnUse': '01', 'objectBoundingBox': '10'}
    dict['primitiveUnits'] = {'userSpaceOnUse': '01', 'objectBoundingBox': '10'}
    dict['color-interpolation-filters'] = {'linearRGB': '01', 'sRGB': '10'}
    dict['fill-rule'] = {'nonzero': '01', 'evenodd': '10'}
    dict['gradientUnits'] = {'userSpaceOnUse': '01', 'objectBoundingBox': '10'}
    dict['maskUnits'] = {'userSpaceOnUse': '01', 'objectBoundingBox': '10'}
    dict['maskContentUnits'] = {'userSpaceOnUse': '01', 'objectBoundingBox': '10'}
    dict['clip-rule'] = {'nonzero': '01', 'evenodd': '10'}
    dict['stroke-linecap'] = {'butt': '00', 'round': '10', 'square': '01'}
    dict['stroke-linejoin'] = {'miter': '00', 'round': '10', 'bevel': '01'}
    dict['in'] = {'SourceGraphic': '000', 'SourceAlpha': '001', 'BackgroundImage': '010', 'BackgroundAlpha': '011', 'FillPaint': '100', 'StrokePaint': '101'}
    dict['in2'] = {'shape': '0001', 'SourceGraphic': '0010', 'SourceAlpha': '0011', 'hardAlpha': '0100', 'BackgroundImage': '0101', 'BackgroundAlpha': '0110', 'BackgroundImageFix': '1000', 'FillPaint': '1001', 'StrokePaint': '1011'}
    dict['type'] = {'matrix': '000', 'saturate': '001', 'hueRotate': '010', 'luminanceToAlpha': '011', 'fractalNoise': '100', 'turbulence': '101'}
    dict['result'] = {'SourceGraphic': '0001', 'SourceAlpha': '0010', 'BackgroundImage': '0011', 'BackgroundAlpha': '0100', 'FillPaint': '0110', 'StrokePaint': '0111', 'shape': '1000', 'hardAlpha': '1001', 'BackgroundImageFix': '1011'}

    enum_len = {'mode': 3, 'operator': 4, 'filterUnits': 2, 'primitiveUnits': 2, 'color-interpolation-filters': 2, 'fill-rule': 2, 'gradientUnits': 2, 'maskUnits': 2, 'maskContentUnits': 2, 'clip-rule': 2, 'stroke-linecap': 2, 'stroke-linejoin': 2, 'in': 3, 'in2': 4, 'type': 3, 'result': 4}

    def get_encode_dict(self, attr_name, attr_value):
        return self.dict[attr_name].get(attr_value)
    def get_decode_dict(self, attr_name, seq, start_idx):
        decode_dict = {k: v for v, k in self.dict[attr_name].items()}
        end_idx = self.enum_len[attr_name] + start_idx
        if seq[start_idx:end_idx] in decode_dict.keys():
            return decode_dict[seq[start_idx:end_idx]], end_idx
        return None, start_idx