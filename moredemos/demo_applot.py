import autoplot as ap
import jpype
org = ap.javaaddpath()
apds = jpype.JClass('org.autoplot.idlsupport.APDataSet')()  # instaciate the class
apds.loadDataSet( 'vap+cdaweb:ds=OMNI2_H0_MRG1HR&id=DST1800&timerange=Oct+2016' )
epoch = ap.to_ndarray( apds,'Epoch' )
dst = ap.to_ndarray( apds,'DST' )
ap.applot( epoch,dst )
