'''This uses Autoplot Java/Swing GUIs to create URIs'''
from autoplot import *
import jpype

org = javaaddpath('http://autoplot.org/latest/autoplot.jar')

javax = jpype.JPackage('javax')
java = jpype.JPackage('java')
WindowManager = org.autoplot.datasource.WindowManager

oldURI = 'vap+cdaweb:'

parent = javax.swing.JPanel()
parent.setLayout( java.awt.BorderLayout() )

DataSourceEditorPanelUtil = org.autoplot.datasource.DataSourceEditorPanelUtil
p = DataSourceEditorPanelUtil.getDataSourceEditorPanel(None,oldURI);

if WindowManager.OK_OPTION == WindowManager.showConfirmDialog(
    None, p, "Editing URI", WindowManager.OK_CANCEL_OPTION ):
                                                          
    print( p.getURI() )
