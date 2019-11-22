from __future__ import print_function

def printNoNewline(s):
    print(s, end=' ')
    
def javaaddpath(url='', jdwpPort=-1):
    '''Start up JVM, import JAR at URL, and import the paths starting with org 
    into the Python namespace.
      com= jpype.JPackage('com') 
    can be used to the com package into the Python namespace.
    Example:
      org = javaaddpath('http://autoplot.org/devel/autoplot.jar')
    if no url is provided, then the default http://autoplot.org/latest/autoplot.jar is used.
    '''

    import os
    import jpype
    import tempfile

    # TODO: Use requests package.
    try:
        # For Python 3.0 and later
        from urllib.request import urlopen
    except ImportError:
        # Fall back to Python 2's urllib2
        from urllib2 import urlopen

    if url=='':
        url='http://autoplot.org/latest/autoplot.jar'

    file_name = url.split('/')[-1]
    u = urlopen(url)
    i = u.info()
    file_size = int(i.get("Content-Length"))
    cacheFile = tempfile.gettempdir()+os.sep+file_name
    useCache = False
    if os.path.exists(cacheFile):
        cacheFileSize = os.path.getsize(cacheFile)
        print('cache file size: %d' % cacheFileSize)
        if cacheFileSize == file_size:
            useCache = True

    if useCache:
        print("Using existing file: %s" % cacheFile)

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
            printNoNewline(status)  # support Python 2.7 / 3.x

        print('')

        f.close()

    if not jpype.isJVMStarted():
        if jdwpPort > -1:
            print('Java is waiting for debugger at port %d' % jdwpPort)
            jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.class.path='+cacheFile, '-Xdebug',
                           '-Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=%d' % jdwpPort)

        else:
            print('Java is starting')
            jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.class.path='+cacheFile)
    else:
        print('Java is already running.')

    return jpype.JPackage("org")


def to_ndarray(apds, name):
    'extract the data identified by name to numpy array, using datetime64 for times.'
    import numpy as np
    import jpype
    org = jpype.JPackage('org')
    apds.setPreferredUnits('microseconds since 2000-01-01T00:00')
    u = org.das2.datum.Units.lookupUnits(apds.propertyAsString(name, 'UNITS'))
    if u.isConvertibleTo(org.das2.datum.Units.us2000):
        g_base = np.datetime64('2000-01-01T00:00:00Z')
        dd = apds.values(name)
        result = np.array([g_base + np.timedelta64(int(dd[i]*1000), 'ns') for i in range(len(dd))])
    else:
        dd = apds.values(name)
        result = np.array(dd)
    return result


def to_qdataset(X, Y=None, Z=None):
    '''convert the ndarrays or array like objects to Autoplot QDataSet objects.
    datetime64 are handled by converting to QDataSet with Units.us2000'''
    import jpype
    if not jpype.isJVMStarted():
        raise Exception('Java is not running, use javaaddpath')
    org = jpype.JPackage('org')
    dataset = org.das2.qds.ops.Ops.dataset
    link = org.das2.qds.ops.Ops.link
    transpose = org.das2.qds.ops.Ops.transpose
    import numpy as np

    if Y is None and Z is None:
        if isinstance(X, jpype.JavaObject):
            xds = X  # assume it's a QDataSet already
        else:
            if not hasattr(X, 'dtype'):
                X = np.array(X)
            if (str(X.dtype).startswith('datetime64') or str(X.dtype).startswith('<M8')):
                g_base = np.datetime64('2000-01-01T00:00:00Z')
                X = (X - g_base) / np.timedelta64(1000, 'ns')
                xds = dataset(jpype.JArray(jpype.JDouble, X.ndim)(X.tolist()))
                xds.putProperty(org.das2.qds.QDataSet.UNITS,
                                org.das2.datum.Units.us2000)
            else:
                xds = dataset(jpype.JArray(jpype.JDouble, X.ndim)(X.tolist()))
            if xds.rank() == 2:
                xds = transpose(xds)
        return xds
    elif Z is None:
        xds = to_qdataset(X)
        yds = to_qdataset(Y)
        return link(xds, yds)
    else:
        xds = to_qdataset(X)
        yds = to_qdataset(Y)
        zds = to_qdataset(Z)
        return link(xds, yds, zds)


