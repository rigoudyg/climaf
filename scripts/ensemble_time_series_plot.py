#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------
# -- Interfacing the script with CliMAF: writing a command line taking arguments
# -- The associated CliMAF operation is:
#    cscript('ensemble_plot','python ensemble_plot.py --filenames="${mmin}" --outfig=${out}
#            --labels=\'\"${labels}\"\' ', format='png')
# -- Authors:
# -    Jerome Servonnat - LSCE
# -    Hugo Dayan - LSCE
# -
# - Contact: jerome.servonnat at lsce.ipsl.fr
# --------------------------------------------------------------------------------------------------

# -- For this, we use the python library argparse
# --------------------------------------------------------------------------------------------------
from __future__ import print_function, division, unicode_literals, absolute_import

import argparse

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from datetime import timedelta
try:
    from datetime import datetime as cdatetime
except:
    import datetime as cdatetime
import cftime
import numpy as np

# This use of netCDF4 should be changed to using xarray, for
# homogeneity with CliMAF main code
from netCDF4 import Dataset, num2date


# SS : Try to bypass use of netcdftime, which is not included in conda's NetCDF4, and
# which would like to avoid to add as a conda package
#
# from env.site_settings import atCerfacs, onCiclad
# if atCerfacs or onCiclad:
#     import netcdftime
# else:
#     try:
#         from netCDF4 import netcdftime
#     except:
#         import netcdftime


# -- Initialize the parser
# --------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Plot script for CliMAF that handles CliMAF ensemble')

# -- Describe the arguments you need
# --------------------------------------------------------------------------------------------------
# --> filenames = ${ins} in cscript
parser.add_argument('--filenames', action='store',
                    help='Netcdf files provided by CliMAF')
# --> labels = ${labels} (automatically provided by CliMAF in cscript)
parser.add_argument('--labels', action='store', default=None,
                    help='Labels (automatically provided by CliMAF) with ${labels} in cscript')
# --> outfig = ${out}
parser.add_argument('--outfig', action='store', default='fig.png',
                    help='path/filename of the output figure (png)')
parser.add_argument('--variable', action='store', default=None,
                    help='variable')
# --> colors = ${colors}
parser.add_argument('--colors', action='store', default=None,
                    help='colors separated by commas')
parser.add_argument('--lw', action='store', default=None,
                    help='lines thicknesses (commas separated)')
parser.add_argument('--alphas', action='store', default=None,
                    help='lines opacity (commas separated, 0 = transparent, 1=opac)')
parser.add_argument('--linestyles', action='store', default=None,
                    help='lines styles (https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html)')
parser.add_argument('--highlight_period', action='store', default=None,
                    help='Highlight a period on a time series (thicker line) ; provide the periods yearstart_yearend '
                         'separated by commas (Ex: 1980_2005,1990_2000 to highlight the first period on the first '
                         'dataset, and the second period on the second dataset)')
parser.add_argument('--highlight_period_lw', action='store', default=None,
                    help='Thickness of the highlighted period')
parser.add_argument('--min', action='store', default=None,
                    help='minimum value')
parser.add_argument('--max', action='store', default=None,
                    help='maximum value')
parser.add_argument('--offset', action='store', default="",
                    help='Offset')
parser.add_argument('--scale', action='store', default="",
                    help='Scale')
parser.add_argument('--x_axis', action='store', default='Real',
                    help='Use either real x axis, or force align')
parser.add_argument('--xlim', action='store', default='',
                    help='Provide the start date and end date to force the X axis. Ex: 1950-01-01,2005-12-31')
parser.add_argument('--ylim', action='store', default='',
                    help='Provide the interval for the Y axis')

parser.add_argument('--time_offset', action='store', default=None,
                    help='Add a time offset to the beginning of the time series')

parser.add_argument('--text', action='store', default="",
                    help='add some text in the plot; the user provides a triplet separared with commas x,y,text;'
                         ' separate the triplets with | if you want to provide multiple texts.'
                         ' Ex: x1,y1,text1|x2,y2,text2')
