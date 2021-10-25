#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from env.environment import *
from climaf.operators_derive import derive

for variable in ["ua", "va", "ta", "hur", "hus", "zg"]:
    for level in [850, 500, 200]:
        derived_variable = variable + str(level)
        derive("*", derived_variable, "select_level", variable, level=str(level * 100))
