from climaf.api import *
from climaf.operators import *

# -- Fonctions de plot interractives
from IPython.display import Image


def apply_scale_offset(dat,scale,offset):
    """Returns a CliMAF object after applying a scale and offset
    ! Shortcut to: ccdo(ccdo(dat,operator='mulc,'+str(float(scale))),operator='addc,'+str(float(offset)))

    **Note** : this function should be used parcimonioulsy because the model in CliMAF 
    for dealing with scaling and offset is rather :

      - to automatically scale and offset the data to S.I. units at
        input/reading stage; this si done by declaring scaling for
        each relevant variable in a project using function
        :py:func:`~climaf.dataloc.calias`; it also allows to set the units
      - if the S.I. units are not suitable for a plot, to use plot 
        operators arguments 'scale' and 'offset' to change the values

    """
    return ccdo(ccdo(dat,operator='mulc,'+str(float(scale))),operator='addc,'+str(float(offset)))
#


def mul(dat1,dat2):
    """
    Multiply dat1 by dat2 ; dat2 can be either a CliMAF object of same dimension as dat1, 
    or constant (string, float or integer).
    Shortcut to ccdo(dat1,dat2,operator='mul') and ccdo(dat,operator='mulc,'+c)
    """
    if isinstance(dat2,(str,float,int)):
       c = str(float(dat2))
       return ccdo(dat1,operator='mulc,'+c)
    else: 
       return ccdo2(dat1,dat2,operator='mul')

def div(dat1,dat2):
    """
    Divide dat1 by dat2 ; dat2 can be either a CliMAF object of same dimension as dat1, 
    or constant (string, float or integer).
    Shortcut to ccdo(dat1,dat2,operator='div') and ccdo(dat,operator='divc,'+c)
    """
    if isinstance(dat2,(str,float,int)):
       c = str(float(dat2))
       return ccdo(dat1,operator='divc,'+c)
    else:
       return ccdo2(dat1,dat2,operator='div')

def add(dat1,dat2):
    """
    Add dat1 to dat2; dat2 can be either a CliMAF object of same dimension as dat1, or constant (string, float or integer)
    Shortcut to ccdo(dat,operator='addc,'+str(c)) and ccdo2(dat1,dat2,operator='add')
    """
    if isinstance(dat2,(str,float,int)):
       c = str(float(dat2))
       return ccdo(dat1,operator='addc,'+c)
    else:
       return ccdo2(dat1,dat2,operator='add')

def sub(dat1,dat2):
    """
    Subtract dat2 to dat1; dat2 can be either a CliMAF object of same dimension as dat1, or constant (string, float or integer)
    Shortcut to ccdo(dat,operator='subc,'+str(c)) and ccdo2(dat1,dat2,operator='sub')
    """
    if isinstance(dat2,(str,float,int)):
       c = str(float(dat2))
       return ccdo(dat1,operator='subc,'+c)
    else:
       return ccdo2(dat1,dat2,operator='sub')



def iplot(map):
    """
    Interactive version of plot for display in IPython Notebooks
    Similar to implot() but you provide a figure (a CliMAF object produced with e.g. plot() )
    (while implot() takes a dataset as argument and invokes plot()).
    """
    return Image(filename=cfile(map))


# -- Calcul de moyenne sur la verticale dans l'ocean

# -> Identifie les niveaux verticaux du fichier compris entre zmin et zmax
def getLevs(dat,zmin=0,zmax=100000,convertPressureUnit=None):
    """
    TBD
    """
    from Scientific.IO.NetCDF import NetCDFFile as ncf
    filename=cfile(dat)
    fileobj=ncf(filename)
    min_lev = zmin
    max_lev = zmax
    my_levs=None
    levname=None
    for varname in fileobj.variables:
        if varname in ['level','levels','lev','levs','depth','deptht','DEPTH','DEPTHT','plev']:
            levname=varname
    levunits = fileobj.variables[levname].units
    for lev in fileobj.variables[levname].getValue():
        #print lev
        if min_lev <= lev <= max_lev:
            if convertPressureUnit:
               if convertPressureUnit=='hPaToPa':
                  lev = lev*100
               if convertPressureUnit=='PaTohPa':
                  lev = lev/100
            if my_levs:
                my_levs=my_levs+','+str(int(lev))
            else:
                my_levs=str(int(lev))
    return my_levs


def vertical_average(dat,zmin,zmax):
    """
    Computes a vertical average on the vertical levels between zmin and zmax
    """
    levs = getLevs(dat,zmin,zmax)
    print ' --> Compute average on the following vertical levels : '+levs
    tmp = ccdo(dat, operator="'vertmean -sellevel,'+levs'")
    return tmp


import numpy as np

def implot(field,**kwargs):
    """
    Interactive version of plot for display in IPython Notebooks
    Similar to iplot() except that you provide a dataset and a dict of plot arguments
    """
    return Image(filename=cfile(plot(field,**kwargs)))


