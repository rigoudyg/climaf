ccdfheatc : computes the heat content in the specified area 
--------------------------------------------------------------

Computes the heat content in the specified area (Joules). A sub-domain
can be specified in option. 

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call): 

  - a dataset with salinity ([T-file])
  - a dataset with temperature ([T-file])

**Mandatory arguments**: None

**Optional arguments**:

  - ``imin``, ``imax``, ``jmin``, ``jmax``,  ``kmin``, ``kmax`` :
    limit of a sub domain where the heat content will be calculated
    (use by imin=..., imax=..., etc): 

    - if imin = 0 then ALL i are taken
    - if jmin = 0 then ALL j are taken
    - if kmin = 0 then ALL k are taken
  - ``-full`` : assume full step model output instead of default
    partial steps (use by opt='-full') 
       
**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc must be in
the current directory. 

**Outputs**:

  - main output : standard output

**Climaf call example**::

  >>> from climaf.api import *
  >>> from climaf.operators import fixed_fields
  >>> cdef("frequency","monthly") 
  >>> cdef("project","EM")
  >>> # How to get required files for cdfheatc cdftools binary
  >>> tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
  >>> lpath='/cnrm/aster/data3/aster/vignonl/code/climaf/'
  >>> fixed_fields('ccdfheatc',
             target=[tpath+'ORCA1_mesh_mask.nc',tpath+'ORCA1_mesh_hgr.nc',tpath+'ORCA1_mesh_zgr.nc'],
             link=[lpath+'mask.nc',lpath+'mesh_hgr.nc',lpath+'mesh_zgr.nc'])
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O") # dataset with salinity
  >>> d2=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") # dataset with temperature
  >>> my_cdfheatc=ccdfheatc(d1,d2,imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2,opt='-full')
  >>> cfile(my_cdfheatc) # to compute the heat content in the specified area and get the result on standard output

**Implementation**: The operator is implemented as a binary using
cdfheatc cdftools operator. 

**CliMAF call sequence pattern** (for reference)::
  
  >>> 'tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfheatc $tmp_file ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; rm -f $tmp_file'

