import os
import json

import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

import cartopy
import cartopy.crs as ccrs
from cartopy.vector_transform import vector_scalar_to_grid as vector_to_grid
import geocat.viz as gv
import cmaps

from plotmap_parsing import create_parser, process_args, mimic_gplot


# -*- coding: utf-8 -*-

""" This script aims at plotting different fields on the same map, and
replacing/reproducing a former ploting script used in CliMAF,
gplot.ncl.  """

lefttitle = ""
righttitle = ""


def read_dataset(input_file, variable=None):
    with xr.open_dataset(input_file, decode_cf=True, decode_times=True,
                         decode_coords=True, decode_timedelta=True,
                         use_cftime=True) as ds:
        if variable is None:
            return ds
        else:
            return ds.__getattr__(variable)


def filter_dataset(dataset, dimensions, selection_options=dict()):
    if debug:
        print("Filter_dataset. selection_options=",
              selection_options, " dimensions=", dimensions)
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


def find_ccrs(crs_name, options=dict(), data_filename=None):
    """
    Returns a cartopy Coordinate Reference System based on its name and options.
    If CRS_NAME is a filename, first tries to find both CRS name and options
    in file's NetCDF metadata;
    Else, if CRS_NAME is None, tries the same with file DATA_FILENAME
    If both unsuccessful, return cartopy.crs.PlateCarree()
    """
    if debug:
        print("Find_ccrs with ", crs_name, options, data_filename)
    # First try to identify a file using first crs_name then data_filename
    fic = None
    if crs_name is not None and os.path.exists(crs_name):
        fic = crs_name
    elif crs_name is None and data_filename is not None and os.path.exists(data_filename):
        fic = data_filename

    # If there is a file, try yo get CRS from its metadata
    if fic is not None:
        crs_name, options = ccrs_from_metadata(fic)

    # Default CRS is PlateCarree
    if crs_name is None:
        # raise ValueError(
        #     "crs_name is None (can't deduce it from file %s)" % fic)
        return ccrs.PlateCarree()

    if debug:
        print("In find_ccrs, crs_name=", crs_name)

    if crs_name in ccrs.__dict__:
        return ccrs.__dict__[crs_name].__call__(**options)
    else:
        raise ValueError("Unknown coordinates reference system %s." % crs_name)


def ccrs_from_metadata(filename):
    """
    Returns a Cartopy's Coordinate Reference System name and options dict
    by analyzing NetCDF metadata, assuming it follows the CF convention at
    http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#appendix-grid-mappings

    Yet limited to the case of Lambert Conformal projection, as coded in Aladin model outputs.
    """
    ccrs_name = None
    ccrs_options = {}
    f = xr.open_dataset(filename)
    for attr in f.attrs:
        if 'lambert_conformal' in attr.lower():
            ccrs_name = 'LambertConformal'
            if 'longitude_of_central_meridian' in attr.lower():
                ccrs_options['central_longitude'] = float(f.attrs[attr][:-1])
            if 'latitude_of_projection_origin' in attr.lower():
                ccrs_options['central_latitude'] = float(f.attrs[attr][:-1])
            if 'standard_parallel' in attr.lower():
                ccrs_options['standard_parallels'] = (float(f.attrs[attr][:-1]),
                                                      float(f.attrs[attr][:-1]))
    return(ccrs_name, ccrs_options)


def fix_longitudes(lons):
    """
    Useful for e.g. ORCA grid : avoid discontinuity in longitudes due
    to 2*PI steps, in order that pcolormesh works fine
    """
    fixed_lons = lons.copy()
    for i, start in enumerate(np.argmax(np.abs(np.diff(lons)) > 180, axis=1)):
        fixed_lons[i, start+1:] += 360
    return fixed_lons


