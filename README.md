A python implementation of the UDBF ("Universal Data Bin File") data format version 1.07. The UDBF format is e.g. frequently used for data exchange with 
Gantner Instruments data acquisition systems.

The main entrance to the module is pyudbf.py where two classes are defined. 
The class UDBFFileReader can be used to read a given UDBF file while the class UDBFBytesReader interprets bytestring data in UDBF.

The "tests"-folder contains a small example UDBF file and the reader script "udbf_file_reader.py" for testing. Run

```
python tests/udbf_file_reader.py --help
```

for usage information.

Technically, there are two main modules:
- UDBFParser.py implements various classes used to read and parse UDBF data.
- UDBFData.py implements two data-classes to store UDBF data. The UDBFHeader class stores meta-information while the UDBFData class stores e.g. the channel raw-data.
