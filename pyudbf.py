from UDBFParser import UDBFParser, BytesReader
from UDBFData import UDBFData


class UDBFFileReader(UDBFData):

    def __init__(self, infile: str):

        self.infile = infile
        with open(infile, mode="rb") as fin:
            data = fin.read()
	
        reader = BytesReader(data)
        parser = UDBFParser(reader)

        timestamps, signals = parser.signal()
        header = parser.header

        super().__init__(timestamps, signals, header)


class UDBFBytesReader(UDBFData):

    def __init__(self, udbf_data: bytes):

        reader = BytesReader(udbf_data)
        parser = UDBFParser(reader)

        timestamps, signals = parser.signal()
        header = parser.header

        super().__init__(timestamps, signals, header)
