# example for 
#  1- defining a dataset restricted to a lat-lon box
#  2- applying a further, explicit extraction of a smaller lat-lon box
#
from climaf.api import *
clog(logging.DEBUG)

cdef("frequency","monthly")
dataloc(experiment="AMIPV6ALB2G", organization="EM",url=[cpath+"/../examples/data/AMIPV6ALB2G"])

dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980-1981", domain=[10,80,-50,40])
cobj(ncview(dg))
	
de=llbox(dg, latmin=30, latmax=60, lonmin=-30, lonmax=30)
cobj(ncview(de))