def compute_xy(lat2d, lon2d, projection, regular=False):
    """
    Compute args X and Y for matplotlib's contour-type functions,
    for a given PROJECTION and a grid with the given LAT2D
    and LON2D values

    X and Y units are coordinates on the projection plane

    If REGULAR is True, assume that the data are evenly spaced on
    the projection plane, which allows to speed up the process

    """
    if regular is False:
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
        xsize = lat2d.shape[1]
        ysize = lat2d.shape[0]
        if debug and False:
            print("0,0 -> ", first_point)
            print("-1 -1-> ", *last_point)
            print(
                f"x0={x0}, xm={xm}, y0={y0}, ym={ym}, xsize={xsize}, ysize={ysize}")
        X = np.linspace(x0, xm, xsize)
        Y = np.linspace(y0, ym, ysize)
        grid = np.meshgrid(X, Y)
        return grid


def get_variable_and_coordinates_from_dataset(
        input_file, variable, dimensions, projection,
        selection_options=list(), regular=False):
    """
    Main goals :
    - identify coordinates order based on heuristics (see horizontal_dimensions())
    - convert coordinates to projection space if they are 2D
    - add a cyclic point in longitude under some conditions
    - select data 

    If REGULAR is True, and when variable coordinates are 2D,
    values for coordinates are assumed to be regularly
    spaced between first and last points

    """
    # Check that the file exists
    if not os.path.isfile(input_file):
        raise ValueError("The input file %s does not exist" % input_file)
    variable_dataset = read_dataset(input_file, variable)
    if dimensions == ["auto"]:
        dimensions = horizontal_dimensions(variable_dataset.dims)
        if debug:
            print("Using horizontal dimensions :", dimensions)
    variable_dataset = filter_dataset(
        variable_dataset, dimensions, selection_options)

    # add cyclic point if one of the dimensions is a longitude and longitude range is ~ 360
    d0 = dimensions[0]  # Name of first dimension
    d0v = variable_dataset[dimensions[0]]  # Values for that dimension
    if d0 in ['lon', 'longitude', 'LON', 'Lon']:
        # Compute longitude range
        lon_range = d0v.max() % 360. - d0v.min() % 360.
        # add longitude grid increment
        delta = d0v[1] % 360. - d0v[0] % 360.
        lon_range = (lon_range + delta) % 360
        if lon_range > 359.9 or lon_range < 0.1:
            if debug:
                print("Adding cyclic longitude")
            variable_dataset = gv.xr_add_cyclic_longitudes(
                variable_dataset, d0)

    # Retrieve and possibly compute coordinates data
    variable_coordinates_data = list()
    coords = horizontal_dimensions(variable_dataset.coords)
    #
    if len(variable_dataset.coords[coords[0]].shape) == 2:
        # The variable has 2d coordinates
        # e.g. the case of Aladin LambertII projection, or Nemo ORCA grid,
        # which provides lat/lon as 2d-arrays indexed by grid variables
        if debug:
            print(f"Using 2D variables {coords} for computing X and Ys")
        lon2d = variable_dataset.coords[coords[0]]
        lat2d = variable_dataset.coords[coords[1]]
        X, Y = compute_xy(lat2d, lon2d, projection, regular)
        variable_coordinates_data.append(X)
        variable_coordinates_data.append(Y)
        #
    else:
        # Coordinates are 1D
        if debug:
            print(f"Coordinates ({dimensions}) are file variables")
        # dataset = read_dataset(input_file)
        for dim in dimensions:
            if debug:
                print("Adding coordinates data for ", dim)
            # variable_coordinates_data.append(dataset.variables[dim])
            variable_coordinates_data.append(variable_dataset[dim])
        #
    return variable_dataset, variable_coordinates_data


