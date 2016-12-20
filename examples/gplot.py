# Example for general-purpose plot using NCL
# Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/plot.html

from climaf.api import *
craz()

##########
# Maps
##########

# Define datasets for main field, auxiliary field and vectors
tas=ds(project='example', simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="198001")
sub_tas=llbox(tas, latmin=30, latmax=80, lonmin=60, lonmax=120) # extraction of 'tas' sub box for auxiliary field
uas=ds(project='example', simulation="AMIPV6ALB2G", variable="uas", period="198001")
vas=ds(project='example', simulation="AMIPV6ALB2G", variable="vas", period="198001")

# A Map with one field and vectors, with contours lines like color fill, default projection (a cylindrical equidistant),
# with 'pdf' output format and paper resolution of 17x22 inches (<=> 1224x1584 pixels)
plot_map1=plot(tas, None, uas, vas, title='1 field (contours lines follow color filled contours) + vectors',
              contours=1, vcRefLengthF=0.02, vcRefMagnitudeF=11.5, format="pdf", resolution='17*22') 
 
# Displaying a figure object will compute and cache it if not already done
cshow(plot_map1)
# 'cpdfcrop' operator applied on 'plot_map1' object ('cpdfcrop' <=> 'pdfcrop' by preserving metadata)
cshow(cpdfcrop(plot_map1))

# A Map of one field and vectors, with user-controled contours lines, stereopolar projection
# and with 'png' output format (default)
plot_map2=plot(tas, None, uas, vas, title='1 field (user-controled contours) + vectors', proj='NH',
               contours='230 235 240 245 250 255 260 265 270 275 280', vcRefLengthF=0.03, vcRefMagnitudeF=11.5)
cshow(plot_map2)

# A Map of two fields and vectors, with explicit contours levels for auxiliary field
plot_map3=plot(tas, sub_tas, uas, vas, title='2 fields (user-controled auxiliary field contours) + vectors',
               contours='230 235 240 245 250 255 260 265 270', vcRefLengthF=0.02, vcRefMagnitudeF=11.5)
cshow(plot_map3)

# A Map of two fields and vectors, with automatic contours levels for auxiliary field 
plot_map4=plot(tas, sub_tas, uas, vas, title='2 fields (automatic contours levels for auxiliary field) + vectors', 
               proj="NH", vcRefLengthF=0.05, vcRefMagnitudeF=11.5, vcMinDistanceF=0.012, vcLineArrowColor="yellow")
cshow(plot_map4)

# Same map but with an other vector style: curly vectors (default: "LineArrow")
plot_map5=plot(tas, sub_tas, uas, vas, title='2 fields (automatic contours levels for auxiliary field) + vectors (curly)', 
               proj="NH", vcRefLengthF=0.05, vcRefMagnitudeF=11.5, vcMinDistanceF=0.012, vcLineArrowColor="yellow",
               vcGlyphStyle="CurlyVector")
cshow(plot_map5)

# Same map without vectors
plot_map6=plot(tas, sub_tas, title='2 fields (automatic contours levels for auxiliary field)', proj="NH")
cshow(plot_map6)

# A Map of two fields and vectors, with index selection of time step and/or level step for all fields which have this dimension :
# case where (t,z,y,x) are not degenerated
ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1980") # ta(time, plev, lat, lon)
sub_ta=llbox(ta, latmin=30, latmax=80, lonmin=60, lonmax=120) # extraction of 'ta' sub box for auxiliary field
uas=ds(project='example', simulation="AMIPV6ALB2G", variable="uas", period="1980") # uas(time, lat, lon)
vas=ds(project='example', simulation="AMIPV6ALB2G", variable="vas", period="1980") # vas(time, lat, lon)

map_select1=plot(ta, sub_ta, uas, vas, title='Selecting index 10 for level and 0 for time', vcRefLengthF=0.02, vcRefMagnitudeF=11.5,
                 level=10, time=0) # level selection has no impact for vectors because they have not depth dimension, so only time selection is done for vectors
cshow(map_select1)

