import six
import json
import argparse
import re
import numpy as np
import cartopy.feature


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


def create_parser():
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add colored map features
    colored_map_group = parser.add_argument_group(
        "colored_map", description="Arguments linked with colored map")
    colored_map_group.add_argument("--colored_map_file",
                                   help="File which content should be plotted as a colored map.",
                                   type=str, default=None)
    colored_map_group.add_argument("--colored_map_variable",
                                   help="Variable to be plotted on colored map",
                                   type=str, default=None)
    colored_map_group.add_argument("--colored_map_levels",
                                   help="Number or list of levels for the colored map regions",
                                   type=check_json_format, default=None)
    colored_map_group.add_argument("--colored_map_cmap",
                                   help="Colors list or colormap name to use for the colored map",
                                   type=check_json_format, default='"BlueDarkRed18"')
    colored_map_group.add_argument("--missing_value_color",
                                   help="Name of the color to use for representing the missing/fill value",
                                   type=check_json_format, default=None)
    colored_map_group.add_argument("--colored_map_transform",
                                   help="Coordinate system on which the colored map data is.",
                                   type=str, default=None)
    colored_map_group.add_argument("--colored_map_transform_options",
                                   help="Options of the coordinate system on which the colored map data is.",
                                   type=check_json_format, default=dict())
    colored_map_group.add_argument("--colored_map_selection_options",
                                   help="Options to be used to select data at some coordinate values if needed."
                                   "Expected format: dict with key=selection method and value=dict of args",
                                   type=check_json_format, default=dict())
    colored_map_group.add_argument("--colored_map_engine",
                                   help="Plot engine: can be set to 'pcolormesh'; default is 'contourf'",
                                   type=str, default="contourf")
    colored_map_group.add_argument("--colored_map_engine_options",
                                   help="Args for the plot engine",
                                   type=check_json_format, default=dict())
    colored_map_group.add_argument("--colored_map_min",
                                   help="Min value to plot on the colored map",
                                   type=float, default=None)
    colored_map_group.add_argument("--colored_map_max",
                                   help="Max value to plot on the colored map",
                                   type=float, default=None)
    colored_map_group.add_argument("--colored_map_delta",
                                   help="For the colored map, interval defining the number of levels/colors between min and max ",
                                   type=float, default=None)
    colored_map_group.add_argument("--colored_map_scale",
                                   help="Scale factor to apply to the colored map field",
                                   type=float, default=None)
    colored_map_group.add_argument("--colored_map_offset",
                                   help="Offset to apply to the colored map field",
                                   type=float, default=None)
    colored_map_group.add_argument("--colored_map_methods",
                                   help="A dict of the methods to call on colored map, dict values are the args key/values pairs",
                                   type=check_json_format, default=dict())
    colored_map_group.add_argument("--colorbar_options",
                                   help="Arguments dict for plt.colorbar()",
                                   type=check_json_format, default=dict())

    # Add contours map features
    contours_map_group = parser.add_argument_group(
        "contours_map", description="Arguments linked with contours map")
    contours_map_group.add_argument("--contours_map_file",
                                    help="File which content should be plotted as a contours map.",
                                    type=str, default=None)
    contours_map_group.add_argument("--contours_map_variable",
                                    help="Variable to be plotted on contours map",
                                    type=str, default=None)
    contours_map_group.add_argument("--contours_map_levels",
                                    help="List of levels for the contours",
                                    type=check_json_format, default=None)
    contours_map_group.add_argument("--contours_map_colors",
                                    help="Colors that should be used for the contours map",
                                    type=list, default=[])
    contours_map_group.add_argument("--contours_map_transform",
                                    help="Coordinate system on which the contours data is.",
                                    type=str, default=None)
    contours_map_group.add_argument("--contours_map_transform_options",
                                    help="Options of the coordinate system on which the contours data is.",
                                    type=check_json_format, default=dict())
    contours_map_group.add_argument("--contours_map_selection_options",
                                    help="Options to be used to select data at some coordinate values if needed."
                                    "Expected format: dict with key=selection method and value=dict of args",
                                    type=check_json_format, default=dict())
    contours_map_group.add_argument("--contours_map_engine_options",
                                    help="Args for the contour plot engine",
                                    type=check_json_format, default=dict())
    contours_map_group.add_argument("--contours_map_min",
                                    help="Min value to plot on the contours map",
                                    type=float, default=None)
    contours_map_group.add_argument("--contours_map_max",
                                    help="Max value to plot on the contours map",
                                    type=float, default=None)
    contours_map_group.add_argument("--contours_map_scale",
                                    help="Scale factor to apply to the contours map field",
                                    type=float, default=None)
    contours_map_group.add_argument("--contours_map_offset",
                                    help="Offset to apply to the contours map field",
                                    type=float, default=None)
    # Add shaded map features
    shaded_map_group = parser.add_argument_group(
        "shaded_map", description="Arguments linked with shaded map")
    shaded_map_group.add_argument("--shaded_map_file",
                                  help="File which content should be plotted as a shaded map.",
                                  type=str, default=None)
    shaded_map_group.add_argument("--shaded_map_variable",
                                  help="Variable to be plotted on shaded map",
                                  type=str, default=None)
    shaded_map_group.add_argument("--shaded_map_levels",
                                  help="List or number of levels of the shaded map color bar",
                                  type=check_json_format, default=1)
    shaded_map_group.add_argument("--shaded_map_hatches",
                                  help="Hatches that should be used for the shaded map",
                                  type=check_json_format, default=[None, "/"])
    shaded_map_group.add_argument("--shaded_map_transform",
                                  help="Coordinate system on which the shaded data is.",
                                  type=str, default=None)
    shaded_map_group.add_argument("--shaded_map_transform_options",
                                  help="Options of the coordinate system on which the shaded data is.",
                                  type=check_json_format, default=dict())
    shaded_map_group.add_argument("--shaded_map_selection_options",
                                  help="Options to be used to select data at some coordinate values if needed."
                                  "Expected format: dict with key=selection method and value=dict of args",
                                  type=check_json_format, default=dict())
    shaded_map_group.add_argument("--shaded_map_min",
                                  help="Min value to plot on the shaded map",
                                  type=float, default=None)
    shaded_map_group.add_argument("--shaded_map_max",
                                  help="Max value to plot on the shaded map",
                                  type=float, default=None)
    shaded_map_group.add_argument("--shaded_map_scale",
                                  help="Scale factor to apply to the shaded map field",
                                  type=float, default=None)
    shaded_map_group.add_argument("--shaded_map_offset",
                                  help="Offset to apply to the shaded map field",
                                  type=float, default=None)
    # Add shaded map features
    shade2_map_group = parser.add_argument_group(
        "shade2_map", description="Arguments linked with shade2 map")
    shade2_map_group.add_argument("--shade2_map_file",
                                  help="File which content should be plotted as a shade2 map.",
                                  type=str, default=None)
    shade2_map_group.add_argument("--shade2_map_variable",
                                  help="Variable to be plotted on shade2 map",
                                  type=str, default=None)
    shade2_map_group.add_argument("--shade2_map_levels",
                                  help="List or number of level of the shade2 map color bar",
                                  type=check_json_format, default=1)
    shade2_map_group.add_argument("--shade2_map_hatches",
                                  help="Hatches that should be used for the shade2 map",
                                  type=check_json_format, default=[None, "*"])
    shade2_map_group.add_argument("--shade2_map_transform",
                                  help="Coordinate system on which the shade2 data is.",
                                  type=str, default=None)
    shade2_map_group.add_argument("--shade2_map_transform_options",
                                  help="Options of the coordinate system on which the shade2 data is.",
                                  type=check_json_format, default=dict())
    shade2_map_group.add_argument("--shade2_map_selection_options",
                                  help="Options to be used to select data at some coordinate values if needed."
                                  "Expected format: dict with key=selection method and value=dict of args",
                                  type=check_json_format, default=dict())
    shade2_map_group.add_argument("--shade2_map_min",
                                  help="Min value to plot on the shade2 map",
                                  type=float, default=None)
    shade2_map_group.add_argument("--shade2_map_max",
                                  help="Max value to plot on the shade2 map",
                                  type=float, default=None)
    shade2_map_group.add_argument("--shade2_map_scale",
                                  help="Scale factor to apply to the shade2 map field",
                                  type=float, default=None)
    shade2_map_group.add_argument("--shade2_map_offset",
                                  help="Offset to apply to the shade2 map field",
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
    vectors_map_group.add_argument("--vectors_map_u_variable",
                                   help="Variable (u component) to be plotted on colored map",
                                   type=str, default=None)
    vectors_map_group.add_argument("--vectors_map_v_variable",
                                   help="Variable (v component) to be plotted on colored map",
                                   type=str, default=None)
    vectors_map_group.add_argument("--vectors_map_type",
                                   help="Type of vectors for the vector map",
                                   default="quiver", choices=["quiver", "barbs", "streamplot"])
    vectors_map_group.add_argument("--vectors_map_options",
                                   help="Options of the vector map.",
                                   type=check_json_format, default=dict())
    vectors_map_group.add_argument("--vectors_map_transform",
                                   help="Coordinate system on which the vectors data is.",
                                   type=str, default=None)
    vectors_map_group.add_argument("--vectors_map_transform_options",
                                   help="Options of the coordinate system on which the vectors data is.",
                                   type=check_json_format, default=dict())
    vectors_map_group.add_argument("--vectors_map_selection_options",
                                   help="Options to be used to select data at some coordinate values if needed."
                                   "Expected format: list of tuples (selection method, associated dict options)",
                                   type=check_json_format, default=dict())
    vectors_map_group.add_argument("--vectors_map_scale",
                                   help="Scale factor to apply to the vectors map field",
                                   type=float, default=None)
    vectors_map_group.add_argument("--vectors_map_gridsizes",
                                   help="Size(s) of the vectors grid",
                                   type=check_json_format, default=50)
    # Add generic features
    parser.add_argument("--coordinates",
                        help="Coordinates to be plotted. Useful only in tricky cases (e.g. not CF-compliant)",
                        type=list, default=["auto"])
    parser.add_argument("--projection",
                        help="The projection to be used for the map",
                        type=str, default=None)
    parser.add_argument("--projection_options",
                        help="The options of the projection to be used for the map",
                        type=check_json_format, default=None)
    parser.add_argument("--plt_methods", type=check_json_format, default=dict(),
                        help="Dict of pyplot methods to be called, with values = args dicts list")
    parser.add_argument("--axis_methods", type=check_json_format, default=dict(),
                        help="Dict of axis methods to be called, with values = args dicts list")
    parser.add_argument("--gv_methods", type=check_json_format, default=dict(),
                        help="Dict of Geocat.viz methods to be called, with values = args dicts list")
    parser.add_argument(
        "--output_file",
        help="Path of the output_file", default=None)
    parser.add_argument("--format",
                        help="Output format",
                        type=str, default="png")
    parser.add_argument("--figure_options",
                        help="Arguments for plt.figure()", type=check_json_format, default=dict())
    parser.add_argument("--savefig_options",
                        help="Arguments for plt.savefig()", type=check_json_format, default=dict())
    parser.add_argument("--title_options", help="Arguments for gv.set_titles_and_labels()",
                        type=check_json_format, default=dict())
    parser.add_argument("--debug",
                        help="To get some details",
                        type=bool, default=True)

    gplot_group = parser.add_argument_group(
        "gplot", description="Arguments reproducing those of gplot.ncl")
    gplot_group.add_argument("--title",
                             help="Title of the graphic", default=None)
    gplot_group.add_argument("--trim",
                             help="Crop the surrounding extra white space",
                             type=check_json_format, default=True)
    gplot_group.add_argument("--resolution",
                             help="Image size (in pixels for png, in inches for pdf and eps) e.g. '1200x800'",
                             type=str, default=None)
    gplot_group.add_argument("--dpi",
                             help="Resolution in dots per inch",
                             type=int, default=None)
    gplot_group.add_argument("--focus",
                             help="Should plot focus on ocean or land",
                             type=str, default=None, choices=['ocean', 'land'])
    gplot_group.add_argument("--scale",
                             help="Scale factor for colored map, else for contours map",
                             type=float, default=None)
    gplot_group.add_argument("--offset",
                             help="Offset for colored map, else for contours map",
                             type=float, default=None)
    gplot_group.add_argument("--units",
                             help="An alternate label for units (showing on top right)",
                             type=str, default=None)
    gplot_group.add_argument("--vcb",
                             help="Should we have a Vertical ColorBar",
                             type=check_json_format, default=None)
    gplot_group.add_argument("--time",
                             help="A time value (not a date) for selecting data. Use an integer for index (xarray's 'isel') and a float for value (xarray's 'sel')",
                             type=check_json_format, default=None)
    gplot_group.add_argument("--date",
                             help="A date for selecting data. e.g. 1850, 185001, 18500101, 1850-01 1850-01-01 ",
                             type=str, default=None)
    gplot_group.add_argument("--level",
                             help="A level for selecting data. Use an integer for index (xarray's 'isel') and a float for value (xarray's 'sel')",
                             type=float, default=None)
    gplot_group.add_argument("--print_time",
                             help="Should we print colored map field time attribute",
                             type=bool, default=False)
    gplot_group.add_argument("--xpolyline",
                             help="x or lon values for a line of points to draw (spaces separated)",
                             type=str, default=None)
    gplot_group.add_argument("--ypolyline",
                             help="y or lat values for a line of points to draw (spaces separated)",
                             type=str, default=None)
    gplot_group.add_argument("--polyline_options",
                             help="A dict of arguments to plot for drawing polyline",
                             type=check_json_format, default=dict(color='blue'))
    # gplot_group.add_argument("--", help="",
    #                         type=, default=)

    return (parser)


def process_args(args):
    # Transform or process arguments for implementing shortcuts
    # Also set sensible values for parameters if not set by user

    # Put args.format in savefig options (possibly overriding the value there)
    # This for consistency when used in CliMAF (hard-coded in CliMAF driver)
    args.savefig_options['format'] = args.format

    # We allow axis_methods and plt_methods values (kwargs) to be
    # dicts rather than dicts lists. Here, we normalize for that
    for methods in [args.axis_methods, args.plt_methods, args.gv_methods]:
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
                        dic['feature'] = eval(f"cartopy.feature.{feature}")
                else:
                    raise ValueError(
                        "axis_methods 'add_feature' does not include key 'feature' in its args  dic :",
                        dic)

    # Transform string-typed lists to a list for some args
    if type(args.colored_map_levels) is str:
        if "," in args.colored_map_levels:
            spliter = ","
        else:
            spliter = " "
        args.colored_map_levels = args.colored_map_levels.split(spliter)

    if type(args.contours_map_levels) is str:
        if "," in args.contours_map_levels:
            spliter = ","
        else:
            spliter = " "
        args.contours_map_levels = args.contours_map_levels.split(spliter)

    # Set some title font sizes, and put 'title', in 'title_options'
    if 'maintitle' not in args.title_options and args.title is not None:
        args.title_options['maintitle'] = args.title
    if 'maintitlefontsize' not in args.title_options:
        args.title_options['maintitlefontsize'] = 21
    if 'lefttitlefontsize' not in args.title_options:
        args.title_options['lefttitlefontsize'] = 15
    if 'righttitlefontsize' not in args.title_options:
        args.title_options['righttitlefontsize'] = 15

    # For map projection, translate symbolic names to relevant
    # projection info
    if args.projection == "colored" or args.projection == 'clr':
        if args.colored_map_transform is not None:
            args.projection = args.colored_map_transform
            args.projection_options = args.colored_map_transform_options
        else:
            args.projection = args.colored_map_file
    if args.projection == "contours" or args.projection == 'cnt':
        if args.contours_map_transform is not None:
            args.projection = args.contours_map_transform
            args.projection_options = args.contours_map_transform_options
        else:
            args.projection = args.contours_map_file
    if args.projection == "vectors" or args.projection == 'vec':
        if args.vectors_map_transform is not None:
            args.projection = args.vectors_map_transform
            args.projection_options = args.vectors_map_transform_options
        else:
            args.projection = args.vectors_map_u_file
    if args.projection == "shaded" or args.projection == 'shd':
        if args.shaded_map_transform is not None:
            args.projection = args.shaded_map_transform
            args.projection_options = args.shaded_map_transform_options
        else:
            args.projection = args.shaded_map_file
    if args.projection == "shade2" or args.projection == 'shd2':
        if args.shade2_map_transform is not None:
            args.projection = args.shade2_map_transform
            args.projection_options = args.shade2_map_transform_options
        else:
            args.projection = args.shade2_map_file


def mimic_gplot(args, selection_options_list):
    """
    Translate a series of arguments of the old 'gplot.ncl' script to
    plotmap.py arguments.

    For most cases, this consists in changing 'args'
    For the remaining cases, this translates in returned dict 'settings'

    Currenty handles : trim, date, time, units, focus, vcb
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
            resol = tuple([int(x) for x in resol.split("x")])
            if args.debug:
                print("resolution =", resol)
        else:
            raise ValueError(
                "Issue with resolution %s. (Note : standard format names are not supported)" % resol)

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
                args.figure_options['figsize'] = (1250 / dpi, 1250 / dpi)
            else:
                # User should have provided values in pixels
                args.figure_options['figsize'] = (resol[0] / dpi, resol[1] / dpi)

    # Handle 'trim'
    if args.trim:
        args.savefig_options['bbox_inches'] = 'tight'
        # else just let what the caller may have set

    if 'gridlines' not in args.axis_methods:
        args.axis_methods['gridlines'] = \
            [dict(draw_labels={"bottom": "x", "left": "y"}, alpha=0.1,)]

    # Projection shorcuts
    if args.projection is not None and args.projection[0:2] in ['NH', 'SH']:
        print(
            "TBD : For proj == NHxx or SHxx, limit is not yet a circle. " +
            "This can be improved using that URL: " +
            "https://scitools.org.uk/cartopy/docs/latest/gallery/lines_and_polygons/always_circular_stereo.html")
        if len(args.projection) > 2:
            latitude_limit = float(args.projection[2:])
        ranges_dict = dict(lon_range=[-180, 180])
        if args.projection[0:2] == 'NH':
            args.projection = "NorthPolarStereo"
            ranges_dict['lat_range'] = [latitude_limit, 90]
            settings['polar_stereo_extent'] = [-180, 180, latitude_limit, 90]
        if args.projection[0:2] == 'SH':
            args.projection = "SouthPolarStereo"
            # Sign for latitude of pole is awkward, but that's the gv convention !
            ranges_dict['lat_range'] = [-latitude_limit, 90]
            settings['polar_stereo_extent'] = [-180, 180, -90, -latitude_limit]
        args.gv_methods['set_map_boundary'] = [ranges_dict]

        if args.projection_options is None:
            args.projection_options = dict()
        if "central_longitude" not in args.projection_options:
            args.projection_options["central_longitude"] = 0.0
        if 'gridlines' not in args.axis_methods:
            args.axis_methods['gridlines'] = [dict(draw_labels=True, linestyle="--",
                                                   color='black', alpha=0.5)]

    if args.projection_options is None:
        if args.projection is None:
            args.projection = "PlateCarree"
            args.projection_options = {'central_longitude': 180.}
        else:
            args.projection_options = {}

    # Coastlines. Set it by default, and allow user to override default
    if 'coastlines' not in args.axis_methods:
        args.axis_methods['coastlines'] = [{}]
    else:
        if args.axis_methods['coastlines'] in [None, [None]]:
            args.axis_methods.pop('coastlines')

    # Ticks 'a la Ncl'. Set it by default, and allow user to override default
    if 'add_major_minor_ticks' not in args.gv_methods:
        args.gv_methods['add_major_minor_ticks'] = [{'labelsize': 'large'}]
    else:
        if args.gv_methods['add_major_minor_ticks'] in [None, [None]]:
            args.gv_methods.pop('add_major_minor_ticks')

    #####################
    # Colors and levels
    #####################
    # A dictionnary of options for the colormap engine
    cdic = dict()
    #
    #
    if args.colored_map_cmap is not None:
        if "," in args.colored_map_cmap or type(args.colored_map_cmap) is list:
            # We have an explicit list of color names -> use contourf args 'colors'
            if "," in args.colored_map_cmap:
                cdic['colors'] = args.colored_map_cmap.split(",")
            else:
                cdic['colors'] = args.colored_map_cmap
            cdic['cmap'] = None
            # In that case contourf doesn't support vmin/vmax, nor 'norm'
            # and maybe needs 'levels'.
            if args.colored_map_min is not None or args.colored_map_max is not None:
                raise ValueError("Contourf doesn't support min/max when provided " +
                                 "with a list of colors. As a proxy, you may provide " +
                                 "a list of levels")
            # Next is not done automatically by contourf !
            if args.colored_map_levels is None:
                args.colored_map_levels = len(cdic['colors'])

        else:
            # A single string is a colormap name -> use contourf arg 'cmap'
            cdic['cmap'] = args.colored_map_cmap
            # if args.colored_map_levels is None:
            #     # TBD : diagnose levels number from cmap name
            #     args.colored_map_levels = 50
            # We can handle either a list of levels, or min/max.
            # Contourf rather uses min/max (if provided)
            if args.colored_map_min is not None and args.colored_map_max is not None:
                # cdic["vmin"] = args.colored_map_min
                # cdic["vmax"] = args.colored_map_max
                if args.colored_map_delta is not None:
                    args.colored_map_levels = list(np.arange(
                        args.colored_map_min,
                        args.colored_map_max + args.colored_map_delta,
                        args.colored_map_delta))
                    cdic['levels'] = args.colored_map_levels

    if args.debug:
        print("Colors/levels options for colormap engine=", cdic)
    args.colored_map_engine_options.update(**cdic)

    # Contours
    #############

    if 'linewidths' not in args.contours_map_engine_options:
        args.contours_map_engine_options['linewidths'] = 0.4

    if len(args.contours_map_colors) == 0:
        args.contours_map_colors = ['black']  # args.colored_map_cmap

    # arg 'contours_map_level' (or 'contours')' allows to simply draw
    # contours of the COLORED map field by providing
    # contours_map_levels (a check is done that no contours file is
    # provided)
    use_colored_map_file_for_contours = False
    if args.contours_map_levels is not None and \
       args.contours_map_file is None and \
       args.colored_map_file is not None:
        use_colored_map_file_for_contours = True
        args.contours_map_file = args.colored_map_file
        args.contours_map_variable = args.colored_map_variable
        args.contours_map_transform = args.colored_map_transform
        args.contours_map_transform_options = args.colored_map_transform_options
        args.contours_map_selection_options = args.colored_map_selection_options
        if args.contours_map_levels == 1 and args.colored_map_levels is not None:
            args.contours_map_levels = args.colored_map_levels
        if args.debug:
            print('Using colored_map_file for contours, levels=',
                  args.contours_map_levels, '  colors=', args.contours_map_colors)

    # Focus
    if args.focus:
        if args.focus == 'ocean':
            feature = 'LAND'
        elif args.focus == 'land':
            feature = 'OCEAN'
        else:
            raise ValueError(
                f"Focus value {args.focus} is not an allowed value")
        if 'add_feature' not in args.axis_methods:
            args.axis_methods['add_feature'] = []
        args.axis_methods['add_feature'].append(
            {'feature': eval(f"cartopy.feature.{feature}"), 'facecolor': 'silver', 'zorder': 1})

    if args.scale:
        if args.colored_map_file is not None:
            args.colored_map_scale = args.scale
        elif args.contours_map_file is not None:
            args.contours_map_scale = args.scale
        else:
            raise ValueError(
                "Argument 'scale' can only be use with a colored map or a contours map")
        if use_colored_map_file_for_contours:
            args.contours_map_scale = args.scale

    if args.offset:
        if args.colored_map_file is not None:
            args.colored_map_offset = args.offset
        elif args.contours_map_file is not None:
            args.contours_map_offset = args.offset
        else:
            raise ValueError(
                "Argument 'offset' can only be use with a colored map or a contours map")
        if use_colored_map_file_for_contours:
            args.contours_map_offset = args.offset

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
        if args.debug:
            print("Selection with date=", date)
        for options in selection_options_list:
            if 'sel' not in options:
                options['sel'] = dict()
            options['sel']['time'] = date

    if args.xpolyline is not None and args.ypolyline is not None:
        x = args.xpolyline
        if ' ' in args.xpolyline:
            x = x.split()
        y = args.ypolyline
        if ' ' in args.ypolyline:
            y = y.split()
        if len(x) != len(y):
            raise ValueError(
                "xpolyline and ypolyline does not have the same length")
        plot_args = args.polyline_options.copy()
        plot_args['largs'] = [[float(X) for X in x], [float(Y) for Y in y]]
        if "plot" not in args.plt_methods:
            args.plt_methods["plot"] = []
        args.plt_methods["plot"].append(plot_args)

    settings['print_time'] = args.print_time

    return settings