def horizontal_dimensions(dimensions):
    """
    Heuristics for identifying horizontal dimensions for
    a map, among a set of dimensions or coordinates
    TBD : should used CF convention for choosing horizontal dimensions
    """
    possible_pairs = [("lon", "lat"), ("LON", "LAT"),
                      ("longitude", "latitude"), ("Lon", "Lat"), ("y", "x"), ("i", "j")]
    for x, y in possible_pairs:
        if x in dimensions and y in dimensions:
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
    if type(nlevels) is list:
        nlevels = len(nlevels)
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
                     colorbar_options, print_time):
    if debug:
        print("\n\nPlotting colored map\n", 55*"-")
    # Find the transform
    if colored_map_transform != "do not remap":
        if debug:
            print("Using dedicated transform %s for interpreting colored map field")
            # colored_map_transform)
        transform = find_ccrs(colored_map_transform,
                              colored_map_transform_options,
                              colored_map_file)
    else:
        if debug:
            print("We won't remap")
        transform = projection

    # If user requested to avoid data remapping, this implies he knows
    # data is regularly spaced. This is used to speed up computing
    # coordinates on projection plane when lat and lon are 2D
    regular = False
    if colored_map_transform == "do not remap":
        regular = True

    # Find used data, and coordinates if needed
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        colored_map_file, colored_map_variable, coordinates, transform,
        colored_map_selection_options, regular)

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
        if not args.units:
            units = "?"
    if colored_map_offset:
        variable_data = variable_data + colored_map_offset
        if not args.units:
            units = "?"

    # Allow cmap name to refer to package 'cmaps' - see https://github.com/hhuangwx/cmaps
    try:
        colored_map_cmap = cmaps.__getattribute__(colored_map_cmap)
    except:
        pass

    # Prepare to plot the map
    contourf_args = dict(zorder=0, cmap=colored_map_cmap)
    contourf_args.update(colored_map_engine_options)
    if colored_map_levels is not None and 'levels' not in contourf_args:
        contourf_args['levels'] = colored_map_levels
    contourf_args["transform"] = transform
    #
    if colored_map_engine == "contourf":
        ploter = plt.contourf
        if colored_map_min is not None:
            contourf_args["vmin"] = colored_map_min
            if args.colored_map_cmap is not None and \
               type(colored_map_engine_options.get('colors', None)) is not list:
                variable_data = np.where(
                    variable_data > colored_map_min, variable_data, colored_map_min)
        if colored_map_max is not None:
            contourf_args["vmax"] = colored_map_max
            if args.colored_map_cmap is not None and \
               type(colored_map_engine_options.get('colors', None)) is not list:
                variable_data = np.where(
                    variable_data < colored_map_max, variable_data, colored_map_max)
    #
    elif colored_map_engine == 'pcolormesh':
        ploter = plt.pcolormesh
        contourf_args.pop('levels', None)
        contourf_args['norm'] = create_norm(colored_map_levels,
                                            colored_map_cmap, variable_data,
                                            colored_map_min, colored_map_max)
    else:
        raise ValueError("Unknown plot engine %s" % colored_map_engine)
    #
    if debug:
        print(f"Plotting with {colored_map_engine} ; and kwargs : ",
              contourf_args)
    if colored_map_transform == "do not remap" and ploter == plt.contour:
        ymin = np.min(variable_coordinates_data[1])
        ymax = np.max(variable_coordinates_data[1])
        xmin = np.min(variable_coordinates_data[0])
        xmax = np.max(variable_coordinates_data[0])
        contourf_args["extent"] = (xmin, xmax, ymin, ymax)
        if debug:
            print("Printing with no remapping, extent=",
                  contourf_args["extent"])
        colored_map_plot = ploter(variable_data, **contourf_args)
    else:
        colored_map_plot = ploter(
            *variable_coordinates_data, variable_data, **contourf_args)

    #
    for method in colored_map_methods:
        colored_map_plot.__getattr__(method).__call__(
            **colored_map_methods[method])

    # Colorbar. https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.colorbar
    if 'shrink' not in args.colorbar_options:
        if colorbar_options.get('orientation', 'vertical') == 'vertical':
            # TBD : improve colorbar shrink formula (doesn't account for titles vertical extent)
            xn, xx, yn, yx = ax.get_extent()
            if (xx - xn) > (yx - yn):
                args.colorbar_options['shrink'] = 0.8 * (yx - yn) / (xx - xn)
                if debug:
                    print('shrink :', xx, xn, yx, yn,
                          args.colorbar_options['shrink'])

    fig.colorbar(colored_map_plot, ax=ax, **colorbar_options)

    # Variable name as left title, time + units as right title.
    if timestamp is not None and print_time is True:
        units = timestamp + " / " + units

    return name, units


