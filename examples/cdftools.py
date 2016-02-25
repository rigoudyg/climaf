# Examples for some cdftools operators :
#
# - cdfmean =>
#    * ccdfmean : computes the mean value of the field, 2D or 3D (output: excluded profile)
#    * ccdfmean_profile : vertical profile of horizontal means for 3D fields (output: excluded mean value)
#    * ccdfvar : computes the spatial variance, 2D or 3D (output: excluded mean value, profile and profile of variance)
#    * ccdfvar_profile : vertical profile of spatial variance (output: excluded mean value, profile and variance)
#
# - cdfheatc (computes the heat content in the specified area)
#
# - cdfmxlheatc (computed the heat content in the mixed layer)
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
calias("data_CNRM","vo",filenameVar="grid_V_table2.3")
calias("data_CNRM","so,thetao,omlmax",filenameVar="grid_T_table2.2")

# Define defaults facets for datasets 
cdef("project","data_CNRM")
cdef("frequency","monthly")

# How to get fixed files for all cdftools binaries
# (this can use wildcards ${model}, ${project}, ${simulation}, ${realm})
#tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
tpath='/cnrm/aster/data1/UTILS/climaf/test_data/fixed/'
fixed_fields(['ccdfmean','ccdfmean_profile','ccdfvar','ccdfvar_profile','ccdfheatcm','ccdfmxlheatcm'],
             ('mask.nc',tpath+'ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',tpath+'ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',tpath+'ORCA1_mesh_zgr.nc'))

#-----------
#  cdfmean
#-----------
#
# CDFtools usage :
# cdfmean  IN-file IN-var T|U|V|F|W [imin imax jmin jmax kmin kmax]
#        ... [-full] [-var] [-zeromean] 
#
# CliMAF usage (ccdfmean, ccdfmean_profile, ccdfvar, ccdfvar_profile) :
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
cfile(my_cdfheatc)

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
