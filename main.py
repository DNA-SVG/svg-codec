import argparse

from codec.codec import Codec
from simple_codec.simple import encode_file, decode_file

cdc = Codec()
actions = {
    "encode": cdc.outputDNAseq,
    "decode": cdc.outputSVG
}

actions_simple = {
    "encode": encode_file,
    "decode": decode_file
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simple", action='store_true', default=False, help="use simple program?")
    parser.add_argument("action", help="action to do:encode or decode?")
    parser.add_argument("infile", help="the input filename")
    parser.add_argument("outfile", help="the output filename")
    args = parser.parse_args()
    if args.action not in actions:
        parser.print_help()
        exit
    
    if args.simple:
        actions_simple[args.action](args.infile, args.outfile)
    else:
        actions[args.action](args.infile, args.outfile)