def plot_contours_map(ax, coordinates, contours_map_file, contours_map_variable,
                      contours_map_transform, contours_map_transform_options, projection,
                      contours_map_colors, contours_map_levels,
                      contours_map_selection_options, contours_map_engine_options,
                      contours_map_min, contours_map_max,
                      contours_map_scale, contours_map_offset):
    if debug:
        print("\n\nPlotting contours map\n", 55*"-")
    # Find the transform
    if contours_map_transform != "do not remap":
        transform = find_ccrs(contours_map_transform,
                              contours_map_transform_options,
                              contours_map_file)
    else:
        transform = projection

    # Find used data
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        contours_map_file, contours_map_variable, coordinates,
        transform, contours_map_selection_options)

    # Capture units,long_name and time before changing variable_data type
    if args.units:
        units = args.units
    else:
        units = variable_data.units
    try:
        name = variable_data.__getattr__('long_name')
    except:
        name = contours_map_variable

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
    if contours_map_levels is not None and 'levels' not in kwargs:
        kwargs['levels'] = contours_map_levels
    kwargs.update(contours_map_engine_options)
    if debug:
        print("Plotting with contour and args", kwargs)
    plt.contour(*variable_coordinates_data, variable_data, **kwargs)

    return name, units


def plot_shaded_map(ax, coordinates, shaded_map_file, shaded_map_variable,
                    shaded_map_transform, shaded_map_transform_options, projection,
                    shaded_map_hatches, shaded_map_levels, shaded_map_selection_options,
                    shaded_map_min, shaded_map_max,
                    shaded_map_scale, shaded_map_offset):
    if debug:
        print("\n\n Plotting shaded map\n", 55*"-")
    # Find the transform
    if shaded_map_transform != "do not remap":
        transform = find_ccrs(shaded_map_transform,
                              shaded_map_transform_options,
                              shaded_map_file)
    else:
        transform = projection
    # Find used data
    variable_data, variable_coordinates_data = get_variable_and_coordinates_from_dataset(
        shaded_map_file, shaded_map_variable, coordinates,
        transform, shaded_map_selection_options)

   # Capture units,long_name and time before changing variable_data type
    if args.units:
        units = args.units
    else:
        units = variable_data.units
    try:
        name = variable_data.__getattr__('long_name')
    except:
        name = shaded_map_variable

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
    plt.contourf(*variable_coordinates_data, variable_data,
                 shaded_map_levels, **kwargs)

    return name, units


