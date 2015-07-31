ccdfmxlheatc : computes the heat content in the mixed layer 
--------------------------------------------------------------

Computes the heat content in the mixed layer (Joules/m2).

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call): 

  - a dataset with temperature (gridT)
  - a dataset with mld (gridT)

**Mandatory arguments**: None

**Optional arguments**:

  - ``-full`` : for full step configurations, default is partial step
    (use by opt='-full')  

**Required files**: Files mesh_zgr.nc, mask.nc must be in the current
directory.  

**Outputs**:

  - main output : a netcdf file (variable : somxlheatc (Joules/m2))

**Climaf call example**::

  >>> from climaf.api import *
  >>> from climaf.operators import fixed_fields
  >>> cdef("frequency","monthly") 
  >>> cdef("project","EM")
  >>> # How to get required files for cdfmxlheatc cdftools binary
  >>> tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
  >>> lpath='/cnrm/aster/data3/aster/vignonl/code/climaf/'
  >>> fixed_fields('ccdfmxlheatc',
             target=[tpath+'ORCA1_mesh_mask.nc',tpath+'ORCA1_mesh_hgr.nc',tpath+'ORCA1_mesh_zgr.nc'],
             link=[lpath+'mask.nc',lpath+'mesh_hgr.nc',lpath+'mesh_zgr.nc'])
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") # dataset with temperature
  >>> d2=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807", realm="O") # dataset with mld
  >>> my_cdfmxlheatc=ccdfmxlheatc(d1,d2)
  >>> cfile(my_cdfmxlheatc) # to compute the heat content in the mixed layer and get a filename with the result 

**Implementation**: The operator is implemented as a binary using
cdfmxlheatc cdftools operator. 

**CliMAF call sequence pattern** (for reference)::
  
  >>> 'tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfmxlheatc $tmp_file ${opt}; mv mxlheatc.nc ${out}; rm -f mxlheatc.nc $tmp_file'
