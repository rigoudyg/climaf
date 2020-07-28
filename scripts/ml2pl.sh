# This is a template. Fill in the path to the executable.

# This is a script in Bash.

# Author: Lionel GUEZ

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

# Do not run several instances of this script in parallel in the same
# directory. File names are not made different for different
# instances.

##set -x

# Absolute path to Fortran executable:
#executable=/data/guez/build/Ml2pl/ml2pl
executable=$CLIMAF/scripts/ml2pl
#executable=$(dirname *0)/ml2pl

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

if [[ ! -f $1 ]]
    then
    echo "ml2pl.sh: $1 not found"
    exit 1
fi

if [[ ! -f "press_levels.txt" ]]
    then
    echo "ml2pl.sh: press_levels.txt not found"
    echo "Use option -h for help"
    exit 1
fi

if (($# == 2))
then
    ln -sf $1 input_file_ml2pl.nc
else
    # $# == 3
    if [[ ! -f $3 ]]
    then
	echo "ml2pl.sh: $3 not found"
	exit 1
    fi
    #cp $3 input_file_ml2pl.nc
    #ncks --append ${variable_list_v:+--variable=$variable_list_v} \
    #	${variable_list_w:+--variable=$variable_list_w} \
    #	${variable_list_m:+--variable=$variable_list_m} $1 input_file_ml2pl.nc
    #echo "Appended $1 to $3."
    echo "ncdump de $1"
    ncdump -h $1
    echo "ncdump de $3"
    ncdump -h $3
    echo "cdo merge ${variable_list_v:+-selvar,$variable_list_v} \
    ${variable_list_w:+-selvar,$variable_list_w} \
    ${variable_list_m:+-selvar,$variable_list_m} $1 $3 input_file_ml2pl.nc"
    cdo -O merge ${variable_list_v:+-selvar,$variable_list_v} \
    ${variable_list_w:+-selvar,$variable_list_w} \
    ${variable_list_m:+-selvar,$variable_list_m} $1 $3 input_file_ml2pl.nc
echo "merge done for $1 and $3."
    echo "ncdump du merge "
    ncdump -h input_file_ml2pl.nc
fi

output_file=$2

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
rm input_file_ml2pl.nc variable_list_ml2pl