def show_completions( s ):
    'print completions for the given URI.'
    import jpype
    org= javaaddpath()
    sc= org.autoplot.ScriptContext
    xxs= sc.getCompletions( s )
    for x in xxs:
        print(x)
    

#def applot(X, Y=None, Z=None):
#    'plot Python arrays or ndarrays in Autoplot'
#    import jpype
#    if not jpype.isJVMStarted():
#        raise Exception('Java is not running, use javaaddpath')
#    ds = to_qdataset(X, Y, Z)
#    org = jpype.JPackage('org')
#    sc = org.autoplot.ScriptContext
#    sc.plot(ds)

def das2stream( dataStruct, filename, ytags=None, ascii=1, xunits='' ):

    print( 'writing das2stream to ' + filename )
    import time

    streamHeader= [ '[00]xxxxxx<stream source="applot.pro" localDate="'+time.asctime()+'">', '</stream>' ]
    contentLength= -10  # don't include the packet tag and content length
    for i in range( len( streamHeader ) ):
        contentLength += len( streamHeader[i] ) + 1

    x= streamHeader[0]
    x= '[00]' + '%06d' % contentLength + x[10:]
    streamHeader[0]= x

    if ascii:
         xdatatype= 'ascii24'
    else:
         xdatatype= 'sun_real8'
    if ascii:
         datatype= 'ascii16'
    else:
         datatype='sun_real8'

    packetDescriptor= [ '[01]xxxxxx<packet>' ]
    tags= dataStruct['tags']
    nt= len(tags)
    packetDescriptor.append( '   <x type="'+xdatatype+'" name="'+tags[0]+'" units="'+xunits+'" />' )

    totalItems=1

    format=['%24.12f']
    reclen= 4 + 24 + (nt-1) * 20
    i=0
    for tag in tags:
        d= dataStruct[tag]
        if ( i==0 ):
            name=''
            i=i+1
            continue
        else:
            name= tags[i]    ### stream reader needs a default plane
        if ( isinstance( d, list ) ):
            rank= 1
        elif ( hasattr( d, "shape") ):  # check for numpy
            rank= len(d.shape)

        if ( rank==1 ):
            packetDescriptor.append( '   <y type="'+datatype+'" name="'+name+'" units="" idlname="'+tags[i]+'" />' )

            if ( i<nt-1 ): format.append('%16.4e')
            else: format.append( '%15.3e' )
            totalItems= totalItems + 1
        else:
            if ytags==None: ytags= range(s[2])
            sytags= ','.join( [ "%f"%n for n in ytags ] )
            nitems= len(ytags)
            packetDescriptor.append( '   <yscan type="' +datatype+'" name="' +name +'" units="" nitems="'+str(nitems) +'" yTags="'+sytags+'"' +' />' )
 
            for i in range(1,nitems):
                format.append('%16.4e')
            if ( i<nt-1 ):
                format.append('%16.4e')
            else:
                format.append('%15.4e')
            totalItems+= nitems
        i=i+1;

    packetDescriptor.append( '</packet>' )

    contentLength= -10 # don't include the packet tag and content length
    for i in range(0,len(packetDescriptor)):
        contentLength += len( packetDescriptor[i] ) + 1
  
    x= packetDescriptor[0]
    x= x[0:4]+'%06d' % contentLength + x[10:]
    packetDescriptor[0]= x

    unit= open( filename, 'wb' )

    for i in range(len(streamHeader)):
        unit.write( bytes(streamHeader[i],'utf8') )
        unit.write( bytes('\n','utf8') )

    for i in range(len(packetDescriptor)):
        unit.write( bytes(packetDescriptor[i],'utf8') )
        unit.write( bytes('\n','utf8') )   

    nr= len( dataStruct['x'] )
 
    keys= dataStruct.keys()

    newline= ascii
    for i in range(nr):
        unit.write( bytes(':01:','utf8') )
        for j in range(nt):
            tag= tags[j]
            if ( ascii ):
               rec= dataStruct[tag][i]
               if hasattr(rec, "__len__"):
                   l= len(rec)
                   for k in range(l):
                       s= format[j] %  rec[k]
                       unit.write( bytes(s,'utf8') )
                   if ( j==nt-1 ): newline=False
               else:
                   s= format[j] % rec
                   unit.write( bytes(s,'utf8') )
            else:
               import struct
               rec= dataStruct[tag][i]
               if hasattr(rec, "__len__"):
                   l= len(rec)
                   for j in range(l):
                       unit.write( struct.pack( '>d', rec[j] ) )
               else:
                   unit.write( struct.pack( '>d', rec ) )

        if ( newline ): unit.write( bytes('\n','utf8') )

    unit.close() 


