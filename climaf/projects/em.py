"""This module declares project em , base on data organization 'generic'

EM (Experiment Manager) is a tool used at CNRM for moving simulation post-processed data
from the HPSS to the local filesystem, and to organize it in a file hierarchy governed by a few
configuration files

Simulation names (or 'EXPIDs') are assumed to be unique in the
namespace defined by the user's configuration file, which may include
shared simulation

Examples for defining an EM dataset::

 >>> tas= ds(project='em', simulation='GSAGNS1', variable='tas', period='1975-1976')
 >>> pr = ds(project='em', simulation="C1P60", group="SC, variable="pr"   , period="1850")

See other examples in :download:`examples/data_em.py <../examples/data_em.py>`

The location of ocean variables in the various grid_XX files is for now only partially declared to CliMAF

A number of Seaice fields are duly described with 1.e+20 as missing
value (which is ill described in data files); see code for details

"""
# S.Senesi - april 2016

from climaf.site_settings import atCNRM

if atCNRM :

    from climaf.dataloc import dataloc
    from climaf.classes import cproject, calias, cfreqs,cdef
    

    # In project 'em', there is a ROOT location, data is organized in
    # REALMS, and we handle data FREQUENCY
    # 'root' stands for em root directory for alla experiment data (EM_NETCDF_DIR)

    cproject("em","root","group","realm", "frequency",separator="|")

    # Describe data organization : file hierarchy and filename patterns
    ######################################################################

    # User simulations
    pathg="${root}/${group}/${simulation}/"
    pathA=pathg+"${realm}/${simulation}PLYYYY.nc" #GSAG
    pathL=pathg+"${realm}/${simulation}SFXYYYY.nc"
    pathI=pathg+"${realm}/${variable}_O1_YYYY-YYYY.nc" #HISTNATr8
    pathO=pathg+"${realm}/${simulation}_1${frequency}_YYYYMMDD_YYYYMMDD_grid_${variable}.nc" # var:T_table2.2
    pathO2=pathg+"${realm}/${simulation}_1${frequency}_YYYYMMDD_YYYYMMDD_scalar_table2.2.nc" # PICTLWS2, PRE6CPLCr2alb
    
    dataloc(project="em", organization="generic", url=[pathA,pathL,pathI,pathO,pathO2])
    
    # Shared simulations - example : group=SC
    pathg="/cnrm/aster/data1/simulations/${group}/"
    pathgA=pathg+"Atmos/Regu/${frequency}/${simulation}/${simulation}PLYYYY.nc" #C1P60
    pathgL=pathg+"Land/Regu/${frequency}/${simulation}/${simulation}SFXYYYY.nc" #C1P60
    pathgI=pathg+"Seaice/Origin/Monthly/${simulation}/${variable}_O1_YYYY-YYYY.nc" #HISTNATr8
    pathgO=pathg+"Ocean/Origin/Monthly/${simulation}/${simulation}_1${frequency}_YYYYMMDD_YYYYMMDD_grid_${variable}.nc" 
    
    dataloc(project="em", organization="generic", url=[pathgA,pathgL,pathgI,pathgO])
    

    # Define default values
    ############################################

    # You do not need to use a GROUPs experiment
    cdef("group","",project="em") ;  

    # Files hierarchy and file naming conventions for ocean data requires 
    # to tell freq="m" when defining a monthly ocean dataset. Otherwise, it defaults to 'mon'
    cdef("frequency","mon",project="em") ;

    # Realm is used only for sometimes disambiguating a variable among realms
    cdef("realm","*",project="em") ;  # A/L/I/O or , for shared simulation : Atmos/Land/Seaice/Ocean 


    # More details about data organization
    ############################################

    # Describe how to locate some ocean variables in multi-variable data files
    calias("em", 'sos' ,filenameVar='S*')
    calias("em", 'so'  ,filenameVar='S*')
    calias("em", 'fcalva' ,filenameVar='S*')
    calias("em", 'fcalvg' ,filenameVar='S*')
    calias("em", 'omlmax' ,filenameVar='S*')
    calias("em", 'wfo' ,filenameVar='S*')
    calias("em", 'friver' ,filenameVar='S*')
    calias("em", 'e-p' ,filenameVar='S*')
    calias("em", 'flake' ,filenameVar='S*')
    
    calias("em", 'to'  ,filenameVar='T*')
    calias("em", 'tos' ,filenameVar='T*')
    calias("em", 'tossq' ,filenameVar='T*')
    calias("em", 'zos' ,filenameVar='T*')
    calias("em", 'zossq' ,filenameVar='T*')
    calias("em", 'nshfls' ,filenameVar='T*')
    calias("em", 'rsntds' ,filenameVar='T*')
    
    calias("em", 'uo' ,filenameVar='U*')
    calias("em", 'tauuo' ,filenameVar='U*')
    calias("em", 'uos' ,filenameVar='U*')
    calias("em", 'vo' ,filenameVar='V*')
    calias("em", 'tauvo' ,filenameVar='V*')
    calias("em", 'vos' ,filenameVar='V*')

    # .... to be continued
    
    # A fix for seaice missing values
    calias('em',[ 'sic', 'sit', 'sim', 'snd', 'ialb', 'tsice', 'mpalb', 'snomlet',
                  'tmelt', 'bmelt', 'snc','sic1','sic2', 'sic3', 'sic4', 'ssi', 'ageice'],
           missing=1.e+20)
    # Ideally, one should be able to write :
    #cmissing('em',1.e+20, realm='I')

