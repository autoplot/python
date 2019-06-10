from autoplot import javaaddpath

def test_javaaddpath():
	org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
	assert org is not None

def test_APDataSet():
	org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
	apds = org.autoplot.idlsupport.APDataSet()
	assert apds is not None

def test_doGetDataSet():
	org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
	apds = org.autoplot.idlsupport.APDataSet()
	apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')
	apds.doGetDataSet()
	vv = apds.values()
	assert vv[0] == 3.4716999530792236
