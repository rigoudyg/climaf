# Examples for some cdftools operators :
#
# - cdfmean =>
#    * ccdfmean : computes the mean value of the field, 2D or 3D (output: excluded profile)
#    * ccdfmean_profile : vertical profile of horizontal means for 3D fields (output: excluded mean value)
#    * ccdfmean_profile_box : vertical profile of horizontal means for 3D fields on a given geographical domain (output: excluded mean value)
#    * ccdfvar : computes the spatial variance, 2D or 3D (output: excluded mean value, profile and profile of variance)
#    * ccdfvar_profile : vertical profile of spatial variance (output: excluded mean value, profile and variance)
#
# - cdfheatc (computes the heat content in the specified area)
#
# - cdfmxlheatc (computed the heat content in the mixed layer)
#
# - cdfsaltc (computed the salt content in the mixed layer)
#
# - cdfstd =>
#    * ccdfstd : computes the standard deviation of given variables
#    * ccdfstdmoy : computes the mean value of the field, in addition to the standard deviation
#
# - cdfsections (computes temperature, salinity, sig0, sig1, sig2, sig4, Uorth, Utang
#                 along a section made of Nsec linear segments)
#
# - cdfvT (computes the time average values for second order products
#           V.T, V.S, U.T and U.S used in heat and salt transport computation)
#
# - cdfzonalmean =>
#    * ccdfzonalmean : compute the global zonal mean of the given variable 
#    * ccdfzonalmean_bas : compute the zonal mean of the given variable in a specified sub-basin 
#

#export CLIMAF_FIX_NEMO_TIME='on'  # can be useful at CNRM
from climaf.api import *

if not atCNRM: exit(0)
if 'ccdfmean' not in cscripts :
    print("CDFtools not available")
    exit(0)

# Declare "data_CNRM" project for Nemo raw outputs 
#
cproject('data_CNRM')

# For 'standard' Nemo output files (actually, they are better accessible using project "EM")
#root1="/cnrm/aster/data3/aster/senesi/NO_SAVE/expes/PRE6/${simulation}/O/"
root1="/cnrm/aster/data1/UTILS/climaf/test_data/${simulation}/O/"
suffix="${simulation}_1m_YYYYMMDD_YYYYMMDD_${variable}.nc"
url_nemo_standard=root1+suffix  
#
dataloc(project='data_CNRM', organization='generic', url=[url_nemo_standard])
# 
# Declare how variables are scattered/groupes among files
# (and with mixed variable names conventions - CNRM and  MONITORING)
calias("data_CNRM","uo",filenameVar="grid_U_table2.3")
calias("data_CNRM","vo,vmo",filenameVar="grid_V_table2.3")
calias("data_CNRM","so,thetao,omlmax",filenameVar="grid_T_table2.2")

# Define defaults facets for datasets 
cdef("project","data_CNRM")
cdef("frequency","monthly")

# How to get fixed files for all cdftools binaries
# (this can use wildcards ${model}, ${project}, ${simulation}, ${realm})
#tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
tpath='/cnrm/aster/data1/UTILS/climaf/test_data/fixed/'
fixed_fields(['ccdfmean','ccdfmean_profile','ccdfmean_profile_box','ccdfvar','ccdfvar_profile',\
              'ccdfheatcm','ccdfmxlheatcm','ccdfsaltc','ccdfzonalmean'],
             ('mask.nc',tpath+'ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',tpath+'ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',tpath+'ORCA1_mesh_zgr.nc'))

fixed_fields(['ccdfzonalmean_bas'],
             ('mask.nc',tpath+'ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',tpath+'ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',tpath+'ORCA1_mesh_zgr.nc'),
             ('new_maskglo.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_new_maskglo.nc'))

#-----------
#  cdfmean
#-----------
#
# CDFtools usage :
# cdfmean  IN-file IN-var T|U|V|F|W [imin imax jmin jmax kmin kmax]
#        ... [-full] [-var] [-zeromean] 
#
# CliMAF usage (ccdfmean, ccdfmean_profile, ccdfmean_profile_box, ccdfvar, ccdfvar_profile) :
#

# Define dataset with sea water x velocity ("uo")
duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")

