import numpy as np
import matplotlib.mlab as mlab
from autoplot import *

delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = 10.0 * (Z2 - Z1)

# Use Autoplot to export the data to a CDF file
org = javaaddpath('http://autoplot.org/latest/autoplot.jar')
ds = to_qdataset(x, y, Z)
sc = org.autoplot.ScriptContext
sc.formatDataSet(ds, '/tmp/cdffile.cdf')

