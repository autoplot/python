# demo how Autoplot library is used to export data.  This
# loads an xls file into ndarrays, and then formats the 
# data to a CDF file.

from autoplot import javaaddpath, toDateTime

# Download autoplot.jar if needed and return Python bridge object
org = javaaddpath('http://autoplot.org/jnlp/devel/autoplot.jar')

# Create Autoplot Data Set
apds = org.autoplot.idlsupport.APDataSet()

# Set URI
apds.setDataSetURI('http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0')

# Get the data
apds.doGetDataSet()

print(apds.toString())
# http://autoplot.org/data/swe-np.xls?column=data&depend0=dep0
# data: data[dep0=288] (dimensionless)
# dep0: dep0[288] (days since 1899-12-30T00:00:00.000Z) (DEPEND_0)

# Extract data values
vv = as_ndarray( apds, 'data' )
tt = as_ndarray( apds, 'dep0' )

# Now export the same data using Autoplot
sc= org.autoplot.ScriptContext
ttqds= ndarray2qdataset( tt )
vvqds= ndarray2qdataset( tt, vv )

sc.formatDataSet( ttqds, '/tmp/swe-np.cdf?Times' )
sc.formatDataSet( vvqds, '/tmp/swe-np.cdf?Dens&append=T' )
