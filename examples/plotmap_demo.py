# # Demonstration of the new CLiMAF operator 'plotmap', dedicated to replace operator 'plot' , which backend script gplot.ncl is at threat due to Ncl maintenance announcements

# ## plotmap is backed by script plotmap.py which uses matplotlib, cartopy and geocat

from IPython.display import Image, display
from climaf.api import *

# Some CMIP data
data = fds(
    cpath + "/../examples/data/tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc")


# +
# Convenience functions
def currently_running_in_a_notebook():
    try:
        name = get_ipython().__class__.__name__
        if name == 'ZMQInteractiveShell':
            return True
        else:
            return False
    except:
        return False
    
def cshow(obj, drop=False):
    if drop :
        cdrop(obj)
    if currently_running_in_a_notebook():
        display(Image(cfile(obj)))
    else:
        climaf.api.cshow(obj)


# -

# More example data
dg = ds(project="example", simulation="AMIPV6ALB2G",
        variable="tas", period="1981", frequency="monthly")

# ## Basics

# For reference, a figure using the old script (gplot.ncl)
cshow(plot(data, title="Reference, using gplot.ncl"),True)

# Same with new script. Mapping values to colors is slightly different 
cshow(plotmap(data, title="Using plotmap"),True)

# One can easily tune the number of levels used
cshow(plotmap(data, title="hand-tuned levels #", levels=10),True)

# Changing the Reference longitude
cshow(plotmap(data, title="Changing the Reference longitude", 
              proj="PlateCarree", proj_options={"central_longitude":90},
             ),True)

# The part of the coordinates range shown is called the 'extent'
# You can change it, but you must specify longitudes that fits in central_longitude +/- 180°
# So, by default (i.e. central_longitude=180), that fits in  [ 0, 360 [
cshow(plotmap(data,axis_methods={'set_extent': {'extents': (0 , 90, -10, 30) }}),True)

# ## Title and other strings are managed by function [geocat.viz.util.set_titles_and_labels](https://geocat-viz.readthedocs.io/en/latest/user_api/generated/geocat.viz.util.set_titles_and_labels.html) wich uses arguments in 'title_options'

# Playing with title size
cshow(plotmap(data, title='Main title',
              title_options = {'maintitlefontsize':50}
             ),True)

# If you provide both 'main_title' in 'title_options' and 'title', the former prevails
cshow(plotmap(data, title='Main title',
              title_options = {'maintitle':'title_options prevails'}
             ),True)

# Controling upper left and right strings
cshow(plotmap(data, title='Main title',
              title_options = {
                  'lefttitle':'Left String',
                  'righttitle':'Right String',
                  'righttitlefontsize': 6,
              }
             ),True)

# Controling upper left and right strings
cshow(plotmap(data, title='Main title',
              title_options = {
                  'lefttitle':'Left String',
                  'righttitle':'Right String',
                  'righttitlefontsize': 6,
                  'subtitle':'Subtitle',
              }
             ),True)

# ## Playing with colors

# Play with number of colors
cshow(plotmap(data, levels=15),True)

# Choosing each color
mycolors = 'white,black,RoyalBlue,LightSkyBlue,PowderBlue,lightseagreen,PaleGreen,Wheat,Brown,Pink'
cshow(plotmap(data, color= mycolors),True)

# Choosing the mapping of values to colors
mycolors = 'white,black,RoyalBlue,LightSkyBlue,PowderBlue'
mylevels = '210,220,240,300,310'
cshow(plotmap(data, color= mycolors, levels=mylevels),True)

# 'colors' and levels" can also be python lists
mycolors = [ 'white' , 'black' , 'RoyalBlue' , 'LightSkyBlue' , 'PowderBlue' ]
mylevels = [210,220,240,300,310]
cshow(plotmap(data, color= mycolors, levels=mylevels),True)

# Adding contours between colored regions
mylevels = [210,220,240,290,300,310]
cshow(plotmap(data, levels=mylevels, contours=1),True)

# NCL colormaps are available
cshow(plotmap(data, color = 'helix'),True)

# How to change gridlines look
cshow(plotmap(data, axis_methods={
    'gridlines': { 'linewidths': 5, 'linestyles': 'dashed', 'draw_labels' : {"bottom": "x", "left": "y"}}}),
      True)

