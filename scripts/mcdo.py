#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rewrite of mcdo.sh
"""


from __future__ import print_function

import argparse
import tempfile
import re
import os
import subprocess
import time
import glob
import shutil
import six
import copy

from env.site_settings import onCiclad
from env.clogging import clogger, clog


def correct_args_type(value):
    if value is not None and isinstance(value, six.string_types):
        value = value.strip()
        if len(value) == 0 or value in ["none", "None"]:
            value = None
        if value in ["no", "False"]:
            value = False
        elif value in ["yes", "True"]:
            value = True
    return value


def correct_list_args(value):
    if len(value) == 0:
        return None
    else:
        return [v.strip() for v in value.split(",")]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", nargs=argparse.REMAINDER, type=correct_args_type)
    parser.add_argument("--operator", type=correct_args_type, help="Operator to be applied")
    parser.add_argument("--apply_operator_after_merge", type=bool, default=True,
                        help="If True, the operator is applied after merge time. If false, it is applied before.")
    parser.add_argument("--output_file", type=correct_args_type, help="Name of the output file")
    parser.add_argument("--var", "--variable", dest="variable", type=correct_args_type,
                        help="Variable to be considered")
    parser.add_argument("--period", type=correct_args_type, help="Period to be considered")
    parser.add_argument("--region", type=correct_list_args,
                        help="Region to be considered, i.e. latmin,latmax,lonmin,lonmax")
    parser.add_argument("--alias", type=correct_list_args, help="Alias to be used")
    parser.add_argument("--units", type=correct_args_type, help="Units of the variable")
    parser.add_argument("--vm", type=correct_args_type, help="")

    args = parser.parse_args()
    return dict(input_files=args.input_files, operator=args.operator, output_file=args.output_file,
                variable=args.variable, period=args.period, region=args.region, alias=args.alias, units=args.units,
                vm=args.vm,  apply_operator_after_merge=args.apply_operator_after_merge)


# Define several auxiliary functions
clim_timefix_pattern = re.compile(r'IGCM_OUT.*_SE_.*(?P<value>\d{4})_\d{4}_1M.*nc')
nemo_fix_pattern_mon = re.compile(r'.*1m.*grid_T_table2\.2\.nc')
nemo_fix_pattern_day = re.compile(r'.*1d.*grid_T_table2\.2\.nc')
nemo_fix_pattern = re.compile(r'.*1[m|d].*grid_T_table2\.2\.nc')
aladin_coordinates_pattern = re.compile(r'.*coord.*lon lat.*|.*coord.* lat lon|float longitude|float latitude')
nemo_coordinates_pattern = re.compile(r'coord.*t_ave_01month|t_ave_00086400')


def clim_timefix(file_to_treat):
    # Check if the time axis for a data file should be fixed, based solely on its name,
    # and hence echoes the relevant CDO syntax (to be inserted in a CDO pipe) for fixing it
    # Case for IPSL Seasonal cycle files, such as
    # ... IGCM_OUT/IPSLCM6/DEVT/piControl/O1T04V04/ICE/Analyse/SE/O1T04V04_SE_1850_1859_1M_icemod.nc
    clim_timefix_match = clim_timefix_pattern.match(file_to_treat)
    if clim_timefix_match:
        return "-settaxis,{}-01-16:12:00:00,1mon".format(clim_timefix_match.groupdict()["value"])
    else:
        return None


def nemo_timefix(file_to_treat, tmp_dir):
    # Rename alternate time_counter variables to 'time_counter' for some kind
    # of Nemo outputs  (Nemo 3.2 had a bug when using IOIPSL ...)
    # Echoes the name of a file with renamed variable (be it a modified file or a copy)
    # Creates an alternate file in $tmp if no write permission and renaming is actually useful
    nemo_fix_match = nemo_fix_pattern.match(file_to_treat)
    if nemo_fix_match:
        rep = subprocess.check_output(["ncdump", "-h", file_to_treat])
        rep = rep.split("\n")
        if any([nemo_coordinates_pattern.match(line) for line in rep]):
            if nemo_fix_pattern_mon.match(file_to_treat):
                var2rename = "t_ave_01month"
                vars2d = ["pbo", "sos", "tos", "tossq", "zos", "zoss", "zossq", "zosto"]
                vars3d = ["rhopoto", "so", "thetao", "thkcello", "rhopoto"]
            elif nemo_fix_pattern_day.match(file_to_treat):
                var2rename = "t_ave_00086400"
                vars2d = ["tos", "tossq"]
                vars3d = list()
            out = os.path.sep.join([tmp_dir, "renamed_{}".format(os.path.basename(file_to_treat))])
            if os.path.isfile(out):
                os.remove(out)
            if subprocess.check_output(["ncdump", "-k", file_to_treat]) == "classic":
                temp = file_to_treat
            else:
                temp = out
                subprocess.check_output(["ncks", "-3", file_to_treat, temp])
            subprocess.check_output(["ncrename", "-d", ".{},time_counter".format(var2rename),
                                     "-v {},time_counter".format(var2rename), temp, out])
            for lvar in vars2d:
                subprocess.check_output(["ncatted", "-a", "coordinates,{},m,c,nav_lat nav_lon".format(lvar), out])
            for lvar in vars3d:
                subprocess.check_output(["ncatted", "-a", "coordinates,{},m,c,depth nav_lat nav_lon".format(lvar), out])

    else:
        return file_to_treat


def aladin_coordfix(file_to_treat, tmp_dir, filevar):
    # Rename attribute 'coordinates' of file variable $filevar to 'latitude longitude'
    # for some kind of ALADIN outputs which have 'lat lon' (or 'lon lat') for attribute 'coordinates'
    # of file variable (particularly for outputs created with post-treatment tool called 'postald')
    # Echoes the name of a file with renamed variable attribute (be it a modified file or a copy)
    # Creates an alternate file in $tmp if no write permission and renaming is actually useful
    if re.compile(r".*ALADIN.*.nc").match(file_to_treat) and (not(re.compile(r".*r1i1p1.*.nc").match(file_to_treat)) or
                                                              not(re.compile(r".*MED-11.*.nc").match(file_to_treat))):
        rep = subprocess.check_output(["ncdump", "-h", file_to_treat])
        rep = rep.split("\n")
        if any([aladin_coordinates_pattern.match(line) for line in rep]):
            out = os.path.sep.join([tmp_dir, "renamed_{}".format(os.path.basename(file_to_treat))])
            if os.path.isfile(out):
                os.remove(out)
            subprocess.check_output(["ncks", "-3", file_to_treat, out])
            subprocess.check_output(["ncatted", "-a coordinates,{},o,c,'latitude longitude'".format(filevar), out])
            if os.access(file_to_treat, os.W_OK):
                os.remove(file_to_treat)
                shutil.move(out, file_to_treat)
                return file_to_treat
            else:
                return out
    else:
        return file_to_treat


def call_subprocess(command):
    clogger.debug("Command launched %s" % command)
    clogger.debug("Time at launch %s" % time.time())
    clogger.debug(subprocess.check_output(command, shell=True))
    clogger.debug("Time at end %s" % time.time())


def remove_dir_and_content(path_to_treat):
    if os.path.exists(path_to_treat):
        if os.path.isdir(path_to_treat):
            contents = glob.glob(os.path.sep.join([path_to_treat, "*"]))
            for content in contents:
                remove_dir_and_content(content)
            os.removedirs(path_to_treat)
        else:
            os.remove(path_to_treat)


def main(input_files, output_file, variable=None, alias=None, region=None, units=None, vm=None, period=None,
         operator=None,  apply_operator_after_merge=None):
    clog("debug")
    # Create a temporary directory
    tmp = tempfile.mkdtemp(prefix="climaf_mcdo")
    clogger.debug("Create temporary dir %s" % tmp)
    original_directory = os.getcwd()
    os.chdir(tmp)

    # Initialize cdo commands
    cdo_commands_before_merge = list()
    cdo_command_for_merge = None
    cdo_commands_after_merge = list()

    # Find out which command must be used for cdo
    # For the time being, at most sites, must use NetCDF3 file format chained CDO
    # operations because NetCDF4 is not threadsafe there
    if onCiclad:
        init_cdo_command = "cdo -O"
    else:
        init_cdo_command = "cdo -O -f nc"
    clogger.debug("CDO command init: %s" % init_cdo_command)

    # If needed, select the variable first or compute it if it is an alias
    clogger.debug("Alias and variable considered: %s -- %s" % (alias, variable))
    if variable is not None:
        var = variable
        file_var = var
        # JS#print "var in mcdo.py  = ", var
        # JS#print "-selname,{}".format(str(var))
        # JS#cdo_commands_before_merge.append("-selname,{}".format(var))
        cdo_commands_before_merge.append("-selname,"+var)
    if alias is not None:
        var, filevar, scale, offset = alias[:]
        if variable is not None and filevar != variable:
            clogger.error("Incoherence between variable and input aliased variable: %s %s" % (variable, filevar))
            raise Exception("Incoherence between variable and input aliased variable: %s %s" % (variable, filevar))
        else:
            cdo_commands_before_merge.append("-expr,{}={}*{}+{}".format(var, filevar, scale, offset))
            cdo_commands_before_merge.append("-selname,{}".format(var))

    # Then, if needed, select the domain
    clogger.debug("Region considered: %s" % region)
    if region is not None:
        latmin, latmax, lonmin, lonmax = region[:]
        cdo_commands_before_merge.append("-sellonlatbox,{},{},{},{}".format(lonmin, lonmax, latmin, latmax))

    # Then, if needed, change the units
    clogger.debug("Units considered: %s" % units)
    if units is not None:
        if variable is None:
            clogger.error("Units can be used only if variable is specified")
            raise Exception("Units can be used only if variable is specified")
        else:
            cdo_commands_before_merge.append("-setattribute,{}@units={}".format(variable, units.replace(" ", "*")))

    # Then, if needed, deal with missing values
    clogger.debug("Vm considered: %s" % vm)
    if vm is not None:
        cdo_commands_before_merge.append("-setctomiss,{}".format(vm))

    # Then, deal with merge time
    if len(input_files) > 1:
        cdo_command_for_merge = "-mergetime"

    # Then deal with date selection
    clogger.debug("Period considered: %s" % period)
    if period is not None:
        print("type(str) = ", type(period))
        print("period = ", period)
        seldate = "-seldate,{}".format(period)
        clim_time_fix = clim_timefix(input_files[0])
        if clim_time_fix is not None:
            seldate = " ".join([seldate, clim_time_fix])
        cdo_commands_after_merge.append(seldate)

    # Then, if needed, deal with the operator
    clogger.debug("Operator considered: %s" % operator)
    if operator is not None:
        if apply_operator_after_merge:
            cdo_commands_after_merge.append("-{}".format(operator))
        else:
            cdo_commands_before_merge.append("-{}".format(operator))

    # Some rare, tricky cases need that :
    if len(cdo_commands_after_merge) == 0:
        cdo_commands_after_merge.append("-copy")

    files_to_treat_before_merging = list()
    for a_file in input_files:
        if a_file[0:2] == "./":
            a_file = original_directory + a_file[1:]
        if a_file[0] != "/":
            a_file = original_directory + "/" + a_file
        if os.environ.get("CLIMAF_FIX_NEMO_TIME", False):
            a_file = nemo_timefix(a_file, tmp)
        if os.environ.get("CLIMAF_FIX_ALADIN_COORD", False):
            a_file = aladin_coordfix(a_file, tmp, filevar)
        files_to_treat_before_merging.append(a_file)

    if len(files_to_treat_before_merging) > 1:
        files_to_treat_after_merging = list()
        for a_file in files_to_treat_before_merging:
            tmp_file_name = a_file.split(os.path.sep)[-1]
            tmp_file_path = os.path.sep.join([tmp, tmp_file_name])
            while os.path.exists(tmp_file_path):
                tmp_file_name = "_".join(["tmp", tmp_file_name])
                tmp_file_path = os.path.sep.join([tmp, tmp_file_name])
            if not os.path.isfile(tmp_file_name):
                cdo_command = " ".join([init_cdo_command, ] + list(reversed(cdo_commands_before_merge)) +
                                       [a_file, tmp_file_name])
                call_subprocess(cdo_command)
                if not os.path.isfile(tmp_file_path):
                    clogger.error("Could not create the file %s" % tmp_file_path)
                    raise Exception("Could not create the file %s" % tmp_file_path)
                files_to_treat_after_merging.append(tmp_file_path)
            else:
                clogger.error("Should not pass here...")
                raise Exception("Should not pass here...")
        if cdo_command_for_merge is not None:
            tmp_output_file = os.sep.join([tmp, os.path.basename(output_file)])
            cdo_command = " ".join([init_cdo_command, cdo_command_for_merge] + files_to_treat_after_merging +
                                   [tmp_output_file, ])
            call_subprocess(cdo_command)
            files_to_treat_after_merging = [tmp_output_file, ]
        cdo_command = " ".join([init_cdo_command, ] + list(reversed(cdo_commands_after_merge)) +
                               files_to_treat_after_merging + [output_file, ])
        call_subprocess(cdo_command)
    elif len(files_to_treat_before_merging) == 1:
        cdo_command = " ".join([init_cdo_command, ] + list(reversed(cdo_commands_after_merge)) +
                               list(reversed(cdo_commands_before_merge)) + files_to_treat_before_merging +
                               [output_file, ])
        call_subprocess(cdo_command)
    else:
        raise ValueError("No input file to treat!")

    os.chdir(original_directory)
    remove_dir_and_content(tmp)


if __name__ == "__main__":
    kwargs = parse_args()
    main(**kwargs)
