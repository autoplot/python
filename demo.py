import autoplot as ap

ap.javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
apds = ap.APDataSet()

apds.setDataSetURI('vap+cdaweb:ds=OMNI2_H0_MRG1HR&id=DST1800&timerange=Oct+2016')
apds.doGetDataSet()

print( apds.toString() ) # Shows DST with timetags "Epoch" is loaded.

vv= ap.to_ndarray(apds)
tt= ap.to_ndarray(apds, 'Epoch')

from matplotlib import pyplot as plt

plt.plot(tt,vv)
plt.show()

