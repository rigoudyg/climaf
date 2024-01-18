import os
import argparse
import json
import six

import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmaps

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
colored_map_group.add_argument("--colored_map_levels", help="Number or list of levels for the colored map regions",
                               type=check_json_format, default=None)
colored_map_group.add_argument("--colored_map_cmap", help="Colors list or colormap name to use for the colored map",
                               type=check_json_format, default='"BlueDarkRed18"')
colored_map_group.add_argument("--colored_map_transform", help="Coordinate system on which the colored map data is.",
                               type=str, default=None)
colored_map_group.add_argument("--colored_map_transform_options",
                               help="Options of the coordinate system on which the colored map data is.",
                               type=check_json_format, default=None)
colored_map_group.add_argument("--colored_map_selection_options",
                               help="Options to be used to select data at some coordinate values if needed."
                                    "Expected format: dict with key=selection method and value=dict of args",
                               type=check_json_format, default=dict())
colored_map_group.add_argument("--colored_map_engine", help="Plot engine: can be set to 'pcolormesh'; default is 'contourf'",
                               type=str, default="contourf")
colored_map_group.add_argument("--colored_map_engine_options", help="Args for the plot engine",
                               type=check_json_format, default=dict())
colored_map_group.add_argument("--colored_map_min", help="Min value to plot on the colored map",
                               type=float, default=None)
colored_map_group.add_argument("--colored_map_max", help="Max value to plot on the colored map",
                               type=float, default=None)
colored_map_group.add_argument("--colored_map_delta", help="For the colored map, interval defining the number of levels/colors between min and max ",
                               type=float, default=None)
colored_map_group.add_argument("--colored_map_scale", help="Scale factor to apply to the colored map field",
                               type=float, default=None)
colored_map_group.add_argument("--colored_map_offset", help="Offset to apply to the colored map field",
                               type=float, default=None)
colored_map_group.add_argument("--colored_map_methods",
                               help="A dict of the methods to call on colored map, dict values are the args key/values pairs",
                               type=check_json_format, default=dict())
colored_map_group.add_argument("--colorbar_options", help="Arguments dict for plt.colorbar()",
                               type=check_json_format, default=dict())

# Add contours map features
contours_map_group = parser.add_argument_group(
    "contours_map", description="Arguments linked with contours map")
contours_map_group.add_argument("--contours_map_file", help="File which content should be plotted as a contours map.",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_variable", help="Variable to be plotted on contours map",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_levels", help="Number of level of the contours color bar",
                                type=check_json_format, default=None)
contours_map_group.add_argument("--contours_map_colors", help="Colors that should be used for the contours map",
                                type=list, default=[])
contours_map_group.add_argument("--contours_map_transform", help="Coordinate system on which the contours data is.",
                                type=str, default=None)
contours_map_group.add_argument("--contours_map_transform_options",
                                help="Options of the coordinate system on which the contours data is.",
                                type=check_json_format, default=None)
contours_map_group.add_argument("--contours_map_selection_options",
                                help="Options to be used to select data at some coordinate values if needed."
                                "Expected format: dict with key=selection method and value=dict of args",
                                type=check_json_format, default=dict())
contours_map_group.add_argument("--contours_map_min", help="Min value to plot on the contours map",
                                type=float, default=None)
contours_map_group.add_argument("--contours_map_max", help="Max value to plot on the contours map",
                                type=float, default=None)
contours_map_group.add_argument("--contours_map_scale", help="Scale factor to apply to the contours map field",
                                type=float, default=None)
contours_map_group.add_argument("--contours_map_offset", help="Offset to apply to the contours map field",
                                type=float, default=None)
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
                              type=check_json_format, default=[None, "/"])
shaded_map_group.add_argument("--shaded_map_transform", help="Coordinate system on which the shaded data is.",
                              type=str, default=None)
shaded_map_group.add_argument("--shaded_map_transform_options",
                              help="Options of the coordinate system on which the shaded data is.",
                              type=check_json_format, default=None)
shaded_map_group.add_argument("--shaded_map_selection_options",
                              help="Options to be used to select data at some coordinate values if needed."
                              "Expected format: dict with key=selection method and value=dict of args",
                              type=check_json_format, default=dict())
shaded_map_group.add_argument("--shaded_map_min", help="Min value to plot on the shaded map",
                              type=float, default=None)
shaded_map_group.add_argument("--shaded_map_max", help="Max value to plot on the shaded map",
                              type=float, default=None)
shaded_map_group.add_argument("--shaded_map_scale", help="Scale factor to apply to the shaded map field",
                              type=float, default=None)
shaded_map_group.add_argument("--shaded_map_offset", help="Offset to apply to the shaded map field",
                              type=float, default=None)
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
                              type=check_json_format, default=[None, "*"])
shade2_map_group.add_argument("--shade2_map_transform", help="Coordinate system on which the shade2 data is.",
                              type=str, default=None)
shade2_map_group.add_argument("--shade2_map_transform_options",
                              help="Options of the coordinate system on which the shade2 data is.",
                              type=check_json_format, default=None)
