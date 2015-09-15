ccdfsections2 : computes some variables (Uorth, Utang,...) along a section made of Nsec linear segments (mono-variable input file)
----------------------------------------------------------------------------------------------------------------------------------

Computes temperature, salinity, sig0, sig1, sig2, sig4, Uorth, Utang
along a section made of Nsec linear segments (see output
attributes). Output variables are a function of X(km), depth(m) and
time. 

This is the wrapping around the native cdfsections operator assuming
its usage is::   

 cdfsections  Ufile Vfile Tfile larf lorf Nsec lat1 lon1 lat2 lon2 n1
 ... **[ lat3 lon3 n2 ]** **[ lat4 lon4 n3 ]** .... 

CliMAF optional arguments are the ones surrounded with '**'.

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call): 5 datasets

  - a dataset with salinity [T-file]
  - a dataset with temperature [T-file]
  - a dataset with sea water potential density [T-file]
  - a dataset with zonal velocity component [U-file]
  - a dataset with meridional velocity component [V-file]

**Mandatory arguments**:

  - ``larf`` and ``lorf`` : location of X=0 for the X-absice (may be
    out of section) 
  - ``Nsec`` : number of segments used to compute the whole section 
  - ``lat1``, ``lat2`` : extrema latitudes of the segments (from -90
    to 90) 
  - ``lon1``, ``lon2`` : extrema latitudes of the segments (from 0
    to 360)  
  - ``n1`` : number of output points on each segment
    (you have to give Nsec+1 values of lati/loni and Nsec values of ni)

**Optional arguments**: [ lat3 lon3 n2 ] [ lat4 lon4 n3 ] ....

  - ``more_points`` may be used to pass following keys :

    - ``lat3``, ``lat4``, ... : extrema latitudes of the segments
      (from -90 to 90)  
    - ``lon3``, ``lon4``, ... : extrema latitudes of the segments
      (from 0 to 360)   
    - ``n2``, ``n3``, ... : number of output points on each segment 
      (you have to give Nsec+1 values of lati/loni and Nsec values of ni)

It is recommended to put a lot of points on each section if the aim is
to compute X-integrations along the section (10 x the model
resolution).
   
**Required files**: None

**Outputs**:

  - main output : a netcdf file for ocean speed orthogonal to the
    section oriented south-north (variable : Uorth) 
  - secondary outputs and their names :
     - ``Utang`` : field ocean speed tangential to the section
       oriented south-north 
     - ``so`` : field sea water salinity
     - ``thetao`` : field sea water potential temperature
     - ``sig0`` : field potential density sigma 0
     - ``sig1`` : field potential density sigma 1
     - ``sig2`` : field potential density sigma 2
     - ``sig4`` : field potential density sigma 4

**Climaf call example**:: 

  >>> dso=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O") # dataset with salinity
  >>> dtho=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") # dataset with temperature
  >>> drho=ds(simulation="PRE6CPLCr2alb", variable="rhopoto", period="199807", realm="O") # dataset with sea water potential density 
  >>> duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # dataset with zonal velocity component
  >>> dvo=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O") # dataset with meridional velocity component
  >>> my_cdfsections=ccdfsections2(dso,dtho,drho,duo,dvo,larf=48.0,lorf=125.0,Nsec=1,lat1=50.0,lon1=127.0,lat2=50.5,lon2=157.5,n1=20)
  >>> cfile(my_cdfsections) # to compute all variables along a section made of Nsec linear segments
  >>> Utang_var=my_cdfsections.Utang # Utang_var receives operator output named "Utang", namely the field ocean speed tangential to the section oriented south-north
  >>> so_var=my_cdfsections.so # so_var receives operator output named "so"
  >>> thetao_var=my_cdfsections.thetao # thetao_var receives operator output named "thetao"
  >>> sig0_var=my_cdfsections.sig0 # sig0_var receives operator output named "sig0"
  >>> sig1_var=my_cdfsections.sig1 # sig1_var receives operator output named "sig1"
  >>> sig2_var=my_cdfsections.sig2 # sig2_var receives operator output named "sig2"
  >>> sig4_var=my_cdfsections.sig4 # sig4_var receives operator output named "sig4"
  
  >>> my_cdfsections2=ccdfsections2(dso,dtho,drho,duo,dvo,larf=48.0,lorf=305.0,Nsec=2,lat1=49.0,lon1=307.0,lat2=50.5,lon2=337.5,n1=20,more_points='40.3 305.1 50')
  >>> cfile(my_cdfsections2)

**Implementation**: The operator is implemented as a script which
calls a binary using cdftools cdfsections operator.
