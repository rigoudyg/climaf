#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script aims at plotting different fields on the same map.
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import argparse
import json

from netCDF4 import Dataset

import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs


# Create the parser
parser = argparse.ArgumentParser()
# Add colored map features
colored_map_group = parser.add_argument_group("colored_map", description="Arguments linked with colored map")
colored_map_group.add_argument("--colored_map_file", help="File which content should be plotted as a colored map.",
                               type=str, default=None)
colored_map_group.add_argument("--colored_map_variable", help="Variable to be plotted on colored map",
                               type=str, default=None)
colored_map_group.add_argument("--colored_map_levels", help="Number of level of the colored map color bar",
                               type=int, default=50)
colored_map_group.add_argument("--colored_map_colors", help="Colors that should be used for the colored map",
                               type=list, default=None)
colored_map_group.add_argument("--colored_map_transform", help="Coordinate system on which the colored map data is.",
                               type=str, default=None)
colored_map_group.add_argument("--colored_map_transform_options",
                               help="Options of the coordinate system on which the colored map data is.",
                               type=json.loads, default=None)
# Add contours map features
contours_map_group = parser.add_argument_group("contours_map", description="Arguments linked with contours map")
contours_map_group.add_argument("--contours_map_file", help="File which content should be plotted as a contours map.",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_variable", help="Variable to be plotted on contours map",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_levels", help="Number of level of the contours color bar",
                                type=int, default=20)
contours_map_group.add_argument("--contours_map_colors", help="Colors that should be used for the contours map",
                                type=list, default=None)
contours_map_group.add_argument("--contours_map_transform", help="Coordinate system on which the contours data is.",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_transform_options",
                                help="Options of the coordinate system on which the contours data is.",
                                type=json.loads, default=None)
# Add shaded map features
shaded_map_group = parser.add_argument_group("shaded_map", description="Arguments linked with shaded map")
shaded_map_group.add_argument("--shaded_map_file", help="File which content should be plotted as a shaded map.",
                              type=str, default=None)
shaded_map_group.add_argument("--shaded_map_variable", help="Variable to be plotted on shaded map",
                              type=str, default=None)
shaded_map_group.add_argument("--shaded_map_levels", help="Number of level of the shaded map color bar",
                              type=int, default=1)
shaded_map_group.add_argument("--shaded_map_hatches", help="Hatches that should be used for the shaded map",
                              type=list, default=[None, "/"])
shaded_map_group.add_argument("--shaded_map_transform", help="Coordinate system on which the shaded data is.",
                              type=str, default=None)
shaded_map_group.add_argument("--shaded_map_transform_options",
                              help="Options of the coordinate system on which the shaded data is.",
                              type=json.loads, default=None)
# Add vectors map features
vectors_map_group = parser.add_argument_group("vectors_map", description="Arguments linked with vectors map")
vectors_map_group.add_argument("--vectors_map_u_file",
                               help="File which content should be plotted as a u composant vector map.",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_v_file",
                               help="File which content should be plotted as a v composant vector map.",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_u_variable", help="Variable (u component) to be plotted on shaded map",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_v_variable", help="Variable (v component) to be plotted on shaded map",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_type", help="Number of level of the shaded map color bar",
                               default="quivers", choices=["quivers", "barbs", "streamplots"])
vectors_map_group.add_argument("--vectors_map_options", help="Options of the vector map.",
                               type=json.loads, default=None)
vectors_map_group.add_argument("--vectors_map_transform", help="Coordinate system on which the vectors data is.",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_transform_options",
                               help="Options of the coordinate system on which the vectors data is.",
                               type=json.loads, default=dict())
# Add generic features
parser.add_argument("--coordinates", help="Coordinates to be plotted", type=list, default=["lon", "lat"])
parser.add_argument("--projection", help="The projection to be used for the map", type=str, default="PlateCarree")
parser.add_argument("--projection_options", help="The options of the projection to be used for the map",
                    type=json.loads, default=None)