shade2_map_group.add_argument("--shade2_map_selection_options",
                              help="Options to be used to select data at some coordinate values if needed."
                              "Expected format: dict with key=selection method and value=dict of args",
                              type=check_json_format, default=dict())
shade2_map_group.add_argument("--shade2_map_min", help="Min value to plot on the shade2 map",
                              type=float, default=None)
shade2_map_group.add_argument("--shade2_map_max", help="Max value to plot on the shade2 map",
                              type=float, default=None)
shade2_map_group.add_argument("--shade2_map_scale", help="Scale factor to apply to the shade2 map field",
                              type=float, default=None)
shade2_map_group.add_argument("--shade2_map_offset", help="Offset to apply to the shade2 map field",
                              type=float, default=None)

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
vectors_map_group.add_argument("--vectors_map_type", help="Type of vectors for the vector map",
                               default="quiver", choices=["quiver", "barbs", "streamplot"])
vectors_map_group.add_argument("--vectors_map_options", help="Options of the vector map.",
                               type=check_json_format, default=dict())
vectors_map_group.add_argument("--vectors_map_transform", help="Coordinate system on which the vectors data is.",
                               type=str, default=None)
vectors_map_group.add_argument("--vectors_map_transform_options",
                               help="Options of the coordinate system on which the vectors data is.",
                               type=check_json_format, default=dict())
vectors_map_group.add_argument("--vectors_map_selection_options",
                               help="Options to be used to select data at some coordinate values if needed."
                               "Expected format: list of tuples (selection method, associated dict options)",
                               type=check_json_format, default=dict())
vectors_map_group.add_argument("--vectors_map_scale", help="Scale factor to apply to the vectors map field",
                               type=float, default=None)
# Add generic features
parser.add_argument("--coordinates", help="Coordinates to be plotted. Useful only in tricky cases (e.g. not CF-compliant)",
                    type=list, default=["auto"])
parser.add_argument("--projection", help="The projection to be used for the map",
                    type=str, default="PlateCarree")
parser.add_argument("--projection_options", help="The options of the projection to be used for the map",
                    type=check_json_format, default=None)
parser.add_argument("--features", help="A dict of features and attributes to add : {feature_name : kwargs }",
                    type=check_json_format, default=dict())
parser.add_argument("--plt_methods", type=check_json_format, default=dict(),
                    help="Dict of pyplot methods to be called, with values = args dicts list")
parser.add_argument("--axis_methods", type=check_json_format, default=dict(),
                    help="Dict of axis methods to be called, with values = args dicts list")
parser.add_argument(
    "--output_file", help="Path of the output_file", default=None)
parser.add_argument("--format", help="Output format", type=str, default="png")
parser.add_argument("--figure_options",
                    help="Arguments for plt.figure()", type=check_json_format, default=dict())
parser.add_argument("--savefig_options",
                    help="Arguments for plt.savefig()", type=check_json_format, default=dict())
# parser.add_argument("--title_options",
#                    help="Arguments for figure.suptitle()", type=check_json_format, default=dict())
parser.add_argument(
    "--lines",
    help="List of lines to plot, and their plot options : "
    "[[lats], [lons], options _dict]  or [ [[lats], [lons], options _dict] ]",
    type=check_json_format, default=None)
parser.add_argument("--debug", help="To get some details",
                    type=bool, default=True)

gplot_group = parser.add_argument_group(
    "gplot", description="Arguments reproducing those of gplot.ncl")
gplot_group.add_argument("--title", help="Title of the graphic", default=None)
gplot_group.add_argument("--trim", help="Crop the surrounding extra white space",
                         type=check_json_format, default=True)
gplot_group.add_argument("--resolution", help="Image size (in pixels for png, in inches for pdf and eps) e.g. '1200x800'",
                         type=str, default=None)
gplot_group.add_argument("--dpi", help="Resolution in dots per inch",
                         type=int, default=None)
gplot_group.add_argument("--focus", help="Should plot focus on ocean or land",
                         type=str, default=None, choices=['ocean', 'land'])
gplot_group.add_argument("--scale", help="Scale factor for colored map, else for contours map",
                         type=float, default=None)
gplot_group.add_argument("--offset", help="Offset for colored map, else for contours map",
                         type=float, default=None)
gplot_group.add_argument("--units", help="An alternate label for units (showing on top right)",
                         type=str, default=None)
gplot_group.add_argument("--vcb", help="Should we have a Vertical ColorBar",
                         type=check_json_format, default=None)
gplot_group.add_argument("--time", help="A time value (not a date) for selecting data. Use an integer for index (xarray's 'isel') and a float for value (xarray's 'sel')",
                         type=check_json_format, default=None)
gplot_group.add_argument("--date", help="A date for selecting data. e.g. 1850, 185001, 18500101, 1850-01 1850-01-01 ",
                         type=str, default=None)
gplot_group.add_argument("--level", help="A level for selecting data. Use an integer for index (xarray's 'isel') and a float for value (xarray's 'sel')",
                         type=float, default=None)
gplot_group.add_argument("--xpolyline", help="x or lon values for a line of points to draw (spaces separated)",
                         type=str, default=None)
