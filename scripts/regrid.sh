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
option=${4:-remapbil}
if [ -f $fieldgrid ] ; then 
    cdo griddes $fieldgrid > climaf_tmp_grid
    cdo $option,climaf_tmp_grid $fieldin $fieldout 
    rm climaf_tmp_grid
else
    cdo $option,$fieldgrid $fieldin $fieldout 
fi
