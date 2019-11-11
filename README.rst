Autoplot/Python Interface Tools
-------------------------------

Install using `pip install autoplot`

.. code:: python

  from autoplot import javaaddpath, toDateTime

  # Download autoplot.jar if needed and return Python bridge object
  org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')

  # Create Autoplot Data Set
  apds = org.autoplot.idlsupport.APDataSet()

  # Set URI
  apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')

  # Get the data
  apds.doGetDataSet()

  print(apds.toString())

  # Extract data values
  vv = apds.values()
  tt= toDateTime( apds, 'dep0' )

  from matplotlib import pyplot as plt
  plt.plot(tt,vv)
  plt.show()

Contact
-------------------------------

Jeremy Faden <faden@cottagesystems.net>

