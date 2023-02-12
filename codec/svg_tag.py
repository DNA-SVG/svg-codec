class Tag:
    required_attrs = []
    optional_attrs = {'id', 'class', 'style'}

    @classmethod
    def get_required(cls):
        return cls.required_attrs

    @classmethod
    def get_optional(cls):
        return cls.optional_attrs | Tag.optional_attrs


class circle(Tag):
    required_attrs = ['cx', 'cy', 'r']
    optional_attrs = set()


class g(Tag):
    optional_attrs = set()


class path(Tag):
    required_attrs = ['d']
    optional_attrs = set()


class polygon(Tag):
    required_attrs = ['points']
    optional_attrs = set()


class rect(Tag):
    required_attrs = ['height', 'width', 'x', 'y']
    optional_attrs = set(['rx', 'ry'])


class style(Tag):
    required_attrs = ['text']
    optional_attrs = set()


class ellipse(Tag):
    required_attrs = ['ry', 'rx', 'cy', 'cx']
    optional_attrs = set()


class defs(Tag):
    required_attrs = []
    optional_attrs = set()


class title(Tag):
    required_attrs = ['text']
    optional_attrs = set()


class filter(Tag):
    required_attrs = []
    optional_attrs = {'filterRes','filterUnits'}


class linearGradient(Tag):
    required_attrs = ['x1', 'y1', 'x2', 'y2']
    optional_attrs = {'gradientUnits', 'gradientTransform',
                      'spreadMethod', 'xlink:href'}


class stop(Tag):
    required_attrs = ['offset']
    optional_attrs = {'stop-color', 'stop-opacity'}
    
    
class feOffset(Tag):
    required_attrs = ['in','dx','dy']  
    optional_attrs = {'result'}
    
    
class feComposite(Tag):
    required_attrs = ['in', 'in2', 'operator']
    optional_attrs = {'k1', 'k2', 'k3' ,'k4' , 'result'}


class feColorMatrix(Tag):
    required_attrs = ['in', 'values']
    optional_attrs = {'type' , 'result'}


class feMerge(Tag):
    required_attrs = []
    optional_attrs = set()
    
    
class feMergeNode(Tag):
    required_attrs = ['in']
    optional_attrs = set()
   
class feGaussianBlur(Tag):
    required_attrs = ['in','stdDeviation']   
    optional_attrs = {'edgeNode','result'}
    
    
class svg(Tag):
    optional_attrs = {'width', 'height', 'viewBox', 'id', 'class', 'style'}
