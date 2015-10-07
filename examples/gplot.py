# Example for general-purpose plot using NCL
# Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/gplot.html

from climaf.api import *
craz()

##########
# Maps
##########

# Define datasets for main field, auxiliary field and vectors
tos=ds(project="EM",simulation="PRE6CPLCr2alb", variable="tos", period="199807", realm="O")
sub_tos=llbox(tos, latmin=30, latmax=80, lonmin=-60, lonmax=0) # extraction of 'tos' sub box for auxiliary field
duo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")
dvo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O")

# How to get the required file for rotating vectors from model grid on geographic grid
fixed_fields('plot', ('angles.nc',cpath+"/../tools/angle_${project}.nc"))

# A Map with one field and vectors, with contours lines like color fill, rotation of vectors on geographic grid
# and with default projection (a cylindrical equidistant)
plot_map1=plot(tos, None, duo, dvo, title='1 field (contours lines follow color filled contours) + vectors',
              contours=1, rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)

# Displaying a figure object will compute and cache it if not already done
cshow(plot_map1)

# A Map of one field and vectors, with user-controled contours lines, rotation of vectors on geographic grid
# and with stereopolar projection
plot_map2=plot(tos, None, duo, dvo, title='1 field (user-controled contours) + vectors', contours='1 3 5 7 9 11 13',
               proj='NH', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
cshow(plot_map2)

# A Map of two fields and vectors, with explicit contours levels for auxiliary field and rotation of vectors on geographic grid
plot_map3=plot(tos, sub_tos, duo, dvo, title='2 fields (user-controled auxiliary field contours) + vectors', contours='0 2 4 6 8 10 12 14 16',
               rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
cshow(plot_map3)

# A Map of two fields and vectors, with automatic contours levels for auxiliary field and rotation of vectors on geographic grid
plot_map4=plot(tos, sub_tos, duo, dvo, title='2 fields (automatic contours levels for auxiliary field) + vectors', 
               proj="NH", rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, vcMinDistanceF=0.01, vcLineArrowColor="yellow")
cshow(plot_map4)

# Same map but with an other vector style: curly vectors (default: "LineArrow")
plot_map5=plot(tos, sub_tos, duo, dvo, title='2 fields (automatic contours levels for auxiliary field) + vectors (curly)', 
               proj="NH", rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, vcMinDistanceF=0.01, vcLineArrowColor="yellow",
               vcGlyphStyle="CurlyVector")
cshow(plot_map5)

# Same map without vectors
plot_map6=plot(tos, sub_tos, title='2 fields (automatic contours levels for auxiliary field)', 
               proj="NH", rotation=1)
cshow(plot_map6)


##################
# Cross-sections
##################

# Define datasets for main field and auxiliary field
january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
ta_zonal_mean=ccdo(january_ta,operator="zonmean")     # main field
cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
ta_zonal_mean2=ccdo(cross_field2, operator="zonmean") # auxiliary field

# A vertical cross-section in pressure coordinates of one field without contours lines and with logarithmic scale (default)
plot_cross1=plot(ta_zonal_mean,title='1 field cross-section (without contours lines)')
cshow(plot_cross1)

# A cross-section of one field, which contours lines follow color filled contours
plot_cross2=plot(ta_zonal_mean, contours=1, title='1 field (contours lines follow color filled contours)')
cshow(plot_cross2)

# A cross-section of one field, which contours lines don t follow color filled contours
plot_cross3=plot(ta_zonal_mean, contours="240 245 250", title='1 field (user-controled contours)')
cshow(plot_cross3)

# Same cross-section but with linp=1 (vertical axis will have a index-linear spacing, and logarithmic in pressure)
plot_cross4=plot(ta_zonal_mean, linp=1, contours="240 245 250", title='1 field (user-controled contours)')
cshow(plot_cross4)

# A cross-section of two fields, with explicit contours levels for auxiliary field
plot_cross5=plot(ta_zonal_mean, ta_zonal_mean2, contours="240 245 250", title='2 fields (user-controled auxiliary field contours)')
cshow(plot_cross5)

# A cross-section of two fields, with automatic contours levels for auxiliary field
# and a pressure-linear spacing and logarithmic in index for vertical axis (linp=-1)
plot_cross6=plot(ta_zonal_mean, ta_zonal_mean2, linp=-1, title='2 fields (automatic contours levels for auxiliary field)')
cshow(plot_cross6)


#############
# A profile
#############
# Define datasets for main field and auxiliary field (already done)
#january_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
#ta_zonal_mean=ccdo(january_ta, operator="zonmean") 
#cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
#ta_zonal_mean2=ccdo(cross_field2, operator="zonmean") 
ta_profile=ccdo(ta_zonal_mean,operator="mermean")   # main field
ta_profile2=ccdo(ta_zonal_mean2,operator="mermean") # auxiliary field

# One profile, with a logarithmic scale (default)
plot_profile1=plot(ta_profile, title='A profile')
cshow(plot_profile1)

# Two profiles, with a index-linear spacing for vertical axis
plot_profile2=plot(ta_profile, ta_profile2, title='Two profiles', linp=1)
cshow(plot_profile2)

