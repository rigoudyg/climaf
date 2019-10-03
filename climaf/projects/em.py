#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module declares project em, base on data organization 'generic'

EM (Experiment Manager) is a tool used at CNRM for moving simulation post-processed data
from the HPSS to the local filesystem, and to organize it in a file hierarchy governed by a few
configuration files

Simulation names (or 'EXPIDs') are assumed to be unique in the
namespace defined by the user's configuration file, which may include
shared simulation

Specific facets are :
  - root : root directory for private data files as declared to EM
  - group : group of the simualtion (as declared to ECLIS)
  - frequency : for now, only monthly is managed; it is the default
  - realm : to speed up data search, and to resolve ambiguities. Usable values
    are 'A, Atmos, O, Ocean, I, SeaIce, L, Land. Unfortunately, for now,
    you have to know whether you data is on a private dir (use e.g. 'A') or a
    shared one (use e.g. Atmos). Default is '*' (costly).

Examples for defining an EM dataset::

 >>> tas= ds(project='em', simulation='GSAGNS1', variable='tas', period='1975-1976', realm="(A|Atmos)")
 >>> pr = ds(project='em', simulation="C1P60", group="SC, variable="pr"   , period="1850", realm="(O|Ocean)"))

See other examples in :download:`examples/data_em.py <../examples/data_em.py>`

The location of ocean variables in the various grid_XX files matches the case with :
T_table_2.2, T_table_2.5, T_table_2.7, U_table_2.3, U_table_2.8, W_table2.3 ...
Other cases should be described by another 'project'

WARNING REGARDING OCEAN DATA : for a number of old simulations, there
is an issue with the name of time coordinates, which lead to some
nav_lat/nav_lon coordinates being discarded during CDO processing. You
can tell CLiMAF to deal automatically with that, at the expense of
computing time, by setting and exporting environment variable
CLIMAF_FIX_NEMO_TIME to any value except 'no', '0' and 'None' BEFORE launching
CliMAF. What CliMAF does in that case shows in
:download:`../scripts/mcdo.py` (see function nemo_timefix())

A number of Seaice fields are duly described with 1.e+20 as missing
value (which is ill described in data files); see code for details

"""
# S.Senesi - april 2016

from climaf.site_settings import atCNRM

if atCNRM:
    from climaf.dataloc import dataloc
    from climaf.classes import cproject, calias, cfreqs, cdef

    # In project 'em', there is a ROOT location, data is organized in
    # REALMS, and we handle data FREQUENCY
    # 'root' stands for em root directory for alla experiment data (EM_NETCDF_DIR)

    cproject("em", "root", "group", "realm", "frequency", separator="|")

    # Describe data organization : file hierarchy and filename patterns
    ######################################################################

    # User simulations
    pathg = "${root}/${group}/${simulation}/"
    pathA = pathg + "${realm}/${simulation}PLYYYY.nc"  # GSAG
    pathL = pathg + "${realm}/${simulation}SFXYYYY.nc"
    pathI = pathg + "${realm}/${variable}_O1_YYYY-YYYY.nc"  # HISTNATr8
    pathO = pathg + "${realm}/${simulation}_1${frequency}_${PERIOD}_grid_${variable}.nc"  # var:T_table2.2
    pathO2 = pathg + "${realm}/${simulation}_1${frequency}_${PERIOD}_scalar_table2.2.nc"  # PICTLWS2, PRE6CPLCr2alb

    dataloc(project="em", organization="generic", url=[pathA, pathL, pathI, pathO, pathO2])

    # Shared simulations - example : group=SC
    pathg = "/cnrm/cmip/cnrm/simulations/${group}/"
    pathgA = pathg + "${realm}/Regu/${frequency}/${simulation}/${simulation}PLYYYY.nc"  # C1P60
    pathgL = pathg + "${realm}/Regu/${frequency}/${simulation}/${simulation}SFXYYYY.nc"  # C1P60
    pathgI = pathg + "${realm}/Origin/Monthly/${simulation}/${variable}_O1_${PERIOD}.nc"  # HISTNATr8
    pathgO = pathg + "${realm}/Origin/Monthly/${simulation}/${simulation}_1${frequency}_${PERIOD}_grid_${variable}.nc"

    dataloc(project="em", organization="generic", url=[pathgA, pathgL, pathgI, pathgO])

    # Define default values
    ############################################

    # You do not need to use a GROUPs experiment
    cdef("group", "", project="em")

    # Files hierarchy and file naming conventions for ocean data requires
    # to tell freq="m" when defining a monthly ocean dataset. Otherwise, it defaults to 'mon'
    cdef("frequency", "mon", project="em")

    # Realm is used only for sometimes disambiguating a variable among realms
    cdef("realm", "*", project="em")  # A/L/I/O or , for shared simulation : Atmos/Land/Seaice/Ocean

    # More details about data organization
    ############################################

    # Describe how to locate some ocean variables in multi-variable data files
    # calias("em", 'sos' ,filenameVar='S*')
    # calias("em", 'so'  ,filenameVar='S*')
    # calias("em", 'fcalva' ,filenameVar='S*')
    # calias("em", 'fcalvg' ,filenameVar='S*')
    # calias("em", 'omlmax' ,filenameVar='S*')
    # calias("em", 'wfo' ,filenameVar='S*')
    # calias("em", 'friver' ,filenameVar='S*')
    # calias("em", 'e-p' ,filenameVar='S*')
    # calias("em", 'flake' ,filenameVar='S*')

    calias("em", 'to', offset=273.15, filenameVar='T_table2.2')
    calias("em", 'tos', offset=273.15, filenameVar='T_table2.2')
    calias("em", 'tossq', filenameVar='T_table2.2')
    calias("em", 'zos', filenameVar='T_table2.2')
    calias("em", 'zossq', filenameVar='T_table2.2')
    calias("em", 'zosto', filenameVar='T_table2.2')
    calias("em", 'omlmax', filenameVar='T_table2.2')
    calias("em", 'pbo', filenameVar='T_table2.2')
    calias("em", 'rhopoto', filenameVar='T_table2.2')
    calias("em", 'so', filenameVar='T_table2.2')
    calias("em", 'sos', filenameVar='T_table2.2')
    calias("em", 'thetao', filenameVar='T_table2.2')

    calias("em", 'emps', filenameVar='T_table2.5')
    calias("em", 'evt', filenameVar='T_table2.5')
    calias("em", 'evs', filenameVar='T_table2.5')
    calias("em", 'ficeberg', filenameVar='T_table2.5')
    calias("em", 'friver', filenameVar='T_table2.5')
    calias("em", 'pr', filenameVar='T_table2.5')
    calias("em", 'prsn', filenameVar='T_table2.5')
    calias("em", 'prsnt', filenameVar='T_table2.5')
    calias("em", 'wfcorr', filenameVar='T_table2.5')
    calias("em", 'wfo', filenameVar='T_table2.5')

    calias("em", 'hfcorr', filenameVar='T_table2.7')
    calias("em", 'hfevapds', filenameVar='T_table2.7')
    calias("em", 'hfrainds', filenameVar='T_table2.7')
    calias("em", 'hfrunoffds', filenameVar='T_table2.7')
    calias("em", 'nshfls', filenameVar='T_table2.7')
    calias("em", 'rsntds', filenameVar='T_table2.7')

    calias("em", 'umo', filenameVar='U_table2.3')
    calias("em", 'uo', filenameVar='U_table2.3')
    calias("em", 'hfx', filenameVar='U_table2.3')
    calias("em", 'hfxba', filenameVar='U_table2.3')
    calias("em", 'hfxdiff', filenameVar='U_table2.3')

    calias("em", 'tauuo', filenameVar='U_table2.8')

    calias("em", 'vmo', filenameVar='V_table2.3')
    calias("em", 'vo', filenameVar='V_table2.3')
    calias("em", 'hfy', filenameVar='V_table2.3')
    calias("em", 'hfyba', filenameVar='V_table2.3')
    calias("em", 'hfydiff', filenameVar='V_table2.3')

    calias("em", 'tauvo', filenameVar='V_table2.8')

    calias("em", 'wmo', filenameVar='W_table2.3')
    calias("em", 'wmosq', filenameVar='W_table2.3')

    # .... to be continued

    # A fix for seaice missing values
    calias('em', ['sic', 'sit', 'sim', 'snd', 'ialb', 'tsice', 'mpalb', 'snomlet',
                  'tmelt', 'bmelt', 'snc', 'sic1', 'sic2', 'sic3', 'sic4', 'ssi', 'ageice'],
           missing=1.e+20)
    # Ideally, one should be able to write :
    # cmissing('em',1.e+20, realm='I')
