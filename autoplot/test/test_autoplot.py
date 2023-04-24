import autoplot as ap
from autoplot import javaaddpath
import jpype

def test_javaaddpath():
    javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
    clas = jpype.JClass("org.autoplot.idlsupport.APDataSet")
    assert clas is not None

def test_APDataSet():
    javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
    apds = jpype.JClass("org.autoplot.idlsupport.APDataSet")
    assert apds is not None

def test_doGetDataSet():
    ap.javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
    apds = ap.APDataSet()
    apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')
    apds.doGetDataSet()
    vv = apds.values()
    assert vv[0] == 3.4716999530792236