gplot_group.add_argument("--ypolyline", help="y or lat values for a line of points to draw (spaces separated)",
                         type=str, default=None)
gplot_group.add_argument("--polyline_options", help="A dict of arguments to plot for drawing polyline",
                         type=check_json_format, default=dict(color='blue'))
# gplot_group.add_argument("--", help="",
#                         type=, default=)


def read_dataset(input_file, variable=None):
    with xr.open_dataset(input_file, decode_cf=True, decode_times=True, decode_coords=True, decode_timedelta=True,
                         use_cftime=True) as ds:
        if variable is None:
            return ds
        else:
            return ds.__getattr__(variable)


def filter_dataset(dataset, dimensions, selection_options=dict()):
    # e.g. selection_options ={ "isel": {"time": 0, "level" : 3} }
    for method in selection_options:
        # e.g. kwargs = {"time": 0, "level" : 3}
        kwargs = selection_options[method]
        if debug:
            print("Selecting with %s, %s" % (method, kwargs))
        for dimension in kwargs:
            if dimension not in dataset.dims and dimension in ['time', 'level']:
                # This entry probably has been set by mimic_gplot. Just skip
                continue
            selargs = {dimension: kwargs[dimension]}
            dataset = dataset.__getattribute__(method).__call__(**selargs)
    dims_to_remove = sorted(list(set(dataset.dims) - set(dimensions)))
    if len(dims_to_remove) > 0:
        print("Warning: The following dimensions will be selected by their first value : %s"
              % ", ".join(dims_to_remove))
        dataset = dataset.isel(**{dim: 0 for dim in dims_to_remove})
    missing_dims = sorted(list(set(dimensions) - set(dataset.dims)))
    if len(missing_dims) > 0:
        raise ValueError("The following dimensions cannot be found : %s" %
                         ", ".join(missing_dims))
    # if debug:
    #     print("Tranposing data to ", *dimensions)
    # dataset = dataset.transpose(*dimensions)
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


def fix_longitudes(lons):
    """
    Useful for e.g. ORCA grid : avoid discontinuity in longitudes due
    to 2*PI steps, in order that pcolormesh works fine
    """
    fixed_lons = lons.copy()
    for i, start in enumerate(np.argmax(np.abs(np.diff(lons)) > 180, axis=1)):
        fixed_lons[i, start+1:] += 360
    return fixed_lons


def compute_xy(lat2d, lon2d, projection, exact=True):
    """
    Compute args X and Y for matplotlib's contour-type functions,
    for a given PROJECTION and a grid with the given LAT2D
    and LON2D values

    If EXACT is False, assume that the data are evenly spaced on
    the projection plane, which allows to speed up the process

    X and Y units are coordinates on the projection plane
    """
    if exact:
        if projection != ccrs.PlateCarree():
            ret = projection.transform_points(
                ccrs.PlateCarree(), lon2d.values, lat2d.values)
            return ret[..., 0], ret[..., 1]
        else:
            if debug:
                print("compute_xy : fixing returned longitudes")
            return fix_longitudes(lon2d), lat2d
    else:
        first_point = [lon2d[0][0], lat2d[0][0]]
        last_point = [lon2d[-1][-1], lat2d[-1][-1]]
        x0, y0 = projection.transform_point(*first_point, ccrs.PlateCarree())
        xm, ym = projection.transform_point(*last_point, ccrs.PlateCarree())
        ysize = lat2d.shape[0]
        xsize = lat2d.shape[1]
        if debug:
            print("0,0 -> ", first_point)
            print("-1 -1-> ", *last_point)
            print(
                f"x0={x0}, xm={xm}, y0={y0}, ym={ym}, xsize={xsize}, ysize={ysize}")
        X = np.linspace(x0, xm, xsize)
        Y = np.linspace(y0, ym, ysize)
        grid = np.meshgrid(X, Y)
        if debug:
            print("Grid shape for x and y", grid[0].shape)
        return grid


def get_variable_and_coordinates_from_dataset(
        input_file, variable, dimensions, projection, selection_options=list(), exact=True):
    """
    If EXACT is False, and when variable dimensions are not file variables, values for
    coordinates are assumed to be linear between first and last points
    """
    # Check that the file exists
    if not os.path.isfile(input_file):
        raise ValueError("The input file %s does not exist" % input_file)
    variable_dataset = read_dataset(input_file, variable)
    if dimensions == ["auto"]:
        dimensions = horizontal_dimensions(variable_dataset.dims)
    variable_dataset = filter_dataset(
        variable_dataset, dimensions, selection_options)

    # Retrieve and possibly compute coordinates data
    dataset = read_dataset(input_file)
    variable_coordinates_data = list()
    if all([dim in dataset.variables for dim in dimensions]):
        # First simple case : when the dimensions of the variable are file
        # variables, and hence, are 1D coordinates, hopefully lat and lon
        if debug:
            print(f"Coordinates ({dimensions}) are file variables")
        for dim in dimensions:
            if debug:
                print("Adding coordinates data for ", dim)
            variable_coordinates_data.append(dataset.variables[dim])
    else:
        # e.g. the case of Aladin LambertII projection, or Nemo ORCA grid"
        if debug:
            print(f"Coordinates ({dimensions}) are not file variables")
        # TBD : be more flexible on lat_name. Inspect coords names
        lat_name = "lat"
        lon_name = "lon"
        lat2d = variable_dataset.coords[lat_name]
        lon2d = variable_dataset.coords[lon_name]
        lon2d_fixed = fix_longitudes(lon2d)
        X, Y = compute_xy(lat2d, lon2d_fixed, projection, exact)
        variable_coordinates_data.append(X)
        variable_coordinates_data.append(Y)
    #
    return variable_dataset, variable_coordinates_data


