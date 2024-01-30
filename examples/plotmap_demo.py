from IPython.display import Image, display
from climaf.api import *
#lcmn
#export PROJ_DATA=/net/nfs/tools/Users/SU/jservon/spirit-2021.11_envs/20230904/share/proj
#export PYPROJ_GLOBAL_CONTEXT = ON
#~/climaf_installs/climaf_running/bin/climaf


# +
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

data = fds(
    cpath + "/../examples/data/tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc")

# ## Basics

# For reference, a figure using the old script (gplot.ncl)
cshow(plot(data, title="Reference, using gplot.ncl"),True)

# Same with new script. Mapping values to colors is slightly different 
cshow(plotmap(data, title="Using plotmap"),True)

# Changing the Reference longitude
cshow(plotmap(data, title="Changing the Reference longitude", 
              proj="PlateCarree", proj_options={"central_longitude":90},
             ),True)

# One can easily tune the number of levels used
cshow(plotmap(data, title="hand-tuned levels #", levels=10),True)

# The part of the coordinates range shown is called the 'extent'
# You can change it, but you must specify longitudes that fits in central_longitude +/- 180°
# So, by default (i.e. central_longitude=180), that fits in  [ 0, 360 [
cshow(plotmap(data,axis_methods={'set_extent': {'extents': (0 , 90, -10, 30) }}),True)

# ## Playing with colors

# Play with number of colors
cshow(plotmap(data, clrl=15))

mycolors = 'white,black,RoyalBlue,LightSkyBlue,PowderBlue,lightseagreen,PaleGreen,Wheat,Brown,Pink'
cshow(plotmap(data, color= mycolors),True)

mycolors = 'white,black,RoyalBlue,LightSkyBlue,PowderBlue'
mylevels = '210,220,240,300,310'
cshow(plotmap(data, color= mycolors, levels=mylevels),True)

mycolors = 'white,black,RoyalBlue,LightSkyBlue,PowderBlue'
mylevels = [210,220,240,300,310]
cshow(plotmap(data, color= mycolors, levels=mylevels),True)

clog('warning')
mycolors = 'white,black,RoyalBlue,LightSkyBlue,PowderBlue'
mylevels = [210,220,240,300,310]
cshow(plotmap(data, color= mycolors, levels=mylevels, contours=1),True)

cshow(plotmap(data, color= mycolors, colors=mylevels),True)

cshow(plotmap(data, color = 'helix'),True)

# Using Ncl colormaps
cshow(plotmap(nd, clrmap="helix"))

cshow(plotmap(data, axis_methods={
    'gridlines': { 'linewidths': 5, 'linestyles': 'dashed', 'draw_labels' : {"bottom": "x", "left": "y"}}}),
      True)

cshow(plotmap(data, clre="contourf"),True)

# ## Data selection

# Select on time index
cshow(plotmap(data, time=0, print_time=True),True)

# Again selection on time index, with different index value
cshow(plotmap(data, time=1, print_time=True),True)

# Selection on date
cshow(plotmap(data, date='185003', print_time=True),True)

# Selection by providing explicit 'selection options' argument
cshow(plotmap(data, clrso=[["isel", {"time": 0}]]))

# Again: selection by providing explicit 'selection options' argument
cshow(plotmap(data, clrso=[['sel', {'time': ' 1850-01'}]]))

# ## Mimicking gplot

# Changing image size
cshow(plotmap(data, title="Using plotmap", resolution="600x400"),True)

# Showing only a data range. Here is gplot.ncl reference
cshow(plot(data, min=210, max=250, delta=5),True)

# Showing only a data range. Here is potmap version
cshow(plotmap(data, min = 210, max = 250, delta=5),True)

cshow(plotmap(data,trim=False),True)

# Request an horizontal colorbar
cshow(plotmap(data,vcb=False),True)

# Focus plot on ocean
cshow(plotmap(data,focus='ocean'),True)

# Focus plot on land
cshow(plotmap(data,focus='land'),True)

# Apply offset and change displayed units accordingly
cshow(plotmap(data,offset=-273.15, units="C"),True)

# Polar stereo projection (yet with square limits)
cshow(plotmap(data,proj='NH70'),True)

# Polylines
cshow(plotmap(data,xpolyline="0 90",ypolyline="0 45", polyline_options={'color': 'red'}),True)

# ## Playing with projections

# Next data was generated on a grid that uses Lambert2 projection
l2 = fds(cpath + "/../examples/data/sfcWind_aladin_ext.nc")

# As a default, target projection is PlateCarree
# Plotmap scrutinizes file metadata for identifying data projection parameters
cshow(plotmap(l2),True)


# Changing the colored map engine
cshow(plotmap(l2,clre="pcolormesh"),True)

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
# using args 'proj' and 'proj_options'. We pack them in a small dict
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

# We can also describe target projetion using a file
cshow(plotmap(l2, proj=cfile(l2)),True)

# Same without data remapping.
cshow(plotmap(l2, proj=cfile(l2), clrt="do not remap"),True)

# 
cshow(plotmap(l2, axis_methods={'set_extent': {'extents': (-60 , 90, -20, 70) }}),True)

# 
cshow(plotmap(l2, axis_methods={'set_extent': {'extents': (-20 , 80, -20, 70) }},
             proj="PlateCarree", proj_options={'central_longitude' : 180}),True)

# time(cshow(plotmap(l2, proj="LambertII", proj_options=[ 10, 37, 37], clre="contourf")))
# Wall time: 8.82 s
# time(cshow(plotmap(l2, proj="LambertII", proj_options=[ 10, 37, 37], clre="contourf", clrt="do not remap")))
# Wall time: 7.48 s


