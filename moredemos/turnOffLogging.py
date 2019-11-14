# this shows how to turn off logging messages when apds is created.

import jpype
logging= jpype.JPackage('java.util.logging')

l= logging.Logger.getLogger('qdataset.bridge')
l.setLevel(logging.Level.WARNING)

org= javaaddpath('http://autoplot.org/devel/autoplot.jar')

apds = org.autoplot.idlsupport.APDataSet()
apds.setDataSetURI('vap+cdaweb:ds=OMNI2_H0_MRG1HR&id=DST1800&timerange=Oct+2016')
apds.doGetDataSet()