parser.add_argument('--text_fontsize', action='store', default="",
                    help='fontsize of the text (separate with commas if provide several')
parser.add_argument('--text_colors', action='store', default="",
                    help='color of the text (separate with commas if provide several')
parser.add_argument('--text_verticalalignment', action='store', default="",
                    help='Vertical alignment of the text (separate with commas if provide several')
parser.add_argument('--text_horizontalalignment', action='store', default="",
                    help='Horizontal alignment of the text (separate with commas if provide several')

parser.add_argument('--xlabel', action='store', default=None,
                    help='X axis label')
parser.add_argument('--ylabel', action='store', default=None,
                    help='Y axis label')
parser.add_argument('--xlabel_fontsize', action='store', default="",
                    help='X axis label size')
parser.add_argument('--ylabel_fontsize', action='store', default="",
                    help='Y axis label size')
parser.add_argument('--tick_size', action='store', default="",
                    help='Ticks size')

parser.add_argument('--fig_size', action='store', default="",
                    help='Size of the figure in inches => width*height Ex: 15*5')

parser.add_argument('--title', action='store', default=None,
                    help='Title')
parser.add_argument('--left_string', action='store', default=None,
                    help='Left string')
parser.add_argument('--right_string', action='store', default=None,
                    help='Right string')
parser.add_argument('--center_string', action='store', default=None,
                    help='Center string')
parser.add_argument('--title_fontsize', action='store', default="",
                    help='Title size')
parser.add_argument('--left_string_fontsize', action='store', default="",
                    help='Left string size')
parser.add_argument('--right_string_fontsize', action='store', default="",
                    help='Right string size')
parser.add_argument('--center_string_fontsize', action='store', default="",
                    help='Center string size')

parser.add_argument('--legend_colors', action='store', default='black',
                    help='leg_colors separated by commas')
parser.add_argument('--legend_labels', action='store', default=None,
                    help='Labels of the legend')
parser.add_argument('--legend_xy_pos', action='store', default=None,
                    help='x,y Position of the corner of the box (by default = upper left corner). Example= "1.02,1"')
parser.add_argument('--legend_loc', action='store', default=None,
                    help='Choose the corner of the legend box to specify the position of the legend box;'
                         ' by default 2 (upper left corner), take values 1, 2, 3 or 4'
                         ' (see resource loc of pyplot legend)')
parser.add_argument('--legend_fontsize', action='store', default=None,
                    help='Font size in the legend')
parser.add_argument('--legend_ncol', action='store', default=None,
                    help='Number of columns in the legend')
parser.add_argument('--legend_frame', action='store', default="False",
                    help='Draw the box around the legend? True/False')
parser.add_argument('--legend_lw', action='store', default=None,
                    help='Line widths (provide either one for all, or one by time series separated by commas')
parser.add_argument('--draw_legend', action='store', default='True',
                    help='Draw the legend? True/False')
parser.add_argument('--append_custom_legend_to_default', action='store', default='False',
                    help='Append the custom legend to the default one? True/False')

# -- Control margins
parser.add_argument('--left_margin', action='store', default=None,
                    help='Position of the left border of the figure in the plot')
parser.add_argument('--right_margin', action='store', default=None,
                    help='Position of the right border of the figure in the plot')
parser.add_argument('--bottom_margin', action='store', default=None,
                    help='Position of the bottom border of the figure in the plot')
parser.add_argument('--top_margin', action='store', default=None,
                    help='Position of the top border of the figure in the plot')


parser.add_argument('--horizontal_lines_values', action='store', default=None,
                    help='Y values for horizontal lines')
parser.add_argument('--horizontal_lines_styles', action='store', default=None,
                    help='Horizontal lines styles')
parser.add_argument('--horizontal_lines_lw', action='store', default=None,
                    help='Horizontal lines thickness')
