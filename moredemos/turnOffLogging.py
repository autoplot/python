# this shows how to turn off logging messages when apds is created.

import autoplot
import jpype

jpype.startJVM(jpype.getDefaultJVMPath(),'-Dclasspath=/tmp/autoplot.jar')

# turn off logging
logging= jpype.JPackage('java.util.logging')
l= logging.Logger.getLogger('qdataset.bridge')
l.setLevel(logging.Level.WARNING)

org= javaaddpath('http://autoplot.org/devel/autoplot.jar')
org= jpype.JPackage('org')

apds = org.autoplot.idlsupport.APDataSet()
apds.setDataSetURI('vap+cdaweb:ds=OMNI2_H0_MRG1HR&id=DST1800&timerange=Oct+2016')
apds.doGetDataSet()
