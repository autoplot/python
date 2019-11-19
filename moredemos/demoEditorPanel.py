'''This uses Autoplot Java/Swing GUIs to create URIs'''
from autoplot import *
import jpype

org = javaaddpath('http://autoplot.org/latest/autoplot.jar')

oldURI = 'vap+cdaweb:'

javax = jpype.JPackage('javax')
java = jpype.JPackage('java')
parent = javax.swing.JPanel()
parent.setLayout( java.awt.BorderLayout() )

DataSourceEditorPanelUtil = org.autoplot.datasource.DataSourceEditorPanelUtil
p = DataSourceEditorPanelUtil.getDataSourceEditorPanel(parent,oldURI);

WindowManager = org.autoplot.datasource.WindowManager
if WindowManager.OK_OPTION == WindowManager.showConfirmDialog(
    None, p, "Editing URI", WindowManager.OK_CANCEL_OPTION ):
                                                          
    print( p.getURI() )
