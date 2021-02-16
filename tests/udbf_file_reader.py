from pyudbf import *
import argparse
import os
import time
import pprint


parser = argparse.ArgumentParser()
parser.add_argument("--in", action="store",
                    dest="IN", help="Input UDBF data file", required=True)
parser.add_argument("--out", action="store",
                    dest="OUT", help="Output ASCII data file",
                    default=None)

options = parser.parse_args()
infile = options.IN

udbf_data = UDBFFileReader(infile)

pprint.pprint(udbf_data.header.__dict__)

outfile = options.OUT
if outfile is not None:
    if os.path.isfile(outfile):
        print("Output file aready exists. Appending!")

    udbf_data.serialize_to_ascii(outfile)
