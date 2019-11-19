from autoplot import *
import jpype

org= javaaddpath('http://autoplot.org/latest/autoplot.jar')
javax= jpype.JPackage('javax')

oldURI = 'vap+cdaweb:'

DataSourceEditorPanelUtil = org.autoplot.datasource.DataSourceEditorPanelUtil
p = DataSourceEditorPanelUtil.getDataSourceEditorPanel(None,oldURI);

if WindowManager.OK_OPTION == WindowManager.showConfirmDialog(
    None, p, "Editing URI", WindowManager.OK_CANCEL_OPTION ):
                                                          
    print( p.getURI() )
