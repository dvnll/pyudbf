### The pyudbf repository
A python implementation of the UDBF ("Universal Data Bin File") data format version 1.07. The UDBF format is e.g. frequently used for data exchange with 
Gantner Instruments data acquisition systems.

The main entrance to the module is pyudbf.py where two classes are defined. 
The class UDBFFileReader can be used to read a given UDBF file while the class UDBFBytesReader interprets bytestring data in UDBF.

The "tests"-folder contains a small example UDBF file and the reader script "udbf_file_reader.py" for testing. Run

```
python tests/udbf_file_reader.py --help
```

for usage information.

For use and integration in own Python projects, this project can be installed as a package as described below.

### Installation via pip directly from github.com

`pip install git+https://github.com/dvnll/pyudbf.git`

or

`python -m pip install git+https://github.com/dvnll/pyudbf.git`


### Installation via pip of downloaded code

`python -m pip install -e <path>`

or

`pip install -e <path>`

where "<path>" needs to be replaced by the actual local directory path to the downloaded files. Prior to the package installation the zipped files need to be extracted.

### Import in own projects

`from pyudbf import UDBFFileReader`

### Example code to read the provided UDBF file

The example file 'example.udbf' is located at './tests/example.udbf' and includes among others the channel 'camera links X':

```
# get access to the file
udbf_data = UDBFFileReader('./tests/example.udbf')

# show all information of data file header
print(udbf_data.header.__dict__)
print('Channel count: ' + str(udbf_data.n_channels))
print('Data point count: ' + str(udbf_data.n_points))
print('Data record: ' + str(udbf_data.runlength) + ' s')

# show all existing channels
print(udbf_data.header.channel_names)

# get data of specific channels
timestamp = udbf_data.timestamps
camera_links_X = udbf_data.signal(7)  # get values of selected channel by index
camera_links_X = udbf_data.channel('camera links X')  # get values of selected channel by name
```

### Technically, there are two main modules:
- UDBFParser.py implements various classes used to read and parse UDBF data.
- UDBFData.py implements two data-classes to store UDBF data. The UDBFHeader class stores meta-information while the UDBFData class stores e.g. the channel raw-data.
