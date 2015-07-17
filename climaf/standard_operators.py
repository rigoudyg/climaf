"""
Management of CliMAF standard operators

"""

from climaf import __path__ as cpath
from climaf.operators import cscript

scriptpath=cpath[0]+"/../scripts/" 

def load_standard_operators():
    """ 
    Load CliMAF standard operators. Invoked by standard CliMAF setup

    The operators list also show in variable 'cscripts'
    They are documented elsewhere
    """
    #
    # Compute scripts
    #
    #cscript('select' ,scriptpath+'mcdo.sh "${operator}" "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins} ',
    #       commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #tmp  export CLIMAF_FIX_NEMO_TIME='on'
    cscript('select' ,'/mnt/nfs/d3/aster/data3/aster/senesi/dev/climaf/scripts/mcdo.sh "${operator}" "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins} ',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)    
    #
    cscript('ccdo',
            scriptpath+'mcdo.sh ${operator} "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins}')
    #
    cscript('minus', 'cdo sub ${in_1} ${in_2} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('space_average',
            scriptpath+'mcdo.sh fldmean ${out} ${var} ${period_iso} ${domain} "${alias}" "${missing}" ${ins}', 
            commuteWithTimeConcatenation=True)
    #
    cscript('time_average' ,
            scriptpath+'mcdo.sh timmean  ${out} ${var} ${period_iso} ${domain} "${alias}" "${missing}" ${ins}' ,
            commuteWithSpaceConcatenation=True)
    #
    cscript('llbox' ,
            scriptpath+'mcdo.sh ""  ${out} ${var} ${period_iso} '
            '${latmin},${latmax},${lonmin},${lonmax} "${alias}" "${missing}" ${ins}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('regrid' ,
            scriptpath+'regrid.sh ${in} ${in_2} ${out} ${option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('regridn' ,
            scriptpath+'regrid.sh ${in} ${cdogrid} ${out} ${option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('rescale' ,
            "cdo expr,\"${var}=${scale}*${var}+${offset};\" ${in} ${out}",
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('mean_and_std',
            scriptpath+'mean_and_std.sh ${in} ${var} ${out} ${out_sdev}', 
            # This tells CliMAF how to name output 'sdev' using input variable name
            sdev_var="std(%s)" , 
            commuteWithTimeConcatenation=True)
    #
    # Declare plot scripts
    cscript('ncview'    ,'ncview ${in} 1>/dev/null 2>&1&' )
    #
    cscript('timeplot', 'ncl '+scriptpath+'timeplot.ncl infile=${in} outfile=${out} '
            'var=${var} title=${crs}',format="png")
    #
    cscript('plot'     , '(ncl -Q '+ scriptpath +'gplot.ncl infile=\'\"${in}\"\' '
            'plotname=\'\"${out}\"\' cmap=\'\"${color}\"\' vmin=${min} vmax=${max} vdelta=${delta} '
            'var=\'\"${var}\"\' title=\'\"${title}\"\' scale=${scale} offset=${offset} units=\'\"${units}\"\' '
            'linp=${linp} levels=\'\"${levels}\"\' proj=\'\"${proj}\"\' contours=${contours} focus=\'\"${focus}\"\' && '
            'convert ${out} -trim ${out}) ', format="png")
    #
    # CDFTools operators 
    #
    #cdfmean
    #
    cscript('cdfmean',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x -v mean_${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt')
    #
    cscript('cdfmean_profile',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x -v mean_3D${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt')
    #    
    cscript('cdfvar',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x -v mean_${var},mean_3D${var},var_${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt')
    #    
    cscript('cdfvar_profile',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x -v mean_${var},mean_3D${var},var_3D${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt') 

    #
    #cdftransport : case where VT file must be given 
    #
    cscript('cdftransport',
            scriptpath+'cdftransport.sh ${in_1} ${in_2} ${in_3} ${in_4} ${in_5} ${in_6} ${imin} ${imax} ${jmin} ${jmax} "${opt1}" "${opt2}" ${out} ')
    #
    #sans appel du script 'cdftransport.sh' et avec les ${out_var} a tester
    #cscript('cdftransport',
    #        'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} ${in_3} ${in_4} $tmp_file; (echo climaf; echo ${imin},${imax},${jmin},${jmax}; echo EOF) | cdftransport ${opt1} $tmp_file ${in_5} ${in_6} ${opt2}; cdo selname,vtrp climaf_transports.nc ${out}; cdo selname,htrp climaf_transports.nc ${out_htrp}; cdo selname,strp climaf_transports.nc ${out_strp}; rm -f climaf_transports.nc $tmp_file section_trp.dat htrp.txt vtrp.txt strp.txt', htrp_var="var_htrp", strp_var="var_strp")
          
    #
    #cdfheatc 
    #
    cscript('cdfheatc',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfheatc $tmp_file ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; rm -f $tmp_file')
   
    # 
    #cdfsections -non teste car quelles variables faut-il dans les fichiers U, V et T ? (et bug hors CliMAF)-
    #
    cscript('cdfsections',
            'cdfsections ${in_1} ${in_2} ${in_3} ${larf} ${lorf} ${Nsec} ${lat1} ${lon1} ${lat2} ${lon2} ${n1} ${opt}; mv section.nc ${out}; rm -f section.nc')

    #
    #cdfmxlheatc
    #
    cscript('cdfmxlheatc',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfmxlheatc $tmp_file ${opt}; mv mxlheatc.nc ${out}; rm -f mxlheatc.nc $tmp_file')

    #
    #cdfstd
    #
    cscript('cdfstd',
            'cdfstd ${opt} ${ins}; mv cdfstd.nc ${out}; rm -f cdfstd.nc')
    #
    cscript('cdfstdmoy',
            'cdfstd -save ${opt} ${ins}; mv cdfmoy.nc ${out}; rm -f cdfmoy.nc')
    #
