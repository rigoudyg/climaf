# Example for general-purpose plot using NCL
# Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/gplot.html

from climaf.api import *
craz()

##########
# A map
##########

## one field ##

# without projection
surface_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="198001")

plot_map1=plot(surface_ta, title='A Map without contours lines')
cshow(plot_map1)

plot_map2=plot(surface_ta, contours=0, title='A Map without contours lines')
cshow(plot_map2)

plot_map3=plot(surface_ta, contours=1, title='A Map which contours lines follow color filled contours')
cshow(plot_map3)

plot_map4=plot(surface_ta, contours="290 291 292 293", title='A Map which contours lines don t follow color filled contours')
cshow(plot_map4)

# with projection
plot_map1b=plot(surface_ta, proj='NH', title='A Map without contours lines')
cshow(plot_map1b)

plot_map2b=plot(surface_ta, proj='NH', contours=0, title='A Map without contours lines')
cshow(plot_map2b)

plot_map3b=plot(surface_ta, proj='NH', contours=1, title='A Map which contours lines follow color filled contours')
cshow(plot_map3b)

plot_map4b=plot(surface_ta, proj='NH', contours="230 231 232 233", title='A Map which contours lines don t follow color filled contours')
cshow(plot_map4b)

# with vectors
duo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")
dvo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O") 
tos=ds(project="EM",simulation="PRE6CPLCr2alb", variable="tos", period="199807", realm="O")

tpath='/data/climaf/${project}/${model}/'
fixed_fields(['plot','plot_2fields'],
             ('angles.nc',tpath+'angle_ORCA1.nc'))

