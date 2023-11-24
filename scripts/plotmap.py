from __future__ import division, print_function, unicode_literals, absolute_import
import os
import argparse
import json
import six
#from netCDF4 import Dataset
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script aims at plotting different fields on the same map.
"""


def check_none_or_other(value):
    if value is None or value in ["", "none", "None"]:
        return None
    elif isinstance(value, (int, float)):
        return value
    elif value in ["True", True]:
        return True
    elif value in ["False", False]:
        return False
    elif isinstance(value, six.string_types):
        return value.strip()
    elif isinstance(value, (list, tuple)):
        return [check_none_or_other(elt) for elt in value]
    elif isinstance(value, dict):
        return {check_none_or_other(key): check_none_or_other(value) for (key, value) in value.items()}
    else:
        return str(value).strip()


def check_json_format(value):
    value = json.loads(value)
    if isinstance(value, list):
        value = [check_none_or_other(val) for val in value]
    elif isinstance(value, dict):
        for key in value.keys():
            value[key] = check_none_or_other(value[key])
    return value


# Create the parser
parser = argparse.ArgumentParser()
# Add colored map features
colored_map_group = parser.add_argument_group(
    "colored_map", description="Arguments linked with colored map")
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
                               type=check_json_format, default=None)
colored_map_group.add_argument("--colored_map_selection_options",
                               help="Options to be used to select coordinates if needed."
                                    "Expected format: list of tuples (selection method, associated dict options)",
                               type=check_json_format, default=dict())
colored_map_group.add_argument("--colored_map_scale", help="Scale factor to apply to the colored map field",
                               type=float, default=None)
colored_map_group.add_argument("--colored_map_offset", help="Offset to apply to the colored map field",
                               type=float, default=None)

# Add contours map features
contours_map_group = parser.add_argument_group(
    "contours_map", description="Arguments linked with contours map")
contours_map_group.add_argument("--contours_map_file", help="File which content should be plotted as a contours map.",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_variable", help="Variable to be plotted on contours map",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_levels", help="Number of level of the contours color bar",
                                type=int, default=None)
contours_map_group.add_argument("--contours_map_colors", help="Colors that should be used for the contours map",
                                type=list, default=None)
contours_map_group.add_argument("--contours_map_transform", help="Coordinate system on which the contours data is.",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_transform_options",
                                help="Options of the coordinate system on which the contours data is.",
                                type=check_json_format, default=None)
# Add shaded map features
shaded_map_group = parser.add_argument_group(
    "shaded_map", description="Arguments linked with shaded map")
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
                              type=check_json_format, default=None)
# Add shaded map features
shade2_map_group = parser.add_argument_group(
    "shade2_map", description="Arguments linked with shade2 map")
shade2_map_group.add_argument("--shade2_map_file", help="File which content should be plotted as a shade2 map.",
                              type=str, default=None)
shade2_map_group.add_argument("--shade2_map_variable", help="Variable to be plotted on shade2 map",
                              type=str, default=None)
shade2_map_group.add_argument("--shade2_map_levels", help="Number of level of the shade2 map color bar",
                              type=int, default=1)
shade2_map_group.add_argument("--shade2_map_hatches", help="Hatches that should be used for the shade2 map",
                              type=list, default=[None, "/"])
shade2_map_group.add_argument("--shade2_map_transform", help="Coordinate system on which the shade2 data is.",
                              type=str, default=None)
shade2_map_group.add_argument("--shade2_map_transform_options",
                              help="Options of the coordinate system on which the shade2 data is.",
                              type=check_json_format, default=None)

# Add vectors map features
vectors_map_group = parser.add_argument_group(
    "vectors_map", description="Arguments linked with vectors map")
vectors_map_group.add_argument("--vectors_map_u_file",
                               help="File which content should be plotted as a u composant vector map.",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_v_file",
                               help="File which content should be plotted as a v composant vector map.",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_u_variable", help="Variable (u component) to be plotted on colored map",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_v_variable", help="Variable (v component) to be plotted on colored map",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_type", help="Number of level of the shaded map color bar",
                               default="quivers", choices=["quivers", "barbs", "streamplots"])
vectors_map_group.add_argument("--vectors_map_options", help="Options of the vector map.",
                               type=check_json_format, default=None)
vectors_map_group.add_argument("--vectors_map_transform", help="Coordinate system on which the vectors data is.",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_transform_options",
                               help="Options of the coordinate system on which the vectors data is.",
                               type=check_json_format, default=dict())
# Add generic features
parser.add_argument("--coordinates", help="Coordinates to be plotted. Useful only in tricky cases (e.g. not CF-compliant)",
                    type=list, default=["auto"])
parser.add_argument("--projection", help="The projection to be used for the map",
                    type=str, default="PlateCarree")
parser.add_argument("--projection_options", help="The options of the projection to be used for the map",
                    type=check_json_format, default=None)
parser.add_argument("--feature_name", help="The cartopy.feature name of feature to add",
                    type=str, default=None)
parser.add_argument("--feature_color", help="The color of feature to add",
                    type=str, default='lightgray')
parser.add_argument(
    "--output_file", help="Path of the output_file", default=None)
parser.add_argument("--title", help="Title of the graphic", default=None)
parser.add_argument("--format", help="Output format", type=str, default="png")
parser.add_argument("--savefig_options",
                    help="Arguments for plt.savefig", type=check_json_format, default=dict())
parser.add_argument(
    "--lines",
    help="List of lines to plot, and their plot options : "
    "[[lats], [lons], options _dict]  or [ [[lats], [lons], options _dict] ]",
    type=check_json_format, default=None)
parser.add_argument("--debug", help="The color of feature to add",
                    type=bool, default=True)


def read_dataset(input_file, variable=None):
    with xr.open_dataset(input_file, decode_cf=True, decode_times=True, decode_coords=True, decode_timedelta=True,
                         use_cftime=True) as ds:
        if variable is None:
            return ds
        else:
            return ds.__getattr__(variable)


def filter_dataset(dataset, dimensions, selection_options=list()):
    for (key, opts) in selection_options:
        dataset = dataset.__getattribute__(key).__call__(**opts)
    dims_to_remove = sorted(list(set(dataset.dims) - set(dimensions)))
    if len(dims_to_remove) > 0:
        print("Warning: The following dimensions will be selected by their first value : %s"
              % ", ".join(dims_to_remove))
        dataset = dataset.isel(**{dim: 0 for dim in dims_to_remove})
    missing_dims = sorted(list(set(dimensions) - set(dataset.dims)))
    if len(missing_dims) > 0:
        raise ValueError("The following dimensions can not be found : %s" %
                         ", ".join(missing_dims))
    if debug:
        print("Tranposing data to ", *dimensions)
    dataset = dataset.transpose(*dimensions)
    print(dataset)
    return dataset


# Define a few functions for generic treatments
def find_data_in_dataset(variable_dataset, dimensions):
    variable_dimensions = variable_dataset.dims
    intersect_dimensions = list(set(variable_dimensions) & set(dimensions))
    # Find out the dimensions to keep
    select_variable_dimension = list()
    for i in variable_dimensions:
        if i in intersect_dimensions:
            select_variable_dimension.append(slice(None))
        else:
            select_variable_dimension.append(0)
    select_variable_dimension = tuple(select_variable_dimension)
    # print("dimensions=", dimensions)
    # print("select=", select_variable_dimension)
    return variable_dataset[select_variable_dimension]


def find_ccrs(coordinates, options=None):
    if debug:
        print("In find_ccrs, coordinates=", coordinates)
    # Allows for shortcuts for a few cases
    if coordinates == "LambertII":
        # Tag for a tangent Lambert Conformal proj with no false easting/northing.
        if debug:
            print("Using shortcut LambertII for projection")
        # Interpret options as an ordered list :
        # [ longitude_of_central_meridian, standard_parallel, latitude_of_projection_origin ]
        # and transform that for cartopy.crs.LambertConformal args
        new_options = dict()
        new_options["central_longitude"] = float(options[0])
        new_options["central_latitude"] = float(options[1])
        new_options["standard_parallels"] = (
            float(options[1]), float(options[1]))
        if options[1] != options[2]:
            raise ValueError(
                "LambertII coordinates implements only the case without false northing")
        #
        coordinates = "LambertConformal"
        options = new_options

    if coordinates in ccrs.__dict__:
        if options:
            return ccrs.__dict__[coordinates].__call__(**options)
        else:
            return ccrs.__dict__[coordinates].__call__()
    else:
        raise ValueError("Unknown coordinates system %s." % coordinates)


def compute_xy(lat2d, lon2d, projection):
    """
    Compute args X and Y for matplotlib's contour-type functions,
    for a given PROJECTION and a grid with the given LAT2D
    and LON2D values
    X and Y units are coordinates on the projection plane
    """
    first_point = [lon2d.values[0][0], lat2d.values[0][0]]
    last_point = [lon2d.values[-1][-1], lat2d.values[-1][-1]]
    y0, x0 = projection.transform_point(*first_point, ccrs.PlateCarree())
    ym, xm = projection.transform_point(*last_point, ccrs.PlateCarree())
    xsize = lat2d.shape[0]
    ysize = lat2d.shape[1]
    print("0,0 -> ", first_point)
    print("-1 -1-> ", *last_point)
    print(f"x0={x0}, xm={xm}, y0={y0}, ym={ym}, xsize={xsize}, ysize={ysize}")
    X = np.linspace(x0, xm, xsize)
    Y = np.linspace(y0, ym, ysize)
    grid = np.meshgrid(Y, X)
    if debug:
        print("Grid shape for x and y", grid[0].shape)
    return grid


def get_variable_and_coordinates_from_dataset(input_file, variable, coordinates, projection, selection_options=list()):
    # Check that the file exists
    if not os.path.isfile(input_file):
        raise ValueError("The input file %s does not exist." % input_file)
    variable_dataset = read_dataset(input_file, variable)

    if coordinates == ["auto"]:
        coordinates = horizontal_dimensions(variable_dataset.dims)

    variable_dataset = filter_dataset(
        variable_dataset, coordinates, selection_options=list())

    # Retrieve and possibly compute coordinates data
    dataset = read_dataset(input_file)
    variable_coordinates_data = list()
    if all([dim in dataset.variables for dim in coordinates]):
        # First simple case : when the dimensions of the variable are file
        # variables, and hence, are 1D coordinates
        if debug:
            print("Coordinates are file variables")
        for dim in coordinates:
            if debug:
                print("Adding coordinates data for ", dim)
            variable_coordinates_data.append(dataset.variables[dim][:])
    else:
        # Less simple case: data dimensions do not directly carry
        # geographic information. Example : Aladin data on Lambert
        # grid -> must use coordinates variables for getting
        # geographic coordinates
        if debug:
            print("Coordinates are not file variables")
        CF_coords = getattr(variable_dataset, 'coords', False)
        if CF_coords:
            # Use attribute 'coordinates' of the
            # variable, to identify the relevant file variables
            #coords = choose_among_CF_coordinates(CF_coords)
            coords = ["lat", "lon"]
        else:
            # Use user-provided (or heuristic) info
            coords = coordinates
            if debug:
                print("Using provided coordinates : ", coordinates)
        # if debug:
        #    print("Dataset_variables", repr(dataset.variables))
        lat2d = dataset.variables[coords[0]].transpose(*coordinates)
        lon2d = dataset.variables[coords[1]].transpose(*coordinates)
        X, Y = compute_xy(lat2d, lon2d, projection)
        variable_coordinates_data.append(X)
        variable_coordinates_data.append(Y)

    # Return the values found
    # print("variable_dimensions_data=", variable_dimensions_data)
    return variable_dataset, variable_coordinates_data


def horizontal_dimensions(dimensions):
    """
    Heuristics for identifying horizontal dimensions for
    a map, among a set of dimensions
    """
    possible_pairs = [("lon", "lat"), ("LON", "LAT"),
                      ("longitude", "latitude"), ("Lon", "Lat"), ("y", "x")]
    for x, y in possible_pairs:
        if x in dimensions and y in dimensions:
            if debug:
                print("Using horizontal dimensions :", x, y)
            return [x, y]
    raise ValueError("Cannot identify horizontal dimensions in ", dimensions)


def choose_among_CF_coordinates(CF_coords):
    """
    Transform a CF coordinates attribute in a coordinates list without
    Z-type coordinates
    Method is yet quite simple. A finer one would need more input
    """
    coordinates = CF_coords.split()
    chosen = list()
    for coordinate in coordinates:
        if coordinate != "height":
            chosen.append(coordinate)
    if chosen == ['lat', 'lon']:
        chosen = ['lon', 'lat']
    if debug:
        print("Choosing coordinates %s among CF coordinates %s" %
              (CF_coords, chosen))
    return(chosen)


# Define a few functions for plots
def plot_colored_map(ax, coordinates, colored_map_file, colored_map_variable,
                     colored_map_transform, colored_map_transform_options, projection,
                     colored_map_colors, colored_map_levels, colored_map_selection_options,
                     colored_map_scale, colored_map_offset):
    # Find the transform
    if colored_map_transform:
        if debug:
            print("Using specific transform %s for colored map",
                  colored_map_transform)
        transform = find_ccrs(colored_map_transform,
                              colored_map_transform_options)
    else:
        if debug:
            print("Using common transform %s for colored map", repr(projection))
        transform = projection

    # Find used data
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        colored_map_file, colored_map_variable, coordinates, transform, colored_map_selection_options)

    # Apply scale and offset if applicable
    if colored_map_scale:
        variable_data = variable_data * colored_map_scale
    if colored_map_offset:
        variable_data = variable_data + colored_map_offset

    # Plot the map
    colored_map_plot = plt.contourf(*variable_coordinates_data,
                                    variable_data, colored_map_levels,
                                    transform=transform, colors=colored_map_colors, zorder=0)
    plt.colorbar(colored_map_plot, ax=ax)


def plot_contours_map(ax, coordinates, contours_map_file, contours_map_variable,
                      contours_map_transform, contours_map_transform_options, projection,
                      contours_map_colors, contours_map_levels):
    # Find the transform
    if contours_map_transform:
        transform = find_ccrs(contours_map_transform,
                              contours_map_transform_options)
    else:
        transform = projection

        # Find used data
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        contours_map_file, contours_map_variable, coordinates, transform)

    # Plot the map
    plt.contour(*variable_coordinates_data, variable_data,
                contours_map_levels, transform=transform, colors=contours_map_colors, zorder=1)


def plot_shaded_map(ax, coordinates, shaded_map_file, shaded_map_variable,
                    shaded_map_transform, shaded_map_transform_options, projection,
                    shaded_map_hatches, shaded_map_levels):
    # Find the transform
    if shaded_map_transform:
        transform = find_ccrs(shaded_map_transform,
                              shaded_map_transform_options)
    else:
        transform = projection
    # Find used data
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        shaded_map_file, shaded_map_variable, coordinates, transform)
    # Plot the map
    plt.contourf(*variable_coordinates_data, variable_data,
                 shaded_map_levels, transform=transform,
                 hatches=shaded_map_hatches, colors="none")


def plot_vector_map(ax, coordinates, vectors_map_u_file, vectors_map_v_file,
                    vectors_map_u_variable, vectors_map_v_variable,
                    vectors_map_transform, vectors_map_transform_options, projection,
                    vectors_map_type, vectors_map_options):
    # Find the transform
    if args.vectors_map_transform:
        transform = find_ccrs(vectors_map_transform,
                              vectors_map_transform_options)
    else:
        transform = projection
    # Get the datasets and dimensions
    variable_u_data, variable_u_coordinates_data = \
        get_variable_and_coordinates_from_dataset(
            vectors_map_u_file, vectors_map_u_variable, coordinates, transform)
    variable_v_data, variable_v_coordinates_data = \
        get_variable_and_coordinates_from_dataset(vectors_map_v_file, vectors_map_v_variable,
                                                  coordinates, transform)
    # Check that coordinates are the same
    if variable_u_coordinates_data != variable_v_coordinates_data:
        raise ValueError(
            "Zonal and meridian component of the vector field must have same coordinates.")
    # Plot the map
    if vectors_map_type in ax.__dict__:
        ax.__dict__[vectors_map_type].__call__(*variable_u_coordinates_data,
                                               variable_u_data, variable_v_data,
                                               transform=transform, **vectors_map_options)
    else:
        raise ValueError("unknown vectors map type %s." % vectors_map_type)


def plot_lines(lines, transform):
    """
    Plot lines, strucuture as
        - [ [[lons], [lats], options _dict] ]
        -   [[lons], [lats], options _dict]
    where options_dict may be missing
    """
    # If we have a single line, transform it to a list of lines.
    if type(lines[0][0]) is not list:
        lines = [lines]
    for line in lines:
        if (len(line) == 2):
            options = dict()
        else:
            options = line[2]
        # plt.plot(line[0], line[1], transform=transform, **options)
        plt.plot(line[1], line[0], transform=ccrs.PlateCarree(), **options)


def plot_map(args):
    # Get coordinates
    coordinates = args.coordinates

    # Deal with projection
    projection = find_ccrs(args.projection, args.projection_options)
    if debug:
        print("Map projection set to "+repr(projection))

    # Initialize the plot
    ax = plt.axes(projection=projection)
    #ax.set_extent((-50, 120., -30, 70), crs=ccrs.PlateCarree())

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
                         colored_map_levels=args.colored_map_levels,
                         colored_map_selection_options=args.colored_map_selection_options,
                         colored_map_scale=args.colored_map_scale,
                         colored_map_offset=args.colored_map_offset,
                         )

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

    # Deal with the shade2 map if needed
    if args.shade2_map_file is not None:
        plot_shaded_map(ax=ax,
                        coordinates=coordinates,
                        shaded_map_file=args.shade2_map_file,
                        shaded_map_variable=args.shade2_map_variable,
                        shaded_map_transform=args.shade2_map_transform,
                        shaded_map_transform_options=args.shade2_map_transform_options,
                        projection=projection,
                        shaded_map_hatches=args.shade2_map_hatches,
                        shaded_map_levels=args.shade2_map_levels)

    # Deal with the vector map if needed
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

    # Plot lines if provided
    if args.lines is not None:
        plot_lines(lines=args.lines, transform=projection)

    # Deal with output
    output_file = args.output_file
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file, **args.savefig_options)


def heuristics(args):
    # Transform or process arguments for implementing shortcuts
    # or adapting the real world to the strict logic above

    # Allow to simply draw contours of the colored map field
    # by providing contours_map_levels
    if args.contours_map_levels is not None and args.contours_map_file is None and \
       args.colored_map_file is not None:
        args.contours_map_file = args.colored_map_file
        args.contours_map_variable = args.colored_map_variable
        args.contours_map_transform = args.colored_map_transform
        args.contours_map_transform_options = args.colored_map_transform_options
        if args.contours_map_colors is None:
            args.contours_map_colors = args.colored_map_colors
    #
    # Put args.format in savefig options (possibly overriding the value there)
    # This for consistency when used in CliMAF (hard-coded in CliMAF driver)
    args.savefig_options['format'] = args.format


if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    debug = args.debug
    # Apply heuristics which implements shortcuts in arguments
    heuristics(args)
    # Plot the map
    plot_map(args)