# A Map of two fields and vectors, with value selection of time step and/or level step for all fields which have this dimension : 
# case where (t,y,x) are not degenerated
tas=ds(project='example', simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980") # tas(time, lat, lon)
sub_tas=llbox(tas, latmin=30, latmax=80, lonmin=60, lonmax=120) # extraction of 'tas' sub box for auxiliary field

map_select2=plot(tas, sub_tas, uas, vas, title='Selecting level and time close to 10 and 1400000 respectively',
                 vcRefLengthF=0.02, vcRefMagnitudeF=11.5, level=10., time=1400000.) # level selection has no impact on fields because they have not depth dimension, whereas time selection is done for all fields 
cshow(map_select2)

map_select3=plot(tas, sub_tas, uas, vas, title='Selecting level and time close to 10 and 19800131 respectively',
                 vcRefLengthF=0.02, vcRefMagnitudeF=11.5, level=10., date=19800131) # level selection has no impact on fields because they have not depth dimension, whereas time selection is done for all fields 
cshow(map_select3)


#
# This example will work on CNRM's Lustre. An only new feature is added: ROTATION of VECTORS from model grid on geographic grid
#
if atCNRM:
    # Declare "data_CNRM" project with some 'standard' Nemo output files
    # (actually, they are easier accessible using project "EM")
    cproject('data_CNRM')
    root="/cnrm/est/COMMON/climaf/test_data/${simulation}/O/"
    suffix="${simulation}_1m_YYYYMMDD_YYYYMMDD_${variable}.nc"
    data_url=root+suffix
    dataloc(project='data_CNRM',organization='generic',url=data_url)
    # Declare how variables are scattered/grouped among files
    calias("data_CNRM","tos,thetao",filenameVar="grid_T_table2.2")
    calias("data_CNRM","uo",filenameVar="grid_U_table2.3")
    calias("data_CNRM","vo",filenameVar="grid_V_table2.3")
  
    # Define datasets for main field, auxiliary field and vectors
    tos=ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="tos", period="199807")
    sub_tos=llbox(tos, latmin=30, latmax=80, lonmin=-60, lonmax=0) # extraction of 'tos' sub box for auxiliary field
    duo=ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="uo", period="199807")
    dvo=ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="vo", period="199807")

    # How to get the required file for rotating vectors from model grid on geographic grid
    fixed_fields('plot', ('angles.nc',cpath+"/../tools/angle_${project}.nc"))
    
    # A Map with one field and vectors, with contours lines like color fill, rotation of vectors on geographic grid,
    # default projection (a cylindrical equidistant)
    plot_map1b=plot(tos, None, duo, dvo, title='1 field (contours lines follow color filled contours) + vectors',
                  contours=1, rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02) 

    # Displaying a figure object will compute and cache it if not already done
    cshow(plot_map1b)

    # A Map of one field and vectors, with user-controled contours lines, rotation as above, stereopolar projection
    # and with 'png' output format (default)
    plot_map2b=plot(tos, None, duo, dvo, title='1 field (user-controled contours) + vectors', contours='1 3 5 7 9 11 13',
                   proj='NH', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
    cshow(plot_map2b)

    # A Map of two fields and vectors, with explicit contours levels for auxiliary field and rotation of vectors on geographic grid
    plot_map3b=plot(tos, sub_tos, duo, dvo, title='2 fields (user-controled auxiliary field contours) + vectors',
                   contours='0 2 4 6 8 10 12 14 16', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
    cshow(plot_map3b)

    # A Map of two fields and vectors, with automatic contours levels for auxiliary field and rotation of vectors on geographic grid
    plot_map4b=plot(tos, sub_tos, duo, dvo, title='2 fields (automatic contours levels for auxiliary field) + vectors', 
                   proj="NH", rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, vcMinDistanceF=0.01, vcLineArrowColor="yellow")
    cshow(plot_map4b)

    # A Map of two fields and vectors, with index selection of time step and/or level step for all fields which have this dimension :
    # case where (t,z,y,x) are not degenerated
    thetao=ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="thetao", period="1998") # thetao(time_counter, deptht, y, x) 
    sub_thetao=llbox(thetao, latmin=30, latmax=80, lonmin=-60, lonmax=0) # extraction of 'thetao' sub box for auxiliary field
    
    map_select1b=plot(thetao, sub_thetao, duo, dvo, title='Selecting index 10 for level and 0 for time', rotation=1,
                      vcRefLengthF=0.002, vcRefMagnitudeF=0.02, level=10, time=0) # time selection has no impact for vectors because time dimension is degenerated, so only level selection is done for vectors
    cshow(map_select1b)
    
    # A Map of two fields and vectors, with value selection of time step and/or level step for all fields which have this dimension : 
    # case where (t,y,x) are not degenerated
    duo=ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="uo", period="1998") # uo(time_counter, depthu, y, x) 
    dvo=ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="vo", period="1998")
    tos=ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="tos", period="1998") # tos(time_counter, y, x) 
    sub_tos=llbox(tos, latmin=30, latmax=80, lonmin=-60, lonmax=0) # extraction of 'tos' sub box for auxiliary field
    
    map_select2b=plot(tos, sub_tos, duo, dvo, title='Selecting level and time close to 10 and 1400000 respectively', rotation=1,
                      vcRefLengthF=0.002, vcRefMagnitudeF=0.02, level=10., time=1400000.) # level selection has no impact on main field and auxiliary field because they have not depth dimension, whereas level (and time) selection is done for vectors 
    cshow(map_select2b)


