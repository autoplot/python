Autoplot is a Java application which can read data from many sources, such as ASCII tables, NASA CDF files, and HDF5 files.  It can also read data from data servers, such as the server at NASA/Goddard/CDAWeb, Das2Servers used by the Radio and
Plasma Wave Group at the University of Iowa, and servers supporting the HAPI API.

Autoplot identifies data using "URIs", which are one-line strings containing a data source ID and configuration to read the data.  
These URIs can be created using the Autoplot application, available at http://autoplot.org/.
Data are read into a standard data model, QDataSet, which is easily adapted to Python using "JPype".
Helper procedures from the autoplot package convert QDataSets into ndarrays.

Autoplot/Python Interface Tools
-------------------------------

Install using `pip install autoplot`

.. code:: python

  import autoplot as ap

  # Download autoplot.jar if needed and return Python bridge object
  ap.init()

  # Create Autoplot Data Set.  This object manages loading the data and then containing it until extracted.
  apds = ap.APDataSet()

  # Set URI
  apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')

  # Get the data
  apds.doGetDataSet()

  print(apds.toString())
  # http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0
  # data: data[dep0=288] (dimensionless)
  # dep0: dep0[288] (days since 1899-12-30T00:00:00.000Z) (DEPEND_0)

  # Extract data values
  vv = ap.to_ndarray(apds, 'data')
  tt = ap.to_ndarray(apds, 'dep0')

  from matplotlib import pyplot as plt
  plt.plot(tt,vv)
  plt.show()

Contact
-------------------------------
Jeremy Faden <faden@cottagesystems.com>

