A python implementation of the UDBF data format. The format is e.g. frequently used in Gantner data acquisition systems.

There are two main modules:
- UDBFParser implements various classes used to read and parse UDBF data.
- UDBFData implements two data-classes to store UDBF data. The UDBFHeader stores meta information while the UDBFData class stores e.g. the raw-data.

The main entrance to the code is udbf_file_reader.py which reads an UDBF file and converts it into an ASCII file. Call udbf_file_reader.py --help for usage information. The provided methods 
can be used to create more advanced I/O.

The folder test contains a small UDBF test file for testing.
