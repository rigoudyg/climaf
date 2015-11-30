"""

This module declares how to access OCMIP5 data on Ciclad.

Use attributes 'model' and 'frequency'

Example of a path : /prodigfs/project/OCMIP5/OUTPUT/IPSL/IPSL-CM4/CTL/mon/CACO3/CACO3_IPSL_IPSL-CM4_CTL_1860-1869.nc


Example ::

    >>> cdef('model','IPSL-CM4') 
    >>> cdef('frequency','monthly') 
    >>> cactl=ds(project='OCMIP5_Ciclad', simulation='CTL', variable='CACO3', period='1860-1861')


"""

import os

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs
from climaf.site_settings import onCiclad

if onCiclad :
    cproject("OCMIP5","model","simulation",("frequency","monthly"),ensemble=["model"])
    #
    # Declare which facets can be used for defining an ensemble
    #
    dataloc(project="OCMIP5", organization="generic",
            url=['/prodigfs/project/OCMIP5/OUTPUT/*/${model}/${simulation}/${frequency}/'
                 '${variable}/${variable}_*_${model}_${simulation}_YYYY-YYYY.nc'])
    #
    cfreqs('OCMIP5',{'monthly':'mon' })
