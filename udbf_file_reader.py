from UDBFParser import UDBFParser, BinaryFileReader
import argparse
import os
import logging
import time
from UDBFData import UDBFData


class UDBFFileData(UDBFData):

    def __init__(self, infile):


        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(message)s")

        self.infile = infile

        binary_reader = BinaryFileReader(infile)
        self.parser = UDBFParser(binary_reader)

        timestamps, signals = self.parser.signal()
        header = self.parser.header

        super().__init__(timestamps, signals, header)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", action="store",
                        dest="IN", help="Input UDBF data file", required=True)
    parser.add_argument("--out", action="store",
                        dest="OUT", help="Output ASCII data file",
                        default=None)

    options = parser.parse_args()
    infile = options.IN

    udbf_data = UDBFFileData(infile)

    udbf_data.header.print()

    outfile = options.OUT
    if outfile is not None:
        if os.path.isfile(outfile):
            print("Output file aready exists. Appending!")
            time.sleep(3)

        udbf_data.to_ascii(outfile)
