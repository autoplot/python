from autoplot import javaaddpath,toDateTime

org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
apds = org.autoplot.idlsupport.APDataSet()

apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')
apds.doGetDataSet()

print( apds.toString() )

vv= apds.values()
tt= toDateTime( apds, 'dep0' )

from matplotlib import pyplot as plt

plt.plot(tt,vv)
plt.show()

