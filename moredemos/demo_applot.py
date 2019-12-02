import autoplot as ap
org = ap.javaaddpath()
apds = org.autoplot.idlsupport.APDataSet()
apds.loadDataSet( 'vap+cdaweb:ds=OMNI2_H0_MRG1HR&id=DST1800&timerange=Oct+2016' )
epoch = ap.to_ndarray( apds,'Epoch' )
dst = ap.to_ndarray( apds,'DST' )
ap.applot( epoch,dst )
