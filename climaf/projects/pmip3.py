#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module declares the PMIP3 model, with access using
intake (so yet only on Spirit)
"""

from env.site_settings import onSpirit
from climaf.classes import cproject, calias, cfreqs, cdef, crealms

if onSpirit:
    # a dict translating CliMAF facets to PMIP3 facets (those known by intake)
    translate_facet = {
        'table': 'cmor_table',
        'frequency': 'time_frequency',
        'simulation': None,
        'domain': None,
    }

    # A pattern for finding period in filename when using intake catalogs
    # (which, as of 20240517, have buggy values for period_start and
    # period_end)
    period_pattern = "*_${PERIOD}.nc"

    cproject('PMIP3', 'institute', 'model', 'experiment', 'frequency', 'realm',
             'table',  'ensemble',  'version', ensemble=['model', 'ensemble'],
             translate_facet=translate_facet, period_pattern=period_pattern, separator='%')

    cfreqs('PMIP3', {'monthly': 'mon', 'daily': 'day'})
    #
    crealms('PMIP3', {'seaice': 'seaIce'})
    #
    cdef('experiment', '*', project='PMIP3')
    cdef('version', '*', project='PMIP3')
    cdef('institute', '*', project='PMIP3')
    cdef('ensemble', 'r1i1p1', project='PMIP3')
    cdef('frequency', '*', project='PMIP3')
    cdef('model', '*', project='PMIP3')
    cdef('realm', '*', project='PMIP3')
    cdef('table', '*', project='PMIP3')