##################
# Cross-sections
##################

# Define datasets for main field and auxiliary field
january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
ta_zonal_mean=ccdo(january_ta,operator="zonmean")     # main field
cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
ta_zonal_mean2=ccdo(cross_field2, operator="zonmean") # auxiliary field

# A vertical cross-section in pressure coordinates of one field without contours lines and with logarithmic scale 
plot_cross1=plot(ta_zonal_mean,title='1 field cross-section (without contours lines)', y="log")
cshow(plot_cross1)

# A cross-section of one field, which contours lines follow color filled contours
plot_cross2=plot(ta_zonal_mean, contours=1, title='1 field (contours lines follow color filled contours)')
cshow(plot_cross2)

# A cross-section of one field, which contours lines don t follow color filled contours
plot_cross3=plot(ta_zonal_mean, contours="240 245 250", title='1 field (user-controled contours)')
cshow(plot_cross3)

# Same cross-section but with y="index" (vertical axis will have a index-linear spacing, and logarithmic in pressure)
plot_cross4=plot(ta_zonal_mean, y="index", contours="240 245 250", title='1 field (user-controled contours)')
cshow(plot_cross4)

# A cross-section of two fields, with explicit contours levels for auxiliary field
plot_cross5=plot(ta_zonal_mean, ta_zonal_mean2, contours="240 245 250", title='2 fields (user-controled auxiliary field contours)')
cshow(plot_cross5)

# A cross-section of two fields, with automatic contours levels for auxiliary field
# and a pressure-linear spacing and logarithmic in index for vertical axis (y="lin", it is by default)
plot_cross6=plot(ta_zonal_mean, ta_zonal_mean2, y="lin", title='2 fields (automatic contours levels for auxiliary field)')
cshow(plot_cross6)

# Two plots where (t,z,y) are not degenerated, with selection of time step and/or level step for all fields which have this dimension :
# we will have a cross-section or a profile depending on time and level selection
january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta", period="1980") # ta(time, plev, lat, lon) 
ta_zonal_mean=ccdo(january_ta,operator="zonmean") # => (t,z,y)
cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
ta_zonal_mean2=ccdo(cross_field2, operator="zonmean") # => (t,z,y)

select_cross1=plot(ta_zonal_mean, ta_zonal_mean2, title='Selecting index 10 for time', y="index", time=3000.) # time selection is done for main and auxiliary field => dim:=(z,y) => we have a cross-section
cshow(select_cross1)

select_cross2=plot(ta_zonal_mean, ta_zonal_mean2, title='Time and level selection => profile', y="index", time=0, level=4) # time and level selection is done for two fields => dim:=(y) => we have a vertical profile 
cshow(select_cross2) 


#############
# A profile
#############
# Define datasets for main field and auxiliary field (already done)
january_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
ta_zonal_mean=ccdo(january_ta, operator="zonmean") 
cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
ta_zonal_mean2=ccdo(cross_field2, operator="zonmean") 
ta_profile=ccdo(ta_zonal_mean,operator="mermean")   # main field
ta_profile2=ccdo(ta_zonal_mean2,operator="mermean") # auxiliary field

# One profile, with a logarithmic scale 
plot_profile1=plot(ta_profile, title='A profile', y="log")
cshow(plot_profile1)

# Two profiles, with a index-linear spacing for vertical axis (default)
plot_profile2=plot(ta_profile, ta_profile2, title='Two profiles', y="lin")
cshow(plot_profile2)

# A (t,z) profile, with a a logarithmic scale
january_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1980")
ta_zonal_mean=ccdo(january_ta, operator="zonmean") 
cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
ta_zonal_mean2=ccdo(cross_field2, operator="zonmean") 
ta_profile=ccdo(ta_zonal_mean,operator="mermean")   # main field
ta_profile2=ccdo(ta_zonal_mean2,operator="mermean") # auxiliary field

plot_profile3=plot(ta_profile, ta_profile2, title='Profiles (t,z)', y="log", invXY=True)
cshow(plot_profile3)

