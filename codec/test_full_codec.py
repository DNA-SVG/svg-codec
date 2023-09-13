import xml.etree.ElementTree as ET
import pytest, ruff

from .encode_attr_type import float_to_seq, int_to_seq, str_to_seq
from .decode_attr_type import decode as decoder
from .svg_type import SVGCoordinate, SVGNumber, SVGString
from .svg_tag import svg
from .svg_code import decode_optional, encode_optional
from .segment import optimize_seq_len, restore_seq_len
from .encode_svg import Encoder
from .decode_svg import Decoder
from .codec import Codec


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


class TestOptional:
    def test_optional(self):
        root = ET.fromstring(
        '<svg width="64px" height="64px" viewBox="0 0 64px 64px" style="enable-background:new 0 0 64 64;"/>')
        s = encode_optional(root, svg)
        print(s)
        ss = decode_optional(s)
        root = ET.fromstring(
        '<svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" id="1"/>')
        op = encode_optional(root, svg)
        deop = decode_optional(op)


class TestSegment:
    def test_dfs(self):
        filename = './test-images/river.svg'
        with open(filename, 'r') as f:
            enc = Encoder()
            tree = ET.parse(f)
            dfsroot = tree.getroot()
            a = enc._Encoder__dfs(dfsroot)
            print(a)

    def test_segment(self):
        filename = './test-images/river.svg'
        enc = Encoder()
        dec = Decoder()
        initial_encoding = enc.encode_file(filename)
        optimized_encoding = optimize_seq_len(initial_encoding)
        restored = restore_seq_len(optimized_encoding)
        assert(set(restored) == set(initial_encoding))
        assert(dec.generate_svg(initial_encoding) == dec.generate_svg(restored))


class TestCodec:
    def test_codec(self):
        codec = Codec()
        file = './test-images/building-construction-education-svgrepo-com.svg'
        codec.outputDNAseq(file, 'test_codec.txt')
        codec.outputSVG("test_codec.txt", 'test_result.svg')