parser.add_argument('--horizontal_lines_colors', action='store', default=None,
                    help='Horizontal lines colors')
parser.add_argument('--vertical_lines_values', action='store', default=None,
                    help='Y values for vertical lines')
parser.add_argument('--vertical_lines_styles', action='store', default=None,
                    help='vertical lines styles')
parser.add_argument('--vertical_lines_lw', action='store', default=None,
                    help='vertical lines thickness')
parser.add_argument('--vertical_lines_colors', action='store', default=None,
                    help='vertical lines colors')

# -- Default values
default_left_string_fontsize = 30.
default_title_fontsize = 30.
default_center_string_fontsize = 20.
default_right_string_fontsize = 20.
default_tick_size = 15.
default_xlabel_fontsize = 20.
default_ylabel_fontsize = 20.


# -- Retrieve the arguments in the script
# --------------------------------------------------------------------------------------------------
args, unknown = parser.parse_known_args()

filenames = args.filenames
outfig = args.outfig
labels = args.labels.replace('"', '')  # -- We remove the " from labels
#  -> the string ${labels} provided by CliMAF contains $. If we simply provide a string with $
#     to python, the $ and strings immediately following it are removed it to the string.
#     For instance: label_1$label_2$label_3 will be converted to _1_2_3
#     We thus need to pass '"label_1$label_2$label_3"' instead of label_1$label_2$label_3
#     This explains the specific syntax for labels in the cscript call (example line 5 of this script)
variable = args.variable
if args.min:
    mini = float(args.min)
if args.max:
    maxi = float(args.max)

offset = (float(args.offset) if args.offset else 0.)
scale = (float(args.scale) if args.scale else 1.)

print('==> args = ', args)


# -- We cut the strings to do python lists
# --------------------------------------------------------------------------------------------------
filenames_list = filenames.split(' ')
labels_list = labels.split('$')
# colors_list    = str.split(colors,',')

if args.highlight_period:
    highlight_period_list = args.highlight_period.split(',')
    if not len(filenames_list) == len(highlight_period_list):
        print('Provided ', len(filenames_list), ' time series and only ', len(highlight_period_list),
              ' periods to highlight')
        print('==> Discard highlighting')
        args.highlight_period = None


# --------------------------------------------------------------------------------------------------
# -- Plotting (here it's just a dummy plot to produce a result; otherwise CliMAF returns an error
# --------------------------------------------------------------------------------------------------


# -- Colors
if args.colors:
    colors = args.colors.split(',')
else:
    colors = ['royalblue', 'red', 'green', 'mediumturquoise', 'orange',
              'navy', 'limegreen', 'steelblue', 'fuchsia',
              'blue', 'goldenrod', 'yellowgreen', 'blueviolet', 'darkgoldenrod', 'darkgreen',
              'mediumorchid', 'lightslategray', 'gold', 'chartreuse', 'saddlebrown', 'tan',
              'tomato', 'mediumvioletred', 'mediumspringgreen', 'firebrick']

colors = colors + colors

# -- Line width
if args.lw:
    lw_list = args.lw.split(',')
    if len(lw_list) == 1:
        lw_list = lw_list * len(filenames_list)
else:
    lw_list = [1] * len(filenames_list)

# -- alphas
if args.alphas:
    alphas_list = str.split(args.alphas, ',')
    if len(alphas_list) == 1:
        alphas_list = alphas_list * len(filenames_list)
else:
    alphas_list = [1] * len(filenames_list)

# -- line styles
if args.linestyles:
    linestyles_list = str.split(args.linestyles, ',')
    if len(linestyles_list) == 1:
        linestyles_list = linestyles_list * len(filenames_list)
else:
    linestyles_list = ['solid'] * len(filenames_list)
for elt in linestyles_list:
    if '-' in elt:
        dumsplit = elt.split('-')
        print((0, tuple(map(int, dumsplit[1:len(dumsplit)]))))
        linestyles_list[linestyles_list.index(elt)] = (0, tuple(map(int, dumsplit[1:len(dumsplit)])))

