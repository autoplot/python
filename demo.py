from autoplot import javaaddpath

org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
apds = org.autoplot.idlsupport.APDataSet()

apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')
apds.doGetDataSet()

print( apds.toString() )

vv= apds.values()

from matplotlib import pyplot as plt

plt.plot(vv)