def plot_vector_map(ax, coordinates, vectors_map_u_file, vectors_map_v_file,
                    vectors_map_u_variable, vectors_map_v_variable,
                    vectors_map_transform, vectors_map_transform_options, projection,
                    vectors_map_type, vectors_map_options, vectors_map_selection_options,
                    vectors_map_scale, vectors_map_gridsizes):
    if debug:
        print("\n\n Plotting vector map\n", 55*"-")
    # Find the transform
    if vectors_map_transform != "do not remap":
        transform = find_ccrs(vectors_map_transform,
                              vectors_map_transform_options,
                              vectors_map_u_file)
    else:
        transform = projection

    # Get the datasets and dimensions
    variable_u_data, variable_u_coordinates_data = get_variable_and_coordinates_from_dataset(
        vectors_map_u_file, vectors_map_u_variable, coordinates,
        transform, vectors_map_selection_options)
    variable_v_data, variable_v_coordinates_data = get_variable_and_coordinates_from_dataset(
        vectors_map_v_file, vectors_map_v_variable, coordinates,
        transform, vectors_map_selection_options)

    # Check that coordinates are the same
    if any([(ucoord != vcoord).any() for ucoord, vcoord in
            zip(variable_u_coordinates_data, variable_v_coordinates_data)]):
        raise ValueError(
            "Zonal and meridian component of the vector field must have same coordinates.")

    # Capture units,long_name and time before changing variable_data type
    if args.units:
        units = args.units
    else:
        units = variable_u_data.units
    try:
        name = variable_u_data.__getattr__('long_name')
    except:
        name = vectors_map_u_variable

    # Apply scale
    if vectors_map_scale:
        variable_u_data = variable_u_data * vectors_map_scale
        variable_v_data = variable_v_data * vectors_map_scale
        if not arg.units:
            units = "?"

    if type(vectors_map_gridsizes) is int:
        x0 = variable_u_coordinates_data[0].min()
        xm = variable_u_coordinates_data[0].max()
        coord_std_name = variable_u_coordinates_data[0].attrs.get(
            'standard_name', '')
        if coord_std_name == 'longitude':
            x0 = x0 % 360.
            xm = xm % 360.
        y0 = variable_u_coordinates_data[1].min()
        ym = variable_u_coordinates_data[1].max()
        # if variable_u_coordinates_data[0].
        ysize = int(float(vectors_map_gridsizes) * (ym - y0) / (xm - x0))
        sizes = (vectors_map_gridsizes, ysize)
    elif type(vectors_map_gridsizes) is list:
        sizes = tuple(vectors_map_gridsizes)
    else:
        raise ValueError(
            "Grid sizes muts be an int or a list of int : ", vectors_map_gridsizes)
    if debug:
        print("Vectors grid sizes : ", sizes)
    xp, yp, up, vp = vector_to_grid(transform, projection, sizes,
                                    *variable_u_coordinates_data,
                                    variable_u_data, variable_v_data)

    # Plot the map
    if vectors_map_type in dir(ax):
        ax.__getattribute__(vectors_map_type).__call__(xp, yp, up, vp,
                                                       **vectors_map_options)
        # Ci-dessous : marche pareil
        # ax.__getattribute__(vectors_map_type).__call__(xp, yp, up, vp,
        #         **vectors_map_options, transform=projection)
    else:
        raise ValueError("unknown vectors map type %s." % vectors_map_type)

    return name, units


