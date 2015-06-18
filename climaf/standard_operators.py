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
    cscript('select' ,scriptpath+'mcdo.sh "${operator}" "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins} ',
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
    # Operators CDFTools
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
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} ${in_3} ${in_4} $tmp_file; (echo climaf; echo ${imin},${imax},${jmin},${jmax}; echo EOF) | cdftransport ${opt1} $tmp_file ${in_5} ${in_6} ${opt2}; cdo selname,vtrp climaf_transports.nc ${out}; cdo selname,htrp climaf_transports.nc htrp.nc; cdo selname,strp climaf_transports.nc strp.nc; rm -f climaf_transports.nc $tmp_file section_trp.dat htrp.txt vtrp.txt strp.txt')
    #
    #2 "bugs"
    #1: necessite en premier un executable donc jai mis temporairement un echo
    #2: bug avec les fichiers outputs ${out_word}, quand ce sera resolu faire:
    #cdo selname,htrp climaf_transports.nc ${out_htrp}; cdo selname,strp climaf_transports.nc ${out_strp}; rm -f climaf_transports.nc'
          
    #
    #cdfheatc 
    #
    cscript('cdfheatc',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfheatc $tmp_file ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; rm -f $tmp_file')
    #
    #2 "bugs"
    #1: necessite en premier un executable donc jai mis temporairement un echo
    #2: pb avec le fichier IN. Quand on le scinde en fichiers mono-variables (en utilisant cdo selname), comme la variable 'time_counter' du fichier IN ne contient pas de data, 'cdo selname' la remplace par 't_ave_01month' => pb...
    #Car 'cdfheatc' a besoin de la var 'time_counter' dans le fichier .nc IN (meme si elle ne contient pas de data) alors que 'cdo selname' a besoin de data dans la variable temporelle pr extraire des data... Il prend donc la var ayant des data.
    #Donc il faut: soit des data dans la var 'time_counter', soit remplacer cn_t='time_counter' par cn_t='t_ave_01month' dans modcdfnames.f90 (pr que la var lue dans les fichiers nc soit 't_ave_01month' et non 'time_counter').

    # 
    #cdfsections -non teste au vu du bug 2-
    #
    cscript('cdfsections',
            'cdfsections ${in_1} ${in_2} ${in_3} ${larf} ${lorf} ${Nsec} ${lat1} ${lon1} ${lat2} ${lon2} ${n1} ${lat3} ${lon3} ${n2} ${lat4} ${lon4} ${n3} ${opt}; mv section.nc ${out}; rm -f section.nc')
    #
    #2 "pbs" hors CliMAF:
    #1: necessite de remplacer dans 'cdfsections.f90',les variables: "vosaline" par cn_vosaline, "votemper" par cn_votemper et "vomecrty" par cn_vomecrty
    #2: un pb persiste hors CliMAF: La variable 'time_counter' est presente dans les fichiers U et V (entete et data) mais pas dans T (entete mais pas de data).

    #
    #cdfmxlheatc
    #
    cscript('cdfmxlheatc',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfmxlheatc $tmp_file ${opt}; mv mxlheatc.nc ${out}; rm -f mxlheatc.nc $tmp_file')
    #
    #1 "contrainte":
    #Dans 'cdfmxlheatc.f90', la mixed_layer souhaitee est 'cn_somxl010' mais elle n est pas disponible.
    #Dans 'modcdfnames.f90', il y en a 2 possibles: cn_somxl010='somxl010' ou cn_somxlt02='somxlt02'. Dans le fichier IN nc, la variable est 'omlmax'.
    #Donc:
    #dans 'modcdfnames.f90': remplacer cn_somxlt02='somxlt02' par  cn_somxlt02='omlmax' (car le fichier nc contient la variable 'omlmax')
    #dans 'cdfmxlheatc.f90': remplacer 'cn_somxl010' par 'cn_somxlt02'.
    #
    #2 bugs idem que cdfheatc:
    #1: necessite en premier un executable donc jai mis temporairement un echo
    #2:pb avec le fichier IN. Quand on le scinde en fichiers mono-variables (en utilisant cdo selname), comme la variable 'time_counter' du fichier IN ne contient pas de data, 'cdo selname' la remplace par 't_ave_01month' => pb...
    #Car 'cdfmxlheatc' a besoin de la var 'time_counter' dans le fichier .nc IN (meme si elle ne contient pas de data) alors que 'cdo selname' a besoin de data dans la variable temporelle pr extraire des data... Il prend donc la var ayant des data.
    #Donc il faut: soit des data dans la var 'time_counter', soit remplacer cn_t='time_counter' par cn_t='t_ave_01month' dans modcdfnames.f90 (pr que la var lue dans les fichiers nc soit 't_ave_01month' et non 'time_counter').

    #
    #cdfstd
    #
    cscript('cdfstd',
            'cdfstd ${opt} ${in_1} ${in_2}; mv cdfstd.nc ${out}; rm -f cdfstd.nc')
    #
    #Pb 1: comment faire vu que le nombre de fichiers IN (et donc de variables) n est pas fixe pour cet operateur ? Ou comment rendre un fichier IN optionnel ? Car ${in_1} ${in_2} signifie qu on ne peut donner qu exactement 2 variables en entree.
    #Remarque importante pour l'integration dans Climaf: si c'est le meme fichier, cdfstd calcule de la meme facon que s il ne l avait qu une fois en argument (donc utilisation d un cdo merge inutile).
    #Faire 2 operateurs pr le cas ou l argument -save est utilise => cdfmoy.nc ?
    #Creer une sortie ${out_cdfmoy} - a voir

    #1 bug idem que cdfheatc:
    #pb avec les fichiers IN. Si un fichier IN ne contient pas de data pour la variable 'time_counter', le resultat est faux: il contient des zeros pour les variables calculees.
    #Si on utilise le calcul de cdfstd hors Climaf, le resultat est ok meme si la variable 'time_counter' ne contient pas de data. Car 'cdfstd' a besoin de la var 'time_counter' dans le fichier .nc IN (meme si elle ne contient pas de data) alors que Climaf (qui doit utiliser 'cdo selname' pr l'extraction des donnees) a besoin de data dans la variable temporelle pr extraire des data... sans data, il doit faire une extraction fausse.
    #Donc il faut: soit des data dans la var 'time_counter', soit remplacer cn_t='time_counter' par cn_t='t_ave_01month' (present dans les fichiers nc ne contenant pas de data pour 'time_counter') dans modcdfnames.f90 (pr que la var lue dans les fichiers nc soit 't_ave_01month' et non 'time_counter'). En sachant que ces deux variables sont sans doute differentes...
    # => fonctionne pour les fichiers contenant des data pour time_counter
    
