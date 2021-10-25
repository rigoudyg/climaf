#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for IPSL CMIP6 outputs produced by libIGCM for all frequencies,
on Ciclad.

Contact: jerome.servonnat@lsce.ipsl.fr

"""

from __future__ import print_function, division, unicode_literals, absolute_import


from env.site_settings import atTGCC, onCiclad, onSpip
from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, crealms, cdef

root = None
login = None
if atTGCC:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/ccc/work/cont003/gencmip6"
if onCiclad:
    # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
    root = "/ccc/work/cont003/thredds"
    login = "fabric"
if onSpip:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/Users/marti/Volumes/CURIE/ccc/store/cont003/dsm"
    print('igcm_out : declaration root sur Spip : ', root)

if root:
    # -- Declare a 'CMIP' CliMAF project (a replicate of the CMIP5 project)
    # ---------------------------------------------------------------------------- >
    cproject('IGCM_CMIP6', 'root', 'login', 'IPSL_MODEL', 'status', 'experiment', 'realm', 'frequency', 'table',
             'model', 'realization', 'grid', ensemble=['model', 'simulation', 'realization'], separator='%')
    # --> systematic arguments = simulation, frequency, variable
    # -- Set the aliases for the frequency
    cfreqs('IGCM_CMIP6', {'monthly': 'mon', 'yearly': 'yr', 'daily': 'day'})
    crealms('IGCM_CMIP6', {'atmos': 'ATM', 'ocean': 'OCE', 'land': 'SRF', 'seaice': 'ICE'})
    # -- Set default values
    cdef('IPSL_MODEL', 'IPSLCM6', project='IGCM_CMIP6')
    cdef('realization', 'r1i1p1f1', project='IGCM_CMIP6')
    cdef('status', '*', project='IGCM_CMIP6')
    cdef('experiment', 'historical', project='IGCM_CMIP6')
    cdef('realm', '*', project='IGCM_CMIP6')
    cdef('table', '_', project='IGCM_CMIP6')
    cdef('frequency', 'monthly', project='IGCM_CMIP6')
    cdef('grid', 'gr', project='IGCM_CMIP6')
    cdef('root', root, project='IGCM_CMIP6')

    # -- Specify the pattern
    pattern1 = "${root}/${login}/IGCM_OUT/${IPSL_MODEL}/${status}/${experiment}/${simulation}/CMIP6/${realm}/" \
               "${variable}_*${frequency}_${model}_${experiment}_${realization}_${grid}_${PERIOD}.nc"
    pattern2 = "${root}/${login}/IGCM_OUT/${IPSL_MODEL}/${status}/${experiment}/${simulation}/CMIP6/${realm}/" \
               "${variable}_${table}_${model}_${experiment}_${realization}_${grid}_${PERIOD}.nc"
    # pattern3="${root}/${login}/IGCM_OUT/${IPSL_MODEL}/${status}/${experiment}/${simulation}/CMIP6/${realm}/"
    #          "${variable}_${MIP_prefix}${frequency}${MIP_suffix}${qualifier}_${model}_${experiment}_${realization}_"
    #          "${grid}_${PERIOD}.nc"
    # pattern4="${root}/${login}/IGCM_OUT/${IPSL_MODEL}/${status}/${experiment}/${simulation}/CMIP6/${realm}/"
    #          "${variable}_${miptable}_${model}_${experiment}_${realization}_${grid}_${PERIOD}.nc"
    # -- Si on precise seulement la MIP table, on n'a pas la frequence ;
    #    on pourrait rajouter une analyse de la table, si elle existe, pour rajouter la frequence?
    #

    # pattern1="${root}/*/${variable}_${table}_${model}_${experiment}_${realization}_${gr}_${PERIOD}.nc"
    # pattern2="${root}/${variable}_${table}_${model}_${experiment}_${realization}_${gr}_${PERIOD}.nc"
    # -- call the dataloc CliMAF function
    dataloc(project='IGCM_CMIP6', organization='generic', url=[pattern2])

    calias('IGCM_CMIP6', 'tos', offset=273.15)
    calias('IGCM_CMIP6', 'thetao', offset=273.15)
    calias('IGCM_CMIP6', 'sic', 'siconc')
    calias('IGCM_CMIP6', 'sit', 'sithick')
    calias('IGCM_CMIP6', 'wfo', 'wfonocorr')
    calias('IGCM_CMIP6', 'sivolu', 'sivol')
    calias('IGCM_CMIP6', 'NO3', 'no3')
    calias('IGCM_CMIP6', 'PO4', 'po4')
    calias('IGCM_CMIP6', 'Si', 'si')
    calias('IGCM_CMIP6', 'O2', 'o2')