def plot_map(args, polar_stereo_extent=None, print_time=False):
    # Get coordinates
    coordinates = args.coordinates

    # Deal with projection
    projection = find_ccrs(args.projection, args.projection_options)
    if debug:
        print("Map projection set to %s %s" %
              (args.projection, args.projection_options))

    # Initialize the plot
    fig = plt.figure(**args.figure_options)
    ax = plt.axes(projection=projection)
    if debug:
        print("extent=", ax.get_extent())

    titles_are_set = False

    # Axes methods
    for method in args.axis_methods:
        for kwargs in args.axis_methods[method]:
            largs = kwargs.pop('largs', [])
            if method == 'set_extent':
                # kwargs['crs'] = projection
                kwargs['extents'] = tuple(kwargs['extents'])
            if debug:
                print(f"Calling axis method {method} with kwargs: {kwargs}")
            ax.__getattribute__(method).__call__(*largs, **kwargs)
            if debug:
                print("extent=", ax.get_extent())

    # Plt methods
    for method in args.plt_methods:
        for kwargs in args.plt_methods[method]:
            largs = kwargs.pop('largs', [])
            if debug:
                print(f"Calling plt method {method} with kwargs: {kwargs}")
            plt.__getattribute__(method).__call__(*largs, **kwargs)

    # Deal with the colored map if needed
    if args.colored_map_file:
        name, units = plot_colored_map(fig=fig, ax=ax, coordinates=coordinates,
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
                                       print_time=print_time,
                                       )
        if not titles_are_set:
            lefttitle = name
            righttitle = units
            titles_are_set = True

    # Deal with the contours map if needed
    if args.contours_map_file:
        name, units = plot_contours_map(ax=ax,
                                        coordinates=coordinates,
                                        contours_map_file=args.contours_map_file,
                                        contours_map_variable=args.contours_map_variable,
                                        contours_map_transform=args.contours_map_transform,
                                        contours_map_transform_options=args.contours_map_transform_options,
                                        projection=projection,
                                        contours_map_colors=args.contours_map_colors,
                                        contours_map_levels=args.contours_map_levels,
                                        contours_map_selection_options=args.contours_map_selection_options,
                                        contours_map_engine_options=args.contours_map_engine_options,
                                        contours_map_min=args.contours_map_min,
                                        contours_map_max=args.contours_map_max,
                                        contours_map_scale=args.contours_map_scale,
                                        contours_map_offset=args.contours_map_offset,
                                        )
        if not titles_are_set:
            lefttitle = name
            righttitle = units
            titles_are_set = True

    # Deal with the shaded map if needed
    if args.shaded_map_file is not None:
        name, units = plot_shaded_map(ax=ax,
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
        if not titles_are_set:
            lefttitle = name
            righttitle = units
            titles_are_set = True

    # Deal with the shade2 map if needed
    if args.shade2_map_file is not None:
        name, units = plot_shaded_map(ax=ax,
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
        if not titles_are_set:
            lefttitle = name
            righttitle = units
            titles_are_set = True

    # Deal with the vector map if needed
    if args.vectors_map_u_file is not None and args.vectors_map_v_file is not None:
        name, units = plot_vector_map(ax=ax,
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
                                      vectors_map_gridsizes=args.vectors_map_gridsizes,
                                      )
        if not titles_are_set:
            lefttitle = name
            righttitle = units
            titles_are_set = True

    # Geocat-viz methods
    for method in args.gv_methods:
        for kwargs in args.gv_methods[method]:
            largs = kwargs.pop('largs', [])
            if debug:
                print(
                    f"Calling geocat.viz method {method} with kwargs: {kwargs}")
            gv.__getattribute__(method).__call__(ax, *largs, **kwargs)

    if polar_stereo_extent is not None:
        if debug:
            print("Setting extent to ", polar_stereo_extent)
        ax.set_extent(polar_stereo_extent, crs=ccrs.PlateCarree())

    # gv.add_major_minor_ticks(ax)
    # gv.add_lat_lon_ticklabels(ax)

    title_args = dict(lefttitle=lefttitle, righttitle=righttitle)
    title_args.update(args.title_options)
    gv.set_titles_and_labels(ax, **title_args)
    #
    if debug:
        print("extent=", ax.get_extent())

    # Deal with output
    output_file = args.output_file
    if output_file is not None:
        if debug:
            print("Calling savefig with options :", args.savefig_options)
        plt.savefig(output_file, **args.savefig_options)
    else:
        plt.show(block=True)


if __name__ == "__main__":
    # Parse the arguments
    args = create_parser().parse_args()

    debug = args.debug

    # Apply heuristics which implements shortcuts in arguments
    process_args(args)

    # selection_options_list is used in mimic_gplot
    selection_options_list = [args.colored_map_selection_options,
                              args.contours_map_selection_options,
                              args.vectors_map_selection_options,
                              args.shaded_map_selection_options,
                              args.shade2_map_selection_options]

    # Analyze arguments for compatibility with the old plot routine
    # gplot.ncl and translate it in changed args, and in a returned
    # dict of settings
    gplot_settings = mimic_gplot(args, selection_options_list)

    # Plot the map
    plot_map(args, **gplot_settings)
