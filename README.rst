Autoplot/Python Interface Tools
-------------------------------

Under development. 

Install using

`pip install autoplot`

```
from autoplot import javaaddpath

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

from matplotlib import pyplot as plt
plt.plot(vv)
```

Contact
-------------------------------

Jeremy Faden <faden@cottagesystems.net>

