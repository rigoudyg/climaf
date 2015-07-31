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

#export CLIMAF_FIX_NEMO_TIME='on'
from climaf.api import *

if not atCNRM:
    return

cdef("frequency","monthly") 
cdef("project","EM")

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

tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
#tpath='/cnrm/aster/data3/aster/vignonl/${project}/'

# How to get required files for all cdftools binaries
# fixed_fields(['ccdfmean','ccdfmean_profile','ccdfvar','ccdfvar_profile','ccdfheatc','ccdfmxlheatc'],
#             target=[tpath+'ORCA1_mesh_mask.nc',tpath+'ORCA1_mesh_hgr.nc',tpath+'ORCA1_mesh_zgr.nc'],
#             link=[lpath+'mask.nc',lpath+'mesh_hgr.nc',lpath+'mesh_zgr.nc'])

fixed_fields(['ccdfmean','ccdfmean_profile','ccdfvar','ccdfvar_profile','ccdfheatc','ccdfmxlheatc'],
             ('mask.nc',tpath+'ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',tpath+'ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',tpath+'ORCA1_mesh_zgr.nc'))

# For example, define dataset with sea water x velocity ("uo")
d1=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")

# Compute some mean values
my_cdfmean=ccdfmean(d1,pos_grid='U')
cfile(my_cdfmean)

my_cdfmean2=ccdfmean(d1,pos_grid='U',opt='-full')
cfile(my_cdfmean2)

my_cdfmean3=ccdfmean(d1,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
cfile(my_cdfmean3)

# Compute vertical profile
my_cdfmean_prof=ccdfmean_profile(d1,pos_grid='U')
cfile(my_cdfmean_prof)

# Compute spatial variance
my_cdfvar=ccdfvar(d1,pos_grid='U')
cfile(my_cdfvar)

# Compute vertical profile of spatial variance
my_cdfvar_prof=ccdfvar_profile(d1,pos_grid='U')
cfile(my_cdfvar_prof)


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

# Define dataset with salinity ("so" in .nc <=> "vosaline" for cdftools)
# and temperature ("thetao" in .nc <=> "votemper" for cdftools) 
d2=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O")
d3=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O")

# Compute the heat content in the specified area
my_cdfheatc=ccdfheatc(d2,d3,imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
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

# Define dataset with temperature ("thetao" in .nc <=> "votemper" for cdftools)
# and mld ("omlmax" in .nc <=> "somxlt02" for cdftools)
d4=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O")
d5=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807", realm="O")

# Compute the heat content in the mixed layer
my_cdfmxlheatc=ccdfmxlheatc(d4,d5)
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
d6=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807-199810", realm="O")

# Compute the standard deviation of variable "omlmax"
my_cdfstd=ccdfstd(d6)
cfile(my_cdfstd)

# Compute the mean value and standard deviation of "uo" field (sea water velocity)
my_cdfstd_moy=ccdfstdmoy(d1)
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

# Define dataset with salinity ("so" in .nc <=> "vosaline" for cdftools),
# temperature ("thetao" in .nc <=> "votemper" for cdftools),
# mld ("omlmax" in .nc <=> "somxlt02" for cdftools) - a remplacer par "rhopoto" -,
# sea water x velocity ("uo") and sea water y velocity ("vo")
ds1=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O")      #<=> d2
ds2=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O")  #<=> d3 & d4
ds3=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807", realm="O")  #<=> d5 #change 'omlmax' by 'rhopoto' (bug with ncrename caused by data pre-processing; ok with 'good' data)
ds4=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")      #<=> d1
ds5=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O")

# Compute temperature, salinity, sig0, sig1, sig2, sig4, Uorth, Utang 
# along a section made of Nsec linear segments
my_cdfsections=ccdfsections(ds1,ds2,ds3,ds4,ds5,larf=48.0,lorf=125.0,Nsec=1,lat1=50.0,lon1=127.0,lat2=50.5,lon2=157.5,n1=20)
cfile(my_cdfsections)
cfile(my_cdfsections.Utang)
cfile(my_cdfsections.so)
cfile(my_cdfsections.thetao)
cfile(my_cdfsections.sig0)
cfile(my_cdfsections.sig1)
cfile(my_cdfsections.sig2)
cfile(my_cdfsections.sig4)

my_cdfsections2=ccdfsections(ds1,ds2,ds3,ds4,ds5,larf=48.0,lorf=305.0,Nsec=2,lat1=49.0,lon1=307.0,lat2=50.5,lon2=337.5,n1=20,more_points='40.3 305.1 50')
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

# Define dataset with temperature ("thetao" in .nc <=> "votemper" for cdftools),
# salinity ("so" in .nc <=> "vosaline" for cdftools),
# zonal velocity component ("uo" in .nc <=> "vozocrtx" for cdftools),
# meridional velocity component ("vo" in .nc <=> "vomecrty" for cdftools)
ds2=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") 
ds1=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O")   
ds4=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")    
ds5=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O")

# Compute the time average values for second order products 
# V.T, V.S, U.T and U.S used in heat and salt transport computation
my_cdfvT=ccdfvT(ds2,ds1,ds4,ds5)
cfile(my_cdfvT)