if args.highlight_period_lw:
    highlight_period_lw_list = args.highlight_period_lw.split(',')
    if len(highlight_period_lw_list) == 1:
        highlight_period_lw_list = highlight_period_lw_list * len(filenames_list)
else:
    highlight_period_lw_list = [2.5] * len(filenames_list)


# -- Start plot
if args.fig_size:
    fig_width = float(args.fig_size.split('*')[0])
    fig_height = float(args.fig_size.split('*')[1])
    plt.figure(figsize=(fig_width, fig_height))
else:
    plt.figure(figsize=(15, 5))

# -- Plot the horizontal lines
if args.horizontal_lines_values:
    horizontal_lines_values_list = args.horizontal_lines_values.split(',')
    if args.horizontal_lines_lw:
        horizontal_lines_lw_list = args.horizontal_lines_lw.split(',')
    else:
        horizontal_lines_lw_list = [2] * len(horizontal_lines_values_list)
    if len(horizontal_lines_lw_list) == 1 and len(horizontal_lines_values_list) > 1:
        horizontal_lines_lw_list = horizontal_lines_lw_list * len(horizontal_lines_values_list)
    if args.horizontal_lines_colors:
        horizontal_lines_colors_list = args.horizontal_lines_colors.split(',')
    else:
        horizontal_lines_colors_list = ['black'] * len(horizontal_lines_values_list)
    if len(horizontal_lines_colors_list) == 1 and len(horizontal_lines_values_list) > 1:
        horizontal_lines_colors_list = horizontal_lines_colors_list * len(horizontal_lines_values_list)

    for ind in range(0, len(horizontal_lines_values_list)):
        hline_val = horizontal_lines_values_list[ind]
        plt.axhline(y=float(hline_val),
                    linewidth=horizontal_lines_lw_list[ind],
                    color=horizontal_lines_colors_list[ind])


