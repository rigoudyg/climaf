import sys ; sys.path.append("/home/stephane/Bureau/climaf")
from climaf.api import *
#cproject("CMIP5"   ,"model","rip","frequency","table","realm","version")
cproject("example" ,"frequency" )
ds(project="example", experiment="AMIPV6ALB2G", period="1980",variable='tas')

data_pattern_L=cpath+"/../examples/data/${experiment}/L/${experiment}SFXYYYY.nc"
data_pattern_A=cpath+"/../examples/data/${experiment}/A/${experiment}PLYYYY.nc"
dataloc(project="example",organization="generic",url=[data_pattern_A,data_pattern_L])

rst=ds(project="example", experiment="AMIPV6ALB2G", variable="rst", period="1980-1981")
l=rst.baseFiles()
