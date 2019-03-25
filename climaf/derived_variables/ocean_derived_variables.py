#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.api import derive, calias

# -- Potential Temperature and salinity @ 200m, 1000m and 2000m in depth
# derive('*','so_onevar','cncks','so')
# derive('*','thetao_onevar','cncks','thetao')
# derive('*','so200','ccdo','so_onevar',operator='intlevel,200')
derive('*', 'so200', 'ccdo', 'so', operator='intlevel,200')
derive('*', 'so1000', 'ccdo', 'so', operator='intlevel,1000')
derive('*', 'so2000', 'ccdo', 'so', operator='intlevel,2000')
derive('*', 'to200', 'ccdo', 'thetao', operator='intlevel,200')
derive('*', 'to1000', 'ccdo', 'thetao', operator='intlevel,1000')
derive('*', 'to2000', 'ccdo', 'thetao', operator='intlevel,2000')

# -- Biogeochemistry
derive('*', 'NO3_surf', 'ccdo', 'NO3', operator='sellevidx,1')
derive('*', 'NO3_300m', 'ccdo', 'NO3', operator='intlevel,300')
derive('*', 'NO3_1000m', 'ccdo', 'NO3', operator='intlevel,1000')
derive('*', 'NO3_2500m', 'ccdo', 'NO3', operator='intlevel,2500')

derive('*', 'PO4_surf', 'ccdo', 'PO4', operator='sellevidx,1')
derive('*', 'PO4_300m', 'ccdo', 'PO4', operator='intlevel,300')
derive('*', 'PO4_1000m', 'ccdo', 'PO4', operator='intlevel,1000')
derive('*', 'PO4_2500m', 'ccdo', 'PO4', operator='intlevel,2500')

derive('*', 'O2_surf', 'ccdo', 'O2', operator='sellevidx,1')
derive('*', 'O2_300m', 'ccdo', 'O2', operator='intlevel,300')
derive('*', 'O2_1000m', 'ccdo', 'O2', operator='intlevel,1000')
derive('*', 'O2_2500m', 'ccdo', 'O2', operator='intlevel,2500')

derive('*', 'Si_surf', 'ccdo', 'Si', operator='sellevidx,1')
derive('*', 'Si_300m', 'ccdo', 'Si', operator='intlevel,300')
derive('*', 'Si_1000m', 'ccdo', 'Si', operator='intlevel,1000')
derive('*', 'Si_2500m', 'ccdo', 'Si', operator='intlevel,2500')

derive('*', 'tod', 'ccdo', 'thetao', operator='intlevel,50,100,250,500,1000,2000')
derive('*', 'sod', 'ccdo', 'so', operator='intlevel,50,100,250,500,1000,2000')