# -- Loop on the netcdf files
handles_for_legend = []
dataset_number = 0
for pathfilename in filenames_list:
    dat = Dataset(pathfilename)
    test_dat = (dat.variables[variable][:]) * scale + offset
    #
    # -- Deal with time
    for dim in dat.dimensions:
        if dim.lower() in ['time', 'time_counter']:
            tname = dim
            break
    nctime = dat.variables[tname][:]
    t_unit = dat.variables[tname].units  # get unit  "days since 1950-01-01T00:00:00Z"
    if 'months' in t_unit:
        if len(nctime) == 12:
            x = np.array(range(1, 13))
            datevar = []
        else:
            orig_date = str(t_unit).split(' ')[2]
            orig_year = int(orig_date.split('-')[0])
            orig_month = int(orig_date.split('-')[1])
            orig_day = int(orig_date.split('-')[2][0:2])
            tvalue = [cdatetime(orig_year, orig_month, orig_day) +
                      timedelta(seconds=365.25 / 12 * 24.0 * 3600.0 * float(val)) for val in nctime]
            x = np.array(tvalue)
    else:
        try:
            t_cal = dat.variables[tname].calendar
        except AttributeError:  # Attribute doesn't exist
            t_cal = u"gregorian"  # or standard
        #
        #
        tvalue = num2date(nctime, units=t_unit, calendar=t_cal)
        datevar = []
        for elt in tvalue:
            if not isinstance(elt, cdatetime):
                # if isinstance(elt, (netcdftime._netcdftime.DatetimeNoLeap, netcdftime._netcdftime.Datetime360Day,
                # if isinstance(elt, (cftime.DatetimeNoLeap, cftime._cftime.DatetimeGregorian)):
                strdate = elt.strftime().split(' ')[0]
                year = int(strdate.split('-')[0])
                month = int(strdate.split('-')[1])
                day = int(strdate.split('-')[2])
                datevar.append(cdatetime(year, month, day))
            else:
                datevar.append(elt)
        print('datevar = ', datevar)
        #
        x = np.array(datevar)
        # x = np.array(datevar)[0,:]
        
    # y = test_dat[:,0,0]
    y = np.squeeze(test_dat)
    if len(y.shape) > 1:
        print("input data is not 1D")
    print('lw_list[dataset_number]', lw_list[dataset_number])
    print('colors[dataset_number]', colors[dataset_number])
    print('linestyles_list[dataset_number]', linestyles_list[dataset_number])
    print('alphas_list[dataset_number]', alphas_list[dataset_number])

    handles_for_legend.append(
        # plt.plot(x,y,lw=lw_list[filenames_list.index(pathfilename)], color=colors[filenames_list.index(pathfilename)],
        #     label=labels_list[filenames_list.index(pathfilename)])[0]
        plt.plot(x, y,
                 lw=int(lw_list[dataset_number]),
                 color=colors[dataset_number],
                 linestyle=linestyles_list[dataset_number],
                 alpha=float(alphas_list[dataset_number]),
                 label=labels_list[dataset_number])[0]
    )

    print('dataset_numb :', dataset_number)
    print('lw_list :', int(lw_list[dataset_number]))
    print('lw_list :', np.shape(lw_list))
    print('color :', colors[dataset_number])
    print('labels :', labels_list[dataset_number])
    print('nctime :', nctime[0])
    print('nctime :', np.shape(nctime))
    print('nctime :', type(nctime[0]))
    print('X :', x[0])
    print('X :', np.shape(x))
    print('X :', type(x[0]))
    print('Y :', int(y[0]))
    print('Y :', type(int(y[0])))

    # handles_for_legend.append(
    #    #plt.plot(x,y,lw=lw_list[filenames_list.index(pathfilename)], color=colors[filenames_list.index(pathfilename)],
    #    #     label=labels_list[filenames_list.index(pathfilename)])[0]
    #    #plt.plot(x,y,lw=int(lw_list[dataset_number]), color=colors[dataset_number],
    #    #     label=labels_list[dataset_number])[0]
    #    plt.plot(x,y,lw=lw_list[dataset_number], color=colors[dataset_number],
    #         label=labels_list[dataset_number])[0]
    # )

    #
    # -- Highlight the period used to compute the climatology
    if args.highlight_period:
        # highlight_period = highlight_period_list[filenames_list.index(pathfilename)]
        highlight_period = highlight_period_list[dataset_number]  # filenames_list.index(pathfilename)]
        sep = ('_' if '_' in highlight_period else '-')
        dum = highlight_period.split(sep)
        startyear = int(dum[0])
        endyear = int(dum[1])
        #
        ind = np.argwhere((x > cdatetime(startyear, 1, 1)) & (x < cdatetime(endyear, 12, 31))).flatten()
        print('highlight_period = ', highlight_period)
        print("highlight_period_lw_list[dataset_number] = ", highlight_period_lw_list[dataset_number])
        plt.plot(x[ind], y[ind],
                 lw=highlight_period_lw_list[dataset_number],
                 alpha=alphas_list[dataset_number],
                 linestyle=linestyles_list[dataset_number],
                 color=colors[dataset_number])
    #
    dataset_number = dataset_number + 1

# -- Add the grid
plt.grid()

