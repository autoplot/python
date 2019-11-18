import numpy as np
import matplotlib.mlab as mlab
from autoplot import *


org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')

org.autoplot.ScriptContext.createGui()

zz = to_qdataset([1, 2, 3, 4, 5, 6, 4, 3, 2, 1])
applot(zz)

delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = 10.0 * (Z2 - Z1)

org = javaaddpath('http://autoplot.org/jnlp/latest/autoplot.jar')
org.autoplot.ScriptContext.createGui()
applot(x, y, Z)  # will convert to QDataSet internally

