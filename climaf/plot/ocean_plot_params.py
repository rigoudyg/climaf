#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : S.Sénési - nov 2015

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.utils import ranges_to_string
from env.environment import *


dict_plot_params = {
    'wfo': {
        'default': {'units': 'mm/day', 'color': 'precip_diff_12lev', 'scale': 86400., 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 12, 2], add=[1, 3, 15], sym=True)},
        'bias': {'color': 'precip_diff_12lev', 'colors': ranges_to_string(ranges=[2, 8, 2], add=[0.5, 1], sym=True)},
        'model_model': {'color': 'precip_diff_12lev',
                        'colors': ranges_to_string(ranges=[2, 8, 2], add=[0.5, 1], sym=True)},
    },
    'NO3_surf': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[2, 32, 2])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
    },
    'PO4_surf': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[0.25, 5.5, 0.25])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -1, 'max': 1, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -1, 'max': 1, 'delta': 0.1},
    },
    'O2_surf': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[200, 410, 10])},
        # 'colors':"2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32"},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -50, 'max': 50, 'delta': 5},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
    },
    'Si_surf': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 95, 5])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
    },
    'NO3_1000m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[2, 32, 2])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'PO4_1000m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[0.25, 5.5, 0.25])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -1, 'max': 1, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'O2_1000m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[20, 320, 20])},
        # 'colors':"2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32"},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -100, 'max': 100, 'delta': 5},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'Si_1000m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[[10, 95, 5], [100, 150, 10]])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -100, 'max': 100, 'delta': 5},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
    },
    'NO3_300m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[2, 32, 2])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'PO4_300m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[0.25, 5.5, 0.25])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -1, 'max': 1, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'O2_300m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[200, 410, 10])},
        # 'colors':"2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32"},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -50, 'max': 50, 'delta': 5},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'Si_300m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 95, 5])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
    },
    'NO3_2500m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[2, 38, 2])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -10, 'max': 10, 'delta': 1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'PO4_2500m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[0.25, 5.5, 0.25])},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -0.7, 'max': 0.7, 'delta': 0.1},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'O2_2500m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {},  # 'colors':"2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32"},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -50, 'max': 50, 'delta': 5},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': 1, 'max': 1, 'delta': 0.1},
    },
    'Si_2500m': {
        'default': {'units': 'umol/L', 'color': 'nice_gfdl', 'contours': 1, 'focus': 'ocean'},
        'full_field': {'colors': "5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 90 100 110 120 130 140 150"},
        'bias': {'color': 'BlueWhiteOrangeRed', 'min': -30, 'max': 30, 'delta': 3},
        'model_model': {'color': 'BlueWhiteOrangeRed', 'min': -20, 'max': 20, 'delta': 2},
    },

    'zos': {
        'default': {'units': 'm', 'color': 'matlab_jet'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 1.6, 0.2], add=2, sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[0, 1.6, 0.2], add=2, sym=True), 'color': 'testcmap'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 1, 0.2], sym=True), 'color': 'testcmap'},
    },
    'tos': {
        'default': {'color': 'WhViBlGrYeOrRe', 'offset': -273.15, 'units': 'degC', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 30, 2], add=[0.5, 1, 3])},
        'bias': {'colors': ranges_to_string(ranges=[[0, 5, 1], [6, 10, 2]], add=0.5, sym=True), 'color': 'temp_19lev',
                 'offset': 0},
        'model_model': {'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 3, 5], sym=True), 'color': 'temp_19lev',
                        'offset': 0},
    },
    'to200': {
        'default': {'color': 'WhViBlGrYeOrRe', 'offset': -273.15, 'units': 'degC', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 30, 2], add=[0.5, 1, 3])},
        'bias': {'colors': ranges_to_string(ranges=[[0, 5, 1], [6, 10, 2]], add=0.5, sym=True), 'color': 'temp_19lev',
                 'offset': 0},
        'model_model': {'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 3, 5], sym=True), 'color': 'temp_19lev',
                        'offset': 0},
    },
    'to1000': {
        'default': {'color': 'WhViBlGrYeOrRe', 'offset': -273.15, 'units': 'degC', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 13, 1], add=0.5)},
        'bias': {'colors': ranges_to_string(ranges=[[0, 2.5, 0.5], [3, 5, 1]], sym=True), 'color': 'temp_19lev',
                 'offset': 0},
        'model_model': {'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 3, 5], sym=True), 'color': 'temp_19lev',
                        'offset': 0},
    },
    'to2000': {
        'default': {'color': 'WhViBlGrYeOrRe', 'offset': -273.15, 'units': 'degC', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 16, 1], add=0.5)},
        'bias': {'colors': ranges_to_string(ranges=[[0, 2.5, 0.5], [3, 5, 1]], sym=True), 'color': 'temp_19lev',
                 'offset': 0},
        'model_model': {'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 3, 5], sym=True), 'color': 'temp_19lev',
                        'offset': 0},
    },
    'thetao_zonmean': {
        'default': {'color': 'WhBlGrYeRe', 'offset': -273.15, 'units': 'degC', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 30, 2], add=[0.5, 1, 3])},
        'bias': {'colors': ranges_to_string(ranges=[[0, 2.5, 0.5], [3, 5, 1]], sym=True), 'color': 'temp_19lev',
                 'offset': 0},
        'model_model': {'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 3, 5], sym=True), 'color': 'temp_19lev',
                        'offset': 0},
    },

    'sos': {
        'default': {'color': 'matlab_jet', 'units': 'psu', 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[26, 40, 0.5])},
        'bias': {'color': 'BlueDarkRed18', 'colors': ranges_to_string(ranges=[0, 5, 1], add=[0.25, 0.5, 10], sym=True)},
        'model_model': {'color': 'BlueDarkRed18', 'colors': ranges_to_string(add=[0.1, 0.25, 0.5, 1, 2], sym=True)},
    },
    'so200': {
        'default': {'color': 'matlab_jet', 'units': 'psu', 'focus': 'ocean'},
        'full_field': {
            'colors': ranges_to_string(ranges=[26, 40, 0.5])},
        'bias': {'color': 'BlueDarkRed18',
                 'colors': ranges_to_string(ranges=[[0, 2.5, 0.5], [0, 5, 1]], add=0.25, sym=True)},
        'model_model': {'color': 'BlueDarkRed18', 'colors': ranges_to_string(add=[0.1, 0.25, 0.5, 1, 2], sym=True)},
    },
    'so1000': {
        'default': {'color': 'matlab_jet', 'units': 'psu', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[34, 36.5, 0.25])},
        'bias': {'color': 'BlueDarkRed18',
                 'colors': ranges_to_string(ranges=[0.25, 1.5, 0.25], add=0.1, sym=True)},
        'model_model': {'color': 'BlueDarkRed18', 'colors': ranges_to_string(add=[0.1, 0.25, 0.5, 1, 2], sym=True)},
    },
    'so2000': {
        'default': {'color': 'matlab_jet', 'units': 'psu', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[33, 37, 0.25])},
        'bias': {'color': 'BlueDarkRed18',
                 'colors': ranges_to_string(ranges=[0.25, 1.5, 0.25], add=0.1, sym=True)},
        'model_model': {'color': 'BlueDarkRed18', 'colors': ranges_to_string(add=[0.1, 0.25, 0.5, 1, 2], sym=True)},
    },
    'so_zonmean': {
        'default': {'color': 'matlab_jet', 'units': 'psu', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[33, 37, 0.25])},
        'bias': {'color': 'BlueDarkRed18',
                 'colors': ranges_to_string(ranges=[0.25, 1.5, 0.25], add=0.1, sym=True)},
        'model_model': {'color': 'BlueDarkRed18', 'colors': ranges_to_string(add=[0.1, 0.25, 0.5, 1, 2], sym=True)},
    },

    'mlotst': {
        'default': {'color': 'precip3_16lev', 'units': 'm', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[[50, 250, 50], [300, 1000, 100]], add=[1200, 1500, 2000])},
        'bias': {'color': 'BlueDarkRed18',
                 'colors': ranges_to_string(ranges=[[50, 250, 50], [250, 1000, 250], [100, 500, 100]], add=10, sym=True)
                 },
        'model_model': {'color': 'BlueDarkRed18',
                        'colors': ranges_to_string(add=[2, 5, 10, 25, 50, 75, 100, 250], sym=True)},
    },
    'hc300': {
        'default': {'color': 'WhViBlGrYeOrRe', 'units': 'J/m2', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[[-3, 3, 1], [4, 30, 2]])},
        'bias': {'colors': ranges_to_string(ranges=[[1, 5, 1], [6, 10, 2]], add=0.5, sym=True), 'color': 'temp_19lev',
                 'offset': 0},
        'model_model': {'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 3, 5], sym=True), 'color': 'temp_19lev',
                        'offset': 0},
    },
    # -- Sea ice variables
    'sic': {
        'default': {'color': 'WhViBlGrYeOrRe', 'units': '%', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[[15, 25, 2], [80, 95, 5], [20, 90, 10]]), 'contours': '15'},
        'bias': {'colors': ranges_to_string(ranges=[[5, 25, 5], [10, 50, 10]], add=1, sym=True),
                 'color': 'temp_diff_18lev'},
        'model_model': {'colors': ranges_to_string(ranges=[[5, 25, 5], [10, 50, 10]], add=1, sym=True),
                        'color': 'temp_diff_18lev'},
    },
    'sit': {
        'default': {'color': 'WhViBlGrYeOrRe', 'units': '%', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[1, 5, 1], add=[0.1, 0.5])},
        'bias': {'colors': ranges_to_string(ranges=[1, 5, 1], add=0.5, sym=True), 'color': 'temp_diff_18lev'},
        'model_model': {'colors': ranges_to_string(ranges=[1, 5, 1], add=0.5, sym=True), 'color': 'temp_diff_18lev'},
    },
    'sivolu': {
        'default': {'color': 'WhViBlGrYeOrRe', 'units': 'm', 'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[[0.2, 2, 0.2], [1, 5, 1]])},
        'bias': {'min': -1, 'max': 1, 'delta': 0.1, 'color': 'temp_19lev'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.1, 'color': 'temp_19lev'},
    },
    'socurl': {'default': {},
               'full_field': dict(min=-1e-6, max=1e-6, delta=1e-7, focus='ocean', contours=1),
               },
    'tauuo': {
        'default': {'focus': 'ocean', 'mpCenterLonF': 200},
        'full_field': {
            'colors': ranges_to_string(ranges=[0, 0.16, 0.02], sym=True),
            'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': ranges_to_string(ranges=[0, 0.1, 0.02], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 0.1, 0.02], sym=True)},
    },
    'tauvo': {
        'default': {'focus': 'ocean', 'mpCenterLonF': 200},
        'full_field': {'colors': ranges_to_string(ranges=[0.02, 0.1, 0.02], add=0.01, sym=True),
                       'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': ranges_to_string(ranges=[0.01, 0.05, 0.01], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0.01, 0.05, 0.01], sym=True), 'color': 'BlueWhiteOrangeRed'},
    },

    # -- Surface Turbulent Fluxes
    # 'hfls' : {
    #     'default' : { 'color' : 'WhiteBlueGreenYellowRed' , 'units':'W/m2', 'focus':'ocean'},
    #     'full_field'   : {'colors':'0 20 40 60 80 100 120 140 160 180 200' , 'color':'precip3_16lev' },
    #     'bias'        : {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50' , 'color':'BlueDarkRed18' },
    #     'model_model' : {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 15 25 35 45 55', 'color':'BlueDarkRed18'},
    # },
    # 'hfss' : {
    #     'default' : { 'color' : 'WhiteBlueGreenYellowRed' , 'units':'W/m2', 'focus':'ocean'},
    #     'full_field'   : {'colors':'0 10 20 30 40 50 60 70 80 90 100 110 120' , 'color':'precip3_16lev'},
    #     'bias'        : {'colors': '-10 -8 -6 -4 -2 -1 1 2 4 6 8 10' , 'color':'BlueDarkRed18' },
    #     'model_model' : {'colors': '-10 -8 -6 -4 -2 -1 1 2 4 6 8 10', 'color':'BlueDarkRed18'},
    # },
    # 'tauu' : {
    #     'default' : { 'color' : 'testcmap' , 'units':'N/m', 'focus':'ocean'},
    #     'full_field'   : {'colors':'-.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0 0.02 0.04 0.06 0.08 0.1 0.12 0.14'
    #                                ' 0.16' ,'color':'ViBlGrWhYeOrRe' },
    #     'bias'        : {'colors': '-1. -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12 '
    #                                '0.14 0.16 1.' , 'color':'ViBlGrWhYeOrRe' },
    #     'model_model' : {'colors': '-1. -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12 '
    #                                '0.14 0.16 1.'},

    # },
    # 'tauv' : {
    #     'default' : { 'color' : 'testcmap' , 'units':'N/m', 'focus':'ocean'},
    #     'full_field'   : {'colors':'-0.1 -0.08 -0.06 -0.04 -0.02 -0.01 0.01 0.02 0.04 0.06 0.08 0.1' ,
    #                       'color':'ViBlGrWhYeOrRe' },
    #     'bias'        : {'colors': '-0.05 -0.04 -0.03 -0.025 -0.02 -0.015 -0.01 -0.005 0.005 0.01 0.015 0.02 0.025 '
    #                                '0.03 0.04 0.05' ,'color':'ViBlGrWhYeOrRe' },
    #     'model_model' : {'colors': '-1. -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12'
    #                                '0.14 0.16 1.'},
    # },

}