# -- Force setting the X limits
if args.xlim:
    xlim_start_date = args.xlim.split(',')[0]
    xlim_end_date = args.xlim.split(',')[1]

    xlim_period = []
    for xlim_date in [xlim_start_date, xlim_end_date]:
        if len(xlim_date) == 4:
            x_date = cdatetime(int(xlim_date), 8, 1)
        else:
            x_text = xlim_date
            if '-' in x_text or '_' in x_text:
                sep_x = ('-' if '-' in x_text else '_')
                split_x = xlim_date.split(sep_x)
                if len(split_x) == 2:
                    x_date = cdatetime(int(split_x[0]), int(split_x[1]))
                elif len(split_x) == 3:
                    x_date = cdatetime(int(split_x[0]), int(split_x[1]), int(split_x[2]))
            elif len(x_text) == 6:
                x_date = cdatetime(int(x_text[0:4]), int(x_text[4:6]), 15)
            elif len(x_text) == 8:
                x_date = cdatetime(int(x_text[0:4]), int(x_text[4:6]), int(x_text[6:8]))
            else:
                print('--> Date provided as x value could not be interpreted: ', xlim_date)
        xlim_period.append(x_date)
    plt.xlim(xlim_period)

# -- Force setting the Y limits
if args.ylim:
    plt.ylim([float(args.ylim.split(',')[0]), float(args.ylim.split(',')[1])])


# -- Add the titles
if args.left_string:
    plt.title(args.left_string, loc='left',
              fontsize=(float(args.left_string_fontsize) if args.left_string_fontsize
                        else default_left_string_fontsize))

if args.center_string:
    plt.title(args.center_string, loc='center',
              fontsize=(float(args.center_string_fontsize) if args.center_string_fontsize
                        else default_center_string_fontsize))

right_string_fontsize = (float(args.right_string_fontsize)
                         if args.right_string_fontsize else default_right_string_fontsize)
if args.right_string:
    plt.title(args.right_string, loc='right', fontsize=right_string_fontsize)
else:
    plt.title('Variable = ' + variable, loc='right', fontsize=right_string_fontsize)

# -- X and Y axis labels
if args.xlabel:
    plt.xlabel(args.xlabel,
               fontsize=(float(args.xlabel_fontsize) if args.xlabel_fontsize else default_xlabel_fontsize))
if args.ylabel:
    plt.ylabel(args.ylabel,
               fontsize=(float(args.ylabel_fontsize) if args.ylabel_fontsize else default_ylabel_fontsize))

plt.tick_params(labelsize=(float(args.tick_size) if args.tick_size else default_tick_size))
#
# -- Draw legend by hand
draw_legend = (False if args.draw_legend.lower() in ['false'] else True)
if draw_legend:
    legend_xy_pos = (args.legend_xy_pos if args.legend_xy_pos else '1.02,1.')
    legend_loc = (args.legend_loc if args.legend_loc else '2')
    legend_fontsize = (args.legend_fontsize if args.legend_fontsize else '12')
    legend_ncol = (args.legend_ncol if args.legend_ncol else 1)
    legend_frame = (True if args.legend_frame.lower() in ['true'] else False)
    legend_colors_list = (args.legend_colors.split(',') if args.legend_colors else colors)
    leg_dict = dict(bbox_to_anchor=(float(legend_xy_pos.split(',')[0]), float(legend_xy_pos.split(',')[1])),
                    loc=int(legend_loc), borderaxespad=0., prop={'size': float(legend_fontsize)}, ncol=int(legend_ncol),
                    frameon=legend_frame)
    # -- If the user provides a custom list of legend labels
    if args.legend_labels:
        legend_labels_list = args.legend_labels.split(',')
        # if add_custom_legend_to_default:
        # -- Do we start a new legend or append to the existing one?
        legend_handles = (handles_for_legend if args.append_custom_legend_to_default.lower() in ['true'] else [])
        print('colors = ', colors)
        print('legend_colors_list = ', legend_colors_list)
        for legend_label in legend_labels_list:
            leg_ind = legend_labels_list.index(legend_label)
            handle_dict = dict(label=legend_label)
            handle_dict.update(dict(color=legend_colors_list[leg_ind]))
            legend_handles.append(mlines.Line2D([], [], **handle_dict))
        leg_dict.update(dict(handles=legend_handles))

    # !!!
    print('leg_dict = ', leg_dict)
    leg = plt.legend(**leg_dict)
    if args.legend_lw:
        legend_lw_list = args.legend_lw.split(',')
        if len(legend_lw_list) == 1:
            legend_lw_list = legend_lw_list * len(leg.legendHandles)
        if args.legend_labels and args.append_custom_legend_to_default.lower() in ['true']:
            if len(legend_lw_list) == len(legend_labels_list):
                legend_lw_list = [2] * len(filenames_list) + legend_lw_list
            if len(legend_lw_list) == (len(legend_labels_list) + 1):
                legend_lw_list = [legend_lw_list[0]] * len(filenames_list) + legend_lw_list[1:len(legend_lw_list)]

        # for legobj in leg.legendHandles:
        print('legend_lw_list = ', legend_lw_list)
        for ind in range(0, len(leg.legendHandles)):
            leg.legendHandles[ind].set_linewidth(float(legend_lw_list[ind]))

