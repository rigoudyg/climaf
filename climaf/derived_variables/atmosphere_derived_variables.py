#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *
from climaf.operators_derive import derive

# -- DTR
derive('*', 'dtr', 'minus', 'tasmax', 'tasmin')
derive('*', 'tasrange', 'minus', 'tasmax', 'tasmin')

# -- Radiative SW Total at TOA
derive('*', 'rstt', 'minus', 'rsdt', 'rsut')
derive('*', 'rst', 'minus', 'rsdt', 'rsut')
# -- Radiative SW Total at surface
derive('*', 'rsts', 'minus', 'rsds', 'rsus')
# -- Radiative LW Total at surface
derive('*', 'rlts', 'minus', 'rlds', 'rlus')
# -- Radiative LW Total at surface - CS
derive('*', 'rltscs', 'minus', 'rldscs', 'rluscs')
# -- Radiative SW Total at surface - CS
derive('*', 'rstscs', 'minus', 'rsdscs', 'rsuscs')
# -- Radiative SW Total at TOA - CS
derive('*', 'rsttcs', 'minus', 'rsdt', 'rsutcs')

# -- Radiative Total at TOA
derive('*', 'rtt', 'minus', 'rstt', 'rlut')
derive('*', 'rt', 'minus', 'rstt', 'rlut')
# -- Radiative Total at surface
derive('*', 'rts', 'plus', 'rsts', 'rlts')

# -- Cloud radiative effect SW at surface
derive('*', 'cress', 'minus', 'rsds', 'rsdscs')
# -- Cloud radiative effect SW at surface
derive('*', 'crels', 'minus', 'rlds', 'rldscs')
# -- Cloud radiative effect Total at surface
derive('*', 'crets', 'plus', 'cress', 'crels')

# -- Cloud radiative effect SW at TOA
derive('*', 'crest', 'minus', 'rsutcs', 'rsut')
derive('*', 'rstcre', 'minus', 'rsutcs', 'rsut')
# -- Cloud radiative effect LW at TOA
derive('*', 'crelt', 'minus', 'rlutcs', 'rlut')
derive('*', 'rltcre', 'minus', 'rlutcs', 'rlut')
# -- Cloud radiative effect Total at TOA
derive('*', 'crett', 'plus', 'crest', 'crelt')
derive('*', 'rtnetcre', 'plus', 'crest', 'crelt')

# -- Total Non-radiative Heat Fluxes at surface
derive('*', 'hfns', 'plus', 'hfls', 'hfss')
# -- Radiative budget at surface
derive('*', 'bil', 'minus', 'rts', 'hfns')
derive('*', 'tsmtas', 'minus', 'ts', 'tas')

# -- Atm. LW Heat
derive('*', 'rlah', 'minus', 'rlut', 'rlts')
# -- Atm. LW Heat - CS (rlahcs)
derive('*', 'rtmp', 'plus', 'rldscs', 'rlutcs')
derive('*', 'rlahcs', 'minus', 'rlus', 'rtmp')
# -- Atm. LW Heat - CRE
derive('*', 'rlahcre', 'minus', 'rlah', 'rlahcs')
#
# -- Atm. SW Heat
derive('*', 'rsah', 'minus', 'rstt', 'rsts')
# -- Atm. SW Heat - CS (rlahcs)
derive('*', 'rsahcs', 'minus', 'rsttcs', 'rstscs')
# -- Atm. SW Heat - CRE
derive('*', 'rsahcre', 'minus', 'rsah', 'rsahcs')

# -- Atm. Total Heat
derive('*', 'rah', 'plus', 'rsah', 'rlah')
# -- Atm. Total Heat - CS (rlahcs)
derive('*', 'rahcs', 'plus', 'rsahcs', 'rlahcs')
# -- Atm. Total Heat - CRE
derive('*', 'rahcre', 'minus', 'rah', 'rahcs')

# -- Planetary albedo at TOA
derive('*', 'albt', 'divide', 'rsut', 'rsdt')
# -- Planetary albedo at surface
derive('*', 'albs', 'divide', 'rsus', 'rsds')

# -- Atmosphere Curl Tau
derive('*', 'curltau', 'curl_tau_atm', 'tauu', 'tauv')

# -- Atmospheric Variables on vertical levels
for tmpvar in ['ua', 'va', 'ta', 'hus', 'hur', 'zg']:
    for tmplev in ['850', '700', '500', '200']:
        derive('*', tmpvar + tmplev, 'ccdo', tmpvar, operator='intlevel,' + tmplev + '00')

# ua, va et ta sur moyenne sectorielle Atl
Atl_sect = '-60,-15,-90,90'
derive('*', 'ua_Atl_sect', 'ccdo', 'ua', operator='sellonlatbox,' + Atl_sect)
derive('*', 'va_Atl_sect', 'ccdo', 'va', operator='sellonlatbox,' + Atl_sect)
derive('*', 'ta_Atl_sect', 'ccdo', 'ta', operator='sellonlatbox,' + Atl_sect)
derive('*', 'hus_Atl_sect', 'ccdo', 'hus', operator='sellonlatbox,' + Atl_sect)
