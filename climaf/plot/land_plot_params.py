#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created : S.Sénési - nov 2015
# Adapter : J.Servonnat - april 2016

dict_plot_params = {
    # -- Energy Budget
    'fluxsens': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': '-20 -10 0 10 20 30 40 50 60 70 80 90 100 110 120 130'},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -60, 'max': 60, 'delta': 10},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
    },
    'fluxlat': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': '10 20 30 40 50 60 70 80 90 100 110'},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -50, 'max': 50, 'delta': 5},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
    },
    'albvis': {
        'default': {'color': 'precip3_16lev', 'units': 'W/m2'},
        'full_field': {'colors': '0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -0.8, 'max': 0.8, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.2, 'max': 0.2, 'delta': 0.02},
    },
    'albnir': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': '0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -0.8, 'max': 0.8, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.2, 'max': 0.2, 'delta': 0.02},
    },
    'albnir': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': '0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -0.8, 'max': 0.8, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.2, 'max': 0.2, 'delta': 0.02},
    },
    'tair': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'degC'},
        'full_field': {'colors': '-35 -30 -25 -20 -15 -10 -5 -2 0 2 5 10 15 20 25 30 35', 'offset': -273.15},
        'bias': {'min': -0.8, 'max': 0.8, 'delta': 0.1},
        'model_model': {'min': -2, 'max': 2, 'delta': 0.2},
    },
    'swdown': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': '40 60 80 100 120 140 160 180 200 220 240 260 280 300'},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -60, 'max': 60, 'delta': 10},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
    },
    'lwdown': {
        'default': {'color': 'MPL_jet', 'units': 'W/m2'},
        'full_field': {'colors': '160 180 200 220 240 260 280 300 320 340 360 380 420'},
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
        'full_field': {'colors': '0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8'},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.1},
    },
    'subli': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': '0 0.05 0.1 0.15 0.2 0.3 0.4 0.5 0.6 0.7 0.8'},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.05, 'max': 0.05, 'delta': 0.01},
    },
    'evap': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': '0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5'},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.1},
    },
    'drainage': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': '0 1 2 3 4 5 6 8 10 12 14'},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -2, 'max': 2, 'delta': 0.2},
    },
    'frac_snow': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': '0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'},
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
        'full_field': {'colors': '0 1e-8 2e-8 3e-8 4e-8 5e-8 6e-8 7e-8 8e-8 9e-8 1e-7 1.2e-7',
                       'color': 'precip3_16lev'},
        'bias': {'colors': '-1e-7 -8e-8 -6e-8 -4e-8 -2e-8 -1e-8 -5e-9 5e-9 1e-8 2e-8 4e-8 6e-8 8e-8 1e-7',
                 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'colors': '-1e-7 -8e-8 -6e-8 -4e-8 -2e-8 -1e-8 -5e-9 5e-9 1e-8 2e-8 4e-8 6e-8 8e-8 1e-7',
                        'color': 'ViBlGrWhYeOrRe'},
    },
    'lai': {
        'default': {'color': 'precip3_16lev', 'units': '', 'contours': '0'},
        'full_field': {'colors': '0.5 1 1.5 2 2.5 3 3.5 4 4.5 5'},
        'bias': {'min': -2, 'max': 2, 'delta': 0.2, 'color': 'BlueWhiteOrangeRed'},
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
        'full_field': {'colors': '0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.05},
    },
    'maxvegetfrac': {
        'default': {'color': 'precip3_16lev', 'units': ''},
        'full_field': {'colors': '0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'},
        'bias': {},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -0.5, 'max': 0.5, 'delta': 0.05},
    },

}
