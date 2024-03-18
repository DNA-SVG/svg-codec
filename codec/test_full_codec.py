import xml.etree.ElementTree as ET
import pytest, ruff

from .encode_attr_type import str_to_seq, number_to_seq
from .decode_attr_type  import seq_to_number, seq_to_str
from .transform import ParserTransform
from .svg_type import SVGNumber, SVGString
from .path_d import ParserPathD
from .svg_code import decode_tag, encode_tag
from .segment import optimize_seq_len, restore_seq_len
from .encode_svg import Encoder
from .decode_svg import Decoder
from .codec import Codec

filename = './test-images/amazon-pay.svg'
# filename = './test.svg'

class TestAttr:
    def test_encode_attr(self):
        print(number_to_seq(-1))
        print(number_to_seq(45.0))
        print(number_to_seq(10))
        print(str_to_seq('_x34_0-Id_Card'))

    def test_decode_attr(self):
        seq = number_to_seq(-1)
        assert(seq_to_number(seq, call_number=True)[0] == -1)
        seq = number_to_seq(45.0)
        assert(seq_to_number(seq, call_number=True)[0] == 45)
        seq = number_to_seq(10)
        assert(seq_to_number(seq, call_number=False)[0] == '10')
        dec = float(seq_to_number(number_to_seq(3.05176e-05))[0])
        assert(abs(dec - 3.05176e-05) < 1e-7)
        assert(seq_to_str(str_to_seq('_x34_0-Id_Card'))[0] == '_x34_0-Id_Card')


class TestType:
    def test_type(self):
        n = SVGNumber('38.7px .5px 40.83284px 0px').encode()
        print(n)
        m, _ = SVGNumber(n, start_idx=0).decode()
        print(m)
        s = SVGString('hello').encode()
        print(s)
        ss, _ = SVGString(s, start_idx=0).decode()
        print(ss)

    def test_path_d(self):
        parser = ParserPathD()
        string = "M28 3.05176e-05Z"
        codec = parser.encoder(string)
        print(len(codec), 'nts,',
              '{:.2f}'.format(len(string) * 8 / len(codec)), 'bits/nt')
        ret, _ = parser.decoder(codec)
        print(ret)
    
    def test_transform(self):
        parser = ParserTransform()
        string = 'matrix(-1 8.74228e-08 8.74228e-08 1 6 8) matrix(-1,8.74228e-08,8.74228e-08,1,6,8)'
        codec = parser.encoder(string)
        print(codec)
        ret, _ = parser.decoder(codec)
        print(ret)


class TestTag:
    def test_tag_1(self):
        root = ET.fromstring(
            '<svg width="64px" height="64px" viewBox="0 0 64px 64px" style="enable-background:new 0 0 64 64;" stroke="red"/>'
        )
        s = encode_tag(root, 0, 0)
        print(s)
        _ = decode_tag(s)
    
    def test_tag_2(self):
        root = ET.fromstring(
            '<feMorphology radius="8" operator="erode" in="SourceAlpha" result="effect1_innerShadow_397_2949"/>'
        )
        s = encode_tag(root, 0, 0)
        print(s)
        _ = decode_tag(s)

    def test_tag_3(self):
        root = ET.fromstring(
            '<radialGradient cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(8.11514 29.2951) rotate(46.5746) scale(306.642 308.519)"/>'
        )
        s = encode_tag(root, 0, 0)
        print(s)
        _ = decode_tag(s)

class TestSegment:
    def test_dfs(self):
        with open(filename, 'r') as f:
            enc = Encoder()
            tree = ET.parse(f)
            dfsroot = tree.getroot()
            dfsroot = enc._Encoder__pre_process(dfsroot)
            a = enc._Encoder__dfs(dfsroot)
            print(a)

    def test_segment(self):
        enc = Encoder()
        dec = Decoder()
        initial_encoding = enc.encode_file(filename)
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