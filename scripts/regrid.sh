#!/bin/bash
doc="
$0 FIELDIN FIELDGRID FIELDOUT

Interpolate FIELDIN, on grid provided by FIELDGRID, to FIELDOUT,using CDO
If FIELDGRID is not a file, interpret it as a CDO standard grid name

No effort to optimize (e.g. by using pre-computed weights) yet !
"
set -ex
fieldin=$1
fieldgrid=$2
fieldout=$3
var=$4
option=${5:-remapbil}
if [ -f $fieldgrid ] ; then 
    cdo griddes $fieldgrid > climaf_tmp_grid_$$
    cdo $option,climaf_tmp_grid_$$ -selname $var $fieldin $fieldout 
    rm climaf_tmp_grid_$$
else
    cdo $option,$fieldgrid $fieldin $fieldout 
fi
