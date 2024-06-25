#!/bin/bash
doc="
$0 FIELDIN GRIDFIELD FIELDOUT VARIABLE

Interpolate FIELDIN, on grid provided by GRIDFIELD, to FIELDOUT,using CDO
If GRIDFIELD is not a file, interpret it as a CDO standard grid name
Only variable VARIABLE is kept in output

If grids are the same, do not interpolate (because otherwise, CDO 
generate diffs)
No effort to optimize (e.g. by using pre-computed weights) yet !
"
set -ex
fieldin=$1
gridfield=$2
fieldout=$3
var=$4
option=${5:-remapbil}
#
if [ -f $gridfield ] ; then 
    cdo griddes $gridfield > climaf_tmp_target_grid_$$
    
    # interpolate only if input grid is not the same as target grid
    cdo griddes $fieldin > climaf_tmp_input_grid_$$
    if ! diff -q climaf_tmp_target_grid_$$ climaf_tmp_input_grid_$$ ; then
	interpolator="$option,climaf_tmp_target_grid_$$"
    fi
    cdo $interpolator -selname,$var $fieldin $fieldout 
    rm climaf_tmp_*_grid_$$
else
    grid=$gridfield
    cdo $option,$grid -selname,$var $fieldin $fieldout 
fi
