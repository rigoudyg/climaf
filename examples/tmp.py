from climaf.api import *
clog(logging.DEBUG)
#from climaf.site_settings import *
cdef("frequency","monthly") ;  cdef("project","CMIP5") ; cdef ("model","CNRM-CM5")
dataloc(experiment="AMIPV6ALB2G", organization="example", url=[cpath+"/../examples/data/AMIPV6ALB2G"])
#dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980-1981")
#print cfile(dg)
dg2=ds(experiment="AMIPV6ALB2G", variable="tas", period="198001-198002")
dg2=ds(experiment="AMIPV6ALB2G", variable="tas", period="19800101-19800201")
print cfile(dg2)
cdump()

dg2=ds(experiment="AMIPV6ALB2G", variable="tas", period="198002-198003")



avg=time_average(dg)
cshow(ncview(dg))