def horizontal_dimensions(dimensions):
    """
    Heuristics for identifying horizontal dimensions for
    a map, among a set of dimensions
    TBD : should used CF convention for choosing horizontal dimensions
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


def create_norm(nlevels, cmap, z, zmin, zmax):
    if zmin is None:
        zmin = z.min()
    if zmax is None:
        zmax = z.max()
    levels = MaxNLocator(nbins=nlevels).tick_values(zmin, zmax)
    if type(cmap) is str:
        cmap = plt.colormaps[cmap]
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    return norm


# Define a few functions for plots
def plot_colored_map(fig, ax, coordinates, colored_map_file, colored_map_variable,
                     colored_map_transform, colored_map_transform_options, projection,
                     colored_map_cmap, colored_map_levels, colored_map_selection_options,
                     colored_map_engine, colored_map_engine_options,
                     colored_map_min, colored_map_max,
                     colored_map_scale, colored_map_offset, colored_map_methods,
                     colorbar_options, *kwargs):
    # Find the transform
    if colored_map_transform is not None and colored_map_transform != "do not remap":
        if debug:
            print("Using dedicated transform %s for interpreting colored map field",
                  colored_map_transform)
        transform = find_ccrs(colored_map_transform,
                              colored_map_transform_options)
    else:
        if debug:
            print(
                "Assuming color_map field data has common transform %s " % repr(projection))
        transform = projection

    # Find used data, and coordintaes if needed
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        colored_map_file, colored_map_variable, coordinates, transform,
        colored_map_selection_options, colored_map_transform != "do not remap")

    # Capture units,long_name and time before changing variable_data type
    if args.units:
        units = args.units
    else:
        units = variable_data.units
    try:
        name = variable_data.__getattr__('long_name')
    except:
        name = colored_map_variable
    #
    if "time" in variable_data.coords:
        timestamp = str(variable_data.time.values)
    else:
        timestamp = None

    # Apply scale and offset
    if colored_map_scale:
        variable_data = variable_data * colored_map_scale
    if colored_map_offset:
        variable_data = variable_data + colored_map_offset

    # Allow cmap name to refer to package 'cmaps' - see https://github.com/hhuangwx/cmaps
    try:
        colored_map_cmap = cmaps.__getattribute__(colored_map_cmap)
    except:
        pass

    # Prepare to plot the map
    contourf_args = dict(zorder=0, cmap=colored_map_cmap)
    if colored_map_min is not None:
        contourf_args["vmin"] = colored_map_min
        if args.colored_map_cmap is not None and \
           type(colored_map_engine_options.get('colors', None)) is not list:
            # TBD Must apply threshold vmin, otherwise colormap extent will not reflect it
            pass
    if colored_map_max is not None:
        contourf_args["vmax"] = colored_map_max
        if args.colored_map_cmap is not None and \
           type(colored_map_engine_options.get('colors', None)) is not list:
            # TBD Must apply threshold vmax, otherwise colormap extent will not reflect it
            pass
    contourf_args.update(colored_map_engine_options)
    if colored_map_levels is not None and 'colored_map_levels' not in contourf_args:
        contourf_args['levels'] = colored_map_levels

    if colored_map_transform != "do not remap":
        contourf_args["transform"] = transform
        if colored_map_engine == "contourf":
            if debug:
                print("Plotting with contourf and remapping")
                print("Contourf levels=", colored_map_levels)
                print("Contourf args=", contourf_args)
            colored_map_plot = plt.contourf(
                *variable_coordinates_data, variable_data,
                **contourf_args)  # colors=colored_map_cmap,
        else:  # default case : pcolormesh
            if debug:
                print("Plotting with pcolormesh and remapping")
            if colored_map_cmap is not None:
                raise ValueError("Cannot apply desired colors to the color_map plot "
                                 "because plot engine is not set to contourf")
            norm = create_norm(colored_map_levels, colored_map_cmap,
                               variable_data, colored_map_min, colored_map_max)
            colored_map_plot = ax.pcolormesh(
                *variable_coordinates_data, variable_data, norm=norm, **contourf_args)
    else:
        if debug:
            print("Plotting without remapping, and with contourf")
        ymin = np.min(variable_coordinates_data[1])
        ymax = np.max(variable_coordinates_data[1])
        xmin = np.min(variable_coordinates_data[0])
        xmax = np.max(variable_coordinates_data[0])
        contourf_args["extent"] = (xmin, xmax, ymin, ymax)
        contourf_args["transform"] = projection
        # Provided colored_map_transform calls for avoiding to remap data
        colored_map_plot = plt.contourf(variable_data, colored_map_levels,
                                        colors=colored_map_colors, **contourf_args)
    for method in colored_map_methods:
        colored_map_plot.__getattr__(method).__call__(
            **colored_map_methods[method])

    # Colorbar. https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.colorbar
    if 'shrink' not in args.colorbar_options:
        # TBD : compute colorbar shrink based on figure aspect ratio, or heuristic
        args.colorbar_options['shrink'] = 0.4

    fig.colorbar(colored_map_plot, ax=ax, **colorbar_options)

    # Variable name as left title, time + units as right title.
    if timestamp is not None:
        units = timestamp + " / " + units
    plt.title(label=units, loc='right', y=-0.13)
    plt.title(label=name, loc='left')


def plot_contours_map(ax, coordinates, contours_map_file, contours_map_variable,
                      contours_map_transform, contours_map_transform_options, projection,
                      contours_map_colors, contours_map_levels,
                      contours_map_selection_options, contours_map_min, contours_map_max,
                      contours_map_scale, contours_map_offset):
    # Find the transform
    if contours_map_transform:
        transform = find_ccrs(contours_map_transform,
                              contours_map_transform_options)
    else:
        transform = projection

    # Find used data
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        contours_map_file, contours_map_variable, coordinates, transform, contours_map_selection_options)

    # Apply scale and offset
    if contours_map_scale:
        variable_data = variable_data * contours_map_scale
    if contours_map_offset:
        variable_data = variable_data + contours_map_offset

    # Plot the map
    kwargs = dict(zorder=0, transform=transform)
    if contours_map_min is not None:
        kwargs["vmin"] = contours_map_min
    if contours_map_max is not None:
        kwargs["vmax"] = contours_map_max
    if len(contours_map_colors) > 0:
        kwargs["colors"] = contours_map_colors
    if contours_map_levels == 1:
        # TBD : apply colormap levels to contours
        raise ValueError("Cannot yet handle option 'contours=1'." +
                         " Please provide a list of levels or discard argument contours")
    if contours_map_levels is not None:
        plt.contour(*variable_coordinates_data, variable_data,
                    contours_map_levels, **kwargs)
    else
        plt.contour(*variable_coordinates_data, variable_data, **kwargs)


def plot_shaded_map(ax, coordinates, shaded_map_file, shaded_map_variable,
                    shaded_map_transform, shaded_map_transform_options, projection,
                    shaded_map_hatches, shaded_map_levels, shaded_map_selection_options,
                    shaded_map_min, shaded_map_max,
                    shaded_map_scale, shaded_map_offset):
    # Find the transform
    if shaded_map_transform:
        transform = find_ccrs(shaded_map_transform,
                              shaded_map_transform_options)
    else:
        transform = projection
    # Find used data
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        shaded_map_file, shaded_map_variable, coordinates, transform, shaded_map_selection_options)

    # Apply scale and offset
    if shaded_map_scale:
        variable_data = variable_data * shaded_map_scale
    if shaded_map_offset:
        variable_data = variable_data + shaded_map_offset

    # Plot the map
    kwargs = dict(zorder=0, transform=transform,
                  hatches=shaded_map_hatches, colors='none')
    if shaded_map_min is not None:
        kwargs["vmin"] = shaded_map_min
    if shaded_map_max is not None:
        kwargs["vmax"] = shaded_map_max
    print(kwargs)
    plt.contourf(*variable_coordinates_data, variable_data,
                 shaded_map_levels, **kwargs)


def plot_vector_map(ax, coordinates, vectors_map_u_file, vectors_map_v_file,
                    vectors_map_u_variable, vectors_map_v_variable,
                    vectors_map_transform, vectors_map_transform_options, projection,
                    vectors_map_type, vectors_map_options, vectors_map_selection_options, vectors_map_scale):
    # Find the transform
    if args.vectors_map_transform:
        transform = find_ccrs(vectors_map_transform,
                              vectors_map_transform_options)
    else:
        transform = projection
    # Get the datasets and dimensions
    variable_u_data, variable_u_coordinates_data = get_variable_and_coordinates_from_dataset(
        vectors_map_u_file, vectors_map_u_variable, coordinates, transform, vectors_map_selection_options)
    variable_v_data, variable_v_coordinates_data = get_variable_and_coordinates_from_dataset(
        vectors_map_v_file, vectors_map_v_variable, coordinates, transform, vectors_map_selection_options)
    print(variable_u_coordinates_data)
    # print(variable_v_coordinates_data)

    # Check that coordinates are the same
    if any([any(ucoord != vcoord) for ucoord, vcoord in
            zip(variable_u_coordinates_data, variable_v_coordinates_data)]):
        raise ValueError(
            "Zonal and meridian component of the vector field must have same coordinates.")

    # Apply scale
    if vectors_map_scale:
        variable_data = variable_data * vectors_map_scale

    # Plot the map
    if vectors_map_type in dir(ax):
        ax.__getattribute__(vectors_map_type).__call__(*variable_u_coordinates_data,
                                                       variable_u_data, variable_v_data,
                                                       transform=transform, **vectors_map_options)
    else:
        raise ValueError("unknown vectors map type %s." % vectors_map_type)


def plot_map(args, **kwargs):
    # Get coordinates
    coordinates = args.coordinates

    # Deal with projection
    projection = find_ccrs(args.projection, args.projection_options)
    if debug:
        print("Map projection set to "+repr(projection))

    # Initialize the plot
    fig = plt.figure(**args.figure_options)
    ax = plt.axes(projection=projection)
    if 'polar_stereo_extent' in kwargs:
        if debug:
            print("Setting extent to ", kwargs['polar_stereo_extent'])
        ax.set_extent(kwargs['polar_stereo_extent'], ccrs.PlateCarree())
    # ax.set_extent((-50, 120., -30, 70), crs=ccrs.PlateCarree())

    if args.title is not None:
        # fig.suptitle(args.title, **args.title_options)
        if 'title' not in args.plt_methods:
            args.plt_methods['title'] = []
        args.plt_methods['title'].append(
            {'label': args.title, 'fontsize': 'xx-large'})

    # Deal with the colored map if needed
    if args.colored_map_file:
        plot_colored_map(fig=fig, ax=ax, coordinates=coordinates,
                         colored_map_file=args.colored_map_file,
                         colored_map_variable=args.colored_map_variable,
                         colored_map_transform=args.colored_map_transform,
                         colored_map_transform_options=args.colored_map_transform_options,
                         projection=projection,
                         colored_map_cmap=args.colored_map_cmap,
                         colored_map_levels=args.colored_map_levels,
                         colored_map_selection_options=args.colored_map_selection_options,
                         colored_map_engine=args.colored_map_engine,
                         colored_map_engine_options=args.colored_map_engine_options,
                         colored_map_min=args.colored_map_min,
                         colored_map_max=args.colored_map_max,
                         colored_map_scale=args.colored_map_scale,
                         colored_map_offset=args.colored_map_offset,
                         colored_map_methods=args.colored_map_methods,
                         colorbar_options=args.colorbar_options,
                         **kwargs
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
                          contours_map_levels=args.contours_map_levels,
                          contours_map_selection_options=args.contours_map_selection_options,
                          contours_map_min=args.contours_map_min,
                          contours_map_max=args.contours_map_max,
                          contours_map_scale=args.contours_map_scale,
                          contours_map_offset=args.contours_map_offset,
                          )

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
                        shaded_map_levels=args.shaded_map_levels,
                        shaded_map_selection_options=args.shaded_map_selection_options,
                        shaded_map_min=args.shaded_map_min,
                        shaded_map_max=args.shaded_map_max,
                        shaded_map_scale=args.shaded_map_scale,
                        shaded_map_offset=args.shaded_map_offset,
                        )

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
                        shaded_map_levels=args.shade2_map_levels,
                        shaded_map_selection_options=args.shade2_map_selection_options,
                        shaded_map_min=args.shade2_map_min,
                        shaded_map_max=args.shade2_map_max,
                        shaded_map_scale=args.shade2_map_scale,
                        shaded_map_offset=args.shade2_map_offset,
                        )

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
                        vectors_map_options=args.vectors_map_options,
                        vectors_map_selection_options=args.vectors_map_selection_options,
                        vectors_map_scale=args.vectors_map_scale,
                        )

    # Plt methods
    for method in args.plt_methods:
        for kwargs in args.plt_methods[method]:
            largs = kwargs.pop('largs', [])
            if debug:
                print(f"Calling plt method {method} with kwargs: {kwargs}")
            plt.__getattribute__(method).__call__(*largs, **kwargs)

    # Axes methods
    for method in args.axis_methods:
        for kwargs in args.axis_methods[method]:
            largs = kwargs.pop('largs', [])
            if debug:
                print(f"Calling axis method {method} with kwargs: {kwargs}")
            ax.__getattribute__(method).__call__(*largs, **kwargs)

    # Deal with output
    output_file = args.output_file
    if output_file is not None:
        if debug:
            print("Calling savefig with options :", args.savefig_options)
        plt.savefig(output_file, **args.savefig_options)
    else:
        plt.show(block=True)


def heuristics(args):
    # Transform or process arguments for implementing shortcuts
    # Also set sensible values for parameters if not set by user

    # Put args.format in savefig options (possibly overriding the value there)
    # This for consistency when used in CliMAF (hard-coded in CliMAF driver)
    args.savefig_options['format'] = args.format

    # Allow axis_methods and plt_methods values (kwargs) to be
    # dict rather than dict list
    for methods in [args.axis_methods, args.plt_methods]:
        for method in methods:
            if type(methods[method]) is not list:
                methods[method] = [methods[method]]

    # For axis method add_feature : evaluate the feature arg (in all kwargs set)
    for method in args.axis_methods:
        if method == 'add_feature':
            ldic = args.axis_methods['add_feature']
            for dic in ldic:
                if 'feature' in dic:
                    feature = dic['feature']
                    if "." in feature:
                        # Assume we have a fully qualified object path
                        dic['feature'] = eval(feature)
                    else:
                        # Assume we look for a feature in cartopy.feature
                        features = ['BORDERS', 'COASTLINE', 'LAKES',
                                    'LAND', 'OCEAN', 'RIVERS', 'STATES']
                        if feature not in features:
                            raise ValueError(f"Required feature {feature} doesn't " +
                                             f"belong to cartopy.features {features}")
                        dic['feature'] = eval(f"cfeature.{feature}")
                else:
                    raise ValueError(
                        "axis_methods 'add_feature' does not include key 'feature' in this dic :",
                        dic)

    # Transform string-typed lists to a list for some args
    if args.colored_map_levels is not None:
        if "," in args.colored_map_levels:
            spliter = ","
        else:
            spliter = " "
        args.colored_map_levels = args.colored_map_levels.split(spliter)
    if args.contours_map_levels is not None:
        if "," in args.contours_map_levels:
            spliter = ","
        else:
            spliter = " "
        args.contours_map_levels = args.contours_map_levels.split(spliter)


def mimic_gplot(args):
    """
    Translate a series of arguments of the old 'gplot.ncl' script to
    new fashion arguments.

    For most cases, this consists in changing 'args'
    For the remaining cases, this translates in returned dict 'settings'

    Currenty handles : title, trim, date, time, units, focus, vcb
    """

    settings = dict()

    cm = 1. / 2.54

    # if 'figsize' not in args.figure_options:
    #     args.figure_options['figsize'] = (30*cm, 30*cm)

    if 'dpi' not in args.figure_options:
        args.figure_options['dpi'] = 100

    # Change format of args.resolution, e.g. "800x1200"  -> (800,1200)
    resol = args.resolution
    if resol is not None and type(resol) is str:
        if re.fullmatch(r"[0-9]*x[0-9]*", resol):
            resol = tuple(resol.split("x"))
            print("resol=", resol)
        else:
            raise ValueError(
                "Issue with resolution %s. Standard format names are not supported" % resol)

    if 'figsize' not in args.figure_options:
        # Process resolution, the gplot way
        if args.format in ['pdf', 'eps']:
            if resol is None:
                # Ncl default (inches)
                args.figure_options['figsize'] = (8.5, 11.)
            else:
                # User should have provided values in inches
                args.figure_options['figsize'] = resol
        else:
            dpi = args.figure_options['dpi']
            if resol is None:
                # Ncl default is 1024*1024 pixels
                args.figure_options['figsize'] = (1250/dpi, 1250/dpi)
            else:
                # User should have provided values in pixels
                args.figure_options['figsize'] = (resol[0]/dpi, resol[1]/dpi)

    # Handle 'trim'
    if args.trim:
        args.savefig_options['bbox_inches'] = 'tight'
        # else just let what the caller may have set

    # Coastlines. Set it by default, and allow user to override default
    if 'coastlines' in args.axis_methods:
        if args.axis_methods['coastlines'] in [None, [None]]:
            args.axis_methods.pop('coastlines')
    else:
        args.axis_methods['coastlines'] = [{}]

    # Gridlines
    if 'gridlines' in args.axis_methods:
        if args.axis_methods['gridlines'] in [None, [None]]:
            args.axis_methods.pop('gridlines')
    else:
        args.axis_methods['gridlines'] = [{
            'draw_labels': {"bottom": "x", "left": "y"}}]

    #####################
    # Colors and levels
    #####################
    # A dictionnary of options for the colormap engine
    cdic = dict()
    #
    #
    if args.colored_map_cmap is not None:
        if "," in args.colored_map_cmap:
            # We have an explicit list of color names -> use contourf args 'colors'
            cdic['colors'] = args.colored_map_cmap.split(",")
            cdic['cmap'] = None
            # In that case contourf doesn't support vmin/vmax, nor 'norm'
            # and maybe needs 'levels'.
            if args.colored_map_min is not None or args.colored_map_max is not None:
                raise ValueError("Contourf doesn't support min/max when provided " +
                                 "with a list of colors. As a proxy, you may provide "
                                 "a value for list of levels (as a string with space separation)")
            # Next is not done automatically by contourf !
            if args.colored_map_levels is None:
                args.colored_map_levels = len(cdic['colors'])

        else:
            # A single string is a colormap name -> use contourf arg 'cmap'
            cdic['cmap'] = args.colored_map_cmap
            # We can handle either a list of levels, or min/max.
            # Contourf rather uses min/max (if provided)
            if args.colored_map_min is not None and args.colored_map_max is not None:
                cdic["vmin"] = args.colored_map_min
                cdic["vmax"] = args.colored_map_max
                if args.colored_map_delta is not None:
                    # Compute number of levels
                    levels = int(
                        (args.colored_map_max - args.colored_map_min) / args.colored_map_delta)
                    args.colored_map_levels = levels
    if debug:
        print("cdic=", cdic)
    args.colored_map_engine_options.update(**cdic)

    # contours = 1 allows to simply draw contours of the colored map field by
    # providing contours_map_levels (a check is done that no contours file is provided)
    if args.contours_map_levels is not None and \
       args.contours_map_file is None and \
       args.colored_map_file is not None):
        args.contours_map_file=args.colored_map_file
        args.contours_map_variable=args.colored_map_variable
        args.contours_map_transform=args.colored_map_transform
        args.contours_map_transform_options=args.colored_map_transform_options
        if args.contours_map_colors is None:
            args.contours_map_colors=args.colored_map_cmap


    # Focus
    if args.focus:
        if args.focus == 'ocean':
            feature='LAND'
        elif args.focus == 'land':
            feature='OCEAN'
        else:
            raise ValueError(
                f"Focus value {args.focus} is not an allowed value")
        if 'add_feature' not in args.axis_methods:
            args.axis_methods['add_feature']=[]
        args.axis_methods['add_feature'].append(
            {'feature': eval(f"cfeature.{feature}"), 'facecolor': 'white', 'zorder': 1})

    if args.scale:
        if args.colored_map_file is not None:
            args.colored_map_scale = args.scale
        elif args.contours_map_file is not None:
            args.contours_map_scale = args.scale
        else:
            raise ValueError(
                "Argument 'scale' can only be use with a colored map or a contours map")

    if args.offset:
        if args.colored_map_file is not None:
            args.colored_map_offset = args.offset
        elif args.contours_map_file is not None:
            args.contours_map_offset = args.offset
        else:
            raise ValueError(
                "Argument 'offset' can only be use with a colored map or a contours map")

    # Arg 'units' is handled directly in plot_colored_map

    if args.vcb is not None:
        if args.vcb is True:
            orient = 'vertical'
        else:
            orient = 'horizontal'
        args.colorbar_options['orientation'] = orient

    # Selections . See https://docs.xarray.dev/en/stable/user-guide/indexing.html#indexing
    if args.level is not None:
        if type(args.level) is int:
            method = 'isel'
        else:
            method = 'sel'
        # example of result { "isel": {"time": 0, "level" : 3} }
        for options in selection_options_list:
            if method not in options:
                options[method] = dict()
            options[method]['level'] = args.level

    if args.time is not None:
        if type(args.time) is int:
            method = 'isel'
        else:
            method = 'sel'
        for options in selection_options_list:
            if method not in options:
                options[method] = dict()
            options[method]['time'] = args.time

    if args.date is not None:
        date = args.date
        # Change e.g. 198501 to 1985-01
        if len(args.date) > 4 and args.date[4] != '-':
            date = args.date[0:4] + '-' + args.date[4:6]
            # Change e.g. 19850101 to 1985-01-01
            if len(args.date) > 6:
                date = date + '-' + args.date[6:]
        if debug:
            print("Selection with date=", date)
        for options in selection_options_list:
            if 'sel' not in options:
                options['sel'] = dict()
            options['sel']['time'] = date

    # Projection shorcuts
    if args.projection[0:2] in ['NH', 'SH']:
        print(
            "TBD : For proj == NHxx or SHxx, limit is not yet a circle. " +
            "This can be improved using that URL: " +
            "https://scitools.org.uk/cartopy/docs/latest/gallery/lines_and_polygons/always_circular_stereo.html")
        if len(args.projection) > 2:
            latitude_limit = float(args.projection[2:])
        if args.projection[0:2] == 'NH':
            args.projection = "NorthPolarStereo"
            settings['polar_stereo_extent'] = [-180, 180, latitude_limit, 90]
        if args.projection[0:2] == 'SH':
            args.projection = "SouthPolarStereo"
            settings['polar_stereo_extent'] = [-180, 180, -90, -latitude_limit]
        if args.projection_options is None:
            args.projection_options = dict()
        if "central_longitude" not in args.projection_options:
            args.projection_options["central_longitude"] = 0.0

    if args.xpolyline is not None and args.ypolyline is not None:
        x = args.xpolyline.split()
        y = args.ypolyline.split()
        if len(x) != len(y):
            raise ValueError(
                "xpolyline and ypolyline does not have the same length")
        plot_args = args.polyline_options.copy()
        plot_args['largs'] = [[float(X) for X in x], [float(Y) for Y in y]]
        if "plot" not in args.plt_methods:
            args.plt_methods["plot"] = []
        args.plt_methods["plot"].append(plot_args)

    return settings


if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()

    # selection_options_list is used in mimic_gplot
    selection_options_list = [args.colored_map_selection_options, args.contours_map_selection_options,
                              args.vectors_map_selection_options,
                              args.shaded_map_selection_options, args.shade2_map_selection_options]

    debug = args.debug

    # Apply heuristics which implements shortcuts in arguments
    heuristics(args)

    # Analyze arguments for compatibility with the old plot routine
    # gplot.ncl and translate it in changed args
    gplot_settings = mimic_gplot(args)

    # Plot the map
    plot_map(args, **gplot_settings)


# debug = True

# transform = find_ccrs("PlateCarree")

# variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
#     "/home/ssenesi/climaf_installs/climaf_running/examples/data/tos_Omon_CNRM_gn_185001-185003.nc",
#     "tos", ["y", "x"], transform, dict())

# create_norm(10, "RdBu", variable_data, None, None)