# -- Add some text
if args.text:
    text_list = args.text.split('|')
    text_fontsize_list = (args.text_fontsize.split(',') if args.text_fontsize else [12] * len(text_list))
    if len(text_fontsize_list) == 1 and len(text_list) > 1:
        text_fontsize_list = text_fontsize_list * len(text_list)
    text_colors_list = (args.text_colors.split(',') if args.text_colors else ['black'] * len(text_list))
    if len(text_colors_list) == 1 and len(text_list) > 1:
        text_colors_list = text_colors_list * len(text_list)
    text_verticalalignment_list = (args.text_verticalalignment.split(',') if args.text_verticalalignment
                                   else ['bottom'] * len(text_list))
    if len(text_verticalalignment_list) == 1 and len(text_list) > 1:
        text_verticalalignment_list = text_verticalalignment_list * len(text_list)
    text_horizontalalignment_list = (args.text_horizontalalignment.split(',') if args.text_horizontalalignment
                                     else ['left'] * len(text_list))
    if len(text_horizontalalignment_list) == 1 and len(text_list) > 1:
        text_horizontalalignment_list = text_horizontalalignment_list * len(text_list)
    for text_elt in text_list:
        text_ind = text_list.index(text_elt)
        # -- treatment of the x value = date
        x_text = text_elt.split(',')[0]
        if len(x_text) == 4:
            x_date = cdatetime(int(x_text))
        else:
            if '-' in x_text or '_' in x_text:
                sep_x = ('-' if '-' in x_text else '_')
                split_x = x_text.split(sep_x)
                if len(split_x) == 2:
                    x_date = cdatetime(int(split_x[0]), int(split_x[1]))
                elif len(split_x) == 3:
                    x_date = cdatetime(int(split_x[0]), int(split_x[1]), int(split_x[2]))
            elif len(x_text) == 6:
                x_date = cdatetime(int(x_text[0:4]), int(x_text[4:6]))
            elif len(x_text) == 8:
                x_date = cdatetime(int(x_text[0:4]), int(x_text[4:6]), int(x_text[6:8]))
            else:
                print('--> Date provided as x value could not be interpreted: ', x_text)
        # -- y
        y_text = float(text_elt.split(',')[1])
        # -- And text
        text = text_elt.split(',')[2]
        print('text_elt = ', text_elt)
        # -- Plot the text
        plt.text(x_date, y_text, text,
                 fontsize=text_fontsize_list[text_ind],
                 color=text_colors_list[text_ind],
                 verticalalignment=text_verticalalignment_list[text_ind],
                 horizontalalignment=text_horizontalalignment_list[text_ind]
                 )

# -- Control margins
left_margin = (args.left_margin if args.left_margin else '0.1')
right_margin = (args.right_margin if args.right_margin else '0.8')
bottom_margin = (args.bottom_margin if args.bottom_margin else '0.2')
top_margin = (args.top_margin if args.top_margin else '0.9')
plt.subplots_adjust(left=float(left_margin),
                    right=float(right_margin),
                    top=float(top_margin),
                    bottom=float(bottom_margin))

plt.savefig(outfig)
print(outfig)
