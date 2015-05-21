"""
This module declares locations for searching data for project OBS4MIP at CNRM (VDR),  for all frequencies, 

Additional attribute for OBS4MIPS datasets  : only 'frequency'

Example for an OBS4MIPS CMIP5 dataset declaration ::

 >>> pr_obs=ds(project='OBS4MIPS', variable='pr', frequency='monthly', period='1979-1980', experiment='GPCP-SG')


"""
import os.path

if os.path.exists('/cnrm'):
    from climaf.dataloc import dataloc
    from climaf.classes import cproject, calias, cfreqs

    cproject("OBS4MIPS","frequency")
    # Frequency alias
    cfreqs('OBS4MIPS', {'monthly':'monthly_mean' })
    #
    pattern="/cnrm/vdr/DATA/Obs4MIPs/netcdf/${frequency}/${variable}_${experiment}_*_YYYYMM-YYYYMM.nc"
    dataloc(project="OBS4MIPS", organization="generic", url=[pattern])