parser.add_argument("--output_file", help="Path of the output_file", default=None)
parser.add_argument("--title", help="Title of the graphic", default=None)


# Define a few functions for generic treatments
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


def find_coordinates(coordinates, options=None):
    if coordinates in ccrs.__dict__:
        if options:
            return ccrs.__dict__[coordinates].__call__(**options)
        else:
            return ccrs.__dict__[coordinates].__call__()
    else:
        raise ValueError("Unknown coordinates system %s." % coordinates)


def get_variable_and_dimensions_from_dataset(file, variable, coordinates):
    # Check that the file exists
    if not os.path.isfile(file):
        raise ValueError("The input file %s does not exist." % file)
    # Read the file content
    dataset = Dataset(file, "r")
    # Get the variable dataset
    if variable in dataset.variables:
        variable_dataset = dataset.variables[variable]
    else:
        raise ValueError("The input file %s does not contain the variable %s." % file, variable)
    # Retrieve dimensions
    variable_dimensions_data = list()
    for dimension in variable_dataset.dimensions:
        if dimension in coordinates:
            variable_dimensions_data.append(dataset.variables[dimension][:])
    # Retrieve data
    variable_data = find_data_in_dataset(variable_dataset, coordinates)
    # Close the dataset
    dataset.close()
    # Return the values found
    return variable_data, variable_dimensions_data


# Define a few functions for plots
def plot_colored_map(ax, coordinates, colored_map_file, colored_map_variable,
                     colored_map_transform, colored_map_transform_options, projection,
                     colored_map_colors, colored_map_levels):
    # Find used data
    variable_data, variable_dimensions_data = get_variable_and_dimensions_from_dataset(colored_map_file,
                                                                                       colored_map_variable,
                                                                                       coordinates)
    # Find the transform
    if colored_map_transform:
        transform = find_coordinates(colored_map_transform, colored_map_transform_options)
    else:
        transform = projection
    # Plot the map
    colored_map_plot = plt.contourf(variable_dimensions_data[1], variable_dimensions_data[0], variable_data,
                                    colored_map_levels, transform=transform,
                                    colors=colored_map_colors)
    plt.colorbar(colored_map_plot, ax=ax)


def plot_contours_map(ax, coordinates, contours_map_file, contours_map_variable,
                      contours_map_transform, contours_map_transform_options, projection,
                      contours_map_colors, contours_map_levels):
    # Find used data
    variable_data, variable_dimensions_data = get_variable_and_dimensions_from_dataset(contours_map_file,
                                                                                       contours_map_variable,
                                                                                       coordinates)
    # Find the transform
    if contours_map_transform:
        transform = find_coordinates(contours_map_transform, contours_map_transform_options)
    else:
        transform = projection
    # Plot the map
    plt.contour(variable_dimensions_data[1], variable_dimensions_data[0], variable_data,
                contours_map_levels, transform=transform, colors=contours_map_colors)


def plot_shaded_map(ax, coordinates, shaded_map_file, shaded_map_variable,
                    shaded_map_transform, shaded_map_transform_options, projection,
                    shaded_map_hatches, shaded_map_levels):
    # Find used data
    variable_data, variable_dimensions_data = get_variable_and_dimensions_from_dataset(shaded_map_file,
                                                                                       shaded_map_variable,
                                                                                       coordinates)
    # Find the transform
    if shaded_map_transform:
        transform = find_coordinates(shaded_map_transform, shaded_map_transform_options)
    else:
        transform = projection
    # Plot the map
    plt.contourf(variable_dimensions_data[1], variable_dimensions_data[0], variable_data,
                 shaded_map_levels, transform=transform,
                 hatches=shaded_map_hatches, colors="none")


