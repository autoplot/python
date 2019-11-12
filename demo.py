from autoplot import javaaddpath,toDateTime

org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
apds = org.autoplot.idlsupport.APDataSet()

apds.setDataSetURI('vap+cdaweb:ds=OMNI2_H0_MRG1HR&id=DST1800&timerange=Oct+2016')
apds.doGetDataSet()

print( apds.toString() )

vv= apds.values('DST' )
tt= toDateTime( apds, 'Epoch' )

from matplotlib import pyplot as plt

plt.plot(tt,vv)
plt.show()

