#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : S.Sénési - nov 2015

from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *


dict_plot_params = {
    'gpp': {
        'default': {'color': 'precip3_16lev', 'units': 'kg.m-2.s-1'},
        'full_field': {'colors': '0 1e-8 2e-8 3e-8 4e-8 5e-8 6e-8 7e-8 8e-8 9e-8 1e-7 1.2e-7',
                       'color': 'precip3_16lev'},
        'bias': {'colors': '-1e-7 -8e-8 -6e-8 -4e-8 -2e-8 -1e-8 -5e-9 5e-9 1e-8 2e-8 4e-8 6e-8 8e-8 1e-7',
                 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'colors': '-1e-7 -8e-8 -6e-8 -4e-8 -2e-8 -1e-8 -5e-9 5e-9 1e-8 2e-8 4e-8 6e-8 8e-8 1e-7',
                        'color': 'ViBlGrWhYeOrRe'},
    },
}