def qstream(dataStruct, filename, ytags=None, ascii=True, xunits='', delta_plus=None, delta_minus=None):
    """for rank 2, ytags must be specified ascii, boolean, use ascii transfer types"""
    tags = dataStruct['tags']
    nt = len(tags)
    name = tags[-1]
    tname = tags[0]

    print('writing qstream to ' + filename)
    import time

    streamHeader = ['<stream dataset_id="'+name+'" source="applot.pro" localDate="'+time.asctime()+'">', '</stream>']
    contentLength= 0
    for i in range(len(streamHeader)):
        contentLength += len( streamHeader[i] ) + 1

    x = streamHeader[0]
    x = '[00]' + '%06d' % contentLength + x
    streamHeader[0] = x

    if ascii: 
        xdatatype = 'ascii24'
    else: 
        xdatatype = 'double'
    if ascii: 
        datatype = 'ascii16'
    else: 
        datatype = 'double'

    if ytags != None:
        ny = len(ytags)
        svals = str(ytags[0])
        for j in range(1,len(ytags)):
            svals = svals+','+str(ytags[j]).strip()

        dep1Descriptor = [ '<packet>' ]
        dep1Descriptor.append( '     <qdataset id="DEP1" rank="1" >' )
        dep1Descriptor.append( '       <properties>' )
        dep1Descriptor.append( '           <property name="NAME" type="String" value="DEP1" />')
        dep1Descriptor.append( '       </properties>' )
        dep1Descriptor.append( '       <values encoding="'+datatype+'" length="'+str(ny)+'" values="'+svals+'" />' )
        dep1Descriptor.append( '     </qdataset>' )
        dep1Descriptor.append( '     </packet>' )

        contentLength = 0 # don't include the packet tag and content length
        for i in range( len( dep1Descriptor ) ):
            contentLength += len( dep1Descriptor[i] ) + 1
      
        x = dep1Descriptor[0]
        x = '[02]' + '%06d' % contentLength + x
        dep1Descriptor[0] = x

    packetDescriptor = [ '[01]xxxxxx<packet>' ]

    nt = len(tags)
    packetDescriptor.append(  '     <qdataset id="'+tname+'" rank="1" >' )
    packetDescriptor.append(  '       <properties>' )
    packetDescriptor.append(  '           <property name="NAME" type="String" value="'+tname+'" />' )
    packetDescriptor.append(  '           <property name="UNITS" type="units" value="'+xunits+'" />' )
    packetDescriptor.append(  '       </properties>' )
    packetDescriptor.append(  '       <values encoding="'+xdatatype+'" length="" />' )
    packetDescriptor.append(  '     </qdataset>' )

    totalItems = 1

    format = ['%24.12f']
    formats = {'x':format}
   
    reclen = 4 + 24 + (nt-1) * 20

    i = 1
    for tag in tags[1:]:
        formats1 = []
        d = dataStruct[tag]
        if isinstance(d, list):
            rank = 1
        elif hasattr(d, "shape"):  # check for numpy
            rank = len(d.shape)

        name = tag  ### stream reader needs a default plane
        if rank == 1:
            packetDescriptor.append(  '     <qdataset id="'+name+'" rank="1" >' )
            packetDescriptor.append(  '       <properties>' )
            packetDescriptor.append(  '           <property name="NAME" type="String" value="'+name+'" />' )
            packetDescriptor.append(  '           <property name="DEPEND_0" type="qdataset" value="'+tname+'" />' )
            if i == 1:
                if not delta_plus is None:
                    packetDescriptor.append(  '           <property name="DELTA_PLUS" type="qdataset" value="'+delta_plus+'" />' )
                if not delta_minus is None:
                    packetDescriptor.append(  '           <property name="DELTA_MINUS" type="qdataset" value="'+delta_minus+'" />' )
            packetDescriptor.append(  '       </properties>' )
            packetDescriptor.append(  '       <values encoding="'+datatype+'" length="" />' )
            packetDescriptor.append(  '     </qdataset>' )
            if i<nt-1:
                formats1.append('%16.4e')
            else:
                formats1.append('%15.4e')
            totalItems += 1
        else:
            nitems = d.shape[1]
            packetDescriptor.append(  '   <qdataset id="'+name+'" rank="2" >' )
            packetDescriptor.append(  '       <properties>' )
            packetDescriptor.append(  '           <property name="DEPEND_0" type="qdataset" value="'+tname+'" />' )
            packetDescriptor.append(  '           <property name="DEPEND_1" type="qdataset" value="DEP1" />' )
            packetDescriptor.append(  '           <property name="NAME" type="String" value="'+name+'" />' )
            packetDescriptor.append(  '       </properties>' )
            packetDescriptor.append(  '       <values encoding="'+datatype+'" length="'+str(nitems)+'" />' )
            packetDescriptor.append(  '   </qdataset>' )
            for i in range(0, nitems-1):
                formats1.append('%16.4e')
            if i<nt-1: 
                formats1.append('%16.4e')
            else:
                formats1.append('%15.4e')
            totalItems += nitems
        i = i+1
        formats[tag] = formats1
    packetDescriptor.append(  '</packet>' )

    contentLength = -10  # don't include the packet tag and content length
    for i in range(len(packetDescriptor) ):
        contentLength += len( packetDescriptor[i] ) + 1

    x = packetDescriptor[0]
    x = x[0:4] + '%06d' % contentLength + x[10:]
    packetDescriptor[0] = x

    unit = open(filename, 'wb')

    for i in range(len(streamHeader)):
        unit.write(bytes(streamHeader[i],'utf8'))
        unit.write(bytes('\n','utf8'))

    for i in range(len(packetDescriptor)):
        unit.write(bytes(packetDescriptor[i],'utf8'))
        unit.write(bytes('\n','utf8'))

    nr = len( dataStruct['x'] )

    if not ytags is None:
        for i in range(len(dep1Descriptor)):
            unit.write(bytes(dep1Descriptor[i],'utf8'))
            unit.write(bytes('\n','utf8'))

    nr = len(dataStruct['x'])  # number of records to output

    keys = dataStruct.keys()

    newline = False
    for i in range(nr):
        unit.write(bytes(':01:','utf8'))
        for j in range(nt):
            tag = tags[j]
            format = formats[tag]
            if ascii:
                rec = dataStruct[tag][i]
                if hasattr(rec,'__len__'):
                    l = len(rec)
                    for k in range(l):
                        #print( format[k] )
                        s = format[k] % rec[k]
                        unit.write(bytes(s, 'utf8'))
                else:
                    s = format[0] % rec
                    unit.write(bytes(s, 'utf8'))
                if ( j == nt-1 ): 
                    newline = True
            else:
                import struct
                rec = dataStruct[tag][i]
                if hasattr(rec, '__len__'):
                    l = len(rec)
                    for j in range(l):
                        unit.write(struct.pack('>d', rec[j]))
                else:
                    unit.write(struct.pack('>d',rec))
        if ( newline ):
            unit.write(bytes('\n', 'utf8'))
    unit.close()