# To avoid smoothing, use colormap engine 'pcolormesh' 
cshow(plotmap(data, clre="pcolormesh"),True)

# ## Data selection

# Select on time index
cshow(plotmap(data, time=0, print_time=True),True)

# Again selection on time index, with different index value
cshow(plotmap(data, time=1, print_time=True),True)

# Selection on date
cshow(plotmap(data, date='185003', print_time=True),True)

# Selection by providing explicit 'selection options' arguments
cshow(plotmap(data, clrso={"isel" : {"time": 0}}, print_time=True),True)

# Again: selection by providing explicit 'selection options' argument
cshow(plotmap(data, clrso={'sel' : {'time': '1850-02'}}, print_time=True))

# ## Mimicking various gplot options/args

# Changing image size
cshow(plotmap(data, title="Changing image size", resolution="600x400"),True)

# Showing only a data range. Here is gplot.ncl reference
cshow(plot(data, min=210, max=250, delta=5, title="A range, with 'plot'"),True)

# Showing only a data range. Here is potmap version
cshow(plotmap(data, min = 210, max = 250, delta=5, title="A range, with 'plotmap'"),True)

# What if surrounding white space is left
cshow(plotmap(data,trim=False),True)

# Request an horizontal colorbar
cshow(plotmap(data,vcb=False),True)

# Focus plot on ocean
cshow(plotmap(data,focus='ocean'),True)

# Focus plot on land
cshow(plotmap(data,focus='land'),True)

# Apply offset and change displayed units accordingly
cshow(plotmap(data, offset=-273.15, units="C"),True)

# Polar stereo projection (yet with square limits)
cshow(plotmap(data,proj='NH70'),True)

# Polylines
cshow(plotmap(data,xpolyline="0 90",ypolyline="0 45", polyline_options={'color': 'blue'}),True)

# Nemo data :
nd = fds(cpath + "/../examples/data/tos_Omon_CNRM_gn_185001-185003.nc")
cshow(plotmap(nd),True)

# Filling the gaps near ORCA grid poles needs another plot engine  :
cshow(plotmap(nd, clre="pcolormesh"),True)

# ## Shading

# Representing binary fields using shading. 
# Binary field #1 is 5th plotmap arg, #2 is 6th arg
# shdh and shdh2 provides patterns for the binary values
dgsup=ccdo(dg, operator = "gec,282")
dginf=ccdo(dg, operator = "lec,252")
cshow(plotmap(dg, "", "", "", dgsup, dginf,
              shdh = [None, '/'], shd2h = [None, '+']),True)

# Shading, more dense
cshow(plotmap(dg, "", "", "", dgsup, dginf,
      shdh = [None, '///'], shd2h = [None, '+++']),True)

# ## Vectors

# Vector plots. Get data
ua = fds(cpath + "/../examples/data/uas_CNRM-CM6_sample.nc")
va = fds(cpath + "/../examples/data/vas_CNRM-CM6_sample.nc")

# Default vector representation type is 'quiver' (arrows)
# Vector components are args 3 and 4 of plotmap
cshow(plotmap("","",ua,va),True)

# ### Tuning vector grid size and arrows attributes. See [quiver doc](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html#matplotlib.pyplot.quiver) for more options (but don't play with args X,Y, u, v)

cshow(plotmap("","",ua,va,
              vecg=50, 
              veco={'color':'blue', 'headwidth':2.5, 'headlength':4}),
      True)

# Controling the map projection
cshow(plotmap("","",ua,va, proj="Mollweide"),True)

# ###  Another vector representation type is barbs. See [its doc](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.barbs.html#matplotlib.pyplot.barbs) for more options

cshow(plotmap("","",ua,va,vecty="barbs", vecg=40, veco={'length':3.5, 'barbcolor' : 'blue'},),True)

# ### The third vector representation type is streamlines. Here is the [doc](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.streamplot.html#matplotlib.pyplot.streamplot) for more options

cshow(plotmap("","",ua,va,vecty="streamplot", veco={'density' : 3 , 'linewidth': 0.7},),True)

