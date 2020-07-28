#!/usr/bin/env python
# -*- coding: utf-8 -*-

from climaf.api import derive

for variable in ["ua", "va", "ta", "hur", "hus", "zg"]:
    for level in [850, 500, 200]:
        derived_variable = variable + str(level)
        derive("*", derived_variable, "select_level", variable, level=str(level * 100))
