#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script aims at reading netcdf files in python.
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import netcdftime

from netCDF4 import Dataset

import matplotlib.pyplot as plt
import numpy as np


# Parameters of the script
filename = "/home/rigoudy/Bureau/dev/CliMAF/tests/test_data/tas_Amon_CNRM-CM5_historical_r1i1p1_1850.nc"
variable = "tas"
dimensions = ["lon", "lat", "time"]
time_dimension = "time"


# Function to find dimensions of a given variables and get the data content
def find_data_in_dataset(variable_dataset, dimensions):
    variable_dimensions = variable_dataset.dimensions
    intersect_dimensions = list(set(variable_dimensions) & set(dimensions))
    # Find out the dimensions to keep
    select_variable_dimension = list()
    for i in variable_dimensions:
        if i in intersect_dimensions:
            select_variable_dimension.append(slice(None))
        else:
            select_variable_dimension.append(0)
    select_variable_dimension = tuple(select_variable_dimension)
    return variable_dataset[select_variable_dimension]


# Function to read the content of the file and get the variable
def read_variable_from_netcdf(filename, variable, dimensions, time_dimension="time"):
    # Check that the file exists
    if not os.path.isfile(filename):
        raise ValueError("The input file %s does not exists." % filename)
    # Read the file content
    netcdf_fic = Dataset(filename, "r")
    # Get the variable dataset
    if variable in netcdf_fic.variables:
        variable_dataset = netcdf_fic.variables[variable]
    else:
        raise ValueError("Could not find variable %s in file %s" % (variable, filename))
    # Check that the dimensions required exists, put them in the right order and convert time
    variable_dimensions_data = list()
    variable_dimension_label = list()
    for dimension in variable_dataset.dimensions:
        if dimension in dimensions:
            variable_dimension_label.append(dimension)
            if dimension == time_dimension:
                if "calendar" in netcdf_fic.variables[dimension].ncattrs():
                    fic_calendar = netcdf_fic.variables[dimension].getncattr("calendar")
                else:
                    fic_calendar = "gregorian"
                if "units" in netcdf_fic.variables[dimension].ncattrs():
                    fic_units = netcdf_fic.variables[dimension].getncattr("units")
                else:
                    fic_units = "days since 1850-01-01 00:00:00"
                variable_dimensions_data.append(netcdftime.num2date(netcdf_fic.variables[dimension][:],
                                                                    units=fic_units, calendar=fic_calendar)
                                                )
            else:
                variable_dimensions_data.append(netcdf_fic.variables[dimension][:])
    if len(variable_dimensions_data) != len(dimensions):
        raise ValueError("Some coordinates are not available in the file. "
                         "You ask for %s and available dimensions are %s."
                         % (str(list(variable_dataset.dimensions)), str(dimensions)))
    # Retrieve data
    variable_data = find_data_in_dataset(variable_dataset, dimensions)
    # Close the dataset
    netcdf_fic.close()
    # Return the values found
    return variable_data, variable_dimensions_data, variable_dimension_label


# Read tas variable and dimensions (order given by the last result)
tas_variable, tas_dimensions_data, tas_dimensions_label = read_variable_from_netcdf(filename, variable, dimensions,
                                                                                    time_dimension)

# Determine the set of indexes
time_dimension_index = tas_dimensions_label.index(time_dimension)
space_indexes = sorted(list(set(range(len(tas_dimensions_label))) - set([time_dimension_index, ])))

# Compute space average
tas_space_average = np.mean(tas_variable, axis=tuple(space_indexes))

plt.plot(tas_dimensions_data[time_dimension_index], tas_space_average)
plt.show()