def plot_vector_map(ax, coordinates, vectors_map_u_file, vectors_map_v_file,
                    vectors_map_u_variable, vectors_map_v_variable,
                    vectors_map_transform, vectors_map_transform_options, projection,
                    vectors_map_type, vectors_map_options):
    # Get back the datasets and dimensions
    variable_u_data, variable_u_dimensions_data = get_variable_and_dimensions_from_dataset(vectors_map_u_file,
                                                                                           vectors_map_u_variable,
                                                                                           coordinates)
    variable_v_data, variable_v_dimensions_data = get_variable_and_dimensions_from_dataset(vectors_map_v_file,
                                                                                           vectors_map_v_variable,
                                                                                           coordinates)
    # Check that dimensions are equal
    if variable_u_dimensions_data != variable_v_dimensions_data:
        raise ValueError("Zonal and meridian component of the vector field must have the same dimensions.")
    # Find the transform
    if args.vectors_map_transform:
        transform = find_coordinates(vectors_map_transform, vectors_map_transform_options)
    else:
        transform = projection
    # Plot the map
    if vectors_map_type in ax.__dict__:
        ax.__dict__[vectors_map_type].__call__(variable_u_dimensions_data[1], variable_u_dimensions_data[0],
                                               variable_u_data, variable_v_data,
                                               transform=transform, **vectors_map_options)
    else:
        raise ValueError("unknown vectors map type %s." % vectors_map_type)


def plot_map(args):
    # Get coordinates
    coordinates = args.coordinates

    # Deal with projection
    projection = find_coordinates(args.projection, args.projection_options)

    # Initialize the plot
    ax = plt.axes(projection=projection)

    # Deal with the colored map if needed
    if args.colored_map_file:
        plot_colored_map(ax=ax,
                         coordinates=coordinates,
                         colored_map_file=args.colored_map_file,
                         colored_map_variable=args.colored_map_variable,
                         colored_map_transform=args.colored_map_transform,
                         colored_map_transform_options=args.colored_map_transform_options,
                         projection=projection,
                         colored_map_colors=args.colored_map_colors,
                         colored_map_levels=args.colored_map_levels)

    # Deal with the contours map if needed
    if args.contours_map_file:
        plot_contours_map(ax=ax,
                          coordinates=coordinates,
                          contours_map_file=args.contours_map_file,
                          contours_map_variable=args.contours_map_variable,
                          contours_map_transform=args.contours_map_transform,
                          contours_map_transform_options=args.contours_map_transform_options,
                          projection=projection,
                          contours_map_colors=args.contours_map_colors,
                          contours_map_levels=args.contours_map_levels)

    # Deal with the shaded map if needed
    if args.shaded_map_file is not None:
        plot_shaded_map(ax=ax,
                        coordinates=coordinates,
                        shaded_map_file=args.shaded_map_file,
                        shaded_map_variable=args.shaded_map_variable,
                        shaded_map_transform=args.shaded_map_transform,
                        shaded_map_transform_options=args.shaded_map_transform_options,
                        projection=projection,
                        shaded_map_hatches=args.shaded_map_hatches,
                        shaded_map_levels=args.shaded_map_levels)

    # Deal with the shaded map if needed
    if args.vectors_map_u_file is not None and args.vectors_map_v_file is not None:
        plot_vector_map(ax=ax,
                        coordinates=coordinates,
                        vectors_map_u_file=args.vectors_map_u_file,
                        vectors_map_v_file=args.vectors_map_v_file,
                        vectors_map_u_variable=args.vectors_map_u_variable,
                        vectors_map_v_variable=args.vectors_map_v_variable,
                        vectors_map_transform=args.vectors_map_transform,
                        vectors_map_transform_options=args.vectors_map_transform_options,
                        projection=projection,
                        vectors_map_type=args.vectors_map_type,
                        vectors_map_options=args.vectors_map_options)

    # Add title if provided
    if args.title is not None:
        plt.title(args.title)

    # Add coast lines
    ax.coastlines()

    # Deal with output
    output_file = args.output_file
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)


if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    # Plot the map
    plot_map(args)