# Superimposing colored map and streamplot
cshow(plotmap(dg,"",ua,va,
              vecty="streamplot",  
              veco={'density' : 3 , 'linewidth': 0.7},
              axis_methods={'set_extent': {'extents': (0. , 60, 0., 60.) }}
             ),True)

# ## Output formats

# Output in pdf format
f=cfile(plotmap(dg, format='pdf'))
print(f)
# ! display $f

# Output in eps format
f=cfile(plotmap(dg, format='eps'))
print(f)
# ! display $f

# Launching plotmap with format='show' uses 
# matplotlib.show(block=True), which pops up a window. 
# This works only outisde a Notebook 
cfile(plotmap(dg, format="show"))  

# ## Playing with projections, and using data on a rectangular projected grid

# Next data was generated on a grid that uses Lambert2 projection
l2 = fds(cpath + "/../examples/data/sfcWind_aladin_ext.nc")

# As a default, target projection is PlateCarree
# Plotmap scrutinizes file metadata for identifying data projection parameters
cshow(plotmap(l2),True)


# This plot engine option speeds up computaton, but may damage the plot
cshow(plotmap(l2, clreo={'transform_first':True}),True)

# We can request another target projection
cshow(plotmap(l2, proj="Stereographic"),True)

# We can explicitly specify data grid's projection parameters
# which is useful if data file metadata is missing or not 'understandable' by plotmap
transform = { 
    'clrt' : 'LambertConformal', 
    'clrto' : {
        'central_longitude' : 10,
        'central_latitude'  : 37,
        'standard_parallels' : (37,37),
    }
    }
cshow(plotmap(l2, **transform),True)


# Another way to explicitly specify data grid's projection parameters is 
# to provide a file which holds correct metadata
cshow(plotmap(l2, clrt=cfile(l2)),True)


# If we want to plot on the data grid, we have to describe it explicitly, 
# Here we use args 'proj' and 'proj_options', and pack them in a small dict
projection = { 
    'proj' : 'LambertConformal', 
    'proj_options' : {
        'central_longitude' : 10,
        'central_latitude'  : 37,
        'standard_parallels' : (37,37),
    }
    }
# Note : data will actually be remapped on its own grid (To be checked)
cshow(plotmap(l2, **projection),True)

# We can also describe target projection using a file with relevant metadata
cshow(plotmap(l2, proj=cfile(l2)),True)

# We can explictly request that the data is not remapped. But there is no watch dog here !
cshow(plotmap(l2, proj=cfile(l2), clrt="do not remap"),True)

# Still without remapping, and using another plot engine to 'see' data grid cells
cshow(plotmap(l2, proj=cfile(l2), clrt="do not remap", clre="pcolormesh"),True)

# Selecting the plot domain, using 'extents'
cshow(plotmap(l2, axis_methods={'set_extent': {'extents': (0 , 70, 20, 60) }}),True)

# ## Advanced features

# ### The methods of [cartopy.mpl.geoaxes.GeoAxes](https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.mpl.geoaxes.GeoAxes.html#cartopy-mpl-geoaxes-geoaxes) can be called using arg axis_methods
#

cshow(plotmap(dg, axis_methods={'coastlines': {'color': 'white'},
}),True)

cshow(plotmap(dg, axis_methods={'gridlines': {}}),True)

# Add feature (implictly from cartopy.feature) (tested with only a colored map)
cshow(plotmap(dg, axis_methods={
    'add_feature': {'feature': 'LAND', 'facecolor': 'black', 'zorder': 1}}))

# ### Also, [Geocat-viz methods](https://geocat-viz.readthedocs.io/en/latest/user_api/index.html) can be invoked using arg 'gv_method'

cshow(plotmap(dg, 
              gv_methods={'add_major_minor_ticks': { 
                              'labelsize':'small',
                              'x_minor_per_major':2
                              }
                         }),True)

# ### Some methods of [matplotlib.pyplot](https://matplotlib.org/stable/api/pyplot_summary.html#module-matplotlib.pyplot) can be called using arg plt_methods
#

cshow(plotmap(dg, plt_methods={
    'text': {'x':-120, 'y': 45, 's': 'mytext', 'horizontalalignment': 'left'}}))