def diff_regrid(dat1, dat2):
    """
    Regrids dat1 on dat2 and returns the difference between dat1 and dat2
    """
    return sub(regrid(dat1,dat2), dat2)

def diff_regridn (data1, data2, cdogrid='n90'):
    """
    Regrids dat1 and dat2 on a chosen cdogrid (default is n90) and returns the difference between dat1 and dat2 
    """    
    return sub ( regridn( data1, cdogrid=cdogrid), regridn( data2, cdogrid=cdogrid ))


def tableau(n_lin=1, n_col=1):
    """
    Generates a table as used by cpage with n_lin rows and n_col columns.
    """
    view    = [[ None for i in range(n_col)] for j in range(n_lin)]
    return view



def annual_cycle(dat):
    """
    Computes the annual cycle as the 12 climatological months of dat
    (wrapper of ccdo with operator ymonavg)
    """
    return ccdo(dat, operator="ymonavg")


def clim_average(dat,season):
    """
    Computes climatological averages on the annual cycle of a dataset, on the months 
    specified with 'season', either:
    - the annual mean climatology (season => 'ann','annual','time_average','clim','climatology','annual_average','anm')
    - seasonal climatologies (e.g. season = 'DJF' or 'djf' to compute the seasonal climatology 
      over December-January-February; available seasons: DJF, MAM, JJA, SON, JFM, JAS, JJAS
    - individual monthly climatologies (e.g. season = 'january', 'jan', '1' or 1 to get 
      the climatological January)
    - annual maximum or minimum (typically makes sense with the mixed layer depth)

    Note that you can use upper case or lower case characters to specify the months or seasons.
    
    clim_average computes the annual cycle for you.
    """
    #
    if str(season).lower() in ['ann','annual','time_average','clim','climatology','annual_average','anm','annual_mean']:
        avg = time_average(dat)
    else:
        #
        # -- Compute the annual cycle
        scyc = annual_cycle(dat)
        #
        # -- Classic atmospheric seasons
        selmonths=selmonth=None
        if str(season).upper()=='DJF': selmonths ='1,2,12'
        if str(season).upper()=='MAM': selmonths ='3,4,5'
        if str(season).upper()=='JJA': selmonths ='6,7,8'
        if str(season).upper()=='SON': selmonths ='9,10,11'
        # -- Classic oceanic seasons
        if str(season).upper()=='JFM': selmonths ='1,2,3'
        if str(season).upper()=='JAS': selmonths ='7,8,9'
        if str(season).upper()=='JJAS': selmonths ='6,7,8,9'
        if selmonths:
            avg = time_average(ccdo(scyc,operator='selmon,'+selmonths))
        #
        #
        # -- Individual months
        if str(season).lower() in ['january','jan','1']:   selmonth ='1'
        if str(season).lower() in ['february','feb','2']:  selmonth ='2'
        if str(season).lower() in ['march','mar','3']:     selmonth ='3'
        if str(season).lower() in ['april','apr','4']:     selmonth ='4'
        if str(season).lower() in ['may','5']:             selmonth ='5'
        if str(season).lower() in ['june','jun','6']:      selmonth ='6'
        if str(season).lower() in ['july','jul','7']:      selmonth ='7'
        if str(season).lower() in ['august','aug','8']:    selmonth ='8'
        if str(season).lower() in ['september','sep','9']: selmonth ='9'
        if str(season).lower() in ['october','oct','10']:  selmonth ='10'
        if str(season).lower() in ['november','nov','11']: selmonth ='11'
        if str(season).lower() in ['december','dec','12']: selmonth ='12'
        if selmonth:
            avg = ccdo(scyc,operator='selmon,'+selmonth)
        #
        # -- Annual Maximum
        if str(season).lower() in ['max','annual max','annual_max']:
            avg = ccdo(scyc,operator='timmax')
        #
        # -- Annual Maximum
        if str(season).lower() in ['min','annual min','annual_min']:
            avg = ccdo(scyc,operator='timmin')
    #
    return avg


def summary(dat):
    """
    Summary provides the informations on a CliMAF dataset obtained from dataset().
    It returns the path and filename, and the dictionary of pairs keyword-values associated with the CliMAF dataset.
    """
    if 'baseFiles' not in dir(dat):
       print '-- Ensemble members:'
       for m in dat.members:
           for f in str.split(m.baseFiles(),' '): print f
           print 'Keys - values:'
           print m.kvp
           print '--'
    else:
	if not dat.baseFiles():
		print '-- No file found for:'
    	else:
		for f in str.split(dat.baseFiles(),' '): print f
    	return dat.kvp


def projects():
    """
    Lists available projects and their associated facets.
    """
    print '-- Available projects:'
    for key in cprojects.keys():
        print '-- Project:',key
        print 'Facets =>',cprojects[key]

