# example for remapping a dataset 
#  1- to a named grid, 
#  2- to the grid of another dataset

from climaf.api import *
clog(logging.DEBUG)

# 1- regrid to a named grid : use operator 'regridn'
cdef("frequency","monthly")
dataloc(experiment="AMIPV6ALB2G", organization="example",url=[cpath+"/../examples/data/AMIPV6ALB2G"])
dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980")
dgr=regridn(dg,cdogrid="r90x45")
ncview(dgr)


# 2- regrid to the grid of another datset (here, a trivial case : same grid) :
# use operator 'regridn'
dg2=ds(experiment="AMIPV6ALB2G", variable="rst", period="1980")
dgr2=regrid(dg,dg2)
ncview(dgr2)

