from autoplot import *
import jpype

print('This will cause some platforms to hang!')

org = javaaddpath('http://autoplot.org/latest/autoplot.jar')

java= jpype.JPackage('java')
if java.lang.System.getProperty('os.name') == 'Mac OS X':
    print( 'disabling GUI on Mac because it will hang' )
    java.lang.System.setProperty('java.awt.headless','true')

javax= jpype.JPackage('javax')
javax.swing.JOptionPane.showMessageDialog(None, 'Java Swing is Okay')

print('Things didn''t hang, so this platform is okay.')