#
def zonmean_interpolation(dat1,dat2=None,vertical_levels=None,cdo_horizontal_grid='r1x90'):
    """
    Interpolates the zonal mean field dat1 via two possible ways:
    - either by providing a target zonal field dat2 => dat1 is regridded both horizontally and vertically on dat2
    - or by providing a list of vertical levels => dat1 is regridded horizontally on the cdo_horizontal_grid
    (default='r1x90'), and vertically on the list of vertical levels
    The user can provide the vertical levels (in Pa) like this:
    vertical_levels=[100000,85000,50000,20000,...] # or
    vertical_levels='100000,85000,50000,20000'
    Before the computations, the function checks the unit of the vertical axis;
    it is converted to Pa if necessary directly in the netcdf file(s) corresponding to dat1(2).
    
    Examples:
    dat = ds(project='CMIP5',model='IPSL-CM5A-LR',variable='ua',period='1980-1985',
             experiment='historical',table='Amon')
    ref = ds(project='ref_pcmdi',variable='ua',product='ERAINT')
    
    zonmean_dat = zonmean(time_average(dat))
    zonmean_ref = zonmean(time_average(ref))
    
    dat_interpolated_on_ref = zonmean_interpolation(zonmean_dat,zonmean_ref)
    dat_interpolated_on_list_of_levels = zonmean_interpolation(zonmean_dat,vertical_levels='100000,85000,50000,20000,10000,5000,2000,1000')
    """
    
    from climaf.anynetcdf import ncf
    
    file1 = cfile(dat1)    
    ncfile1 = ncf(file1)
    
    # -- First, we check the unit of the vertical dimension of file1
    levname1=None
    for varname in ncfile1.variables:
        if varname.lower() in ['level','levels','lev','levs','depth','deptht','plev']:
            levname1=varname
    if not levname1:
        print 'Name of the vertical axis not found for dat1'
    levunits1 = ncfile1.variables[levname1].units
    if levunits1.lower() in ['hpa','millibar','mbar','hectopascal']:
        # -- Multiplier par 100
        cmd1 = 'ncap2 -As "'+levname1+'='+levname1+'*100" '+file1+' '+file1
        cmd2 = 'ncatted -O -a units,'+levname1+',o,c,Pa '+file1
        print cmd1
        print cmd2
        os.system(cmd1)
        os.system(cmd2)
    # -> The vertical axis of file1 is now set to Pa
    #
    # -- Second, we check the unit of the vertical dimension of file2
    if dat2:
        file2 = cfile(dat2)
        ncfile2 = ncf(file2)
        
        levname2=None
        for varname in ncfile2.variables:
            if varname.lower() in ['level','levels','lev','levs','depth','deptht','plev']:
                levname2=varname
        if not levname2:
            print 'Name of the vertical axis not found for dat2'
        levunits2  = ncfile2.variables[levname2].units
        levValues2 = ncfile2.variables[levname2].getValue()
        if levunits2.lower() in ['hpa','millibar','mbar','hectopascal']:
            # -- Multiplier par 100
            cmd1 = 'ncap2 -As "'+levname2+'='+levname2+'*100" '+file2+' '+file2
            cmd2 = 'ncatted -O -a units,'+levname2+',o,c,Pa '+file2
            print cmd1
            print cmd2
            os.system(cmd1)
            os.system(cmd2)
            # -> The vertical axis of file2 is now set to Pa in the netcdf file
            scale = 100.0
        else:
            scale = 1.0
        #
        # --> We get the values of the vertical levels of dat2 (from the original file, that's why we apply a scale)
        levels = ''
        for lev in levValues2:
            levels = levels+','+str(lev*scale)
        #
        # --> We can now interpolate dat1 on dat2 verticaly and horizontally
        print levels
        regridded_dat1 = ccdo(regrid(dat1,dat2),operator='intlevel'+levels)
    else:
        if vertical_levels:
            if isinstance(vertical_levels,list):
                levels=''
                for lev in vertical_levels:
                    levels = levels+','+str(lev)
            else:
                levels = ','+vertical_levels
            regridded_dat1 = ccdo(regridn(dat1,cdogrid=cdo_horizontal_grid),operator='intlevel'+levels)
        else:
            print '--> Provide a list of vertical levels with vertical_levels'
    return regridded_dat1


def zonmean(dat):
    """
    Return the zonal mean field of dat
    Shortcut to the command ccdo(dat,operator='zonmean')
    """
    return ccdo(dat,operator='zonmean')


def diff_zonmean(dat1,dat2):
    """
    Returns the zonal mean bias of dat1 against dat2
    The function first computes the zonal means of dat1 and dat2.
    Then, it interpolates the zonal mean field of dat1 on the zonal mean field of dat2 with the function zonmean_interpolation.
    It finally returns the bias field.
    """
    #
    zonmean_dat1 = ccdo(dat1, operator='zonmean')
    zonmean_dat2 = ccdo(dat2, operator='zonmean')

    rgrd_dat1 = zonmean_interpolation(zonmean_dat1,zonmean_dat2)
    #
    return sub(rgrd_dat1,zonmean_dat2)


