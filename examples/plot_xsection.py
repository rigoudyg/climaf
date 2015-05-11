#import sys; sys.path.append("/home/stephane/Bureau/climaf")
from climaf.api import *
craz()

# Define a 3D dataset, using a pre-defined data set
##################################################################
january_ta=ds(project='example',experiment="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")

# plot map for first level
map=plot(january_ta,crs='January')
cshow(map)
# Plot on stereopolar grid
mapNH=plot(january_ta,crs='January',proj="NH",min=240,max=290,delta=5)
cshow(mapNH)

# Compute zonal mean and plot it
ta_zonal_mean=ccdo(january_ta,operator="zonmean")
zplot=plot(ta_zonal_mean,crs="Zonal mean")
cshow(zplot)

# Plot with vertical levels equally spaced (with their index)
zplotl=plot(ta_zonal_mean,crs='title',linp=1)
cshow(zplotl)

# Compute meridional mean and plot it 
ta_merid_mean=ccdo(january_ta,operator="mermean")
mplot=plot(ta_merid_mean,crs="Merdional mean")
cshow(mplot)

# Profile of global mean 
ta_profile=ccdo(ta_merid_mean,operator="zonmean")
gplot=plot(ta_profile, crs="TA profile, log(p)")
cshow(gplot)

# Same plot except levels equally spaced
gplotl=plot(ta_profile, crs="TA profile, lin(p)",linp=1)
cshow(gplotl)

# Plot horizontal profile : Meridional profile of zonal tas mean
jtas=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="198001")
tas_profile=ccdo(jtas,operator="zonmean")
profplot=plot(tas_profile, crs="Meridional tas profile")
cshow(profplot)


# Newt line is used for systematic test suite
fig=cfile(plot) ; if (fig  is None) : exit(1)

