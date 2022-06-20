#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : S.Sénési - nov 2015

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.utils import ranges_to_string
from env.environment import *


dict_plot_params = {
    'gpp': {
        'default': {'color': 'precip3_16lev', 'units': 'kg.m-2.s-1'},
        'full_field': {'colors': ranges_to_string(ranges=[0, 1e-7, 1e-8], add=1.2e-7),
                       'color': 'precip3_16lev'},
        'bias': {'colors': ranges_to_string(ranges=[2e-8, 1e-7, 2e-8], add=[5e-9, 1e-8], sym=True),
                 'color': 'ViBlGrWhYeOrRe'},
        'model_model': {'colors': ranges_to_string(ranges=[2e-8, 1e-7, 2e-8], add=[5e-9, 1e-8], sym=True),
                        'color': 'ViBlGrWhYeOrRe'},
    },
}
