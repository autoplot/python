import autoplot as ap
import time
org= ap.javaaddpath('http://autoplot.org/latest/autoplot.jar')
apds = org.autoplot.idlsupport.APDataSet()

apds.loadDataSet('vap+inline:findgen(4000,500)')  # that's 2 000 000 elements
t0= time.time()
dd = ap.to_ndarray( apds, 'ds_0' )
print( '%.1f s  for %s' % ( time.time()-t0, str(dd.shape) ) )
print( '----' )

apds.loadDataSet('vap+inline:findgen(2000000)')  # that's 2 000 000 elements
t0= time.time()
dd = ap.to_ndarray( apds, 'ds_0' )
print( '%.1f s for %s' % ( time.time()-t0, str(dd.shape) ) )
print( '----' )
