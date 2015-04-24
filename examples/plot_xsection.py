#import sys; sys.path.append("/home/stephane/Bureau/climaf")
from climaf.api import *

# Define a dataset, using a built-in pre-defined datafile location
##################################################################
january_ta=ds(project='example',experiment="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")

# Compute zonal mean
ta_zonal_mean=ccdo(january_ta,operator="zonmean")

# Plot
plot=plotxsec(ta_zonal_mean)
cshow(plot)


# Compute meridional mean
ta_merid_mean=ccdo(january_ta,operator="mermean")

# Plot
plotm=plotxsec(ta_merid_mean)
cshow(plotm)

# Profile of global mean 
ta_profile=ccdo(ta_merid_mean,operator="zonmean")
plotp=plotxsec(ta_profile)
cshow(plotp)



# Newt line is used for systematic test suite
fig=cfile(plot) ; if (fig  is None) : exit(1)
