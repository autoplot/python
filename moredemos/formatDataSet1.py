import numpy as np
delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
import matplotlib.mlab as mlab
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = 10.0 * (Z2 - Z1)
from autoplot import *
org= javaaddpath( 'http://autoplot.org/latest/autoplot.jar' )
ds= to_qdataset( x, y, Z )
sc= org.autoplot.ScriptContext
sc.formatDataSet( ds, '/tmp/cdffile.cdf' )
