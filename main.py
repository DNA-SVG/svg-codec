import argparse
import importlib

from codec.codec import outputDNAseq, outputSVG
simple = importlib.import_module("simple-codec.simple")
from simple import encode_file, decode_file

actions = {
    "encode": outputDNAseq,
    "decode": outputSVG
}

actions_simple = {
    "encode": encode_file,
    "decode": decode_file
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simple", type=int, required=False, default=0, help="use simple program?")
    parser.add_argument("action", help="action to do:encode or decode?")
    parser.add_argument("infile", help="the input filename")
    parser.add_argument("outfile", help="the output filename")
    args = parser.parse_args()
    if args.action not in actions:
        parser.print_help()
        exit
    
    if args.simple != 0:
        actions[args.action](args.infile, args.outfile)
    else:
        actions_simple[args.action](args.infile, args.outfile)