zonmean_interpolation : vertical and horizontal interpolation of dat1
---------------------------------------------------------------------------------------

Returns the vertically and horizontally interpolated dat1:
   - either by providing a target zonal field dat2 => dat1 is regridded both horizontally and vertically on dat2
    - or by providing a list of vertical levels => dat1 is regridded horizontally on the cdo_horizontal_grid
    (default='r1x90'), and vertically on the list of vertical levels
The user can provide the vertical levels (in Pa) like this:
    vertical_levels=[100000,85000,50000,20000,...] # or
    vertical_levels='100000,85000,50000,20000'
Before the computations, the function checks the unit of the vertical axis;
it is converted to Pa if necessary directly in the netcdf file(s) corresponding to dat1(2).

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : two CliMAF datasets with at least the latitude dimension, and the same number of time steps

**Mandatory argument**: 

None

**Output** : the zonal mean difference between dat1 and dat2 -> latitude/time (for a lon/lat/time dataset) or latitude/pressure/time (for a lon/lat/pressure/time dataset)

**Climaf call example** ::
 
    >>> dat = ds(project='CMIP5',model='IPSL-CM5A-LR',variable='ua',period='1980-1985',
                experiment='historical',table='Amon')
    >>> ref = ds(project='ref_pcmdi',variable='ua',product='ERAINT')

    >>> zonmean_dat = zonmean(climato(dat))
    >>> zonmean_ref = zonmean(climato(ref))

    >>> dat_interpolated_on_ref = zonmean_interpolation(zonmean_dat,zonmean_ref)
    >>> dat_interpolated_on_list_of_levels = zonmean_interpolation(zonmean_dat,vertical_levels='100000,85000,50000,20000,10000,5000,2000,1000')


**Side effects** : none

**Implementation** : uses regrid, regridn, ccdo(...,operator='intlevel') and a netcdf library to check the units of the vertical axis (using anynetcdf) 