# Compute some mean values
my_cdfmean=ccdfmean(duo,pos_grid='U')
my_cdfmean2=ccdfmean(duo,pos_grid='U',opt='-full')
my_cdfmean3=ccdfmean(duo,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
cfile(my_cdfmean3)

# Compute vertical profile
my_cdfmean_prof=ccdfmean_profile(duo,pos_grid='U')
cfile(my_cdfmean_prof)

# Compute vertical profile on geographical domain [35.4,39,-14,-10]
my_cdfmean_prof_box=ccdfmean_profile_box(duo,pos_grid='U',latmin=35.4,latmax=39,lonmin=-14,lonmax=-10,kmin=1,kmax=2)
cfile(my_cdfmean_prof_box)

# Compute spatial variance
my_cdfvar=ccdfvar(duo,pos_grid='U')
cfile(my_cdfvar)

# Compute vertical profile of spatial variance
my_cdfvar_prof=ccdfvar_profile(duo,pos_grid='U')

# Plot mean values, vertical profile, spatial variance and vertical profile of spatial variance
duo_JASO=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807-199810", realm="O")

my_cdfmean4=ccdfmean(duo_JASO,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
my_plot=curves(my_cdfmean4,labels="uo",title="Mean values")
cshow(my_plot)

my_cdfmean_prof2=ccdfmean_profile(duo_JASO,pos_grid='U')
my_cdfmean_prof2_level0=ccdo(my_cdfmean_prof2,operator="-sellevel,5.02159")
my_plot2=curves(my_cdfmean_prof2_level0,labels="uo",title="Level 0 (gdept=5.02159) of mean values")
cshow(my_plot2)

my_cdfvar2=ccdfvar(duo_JASO,pos_grid='U')
my_plot3=curves(my_cdfvar2,labels="uo",title="Spatial variance")
cshow(my_plot3)

my_cdfvar_prof2=ccdfvar_profile(duo_JASO,pos_grid='U')
my_cdfvar_prof2_level0=ccdo(my_cdfvar_prof2,operator="-sellevel,5.02159")
my_plot4=curves(my_cdfvar_prof2_level0,labels="uo",title="Level 0 (gdept=5.02159) of spatial variance")
cshow(my_plot4)

#-----------
# cdfheatc   
#-----------
#
# CDFtools usage :
# cdfheatc  T-file ...
#     ... [imin imax jmin jmax kmin kmax] [-full] 
#
# CliMAF usage (ccdfheatc) :
#

# Define datasets with salinity and temperature 
dso=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O")
dtho=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O")

# Compute the heat content in the specified area
my_cdfheatc=ccdfheatcm(dso,dtho,imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
cfile(my_cdfheatc) # multi-variable output file: "heatc_2D" and "heatc_3D"

# Select and extract "heatc_2D" in multi-variable output file, and plot profile
heatc_2D=ccdo(my_cdfheatc, operator='selname,heatc_2D')
ncdump(heatc_2D)

heatc_2D.variable="heatc_2D" # replace list of variable, i.e. 'heatc_2D,heatc_3D', by 'heatc_2D'
my_plot5=plot(heatc_2D)
cshow(my_plot5)

#----------------
#  cdfmxlheatc
#----------------
#
# CDFtools usage :
# cdfmxlheatc T-file [-full]
#
# CliMAF usage (ccdfmxlheatc) :
#

# Define dataset with mld 
dmldx=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807", realm="O")

# Compute the heat content in the mixed layer
my_cdfmxlheatc=ccdfmxlheatcm(dtho,dmldx)
cfile(my_cdfmxlheatc)

#-----------
# cdfsaltc   
#-----------
#
# CDFtools usage :
# cdfsaltc  T-file ...
#     ... [imin imax jmin jmax kmin kmax] [-full] 
#
# CliMAF usage (ccdfsaltc) :
#

#export CLIMAF_FIX_NEMO_TIME='on'

# Define dataset with salinity 
dso=ds(simulation="PRE6CPLCr2alb", variable="so", period="1998", realm="O")

# Compute the salt content in the specified area
my_cdfsaltc=ccdfsaltc(dso,imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
cfile(my_cdfsaltc)

# Select and extract "saltc_3D" in multi-variable output file, and plot profile
saltc_3D=select(my_cdfsaltc, var="saltc_3D")
ncdump(saltc_3D)

saltc_3D.variable="saltc_3D" # replace list of variable, i.e. 'saltc_2D,saltc_3D', by 'saltc_3D'
my_plot6=plot(saltc_3D)
cshow(my_plot6)

#-----------
#  cdfstd
#-----------
#
# CDFtools usage :
# cdfstd [-save] [-spval0] [-nomissincl] [-stdopt] list_of files
#
# CliMAF usage (ccdfstd, ccdfstdmoy) : **mono-variable**
#

# For example, define dataset with mld ("omlmax") for period "199807-199810"
dmld=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807-199810", realm="O")

# Compute the standard deviation of variable "omlmax"
my_cdfstd=ccdfstd(dmld)
cfile(my_cdfstd)

# Compute both the mean value and standard deviation of "uo" field (sea water velocity)
my_cdfstd_moy=ccdfstdmoy(duo)
cfile(my_cdfstd_moy)
cfile(my_cdfstd_moy.moy)

#----------------
#  cdfsections 
#----------------
#
# CDFtools usage :
# cdfsections  Ufile Vfile Tfile larf lorf Nsec lat1 lon1 lat2 lon2 n1
#               [ lat3 lon3 n2 ] [ lat4 lon4 n3 ] ....
#
# CliMAF usage (ccdfsections) :
#

# Define datasets with salinity,  temperature, mld, sea water x and y velocity (uo/vo)
dso=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O")      
dtho=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") 
dmld=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807", realm="O") 
duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")      
dvo=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O")

# Compute temperature, salinity, sig0, sig1, sig2, sig4, Uorth, Utang 
# along a section made of Nsec linear segments
my_cdfsections=ccdfsectionsm(dso,dtho,dmld,duo,dvo,larf=48.0,lorf=125.0,Nsec=1,lat1=50.0,lon1=127.0,lat2=50.5,lon2=157.5,n1=20)
cfile(my_cdfsections)
cfile(my_cdfsections.Utang)
cfile(my_cdfsections.so)
cfile(my_cdfsections.thetao)
cfile(my_cdfsections.sig0)
cfile(my_cdfsections.sig1)
cfile(my_cdfsections.sig2)
cfile(my_cdfsections.sig4)

my_cdfsections2=ccdfsectionsm(dso,dtho,dmld,duo,dvo,larf=48.0,lorf=305.0,Nsec=2,lat1=49.0,lon1=307.0,lat2=50.5,lon2=337.5,n1=20,more_points='40.3 305.1 50')
cfile(my_cdfsections2)

#----------------
#  cdfvT 
#----------------
#
# CDFtools usage :
# cdfvT T-file S-file U-file V-file [-o output_file ] [-nc4 ] 'list_of_tags'
#
# CliMAF usage (ccdfvT) :
#

# Define datasets with temperature ("thetao" in .nc <=> "votemper" for cdftools),
# salinity ("so" in .nc <=> "vosaline" for cdftools),
# zonal velocity component ("uo" in .nc <=> "vozocrtx" for cdftools),
# meridional velocity component ("vo" in .nc <=> "vomecrty" for cdftools)
dso=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O")      
dtho=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") 
duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")      
dvo=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O")

# Compute the time average values for second order products 
# V.T, V.S, U.T and U.S used in heat and salt transport computation
my_cdfvT=ccdfvT(dtho,dso,duo,dvo)
cfile(my_cdfvT)

# Select and extract "vozous" in multi-variable output file, and plot map
vozous_var=select(my_cdfvT, var="vozous,nav_lat,nav_lon")
ncdump(vozous_var)

vozous_var.variable="vozous" # replace list of variable, i.e. 'vomevt,vomevs,vozout,vozous', by 'vozous'
my_plot7=plot(vozous_var)
cshow(my_plot7)

#----------------
#  cdfzonalmean
#----------------
#
# CDFtools usage :
# cdfzonalmean IN-file point_type [ BASIN-file] [-debug]...
# ...[-var var1,var2,..] [-max ] [-pdep | --positive_depths]
#
# CliMAF usage (ccdfzonalmean, ccdfzonalmean_bas) :
#

# For example, define dataset with meridional velocity component ("vo")
dvo=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O")
# Compute the zonal mean of "vo"
my_cdfzmean=ccdfzonalmean(dvo,point_type='V')
cfile(my_cdfzmean)

# Define dataset with ocean mass component ("vmo") for period "1998"
dvmo=ds(simulation="PRE6CPLCr2alb", variable="vmo", period="1998", realm="O")
# Compute the zonal mean of "vmo"
my_cdfzmean2=ccdfzonalmean(dvmo,point_type='V')
cfile(my_cdfzmean2)
# Plot result
plot_mycdfzmean2=plot(my_cdfzmean2,title='Zonal mean')
cshow(plot_mycdfzmean2)

# Now, compute the zonal mean of "vmo" in sub-basin 'atl' (file
# 'new_maskglo.nc' is available via fixed_fields; see above)
my_cdfzmean_bas=ccdfzonalmean_bas(dvmo,point_type='V',basin='atl')
# Plot result
plot_mycdfzmean_bas=plot(my_cdfzmean_bas,title='Zonal mean in sub-basin atl')
cshow(plot_mycdfzmean_bas)
