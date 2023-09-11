import xml.etree.ElementTree as ET

from .encode_attr_type import float_to_seq, int_to_seq, str_to_seq
from .decode_attr_type import decode as decoder
from .svg_type import SVGCoordinate, SVGNumber, SVGString
from .segment import optimize_seq_len, restore_seq_len
from . import encode_svg as encode
from . import decode_svg as decode
from .codec import outputDNAseq, outputSVG


class TestAttr:
    def test_decode_attr(self):
        print(decoder('GACTTTCCATCTTTCGATCGATCGG'))

    def test_encode_attr(self):
        print(int_to_seq(-1))
        print(float_to_seq(45.0))
        print(str_to_seq('_x34_0-Id_Card'))
    

class TestType:
    def test_type(self):
        n = SVGCoordinate('0,1', type='encoder').translate()
        m = SVGCoordinate(n, type='decoder').translate()[0]
        print(m)
        n = SVGNumber('38.7px .5px 40.83284px 0px', type='encoder').translate()
        print(n)
        m, _ = SVGNumber(n, type='decoder', start_idx=0).translate()
        print(m)
        s = SVGString('hello', type='encoder').translate()
        print(s)
        ss, _ = SVGString(s, type='decoder', start_idx=0).translate()
        print(ss)


class TestSegment:
    def test_dfs(self):
        file = './test-images/river.svg'
        tree = ET.parse(file)
        root = tree.getroot()
        a = encode.dfs(root, -1, 1, 0)
        print(a)

    def test_segment(self):
        filename = './test-images/river.svg'
        with open(filename, 'r') as f:
            root = ET.fromstring(f.read())
            initial_encoding = encode.dfs(root, -1, 1, 0)
            optimized_encoding = optimize_seq_len(initial_encoding)
            restored = restore_seq_len(optimized_encoding)
            assert(set(restored) == set(initial_encoding))
            assert(decode.generate_svg(initial_encoding) == decode.generate_svg(restored))


class TestCodec:
    def test_codec(self):
        file = './test-images/building-construction-education-svgrepo-com.svg'
        outputDNAseq(file, 'test_codec.txt')
        outputSVG("test_codec.txt", 'test_result.svg')