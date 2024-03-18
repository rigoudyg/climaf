#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : S.Sénési - nov 2015
# Adapter : J.Servonnat - april 2016

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.utils import ranges_to_string
from env.environment import *


dict_plot_params = {
    'pr': {
        'default': {'scale': 86400., 'color': 'precip_11lev', 'contours': 1},
        'full_field': {'colors': ranges_to_string(ranges=[2, 14, 2], add=[0.5, 1, 3])},
        'bias': {'color': 'MPL_BrBG', 'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 5], sym=True)},
        'model_model': {'color': 'precip_diff_12lev',
                        'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 5], sym=True)},
    },
    'pme': {
        'default': {'scale': 86400., 'color': 'precip_diff_12lev', 'contours': 1},
        'full_field': {'colors': ranges_to_string(ranges=[2, 14, 2], add=[0.5, 1, 3], sym=True)},
        'bias': {'color': 'precip_diff_12lev', 'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 5], sym=True)},
        'model_model': {'color': 'precip_diff_12lev',
                        'colors': ranges_to_string(add=[0.1, 0.2, 0.5, 1, 2, 5], sym=True)},
    },
    'hurs': {
        'default': {'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[72, 92, 2]), 'color': 'precip_11lev'},
        'bias': {'colors': ranges_to_string(ranges=[0, 10, 1], sym=True), 'color': 'precip_diff_12lev'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 10, 1], sym=True), 'color': 'precip_diff_12lev'},
    },
    'rstt': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 320, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[-50, 0, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[-50, 0, 10], sym=True)},
    },
    'rlut': {
        'full_field': {'colors': ranges_to_string(ranges=[150, 310, 10]),
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rlus': {
        'full_field': {'colors': ranges_to_string(ranges=[120, 400, 20], add=[440, 480]),
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },
    'rsus': {
        'full_field': {'colors': ranges_to_string(ranges=[10, 150, 10]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },
    'rsuscs': {
        'full_field': {'colors': ranges_to_string(ranges=[20, 150, 10]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },
    'rsds': {
        'full_field': {'colors': ranges_to_string(ranges=[80, 320, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },
    'rlds': {
        'full_field': {'colors': ranges_to_string(ranges=[100, 420, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },
    'rsdscs': {
        'full_field': {'colors': ranges_to_string(ranges=[80, 320, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },
    'rldscs': {
        'full_field': {'colors': ranges_to_string(ranges=[100, 420, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },

    'rtt': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 100, 10], add=5, sym=True),
                       'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'hfns': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 200, 50], add=[25, 75], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[20, 80, 20], add=10, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[20, 80, 20], add=10, sym=True)},
    },
    'hfss': {
        'default': {'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 120, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[[-50, -10, 10], [-5, 55, 10]], add=[-2, 2]),
                 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[[-50, -10, 10], [-5, 55, 10]], add=[-2, 2])},
    },
    'hfls': {
        'default': {'focus': 'ocean'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 200, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[[-50, -10, 10], [-5, 55, 10]], add=[-2, 2]),
                 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[[-50, -10, 10], [-5, 55, 10]], add=[-2, 2])},
    },
    'tas': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed'},
        'full_field': {'colors': ranges_to_string(ranges=[[-40, -10, 5], [6, 30, 4]], add=[-60, -50, -6, 24, 27, 28]),
                       'offset': -273.15},
        'bias': {'colors': ranges_to_string(add=[0.5, 1, 2, 4, 8], sym=True), 'color': 'BlueWhiteOrangeRed',
                 'offset': 0},
        'model_model': {'colors': ranges_to_string(add=[0.5, 1, 2, 4, 8], sym=True), 'color': 'BlueWhiteOrangeRed',
                        'offset': 0},
    },
    'tauu': {
        'default': {'focus': 'ocean', 'mpCenterLonF': 200},
        'full_field': {
            'colors': ranges_to_string(ranges=[0, 0.16, 0.02], sym=True),
            'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': ranges_to_string(ranges=[0.02, 0.1, 0.02], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0.02, 0.1, 0.02], sym=True)},
    },
    'tauv': {
        'default': {'focus': 'ocean', 'mpCenterLonF': 200},
        'full_field': {'colors': ranges_to_string(ranges=[0.02, 0.1, 0.02], add=0.01, sym=True),
                       'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': ranges_to_string(ranges=[0.01, 0.05, 0.01], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0.01, 0.05, 0.01], sym=True),
                        'color': 'BlueWhiteOrangeRed'},
    },
    'psl': {
        'default': {'scale': 0.01, 'units': 'hPa', 'color': 'cmp_b2r', 'mpCenterLonF': 200},
        'full_field': {'colors': ranges_to_string(ranges=[1000, 1016, 2], add=[990, 995, 1020, 1025, 1030, 1040])},
        'bias': {'colors': ranges_to_string(ranges=[1, 10, 1], add=[50, 100], sym=True),
                 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[1, 10, 1], add=[50, 100], sym=True),
                        'color': 'BlueWhiteOrangeRed'},
    },
    'zg500': {
        'full_field': {
            'colors': ranges_to_string(ranges=[4900, 5800, 50])},
        'bias': {
            'colors': ranges_to_string(ranges=[20, 200, 20], add=[10, 230, 260], sym=True),
            'color': 'BlueWhiteOrangeRed'},
        'model_model': {
            'colors': ranges_to_string(ranges=[20, 200, 20], add=[10, 230, 260], sym=True),
            'color': 'BlueWhiteOrangeRed'},
    },
    'rsah': {
        'full_field': {'colors': ranges_to_string(ranges=[10, 130, 10]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rsahcs': {
        'full_field': {'colors': ranges_to_string(ranges=[10, 130, 10]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rsahcre': {
        'full_field': {'colors': ranges_to_string(ranges=[2, 12, 2], add=[16, 20], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rlah': {
        'full_field': {'colors': ranges_to_string(ranges=[160, 420, 20], add=460),
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rlahcs': {
        'full_field': {
            'colors': ranges_to_string(ranges=[-260, -70, 10])},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[1, 5], sym=True)},
    },
    'rlahcre': {
        'full_field': {'colors': ranges_to_string(ranges=[220, 500, 20], add=[540, 580]),
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rah': {
        'full_field': {'colors': ranges_to_string(ranges=[160, 420, 20], add=460), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rahcs': {
        'full_field': {'colors': ranges_to_string(ranges=[-160, -20, 10])},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rahcre': {
        'full_field': {'colors': ranges_to_string(ranges=[240, 500, 20], add=[540, 580]),
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[0, 50, 10], add=5, sym=True)},
    },
    'rsts': {
        'full_field': {
            'colors': ranges_to_string(ranges=[0, 330, 10]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'rsut': {
        'full_field': {'colors': ranges_to_string(ranges=[50, 160, 10], add=180), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'rsutcs': {
        'full_field': {'colors': ranges_to_string(ranges=[50, 160, 10], add=[10, 30, 180]),
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'rlutcs': {
        'full_field': {'colors': ranges_to_string(ranges=[150, 310, 10]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'albs': {
        'full_field': {'colors': ranges_to_string(ranges=[[5, 65, 5], [70, 100, 10]]), 'scale': 100,
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed',
                 'scale': 100},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'scale': 100,
                        'color': 'BlueWhiteOrangeRed'},
    },
    'albt': {
        'full_field': {'colors': ranges_to_string(ranges=[[5, 65, 5], [70, 100, 10]]), 'scale': 100,
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed',
                 'scale': 100},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'scale': 100,
                        'color': 'BlueWhiteOrangeRed'},
    },
    # -- CRE
    'cress': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 100, 10], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'crels': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 100, 10], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'crets': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 100, 10], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    # TODO: Delete useless duplicated keys in dictionary
    'crest': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 100, 10], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'crest': {
        'full_field': {'colors': ranges_to_string(ranges=[-120, -10, 10])},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'crelt': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 100, 10], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'crelt': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 70, 5]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'crett': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 100, 10], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'crett': {
        'full_field': {'colors': ranges_to_string(ranges=[0, 60, 10], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'rts': {
        'full_field': {'colors': ranges_to_string(ranges=[-20, 200, 20]), 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': ranges_to_string(ranges=[10, 50, 10], add=[2, 5], sym=True)},
    },
    'cltcalipso': {
        'full_field': {'colors': ranges_to_string(ranges=[[20, 55, 5], [60, 100, 10]]), 'color': 'precip_11lev'},
        'bias': {'colors': ranges_to_string(ranges=[10, 40, 10], add=[5, 70], sym=True), 'color': 'precip_diff_12lev'},
        'model_model': {'colors': ranges_to_string(ranges=[5, 40, 5], add=[2, 70], sym=True),
                        'color': 'precip_diff_12lev'},
    },
    'clhcalipso': {
        'full_field': {'colors': ranges_to_string(ranges=[[0, 8, 2], [10, 100, 10]]), 'color': 'precip_11lev'},
        'bias': {'colors': ranges_to_string(ranges=[5, 40, 5], add=[2, 70], sym=True), 'color': 'precip_diff_12lev'},
        'model_model': {'colors': ranges_to_string(ranges=[5, 40, 5], add=[2, 70], sym=True),
                        'color': 'precip_diff_12lev'},
    },
    'clmcalipso': {
        'full_field': {'colors': ranges_to_string(ranges=[[0, 8, 2], [10, 60, 10]]), 'color': 'precip_11lev'},
        'bias': {'colors': ranges_to_string(ranges=[5, 40, 5], add=[2, 70], sym=True), 'color': 'precip_diff_12lev'},
        'model_model': {'colors': ranges_to_string(ranges=[5, 40, 5], add=[2, 70], sym=True),
                        'color': 'precip_diff_12lev'},
    },
    'cllcalipso': {
        'full_field': {'colors': ranges_to_string(ranges=[10, 100, 10], add=5), 'color': 'precip_11lev'},
        'bias': {'colors': ranges_to_string(ranges=[5, 40, 5], add=[2, 70], sym=True), 'color': 'precip_diff_12lev'},
        'model_model': {'colors': ranges_to_string(ranges=[5, 40, 5], add=[2, 70], sym=True),
                        'color': 'precip_diff_12lev'},
    },
    'ua': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 30, 5], add=[2, 40], sym=True)},
        # 'bias'        : {'min':-14,'max':14,'delta':2},
        'bias': {'colors': ranges_to_string(ranges=[0.5, 6, 0.5], sym=True)},
        'model_model': {'min': -10, 'max': 10, 'delta': 1},
    },
    'va': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {
            'colors': ranges_to_string(ranges=[0.2, 2, 0.2], add=[0.05, 0.1], sym=True)},
        'bias': {'min': -1, 'max': 1, 'delta': 0.05},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05},
    },
    'ta': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': ranges_to_string(ranges=[[-70, 0, 10], [5, 35, 5]])},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'vitu': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 30, 5], add=[2, 40], sym=True)},
        # 'bias'        : {'min':-14,'max':14,'delta':2},
        'bias': {'colors': ranges_to_string(ranges=[0.5, 6, 0.5], sym=True)},
        'model_model': {'min': -10, 'max': 10, 'delta': 1},
    },
    'vitv': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {
            'colors': ranges_to_string(ranges=[0.2, 2, 0.2], add=[0.05, 0.1], sym=True)},
        'bias': {'min': -1, 'max': 1, 'delta': 0.05},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05},
    },
    'vitw': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'min': -0.05, 'max': 0.05, 'delta': 0.005},
        # 'colors':'-2 -1.8 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 -0.1 -0.05 0.05 0.1
        #           0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8 2'},
        'bias': {'min': -1, 'max': 1, 'delta': 0.05},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05},
    },

    'temp': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': ranges_to_string(ranges=[[-70, 0, 10], [5, 35, 5]])},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },

    'hur': {
        'default': {'color': 'precip_11lev', 'units': 'g/g'},
        'full_field': {'colors': ranges_to_string(ranges=[[10, 40, 10], [40, 100, 20]], add=[0.1, 1, 5])},
        'bias': {'min': -25, 'max': 25, 'delta': 5, 'color': 'MPL_BrBG'},
        'model_model': {'min': -0.001, 'max': 0.001, 'delta': 0.0001, 'color': 'MPL_BrBG'},
    },
    'hus': {
        'default': {'color': 'precip_11lev', 'units': 'g/g'},
        'full_field': {
            'colors': ranges_to_string(ranges=[0.002, 0.02, 0.002], add=[0.00001, 0.0001, 0.0005, 0.001, 0.003])},
        'bias': {'min': -0.002, 'max': 0.002, 'delta': 0.0002, 'color': 'MPL_BrBG'},
        'model_model': {'min': -0.001, 'max': 0.001, 'delta': 0.0001, 'color': 'MPL_BrBG'},
    },
    'uas': {
        'default': {'color': 'BlueYellowRed', 'units': 'm/s', 'mpCenterLonF': 200, 'contours': 1},
        'full_field': {'colors': ranges_to_string(ranges=[0, 10, 2], add=1, sym=True)},
        # 'bias'        : {'min':-3.5, 'max':3.5, 'delta':0.5},
        # 'model_model' : {'colors':'-3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3'},
        # 'default' : { 'color' : 'BlueWhiteOrangeRed' , 'units':'m/s'},
        # 'full_field'   : {'colors':'-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 7 8 9 10'},
        'bias': {'colors': ranges_to_string(ranges=[0.5, 3, 0.5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        # 'model_model' : {'colors':'-3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3'},
    },
    'vas': {
        'default': {'color': 'BlueYellowRed', 'units': 'm/s', 'mpCenterLonF': 200, 'contours': 1},
        'full_field': {'colors': ranges_to_string(ranges=[0, 10, 1], sym=True)},
        'bias': {'colors': ranges_to_string(ranges=[0.5, 3, 0.5], sym=True), 'color': 'BlueWhiteOrangeRed'},
        # 'bias'        : {'min':-3,'max':3,'delta':0.5},
        'model_model': {'min': -5, 'max': 5, 'delta': 0.5},
    },
    'ua_Atl_sect': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[10, 40, 10], add=[2, 5], sym=True)},
        'bias': {'min': -20, 'max': 20, 'delta': 2},
        'model_model': {'min': -10, 'max': 10, 'delta': 1},
    },
    'ua850': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 20, 5], add=2, sym=True)},
        'bias': {'min': -6, 'max': 6, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'ua700': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 20, 5], add=2, sym=True)},
        'bias': {'min': -8, 'max': 8, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'ua500': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 25, 5], add=2, sym=True)},
        'bias': {'min': -8, 'max': 8, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'ua200': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[5, 30, 5], add=[2, 40], sym=True)},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'va850': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[1, 6, 1], add=[8, 10], sym=True)},
        'bias': {'min': -5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'va700': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[1, 6, 1], add=[8, 10], sym=True)},
        'bias': {'min': -5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'va500': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[1, 6, 1], add=[8, 10], sym=True)},
        'bias': {'min': -5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'va200': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': ranges_to_string(ranges=[1, 6, 1], add=[8, 10], sym=True)},
        'bias': {'min': -5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'ta850': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': ranges_to_string(ranges=[[-40, 0, 10], [0, 25, 5]])},
        'bias': {'min': -5, 'max': 5, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'ta700': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': ranges_to_string(ranges=[[-40, 0, 10], [0, 25, 5]])},
        'bias': {'min': -5, 'max': 5, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'ta500': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': ranges_to_string(ranges=[[-40, 0, 10], [0, 25, 5]])},
        'bias': {'min': -5, 'max': 5, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'ta200': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': ranges_to_string(ranges=[-60, -50, 2], add=[-70, -65, -45, -40])},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'curltau': {'default': {},
                'full_field': dict(min=-1e-6, max=1e-6, delta=1e-7, focus='ocean', contours=1),
                }
}
