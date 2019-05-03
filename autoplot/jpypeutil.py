def javaaddpath( url, jdwpPort=-1 ):
    '''Start up JVM, import JAR at URL, and import the path into the Python namespace.

    Example:
      org = javaaddpath('http://autoplot.org/jnlp/devel/autoplot.jar')
    '''

    import os
    import jpype
    import tempfile

    try:
        # For Python 3.0 and later
        from urllib.request import urlopen
    except ImportError:
        # Fall back to Python 2's urllib2
        from urllib2 import urlopen

    file_name = url.split('/')[-1]
    u = urlopen(url)
    i = u.info()
    file_size = int(i.get("Content-Length"))
    cacheFile = tempfile.gettempdir()+os.sep+file_name
    useCache = False
    if os.path.exists( cacheFile ):
       cacheFileSize= os.path.getsize( cacheFile )
       print('cache file size: %d' % cacheFileSize)
       if ( cacheFileSize==file_size ):
           useCache= True

    if useCache:
       print("Using existing file: %s" % cacheFile )

    else:
       print("Downloading: %s Bytes: %s" % (file_name, file_size))
         
       file_size_dl = 0
       block_sz = 8192

       f = open(cacheFile, 'wb')

       while True:
          buffer = u.read(block_sz)
          if not buffer:
              break
   
          file_size_dl += len(buffer)
          f.write(buffer)
          status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
          status = status + chr(8)*(len(status)+1)
          status = '\r' + status
          print( status, end='' )
       print('')

       f.close()
    
    if not jpype.isJVMStarted():
       if jdwpPort > -1:
           print('Java is waiting for debugger at port %d' % jdwpPort)
           jpype.startJVM(jpype.getDefaultJVMPath(),'-Djava.class.path='+cacheFile,'-Xdebug', '-Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=%d' % jdwpPort )

       else:
           print('Java is starting')
           jpype.startJVM(jpype.getDefaultJVMPath(),'-Djava.class.path='+cacheFile)
    else:
       print('Java is already running.')

    return jpype.JPackage("org")


def ndarray2qdataset( X, Y=None, Z=None ):
    import jpype
    if not jpype.isJVMStarted():
        raise Exception('Java is not running, use javaaddpath')
    org= jpype.JPackage('org')
    dataset= org.das2.qds.ops.Ops.dataset
    link= org.das2.qds.ops.Ops.link
    transpose= org.das2.qds.ops.Ops.transpose
    if ( Y is None and Z is None ):
        xds= dataset( jpype.JArray(jpype.JDouble,X.ndim)(X.tolist()) )
        if ( xds.rank()==2 ): xds= transpose( xds )
        return xds
    elif ( Z is None ):
        xds= dataset( jpype.JArray(jpype.JDouble,X.ndim)(X.tolist()) )
        if ( xds.rank()==2 ): xds= transpose( xds )
        yds= dataset( jpype.JArray(jpype.JDouble,Y.ndim)(Y.tolist()) )
        if ( yds.rank()==2 ): yds= transpose( yds )
        return link( xds, yds )
    else:
        xds= dataset( jpype.JArray(jpype.JDouble,X.ndim)(X.tolist()) )
        if ( xds.rank()==2 ): xds= transpose( xds )
        yds= dataset( jpype.JArray(jpype.JDouble,Y.ndim)(Y.tolist()) )
        if ( yds.rank()==2 ): yds= transpose( yds )
        zds= dataset( jpype.JArray(jpype.JDouble,Z.ndim)(Z.tolist()) )
        if ( zds.rank()==2 ): zds= transpose( zds )
        return link( xds, yds, zds )

"""
import numpy as np
delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
import matplotlib.mlab as mlab
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = 10.0 * (Z2 - Z1)
from jpypeutil import *
jpype= javaaddpath( 'https://ci-pw.physics.uiowa.edu/job/autoplot-release/lastSuccessfulBuild/artifact/autoplot/Autoplot/dist/autoplot.jar', jdwpPort=1141 )
ds= ndarray2qdataset( x, y, Z )
org= jpype.JPackage('org')
sc= org.autoplot.ScriptContext
sc.formatDataSet( ds, '/tmp/cdffile.cdf' )

"""
