#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script aims at plotting different fields on the same map.
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import shutil
import argparse
import xarray as xr
import numpy as np
import six


def check_none_or_other(value):
    if value is None or value in ["", "none", "None"]:
        return None
    elif isinstance(value, six.string_types):
        return value.strip()
    else:
        return str(value).strip()


parser = argparse.ArgumentParser()
parser.add_argument("input_files", nargs="+", help="Input files")
parser.add_argument("--field_variable", required=True, help="Variable to be considered in file")
parser.add_argument("--mask_file", type=check_none_or_other, help="Mask to be applied")
parser.add_argument("--mask_variable", default="mask", type=check_none_or_other, help="Variable of the mask file")
parser.add_argument("--constant", type=float, help="Constant with which the field should be multiplied")
parser.add_argument("--output_file", required=True, help="Output file")

args = parser.parse_args()

# The attributes of the resulting file are the ones of the first input file
# Copy it to output file
main_input_file = args.input_files[0]
if args.output_file != main_input_file:
    if os.path.isfile(args.output_file):
        os.remove(args.output_file)
else:
    shutil.copy(main_input_file, main_input_file + ".tmp")
    os.remove(main_input_file)
    main_input_file += ".tmp"

# Open the first file
with xr.open_dataset(main_input_file) as out_fic:
    if args.field_variable not in out_fic.variables:
        raise ValueError("Could not find variable %s in file %s" % (args.field_variable, args.input_files[0]))
    data_var_main = out_fic.variables[args.field_variable].data
    if len(args.input_files) > 1:
        for f in args.input_files[1:]:
            with xr.open_dataset(f) as in_fic:
                if args.field_variable not in in_fic.variables:
                    raise ValueError("Could not find variable %s in file %s" % (args.field_variable, f))
                data_var_main *= in_fic.variables[args.field_variable].data
    if args.mask_file is not None:
        with xr.open_dataset(args.mask_file) as in_fic:
            if args.mask_variable not in in_fic.variables:
                raise ValueError("Could not find variable %s in file %s" % (args.field_variable, args.mask_file))
            data_var_main *= in_fic.variables[args.mask_variable].data
    if args.constant is not None:
        data_var_main *= args.constant
    out_fic.variables[args.field_variable].data = data_var_main
    out_fic.to_netcdf(args.output_file)

