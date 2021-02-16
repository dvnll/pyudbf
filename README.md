A python implementation of the UDBF ("Universal Data Bin File") data format version 1.07. The UDBF format is e.g. frequently used for data exchange with 
Gantner Instruments data acquisition systems.

The main entrance to the module are UDBFFileReader and UDBFBytesReader. The first can be used to read a given udbf file while the second interprets bytestring data in UDBF.

The "tests"-folder contains a small example UDBF file and the reader script "udbf_file_reader.py" for testing. Call udbf_file_reader.py --help for usage information.

Technically, there are two main modules:
- UDBFParser implements various classes used to read and parse UDBF data.
- UDBFData implements two data-classes to store UDBF data. The UDBFHeader stores meta-information while the UDBFData class stores e.g. the channel raw-data.
