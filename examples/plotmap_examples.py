import hplot_operator
lcmn
# export PROJ_DATA=/net/nfs/tools/Users/SU/jservon/spirit-2021.11_envs/20230904/share/proj
# export PYPROJ_GLOBAL_CONTEXT=ON
~/climaf_installs/climaf_running/bin/climaf


clog('debug')

data = fds(
    cpath + "/../examples/data/tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc")
# cfile(plotmap(data))
# cshow(plotmap(data))

# Play with number of colors
cshow(plotmap(data, clrl=15))

# Add feature (tested with only a colored map)
cshow(plotmap(data, clrl=15, feature_name='LAND', feature_color='lightgray'))

# Lambert2
l2 = fds(cpath + "/../examples/data/sfcWind_aladin.nc")

# Ploting without re-projection : 'proj' provides data transform
cshow(plotmap(l2, proj="LambertII", proj_options=[10, 37, 37], cntl=10))

# Ploting in PlateCaree, with lines
cshow(plotmap(l2, clrt="LambertII",
              clrto=[10, 37, 37], lines=[[45, 30], [0, 0]]))

# Playing with projections
cshow(plotmap(l2, clrt="LambertII", clrto=[10, 37, 37], proj="Stereographic"))

# Select options
cshow(plotmap(data, clrso=[('isel', {'time': 0})]))
