import xml.etree.ElementTree as ET
import pytest, ruff

from .encode_attr_type import str_to_seq, number_to_seq
from .decode_attr_type import decode as decoder
from .svg_type import SVGCoordinate, SVGNumber, SVGString
from .path_d import ParserPathD
from .svg_code import decode_tag, encode_tag
from .segment import optimize_seq_len, restore_seq_len
from .encode_svg import Encoder
from .decode_svg import Decoder
from .codec import Codec

filename = './test-images/amazon-pay.svg'

class TestAttr:
    def test_encode_attr(self):
        print(number_to_seq(-1))
        print(number_to_seq(45.0))
        print(number_to_seq(10, True))
        print(str_to_seq('_x34_0-Id_Card'))

    def test_decode_attr(self):
        assert(decoder(number_to_seq(-1))[0] == '-1')
        assert(decoder(number_to_seq(45.0))[0] == '45')
        assert(decoder(number_to_seq(10, True), is_size = True)[0] == 10)
        assert(decoder(str_to_seq('_x34_0-Id_Card'))[0] == '_x34_0-Id_Card')
    

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
        string = "M22.1363 17.0054V16.2814C22.134 16.2318 22.1524 16.1836 22.187 16.1487C22.2216 16.1137 22.269 16.0954 22.3176 16.0982H25.5083C25.5568 16.0965 25.6039 16.1151 25.6386 16.1497C25.6733 16.1843 25.6927 16.2319 25.6922 16.2814V16.9046C25.6922 17.0089 25.6063 17.1456 25.4524 17.3612L23.7991 19.7682C24.4126 19.7533 25.0614 19.8471 25.6191 20.167C25.7221 20.223 25.7878 20.3311 25.791 20.4501V21.2285C25.791 21.3354 25.6767 21.459 25.5556 21.395C24.4972 20.8401 23.2408 20.8424 22.1844 21.4011C22.0735 21.4616 21.9575 21.3398 21.9575 21.2328V20.4922C21.9474 20.3176 21.9887 20.1439 22.0761 19.9934L23.9916 17.1886H22.321C22.2724 17.1905 22.2251 17.172 22.1901 17.1374C22.1552 17.1027 22.1358 17.055 22.1363 17.0054Z"
        codec = parser.encoder(string)
        print(len(codec), 'nts,','{:.2f}'.format(len(string) * 8 / len(codec)), 'bits/nt')
        ret, _ = parser.decoder(codec)
        print(ret)


class TestTag:
    def test_tag(self):
        root = ET.fromstring(
        '<svg width="64px" height="64px" viewBox="0 0 64px 64px" style="enable-background:new 0 0 64 64;" stroke="red"/>')
        s = encode_tag(root, 0)
        print(s)
        _ = decode_tag(s)
        root = ET.fromstring('<feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_503_3869" result="shape"/>')
        op = encode_tag(root, 0)
        print(op)
        _ = decode_tag(op)


class TestSegment:
    def test_dfs(self):

        with open(filename, 'r') as f:
            enc = Encoder()
            tree = ET.parse(f)
            dfsroot = tree.getroot()
            a = enc._Encoder__dfs(dfsroot)
            print(a)

    def test_segment(self):
        enc = Encoder()
        dec = Decoder()
        initial_encoding = enc.encode_file(filename)
        print(initial_encoding)
        initial_decode = dec.generate_svg(initial_encoding)
        optimized_encoding = optimize_seq_len(initial_encoding)
        restored = restore_seq_len(optimized_encoding)
        restore_decode = dec.generate_svg(restored)
        assert(set(restored) == set(initial_encoding))
        assert(initial_decode == restore_decode)


class TestCodec:
    def test_codec(self):
        codec = Codec()
        codec.outputDNAseq(filename, 'test_codec.txt')
        codec.outputSVG("test_codec.txt", 'test_result.svg')