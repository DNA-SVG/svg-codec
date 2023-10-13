import xml.etree.ElementTree as ET
import pytest, ruff

from .encode_attr_type import str_to_seq, number_to_seq
from .decode_attr_type import decode as decoder
from .svg_type import SVGCoordinate, SVGNumber, SVGString
from .svg_tag import svg
from .path_d import ParserPathD
from .svg_code import decode_optional, encode_optional
from .segment import optimize_seq_len, restore_seq_len
from .encode_svg import Encoder
from .decode_svg import Decoder
from .codec import Codec


class TestAttr:
    def test_encode_attr(self):
        print(number_to_seq(-1))
        print(number_to_seq(45.0))
        print(number_to_seq(10, True))
        print(str_to_seq('_x34_0-Id_Card'))

    def test_decode_attr(self):
        assert(decoder(number_to_seq(-1)) == '-1')
        assert(decoder(number_to_seq(45.0)) == '45')
        assert(decoder(number_to_seq(10, True), is_pos_int = True) == 10)
        assert(decoder(str_to_seq('_x34_0-Id_Card')) == '_x34_0-Id_Card')
    

class TestType:
    def test_type(self):
        n = SVGCoordinate('0,1', type='encoder').translate()
        m, _ = SVGCoordinate(n, type='decoder').translate()
        print(m)
        n = SVGNumber('38.7px .5px 40.83284px 0px', type='encoder').translate()
        print(n)
        m, _ = SVGNumber(n, type='decoder', start_idx=0).translate()
        print(m)
        s = SVGString('hello', type='encoder').translate()
        print(s)
        ss, _ = SVGString(s, type='decoder', start_idx=0).translate()
        print(ss)

    def test_path_d(self):
        parser = ParserPathD()
        string = 'M39.7,27.6c0-4.3-3.5-7.7-7.7-7.7s-7.7,3.5-7.7,7.7c0,2.4,1.1,4.5,2.8,5.9c-4.2,1.2-7.3,5-7.3,9.5c0,0.6,0.5,1.1,1.1,1.1H43c0.6,0,1.1-0.5,1.1-1.1c0-4.5-3.1-8.3-7.3-9.5C38.6,32.1,39.7,30,39.7,27.6z M26.5,27.6c0-3,2.5-5.5,5.5-5.5s5.5,2.5,5.5,5.5S35,33.1,32,33.1S26.5,30.6,26.5,27.6z M34.2,35.3c3.9,0,7.1,2.9,7.7,6.6H22.1c0.5-3.7,3.8-6.6,7.7-6.6H34.2z'
        codec = parser.encoder(string)
        print(len(codec), 'nts,','{:.2f}'.format(len(string) * 8 / len(codec)), 'bits/nt')
        ret, _ = parser.decoder(codec)
        print(ret)


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
        print(initial_encoding)
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