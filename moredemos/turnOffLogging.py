# this shows how to turn off logging messages when apds is created.

import autoplot
import jpype

# wget -O /tmp/autoplot.jar https://ci-pw.physics.uiowa.edu/job/autoplot-release/1824/artifact/autoplot/Autoplot/dist/autoplot.jar
jpype.startJVM(jpype.getDefaultJVMPath(),'-Djava.class.path=/tmp/autoplot.jar')

# turn off logging
logging= jpype.JPackage('java.util.logging')
l= logging.Logger.getLogger('qdataset.bridge')
l.setLevel(logging.Level.WARNING)

org= jpype.JPackage('org')

apds = org.autoplot.idlsupport.APDataSet()
apds.setDataSetURI('vap+cdaweb:ds=OMNI2_H0_MRG1HR&id=DST1800&timerange=Oct+2016')
apds.doGetDataSet()
