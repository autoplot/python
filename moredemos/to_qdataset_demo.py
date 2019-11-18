# This does not work presently.

from autoplot import *
org = javaaddpath('http://autoplot.org/jnlp/devel/autoplot.jar')

zz= to_qdataset( [ 1,2,3,4,5,6,4,3,2,1 ] )
applot( zz )

import numpy as np
delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
import matplotlib.mlab as mlab
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = 10.0 * (Z2 - Z1)
ds= to_qdataset( x, y, Z )
applot( zz )
