#!/usr/bin/python
# -*- coding: utf-8 -*-

# Example for plotting a Hovmoller diagram using NCL
# Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/hovm.html
# This example includes all plot types

from climaf.api import *
craz()

############
# 4D fields
############

## Define a 4D dataset: ta(time, plev, lat, lon)
ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1980")

#
# Mean on latitude axis: you must set only one point (xpoint, ypoint or zpoint) because rank=4 and a mean on latitude is done
#

# Plot a Hovmoller diagram on all domain, at level index 3, and using %c for 'fmt' (i.e. small month abbreviation e.g., Jun):
diag1=hovm(ta, title='Temperature', mean_axis='Lat', zpoint=3, fmt="%c") # => diag (x,t)
# Trigger computation of diag1 as a cached file
cshow(diag1)

# Diagram on domain [-10,0,-90,-80] at longitude close to 360 and where X and Y are inverted:
diag2=hovm(ta, title='Temperature', mean_axis='Lat', xpoint=360., fmt="%c",
           invXY=True, latS=-10, latN= 0, lonW=-90, lonE=-80) # => diag (t,z)

#
# Mean on longitude axis: you must set only one point (xpoint, ypoint or zpoint) because rank=4 and a mean on longitude is done
#

# Diagram on 'NINO1-2' box
diag3=hovm(ta, title='Temperature', mean_axis='Lon', ypoint=-80., fmt="%C", **hovm_params('NINO1-2')) # => diag (z,t)
# Diagram with 'CBR_wet' colorpalette and 'options' for tuning NCL graphic resources:
diag4=hovm(ta, title='Temperature', mean_axis='Lon', zpoint=1500., fmt="%C",
           color="CBR_wet", options="tiXAxisString=latitude|cnLinesOn=True") # => diag (y,t)

#
# No mean: section at different points => you must set two points (xpoint, ypoint or zpoint) because rank=4
#
diag5=hovm(ta, title='Temperature', mean_axis='Point', xpoint=2, zpoint=1500., fmt="%C") # => diag (y,t)
diag6=hovm(ta, title='Temperature', mean_axis='Point', xpoint=2, ypoint=3, fmt="%C", color="CBR_wet") # => diag (z,t)
diag7=hovm(ta, title='Temperature', mean_axis='Point', ypoint=3, zpoint=3, fmt="%C") # => diag (x,t)


############
# 3D fields
############

## Define a 3D dataset: tas(time, lat, lon)
tas=ds(project='example', simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")

#
# Mean on latitude axis => you must not set points because rank=3 and a mean on latitude is done
#
diag8=hovm(tas, title='2m_Temperature', mean_axis='Lat',fmt="%C",
           **hovm_params('NINO4')) # => diag (x,t). If you use xpoint/ypoint/zpoint, selected points are not considered.

#
# Mean on longitude axis => you must not set points because rank=3 and a mean on longitude is done
#
diag9=hovm(tas, title='2m_Temperature', mean_axis='Lon',fmt="%C",
           **hovm_params('NINO4')) # => diag (y,t). If you use xpoint/ypoint/zpoint, selected points are not considered.

#
# No mean: section at different points => you must set only one point (xpoint or ypoint) because rank=3
#
diag10=hovm(tas, title='2m_Temperature', mean_axis='Point', xpoint=2, fmt="%N", invXY=True) # => diag (t,y)
diag11=hovm(tas, title='2m_Temperature', mean_axis='Point', ypoint=2, fmt="%C", **hovm_params('NINO4')) # => diag (x,t)


## Compute 'ta' zonal mean => 3D field: ta_zonmean(time, plev, lat)
ta_zonmean=ccdo(ta, operator='zonmean')

#
# Mean on latitude axis => you must not set points because rank=3 and a mean on latitude is done
#
diag12=hovm(ta_zonmean, title='Zonal mean', mean_axis='Lat', fmt="%C",
            **hovm_params('GRL')) # => diag (z,t). If you use xpoint/ypoint/zpoint, selected points are not considered.

#
# No mean: section at different points => you have to select only one point (ypoint or zpoint) because rank=3
#
diag13=hovm(ta_zonmean, title='Zonal mean', mean_axis='Point', ypoint=2, fmt="%C", **hovm_params('GRL')) # => diag (z,t)
diag14=hovm(ta_zonmean, title='Zonal mean', mean_axis='Point', zpoint=1000., fmt="%C", **hovm_params('GRL')) # => diag (y,t)


## Compute 'ta' meridional mean => 3D field: ta_mermean(time, plev, lon)
ta_mermean=ccdo(ta, operator='mermean')

#
# Mean on longitude axis => you must not set points because rank=3 and a mean on longitude is done
#
diag15=hovm(ta_mermean, title='Meridional mean', mean_axis='Lon', fmt="%C",
            **hovm_params('NATL')) # => diag (z,t). If you use xpoint/ypoint/zpoint, selected points are not considered.

#
# No mean: section at different points => you have to select only one point (xpoint or zpoint) because rank=3
#
diag16=hovm(ta_mermean, title='Meridional mean', mean_axis='Point', xpoint=360., fmt="%C", **hovm_params('NATL')) # => diag (z,t)
diag17=hovm(ta_mermean, title='Meridional mean', mean_axis='Point', zpoint=2000., fmt="%C", **hovm_params('NATL')) # => diag (x,t)


############
# 2D fields
############

# If you use arguments 'mean_axis' and/or xpoint/ypoint/zpoint, they are not considered because rank=2
# -> plot supplied coordinates

## Compute 'tas' zonal mean => 2D field: tas_zonmean(time, lat)
tas_zonmean = ccdo(tas, operator='zonmean')

diag18=hovm(tas_zonmean, title='Zonal mean', fmt="%C", **hovm_params('NATL')) # => diag (y,t)

## Compute 'ta' mermean at level 1000 => 2D field: ta1000_zonmean(time, lon)
ta1000=ccdo(ta, operator='sellevel,1000') # (t,y,x)
ta1000_mermean=ccdo(ta1000, operator='mermean') # (t,x)

diag19=hovm(ta1000_mermean, title='Meridional mean', fmt="%C", options="tiXAxisString=longitude",
            **hovm_params('NINO3')) # => diag (x,t)

## Compute 'ta' space average => 2D field: sa(time, plev)
sa=space_average(ta)

diag20=hovm(sa, title='Space average', fmt="%C", **hovm_params('NINO3')) # => diag (z,t)