# Nemo data :
nd = fds(cpath + "/../examples/data/tos_Omon_CNRM_gn_185001-185003.nc")
cshow(plotmap(nd),True)

# Filling the gaps near ORCA grid poles needs another plot engine  :
cshow(plotmap(nd, clre="pcolormesh"),True)

# Example data
dg = ds(project="example", simulation="AMIPV6ALB2G",
        variable="tas", period="1981", frequency="monthly")

cfile(plotmap(dg))
cfile(plotmap(dg, format="show"))  # Use plt.show(block=True)

#
cfile(plotmap(dg, format='pdf'))  # cshow problématique
cfile(plotmap(dg, format='eps'))  # cshow problématique

# Axis_methods
cshow(plotmap(dg, axis_methods={
    'coastlines': {'color': 'grey'},
    'gridlines': {}
}))

# Add feature (implictly from cartopy.feature) (tested with only a colored map)
cshow(plotmap(dg, axis_methods={
    'add_feature': {'feature': 'LAND', 'facecolor': 'black', 'zorder': 1}}))

# Pyplot_methods
# Title, called only once
cshow(plotmap(dg, plt_methods={
    'title': {'label': "mytitle", 'loc': 'right'}}))

# Title, with a list of calls
cshow(plotmap(dg, plt_methods={
    'title': [
        {'label': "mytitle", 'loc': 'right'},
        {'label': "my left title", 'loc': 'left'}
    ]
}))

# For pyplot methods with non-keyword args, such as 'plot', use keyword 'largs'
cshow(plotmap(data, plt_methods={
    'plot': [{'largs': [[0, 90], [0, 45]], 'color': 'blue', 'marker': 'o'}]
}),True)


cshow(plotmap(dg, plt_methods={
    'text': {'x':-120, 'y': 45, 's': 'mytext', 'horizontalalignment': 'left'}}))


# ## Shading

# Shading
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

cshow(plotmap("","",ua,va),True)

# Default vector type is 'quiver'
cshow(plotmap("","",ua,va),True)

# Tuning vector grid size and arrows attributes
cshow(plotmap("","",ua,va,
              vecg=50, 
              veco={'color':'blue', 'headwidth':2.5, 'headlength':4}),
      True)

cshow(plotmap("","",ua,va, proj="Mollweide", vect="PlateCarree"),True)

# +

cshow(plotmap("","",ua,va,vecty="barbs", vecg=40, veco={'length':3.5, 'barbcolor' : 'blue'},),True)

# +

cshow(plotmap(data,"",ua,va,vecty="barbs", vecg=40, veco={'length':3.5, 'barbcolor' : 'blue'},),True)
# -

# Ploting stremalines yet has a bug re. western longitudes
cshow(plotmap("","",ua,va,vecty="streamplot", veco={'density' : 3 , 'linewidth': 0.7},),True)

# Ploting stremalines yet has a bug re. western longitudes
cshow(plotmap("","",ua,va,
              vecty="streamplot",  
              veco={'density' : 3 , 'linewidth': 0.7},
              axis_methods={'set_extent': {'extents': (-180. , 180, -70., 70.) }}
             ),True)

# +

cshow(plotmap(data,"",ua,va,vecty="streamplot",  veco={'density' : 3 , 'linewidth': 0.7}),True)
# -

# ## Development

import xarray as xr

f=xr.open_dataset(cpath + "/../examples/data/sfcWind_aladin_ext.nc")

import xarray as xr

f=xr.open_dataset(cpath + "/../examples/data/tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc")

f.tas.__getattr__('long_name')

dir(f.tas)

f.tas.__getattribute__('isel')

if 'time' in f.tas.isel(time=0).coords:
    print(f.tas.isel(time=0).time.values)

t=f.tas.isel(time=0).time

t.values

a=plot(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),
     title='1 field cross-section (without contours lines)',
     xpolyline='-60.0, -30.0, -30.0, -60.0, -60.0',
     y='log',
     ypolyline='70.0, 70.0, 50.0, 50.0, 70.0')
cshow(a,True)

a=plot(ds('example|AMIPV6ALB2G|tas|1980|global|monthly'),
       llbox(ds('example|AMIPV6ALB2G|tas|1980|global|monthly'),
             latmax=80,latmin=30,lonmax=120,lonmin=60),
       ds('example|AMIPV6ALB2G|uas|1980|global|monthly'),
       ds('example|AMIPV6ALB2G|vas|1980|global|monthly'),
       date=19800131,level=10.0,title='Selecting level and time close to 10 and 19800131 respectively',
       vcRefLengthF=0.02,vcRefMagnitudeF=11.5)
cshow(a,True)



cshow(curves(space_average(ds('example|AMIPV6ALB2G|tas|1980-1981|global|monthly')),title='AMIPV6'), True)

from IPython.display import Image, display
from climaf.api import *
#lcmn
#export PROJ_DATA=/net/nfs/tools/Users/SU/jservon/spirit-2021.11_envs/20230904/share/proj
#export PYPROJ_GLOBAL_CONTEXT = ON
#~/climaf_installs/climaf_running/bin/climaf


# +
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

cshow(plot(ccdo(ccdo(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),
                     operator='zonmean'),
                operator='mermean'),
           ccdo(
               ccdo(llbox(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),
                          latmax=90,latmin=10,lonmax=150,lonmin=50),operator='zonmean'),
               operator='mermean'),
           invXY=True,title='Profiles (t,z)',y='log', resolution='300x300', trim=True,
          color="BlueDarkRed18"), True)
