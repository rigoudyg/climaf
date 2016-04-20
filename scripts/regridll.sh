#!/bin/bash
doc="
$0 FIELDIN FIELDOUT GRIDNAME LATMIN LATMAX LONMIN LONMAX REMAP_OPTION

Interpolate FIELDIN as FIELDOUT on a box of a regular latlon grid 

"
set -ex
fieldin=$1
fieldout=$2
gridname=$3
latmin=$4 ; latmax=$5
lonmin=$6 ; lonmax=$7
option=${8:-remapbil}

[ -z $lonmax ] && echo "Isseu with args" && exit 1

# Create a global field on target grid
cdo const,0,$gridname tmp_grid_$$.nc

# Generate CDO grid description for latlon box in that grid
cdo sellonlatbox,$lonmin,$lonmax,$latmin,$latmax tmp_grid_$$.nc tmp_grid_llb_$$.nc
cdo griddes tmp_grid_llb_$$.nc > climaf_tmp_grid_$$

# Regrid 
cdo $option,climaf_tmp_grid_$$ $fieldin $fieldout 

# Cleanup
rm tmp_grid_*$$.nc  climaf_tmp_grid_$$
