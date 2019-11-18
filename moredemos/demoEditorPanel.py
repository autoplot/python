
org= javaaddpath('http://autoplot.org/latest/autoplot.jar')
javax= jpype.JPackage('javax')

oldURI = 'vap+cdaweb:'

JOptionPane = javax.swing.JOptionPane
DataSourceEditorPanelUtil = org.autoplot.datasource.DataSourceEditorPanelUtil
p = DataSourceEditorPanelUtil.getDataSourceEditorPanel(None,oldURI);
if JOptionPane.OK_OPTION == JOptionPane.showConfirmDialog(None, 
                                                          p, 
                                                          "Editing URI", 
                                                          JOptionPane.OK_CANCEL_OPTION, 
                                                          JOptionPane.QUESTION_MESSAGE, None)
print( p.getURI() )