map_vect1=plot(tos, duo, dvo, title='SST without rotation of vectors on NEMO grid', vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
cshow(map_vect1)

map_vect2=plot(tos, duo, dvo, title='SST with rotation of vectors on NEMO grid', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
cshow(map_vect2)

map_vect3=plot(tos, duo, dvo, title='SST with contours lines and vectors', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, contours=1) #Vector style = "LineArrow" (default)
cshow(map_vect3)
 
map_vect4=plot(tos, duo, dvo, title='SST with curly vectors', rotation=1, vcRefLengthF=0.005, vcRefMagnitudeF=0.02, vcGlyphStyle="CurlyVector", vcLineArrowColor="yellow")
cshow(map_vect4)

map_vect5=plot(tos, duo, dvo, title='SST, proj=NH', rotation=1, vcRefLengthF=0.005, vcRefMagnitudeF=0.02, proj="NH")
cshow(map_vect5)


## two fields ##

# without projection
map_field2=llbox(surface_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'surface_ta' sub box for auxiliary field

plot_map5=plot_2fields(surface_ta, map_field2, contours='230 240 250 260 270 280 290', title='A Map which contours lines of auxiliary field are explicit levels')
cshow(plot_map5)

plot_map6=plot_2fields(surface_ta, map_field2, title='A Map which contours lines of auxiliary field are automatic levels')
cshow(plot_map6)

# with projection
plot_map5b=plot_2fields(surface_ta, map_field2, proj='NH', contours='230 231 231 233 234 235', title='A Map which contours lines of auxiliary field are explicit levels')
cshow(plot_map5b)

plot_map6b=plot_2fields(surface_ta, map_field2, proj='NH', title='A Map which contours lines of auxiliary field are automatic levels')
cshow(plot_map6b)

# with vectors
duo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")
dvo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O") 
tos=ds(project="EM",simulation="PRE6CPLCr2alb", variable="tos", period="199807", realm="O")
sub_tos=llbox(tos, latmin=30, latmax=80, lonmin=-60, lonmax=0) # extraction of 'tos' sub box for auxiliary field

tpath='/data/climaf/${project}/${model}/'
fixed_fields(['plot','plot_2fields'],
             ('angle_ORCA1.nc',tpath+'angle_ORCA1.nc'))

map_vect6=plot_2fields(tos, sub_tos, duo, dvo, title='SST: 2 fields + vectors', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
cshow(map_vect6)

map_vect7=plot_2fields(tos, sub_tos, duo, dvo, title='SST: 2 fields + vectors', rotation=1, vcRefLengthF=0.005, vcRefMagnitudeF=0.02, vcGlyphStyle="CurlyVector", vcLineArrowColor="yellow")
cshow(map_vect7)

map_vect8=plot_2fields(tos, sub_tos, duo, dvo, title='SST: 2 fields + vectors, proj=NH', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, vcMinDistanceF=0.01, vcLineArrowColor="yellow", proj="NH")
cshow(map_vect8)


##################
# A cross-section
##################

## one field ##

# with logp (by default, vertical cross-sections in pressure coordinates will have a logarithmic scale)
january_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
ta_zonal_mean=ccdo(january_ta, operator="zonmean")

plot_cross1=plot(ta_zonal_mean,title='A cross-section without contours lines')
cshow(plot_cross1)

plot_cross2=plot(ta_zonal_mean, contours=0, title='A cross-section without contours lines')
cshow(plot_cross2)

plot_cross3=plot(ta_zonal_mean, contours=1, title='A cross-section which contours lines follow color filled contours')
cshow(plot_cross3)

plot_cross4=plot(ta_zonal_mean, contours="240 245 250", title='A cross-section which contours lines don t follow color filled contours')
cshow(plot_cross4)

# linp=1 (vertical axis will have a index-linear spacing, and logarithmic in pressure)
plot_cross1b=plot(ta_zonal_mean, linp=1, title='A cross-section without contours lines')
cshow(plot_cross1b)

plot_cross2b=plot(ta_zonal_mean, linp=1, contours=0, title='A cross-section without contours lines')
cshow(plot_cross2b)

plot_cross3b=plot(ta_zonal_mean, linp=1, contours=1, title='A cross-section which contours lines follow color filled contours')
cshow(plot_cross3b)

plot_cross4b=plot(ta_zonal_mean, linp=1, contours="240 245 250", title='A cross-section which contours lines don t follow color filled contours')
cshow(plot_cross4b)

# linp=-1 (vertical axis will have a pressure-linear spacing, and logarithmic in index)
plot_cross1c=plot(ta_zonal_mean, linp=-1, title='A cross-section without contours lines')
cshow(plot_cross1c)

plot_cross2c=plot(ta_zonal_mean, linp=-1, contours=0, title='A cross-section without contours lines')
cshow(plot_cross2c)

plot_cross3c=plot(ta_zonal_mean, linp=-1, contours=1, title='A cross-section which contours lines follow color filled contours')
cshow(plot_cross3c)

plot_cross4c=plot(ta_zonal_mean, linp=-1, contours="240 245 250", title='A cross-section which contours lines don t follow color filled contours')
cshow(plot_cross4c)

## two fields ##

# with logp (by default, vertical cross-sections in pressure coordinates will have a logarithmic scale)
cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
ta_zonal_mean2=ccdo(cross_field2, operator="zonmean")

plot_cross5=plot_2fields(ta_zonal_mean, ta_zonal_mean2, contours="240 245 250", title='A cross-section which contours lines of auxiliary field are explicit levels')
cshow(plot_cross5)

plot_cross6=plot_2fields(ta_zonal_mean, ta_zonal_mean2, title='A cross-section which contours lines of auxiliary field are automatic levels')
cshow(plot_cross6)

# linp=1 (vertical axis will have a index-linear spacing, and logarithmic in pressure)
plot_cross5b=plot_2fields(ta_zonal_mean, ta_zonal_mean2, linp=1, contours="240 245 250", title='A cross-section which contours lines of auxiliary field are explicit levels')
cshow(plot_cross5b)

plot_cross6b=plot_2fields(ta_zonal_mean, ta_zonal_mean2, linp=1, title='A cross-section which contours lines of auxiliary field are automatic levels')
cshow(plot_cross6b)

# linp=-1 (vertical axis will have a pressure-linear spacing, and logarithmic in index)
plot_cross5c=plot_2fields(ta_zonal_mean, ta_zonal_mean2, linp=-1, contours="240 245 250", title='A cross-section which contours lines of auxiliary field are explicit levels')
cshow(plot_cross5c)

plot_cross6c=plot_2fields(ta_zonal_mean, ta_zonal_mean2, linp=-1, title='A cross-section which contours lines of auxiliary field are automatic levels')
cshow(plot_cross6c)


#############
# A profile
#############    
#january_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
#ta_zonal_mean=ccdo(january_ta, operator="zonmean")
#cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
#ta_zonal_mean2=ccdo(cross_field2, operator="zonmean")

## one field ##
ta_profile=ccdo(ta_zonal_mean, operator="mermean")

# with logp (by default, vertical profiles in pressure coordinates will have a logarithmic scale)
plot_profile1=plot(ta_profile, title='A profile') 
cshow(plot_profile1)

# without logp (linp=1 <=> logp=False)
plot_profile1b=plot(ta_profile, linp=1, title='A profile')
cshow(plot_profile1b)

## two fields ##
ta_profile2=ccdo(ta_zonal_mean2,operator="mermean")

# with logp (by default, vertical profiles in pressure coordinates will have a logarithmic scale)
plot_profile2=plot_2fields(ta_profile, ta_profile2, title='Two profiles')
cshow(plot_profile2)

# without logp (linp=1 <=> logp=False)
plot_profile2b=plot_2fields(ta_profile, ta_profile2, linp=1, title='Two profiles')
cshow(plot_profile2b)

