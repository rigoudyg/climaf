#!/bin/bash
# This is a template. Fill in the path to the executable.

# This is a script in Bash.

# Author: Lionel GUEZ
# Changes : Stéphane Sénési - 01/2023 - use a workdir (possibly in
#              CLIMAF_CACHE, else in /tmp)

# This script is a wrapper for a Fortran program. The program reads a
# NetCDF file. It interpolates an arbitrary set of NetCDF variables
# from model levels to pressure levels. The interpolation is linear in
# logarithm of pressure. The input variables depend on longitude,
# latitude, vertical level and time. There is no constraint on the
# dimensions.

# The pressure field at model levels can be specified in the input
# NetCDF file or in a separate file, either through "ap", "bp" and
# "ps" or directly as a four-dimensional variable. In all cases,
# pressure must be given in Pa and decrease when the index of model
# level increases. This is checked quickly in the program.

# The program writes results to a new NetCDF file.

# For an explanation of programming choices, see notes.

# Variables following the "-v" option are extrapolated if
# necessary. Variables following the "-w" option are set to zero below
# the surface of the Earth. Variables following the "-m" option are
# set to mssing below the surface of the Earth.

set -e

# Absolute path to Fortran executable (here supposed to be in same dir as this script:
executable=$(dirname $0)/ml2pl

# Workdir
curdir=$(pwd)
workdir=${CLIMAF_CACHE:-/tmp}/ml2pl_$$
mkdir -p $workdir

USAGE="usage: ml2pl.sh [OPTION]... input-file output-file [pressure_file]
Interpolates NetCDF variables from model levels to pressure levels.
Options:
   -h                       : this help message
   -p variable              : name of 4-dimensional variable in the input file
                              or the pressure file containing the
                              pressure field at model levels
   -v variable[,variable...]: names of variables you want to interpolate, 
                              and possibly extrapolate if target pressure 
                              level is below surface
   -w variable[,variable...]: names of variables you want to interpolate, 
                              or set to 0 if target pressure level is below
                              surface
   -m variable[,variable...]: names of variables you want to interpolate, 
                              or set to missing if target pressure level is 
                              below surface

There must be at least one variable listed, following -v, -w or -m. If
option -p is not used then the program will look for \"ap\", \"bp\"
and \"ps\" in the input file or the pressure file.

The target pressure levels should be in a text file called
\"press_levels.txt\" in the current directory. The first line of the
file is skipped, assuming it is a title line. Pressure levels should
be in hPa, in descending order.

The script uses a workdir located in directory $CLIMAF_CACHE or /tmp,
and named ml2pl_$$; this allows for concurrent execution of multiple
instances

For further documentation, see:
http://lmdz.lmd.jussieu.fr/utilisateurs/outils/utilisation-de-lmdz#section-9"

while getopts hp:v:w:m: name
  do
  case $name in
      p) 
	  pressure_var=$OPTARG;;
      v) 
	  variable_list_v=$OPTARG;;
      w) 
	  variable_list_w=$OPTARG;;
      m) 
	  variable_list_m=$OPTARG;;
      h)
	  echo "$USAGE" >&2
	  exit;;
      \?)
	  echo "Use option -h for help"
	  exit 1;;
  esac
done

if [[ -n $pressure_var ]]
then
    # For Climaf, remove pressure_var from variable lists:

    variable_list_v=`echo $variable_list_v | sed -e 's/'$pressure_var'//g' -e s'/,,*/,/g' -e s'/^,//' -e 's/,$//'`
    
    variable_list_w=`echo $variable_list_w | sed -e 's/'$pressure_var'//g' -e s'/,,*/,/g' -e s'/^,//' -e 's/,$//'`

    variable_list_m=`echo $variable_list_m | sed -e 's/'$pressure_var'//g' -e s'/,,*/,/g' -e s'/^,//' -e 's/,$//'`
fi

if [[ -z $variable_list_v && -z $variable_list_w && -z $variable_list_m ]]
    then
    echo "Specify at least one variable, following -v, -w or -m."
    echo "Use option -h for help"
    exit 1
fi

shift $((OPTIND - 1))
input_file=$(realpath $1)
output_file=$(realpath $2)
pressure_file=$(realpath $3)
cd $workdir

if (($# <= 1))
then
    echo "Missing input or output file."
    echo "Use option -h for help"
    exit 1
elif (($# >= 4))
then
    echo "Too many arguments."
    echo "Use option -h for help"
    exit 1
fi

set -e

if [[ ! -x $executable ]]
    then
    echo "$executable not found or not executable"
    exit 1
fi

if [[ ! -f $input_file ]]
    then
    echo "ml2pl.sh: $input_file not found"
    exit 1
fi

if [[ ! -f $curdir/press_levels.txt ]];    then
    echo "ml2pl.sh: press_levels.txt not found"
    echo "Use option -h for help"
    exit 1
else
    ln -sf $curdir/press_levels.txt .
fi

if (($# == 2))
then
    ln -sf $input_file input_file_ml2pl.nc
else
    # $# == 3
    if [[ ! -f $pressure_file ]]
    then
	echo "ml2pl.sh: $pressure_file not found"
	exit 1
    fi
    echo "ncdump de $input_file"
    ncdump -h $input_file
    echo "ncdump de $pressure_file"
    ncdump -h $pressure_file
    echo "cdo merge ${variable_list_v:+-selvar,$variable_list_v} \
    ${variable_list_w:+-selvar,$variable_list_w} \
    ${variable_list_m:+-selvar,$variable_list_m} $input_file $pressure_file input_file_ml2pl.nc"
    cdo -O merge ${variable_list_v:+-selvar,$variable_list_v} \
    ${variable_list_w:+-selvar,$variable_list_w} \
    ${variable_list_m:+-selvar,$variable_list_m} $input_file $pressure_file input_file_ml2pl.nc
    echo "merge done for $input_file and $pressure_file."
    echo "ncdump du merge "
    ncdump -h input_file_ml2pl.nc
fi

IFS=","

if [[ -z $variable_list_v ]]
then
    nv=0
else
    set $variable_list_v
    nv=$#
fi

if [[ -z $variable_list_w ]]
then
    nw=0
else
    set $variable_list_w
    nw=$#
fi

# Create the list of variables:
set $variable_list_v $variable_list_w $variable_list_m
for my_var in $*
  do
  echo $my_var
done >variable_list_ml2pl

# Run the Fortran program:
$executable <<EOF
$nv
$nw
"$pressure_var"
EOF
# (Quotes around $pressure_var are necessary for the case when
# pressure_var is not defined.)

mv output_file_ml2pl.nc $output_file
rm input_file_ml2pl.nc variable_list_ml2pl press_levels.txt
rm -f "="
cd ..
rmdir $workdir
