"""This module declares project emn36 , base on data organization 'generic', for 
handling Nemo36 data such as organized by EM 

EM (Experiment Manager) is a tool used at CNRM for moving simulation post-processed data
from the HPSS to the local filesystem, and to organize it in a file hierarchy governed by a few
configuration files

Simulation names (or 'EXPIDs') are assumed to be unique in the
namespace defined by the user's configuration file, which may include
shared simulation

Specific facets are : 
  - root : root directory for private data files as declared to EM
  - group : group of the simualtion (as declared to ECLIS)
  - frequency 

Examples for defining an EM dataset::

 >>> pr = ...

The location of ocean variables in the various grid_XX files matches the case with :
grid_T.nc, grid_S.nc ...

Seaice fields are still to be described

"""
# S.Senesi - april 2016

from climaf.site_settings import atCNRM

if atCNRM :

    from climaf.dataloc import dataloc
    from climaf.classes import cproject, calias, cfreqs,cdef
    
    # example : /cnrm/aster/data3/aster/voldoire/NO_SAVE/PRE6/CPLTEA623O45

    # In project 'emn36', there is a ROOT location, data is organized in
    # REALMS, and we handle data FREQUENCY
    # 'root' stands for em root directory for alla experiment data (EM_NETCDF_DIR)

    cproject("emn36","root","group", "frequency",separator="|")

    # Describe data organization : file hierarchy and filename patterns
    ######################################################################

    # User simulations
    pathG="${root}/${group}/${simulation}/"
    pathI=pathG+"O/${simulation}_1${frequency}_YYYYMMDD_YYYYMMDD_icemod.nc" # var:T
    pathO=pathG+"O/${simulation}_1${frequency}_YYYYMMDD_YYYYMMDD_grid_${variable}.nc" # var:T
    dataloc(project="emn36", organization="generic", url=[pathI,pathO])
    
    # Shared simulations 
    pathg="/cnrm/aster/data1/simulations/${group}/"
    pathgI=pathg+"O/Origin/Monthly/${simulation}/${simulation}_1${frequency}_YYYYMMDD_YYYYMMDD_icemod.nc" 
    pathgO=pathg+"O/Origin/Monthly/${simulation}/${simulation}_1${frequency}_YYYYMMDD_YYYYMMDD_grid_${variable}.nc" 
    dataloc(project="emn36", organization="generic", url=[pathgI,pathgO])

    # Define default values
    ############################################

    # You do not need to use a GROUPs experiment
    cdef("group","",project="emn36") ;  

    cdef("frequency","monthly",project="emn36") ;
    cfreqs("emn36",{"daily":"d", "monthly":"m"})

    # More details about data organization
    ############################################

    # Describe how to locate some ocean variables in multi-variable data files
    calias("emn36", 'e-p' ,filenameVar='S')
    calias("emn36", 'fcalva' ,filenameVar='S')
    calias("emn36", 'fcalvg' ,filenameVar='S')
    calias("emn36", 'friver' ,filenameVar='S')
    calias("emn36", 'flake' ,filenameVar='S')
    calias("emn36", 'omlmax' ,filenameVar='S')
    calias("emn36", 'so'  ,filenameVar='S')
    calias("emn36", 'sos' ,filenameVar='S')
    calias("emn36", 'wfo' ,filenameVar='S')
    
    calias("emn36", 'thetao',filenameVar='T')
    calias("emn36", 'tos'   ,filenameVar='T')
    calias("emn36", 'tossq' ,filenameVar='T')
    calias("emn36", 'zos'   ,filenameVar='T')
    calias("emn36", 'zossq' ,filenameVar='T')
    calias("emn36", 'nshfls',filenameVar='T')
    calias("emn36", 'rsntds',filenameVar='T')
    
    calias("emn36", 'uo' ,filenameVar='U')
    calias("emn36", 'uos' ,filenameVar='U')
    calias("emn36", 'tauuo' ,filenameVar='U')

    calias("emn36", 'vo' ,filenameVar='U')
    calias("emn36", 'vos' ,filenameVar='U')
    calias("emn36", 'tauvo' ,filenameVar='U')

    calias("emn36", 'wmo' ,filenameVar='W')
    calias("emn36", 'wmosq' ,filenameVar='W')

    # icemod
    # siconc
    # sidive
    # sishea
    # sistre
    # sivelo
    # sivelu
    # sivelv
    # sivolu
    # snvolu
    

    # .... to be continued
    
    # A fix for seaice missing values
    #calias('emn36',[ 'sic', 'sit', 'sim', 'snd', 'ialb', 'tsice', 'mpalb', 'snomlet',
    #              'tmelt', 'bmelt', 'snc','sic1','sic2', 'sic3', 'sic4', 'ssi', 'ageice'],
    #       missing=1.e+20)
    # Ideally, one should be able to write :
    #cmissing('emn36',1.e+20, realm='I')

