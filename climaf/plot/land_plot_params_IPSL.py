#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : S.Sénési - nov 2015
# Adapter : J.Servonnat - april 2016

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.utils import ranges_to_string
from env.environment import *


dict_plot_params = {
    # -- Energy Budget
    'fluxsens': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': ranges_to_string(ranges=[-20, 130, 10])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -60, 'max': 60, 'delta': 10},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
    },
    'fluxlat': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': ranges_to_string(ranges=[10, 110, 10])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -50, 'max': 50, 'delta': 5},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
    },
    'albvis': {
        'default': {'color': 'precip3_16lev', 'units': 'W/m2'},
        'full_field': {'colors': ranges_to_string(ranges=[0.1, 0.9, 0.1])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -0.8, 'max': 0.8, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.2, 'max': 0.2, 'delta': 0.02},
    },
    'albnir': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[0.1, 0.9, 0.1])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -0.8, 'max': 0.8, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.2, 'max': 0.2, 'delta': 0.02},
    },
    'tair': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'degC'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 35, 5], add=2, sym=True), 'offset': -273.15},
        'bias': {'min': -0.8, 'max': 0.8, 'delta': 0.1},
        'model_model': {'min': -2, 'max': 2, 'delta': 0.2},
    },
    'swdown': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': ranges_to_string(ranges=[40, 300, 20])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -60, 'max': 60, 'delta': 10},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
    },
    'lwdown': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': ranges_to_string(ranges=[160, 380, 20], add=420)},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -60, 'max': 60, 'delta': 10},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -5, 'max': 5, 'delta': 1},
    },
    # -- Water Budget
    'transpir': {
        'default': {},
        'full_field': {},
        'bias': {},
        'model_model': {},
    },
    'inter': {
        'default': {},
        'full_field': {},
        'bias': {},
        'model_model': {},
    },
    'evapnu': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[0.2, 1.8, 0.2])},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.1},
    },
    'subli': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[0, 0.8, 0.1], add=[0.05, 0.15])},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.05, 'max': 0.05, 'delta': 0.01},
    },
    'evap': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[0, 5, 0.5])},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.1},
    },
    'drainage': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[[0, 5, 1], [6, 14, 2]])},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -2, 'max': 2, 'delta': 0.2},
    },
    'frac_snow': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[0, 0.9, 0.1])},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.05, 'max': 0.05, 'delta': 0.01},
    },
    'snow': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', },
    },
    # -- Carbon Budget
    'gpp': {
        'default': {'color': 'precip3_16lev', 'units': 'gC.m-2.s-1', 'scale': 1000},
        'full_field': {'colors': ranges_to_string(ranges=[0, 1e-7, 1e-8], add=1.2e-7),
                       'color': 'precip3_16lev'},
        'bias': {'colors': ranges_to_string(ranges=[2e-8, 1e-7, 2e-8], add=[5e-9, 1e-8], sym=True),
                 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'colors': ranges_to_string(ranges=[2e-8, 1e-7, 2e-8], add=[5e-9, 1e-8], sym=True),
                        'color': 'ViBlGrWhYeOrRe'},
    },
    'gpptot': {
        'default': {'color': 'precip3_16lev', 'units': 'gC.m-2.yr-1', 'scale': 365. * 86400. * 1000.},
        'full_field': {'colors': ranges_to_string(ranges=[250, 3500, 250], add=[50, 100]), 'color': 'precip3_16lev'},
        'bias': {'min': -1000., 'max': 1000, 'delta': 100, 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'min': -500., 'max': 500, 'delta': 50, 'color': 'ViBlGrWhYeOrRe'},
    },
    'GPP_treeFracPrimDec': {
        'default': {'color': 'precip3_16lev', 'units': 'gC.m-2.yr-1', 'scale': 365. * 86400. * 1000.},
        'full_field': {'colors': ranges_to_string(ranges=[100, 1200, 100], add=50), 'color': 'precip3_16lev'},
        'bias': {'min': -1000., 'max': 1000, 'delta': 100, 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'min': -500., 'max': 500, 'delta': 50, 'color': 'ViBlGrWhYeOrRe'},
    },
    'GPP_treeFracPrimEver': {
        'default': {'color': 'precip3_16lev', 'units': 'gC.m-2.yr-1', 'scale': 365. * 86400. * 1000.},
        'full_field': {'colors': ranges_to_string(ranges=[250, 3500, 250], add=[50, 100]),
                       'color': 'precip3_16lev'},
        'bias': {'min': -1000., 'max': 1000, 'delta': 100, 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'min': -500., 'max': 500, 'delta': 50, 'color': 'ViBlGrWhYeOrRe'},
    },
    'GPP_c3PftFrac': {
        'default': {'color': 'precip3_16lev', 'units': 'gC.m-2.yr-1', 'scale': 365. * 86400. * 1000.},
        'full_field': {'colors': ranges_to_string(ranges=[100, 900, 100], add=[20, 50]), 'color': 'precip3_16lev'},
        'bias': {'min': -1000., 'max': 1000, 'delta': 100, 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'min': -500., 'max': 500, 'delta': 50, 'color': 'ViBlGrWhYeOrRe'},
    },
    'GPP_c4PftFrac': {
        'default': {'color': 'precip3_16lev', 'units': 'gC.m-2.yr-1', 'scale': 365. * 86400. * 1000.},
        'full_field': {'colors': ranges_to_string(ranges=[[50, 550, 50], [600, 1100, 100]], add=10),
                       'color': 'precip3_16lev'},
        'bias': {'min': -1000., 'max': 1000, 'delta': 100, 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'min': -500., 'max': 500, 'delta': 50, 'color': 'ViBlGrWhYeOrRe'},
    },

    'lai': {
        'default': {'color': 'precip3_16lev', 'units': '', 'contours': '0'},
        # 'full_field': {'colors':'0.5 1 1.5 2 2.5 3 3.5 4 4.5 '},
        'full_field': {'min': 0.5, 'max': 5, 'delta': 0.5},
        'bias': {'min': -2, 'max': 2, 'delta': 0.2, 'color': 'BlueWhiteOrangeRed', 'contours': '0'},
        'model_model': {'min': -2, 'max': 2, 'delta': 0.2, 'color': 'BlueWhiteOrangeRed'},
    },
    'maint_resp': {
        'default': {},
        'full_field': {},
        'bias': {},
        'model_model': {},
    },
    'growth_resp': {
        'default': {},
        'full_field': {},
        'bias': {},
        'model_model': {},
    },
    'auto_resp': {
        'default': {},
        'full_field': {},
        'bias': {},
        'model_model': {},
    },
    'hetero_resp': {
        'default': {},
        'full_field': {},
        'bias': {},
        'model_model': {},
    },
    'nee': {
        'default': {},
        'full_field': {},
        'bias': {},
        'model_model': {},
    },
    'vegetfrac': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[0.1, 0.9, 0.1], add=0.01)},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.05},
    },
    'maxvegetfrac': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': ranges_to_string(ranges=[0.1, 0.9, 0.1], add=0.01)},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.05},
    },
}
