import sys ; sys.path.append("/home/stephane/Bureau/climaf")
from climaf.api import *
cproject("CMIP5"   ,"model","rip","frequency","table","realm","version")
cproject("EM"                    ,"frequency"                          )
ds(project="EM", experiment="AMIPV6ALB2G", period="1980",variable='tas')