def tryPortConnect( host, port ):
    print('tryPortConnect')
    import socket
    s = socket.socket()
    s.connect(('localhost',port))
    s.close()


def sendCommand( s, cmd ):
    s.send( bytes(cmd,'utf8') )
    print('done')

def applot( x=None, y=None, z=None, z4=None, xunits='', ylabel='', tmpfile=None, noplot=0, respawn=0, delta_plus=None, delta_minus=None ):
    '''
NAME:
    plot
PURPOSE:
    Plot to Autoplot instead of the direct graphics plotting, by creating a temporary file of the data and sending a plot
    command to Autoplot with the server turned on.
ARGUMENTS:
    X,Y,Z as with plot.  If X is an integer, then it is the position in Autoplot, so that multiple plots can be sent to 
      one Autoplot canvas.
CALLING SEQUENCE:
    applot( X, Y )
    applot( X, Y, Z )  for a spectrogram

KEYWORDS:
   tmpfile=     explicitly set the file used to move data into Autoplot.  This can also be used with /noplot
   noplot=True  just make the tmpfile, don't actually try to plot.
   xunits=      units as a string, especially like "seconds since 2010-01-01T00:00"
   ylabel=''    label is currently ignored.
   delta_plus=  array of positive lengths showing the upper limit of the 1-sigma confidence interval.
   delta_minus= array of positive lengths showing the lower limit of the 1-sigma confidence interval.
'''

    port= 12345

    useDas2Stream=False

    if useDas2Stream:    
        ext='d2s'
    else:
        ext='qds'

    if ( delta_plus!=None ):
        ext='qds'
   
    if tmpfile==None:
        import datetime
        dt= datetime.datetime.today()
        tag= dt.strftime("%Y%m%dT%H%M%S")
        import glob
        ff= glob.glob( '/tmp/' + 'autoplot.' + tag + '.???.'+ext )
        seq= '.%03d.' % len(ff)
        tmpfile= '/tmp/' + 'autoplot.' + tag + seq + ext  
    else:
        if ( tmpfile.index('.'+ext) != len(tmpfile)-4 ):
            tmpfile= tmpfile + '.'+ext  # add the extension

    if ( not z4 is None ): 
        np=4
    elif ( not z is None ): 
        np=3
    elif( not y is None ): 
        np=2
    elif( not x is None ): 
        np=1
    else:
        raise Exception("no x, which must be specified")
       
   # serialize the data to a das2stream in a temporary file
    if isinstance( x, int ):
        pos= x
        xx= y
        if ( not z is None ):
            yy= z
        if ( not z4 is None ):
            zz= z4
        np= np-1
    else:
        pos= -1
        xx= x
        if ( not y is None ):
            yy= y
        if ( not z is None ):
            zz= z
   
    ascii=1

    if ext=='qds':
     
        if np==3:
            data= { 'x':xx, 'z':zz, 'tags':['x','z'] }
            qstream( data, tmpfile, ytags=yy, xunits=xunits, ascii=ascii  )
        elif np==2:
            if ( delta_plus!=None ):
                data= { 'x':xx, 'y':yy, 'delta_plus':delta_plus, 'delta_minus':delta_minus, 'tags':['x','y','delta_plus','delta_minus'] }
                qstream( data, tmpfile, ascii=ascii, xunits=xunits, delta_plus='delta_plus', delta_minus='delta_minus'  )
            else:
                data= { 'x':xx, 'y':yy, 'tags':['x','y'] }
                qstream( data, tmpfile, ascii=ascii, xunits=xunits  )
        else:
            ndim= len( xx.shape )
            if ndim==2:
                data= { 'x':range(len(xx)), 'z':xx, 'tags':['x','z'] }
                qstream( data, tmpfile, ytags=range(xx.shape[1]), ascii=ascii, xunits='' )
            else:
                if ( delta_plus!=None and delta_minus!=None ):
                    data= { 'x':range(len(xx)), 'y':xx, 'delta_plus':delta_plus, 'delta_minus':delta_minus, 'tags':['x','y','delta_plus','delta_minus']  }
                    qstream( data, tmpfile, ascii=ascii, xunits='', delta_plus='delta_plus', delta_minus='delta_minus' )
                else:
                    data= { 'x':range(len(xx)), 'y':xx, 'tags':['x','y']  }
                    qstream( data, tmpfile, ascii=ascii, xunits='' )
             
    else:
        if np==3:
            data= { 'x':xx, 'z':zz, 'tags':['x','z']  }
            das2stream( data, tmpfile, ytags=yy, xunits=xunits, ascii=ascii )
        elif np==2:
            data= { 'x':xx, 'y':yy, 'tags':['x','y'] }
            das2stream( data, tmpfile, ascii=ascii, xunits=xunits )
        else:
            rank=1
            if ( rank==2 ):
                data= { 'x':range(len(xx)), 'z':xx, 'tags':['x','z']  }
                das2stream( data, tmpfile, ytags=range(s[2]), ascii=ascii, xunits='' )
            else:
                data= { 'x':range(len(xx)), 'y':xx, 'tags':['x','y']  }
                das2stream( data, tmpfile, ascii=ascii, xunits='' )
    
    if noplot==1:
      return

    err= 0
    if ( err==0 ):
        import socket
        s = socket.socket()
        s.connect(('localhost',port))

        if ( pos>-1 ):
            cmd= 'plot( '+str(pos)+', "file:'+tmpfile+'" );\n'  # semicolon means no echo

        else:
            cmd= 'plot( "file:'+tmpfile+'" );\n'  # semicolon means no echo

        foo= sendCommand( s, cmd )
        s.shutdown(1)
        s.close()

    else:
        raise Exception( 'error encountered!' )
      
