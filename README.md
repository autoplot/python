Autoplot is a Java application which can read data from many sources, such as ASCII tables, NASA CDF files, and HDF5 files.  It can 
also read data from data servers, such as the server at NASA/Goddard/CDAWeb, Das2Servers used by the Radio and
Plasma Wave Group at the University of Iowa, and servers supporting the HAPI API.

Autoplot identifies data using "URIs", which are one-line strings containing a data source ID and configuration to read the data.  
These URIs can be created using the Autoplot application, available at http://autoplot.org/.
Data are read into a standard data model, QDataSet, which is easily adapted to Python using "JPype".
Helper procedures from the Autoplot package convert QDataSets into ndarrays.

# Autoplot/Python Interface Tools

The Autoplot/Python package is loaded using pip:

```sh-session
> pip install autoplot
```


Once the package is installed, in Python Autoplot is now accessible.

```python

from autoplot import *

# Download autoplot.jar, if needed, and load it into JPype's classpath.
javaaddpath('http://autoplot.org/latest/autoplot.jar')

# Create Autoplot Data Set, which is an object that loads and temporarily holds data.
apds = APDataSet()

# Set URI which will be loaded.
apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')

# Load the data, initially downloading files into Autoplot's cache.
apds.doGetDataSet()

print(apds.toString())
# http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0
# data: data[dep0=288] (dimensionless)
# dep0: dep0[288] (days since 1899-12-30T00:00:00.000Z) (DEPEND_0)

# Extract data values
vv = to_ndarray(apds)
tt = to_ndarray(apds, 'dep0')

from matplotlib import pyplot as plt
plt.plot(tt,vv)
plt.show()
```

# Changes are Coming
Over the past few years, Python and the JPype interface have changed and some examples no longer work.  The interface
was based on IDL and Matlab use, and a more precisely tuned interface for the Python community is needed.  (For example addjavapath is a Matlab command and is strange to Python programmers.)  This work should be done in 2023.  See https://github.com/autoplot/python/wiki/python_reset.

# Contact
Jeremy Faden <faden@cottagesystems.com>

See also https://github.com/autoplot/python/wiki
