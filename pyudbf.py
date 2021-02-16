from pyudbf.UDBFParser import UDBFParser, BinaryFileReader, BinaryReader
from pyudbf.UDBFData import UDBFData


class UDBFFileReader(UDBFData):

    def __init__(self, infile: str):

        self.infile = infile

        binary_reader = BinaryFileReader(infile)
        parser = UDBFParser(binary_reader)

        timestamps, signals = parser.signal()
        header = parser.header

        super().__init__(timestamps, signals, header)


class UDBFBytesReader(UDBFData):

    def __init__(self, udbf_data: bytes):

        binary_reader = BinaryReader(udbf_data)
        parser = UDBFParser(binary_reader)

        timestamps, signals = parser.signal()
        header = parser.header

        super().__init__(timestamps, signals, header)
