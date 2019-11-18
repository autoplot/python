from autoplot import *
import jpype

print('This will cause some platforms to hang!')

org = javaaddpath('http://autoplot.org/latest/autoplot.jar')
javax= jpype.JPackage('javax')
javax.swing.JOptionPane.showMessageDialog(None, 'Java Swing is Okay')

print('Things didn''t hang, so this platform is okay.')
