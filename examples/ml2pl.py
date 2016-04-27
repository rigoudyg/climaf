# Examples for vertical interpolation
# 1/ interpolating a 3D field on model levels on standard pressure levels using ml2pl
# 2/ computing a model-reference difference using diff_zonmean (based on zonmean_interpolation)


from climaf.api import *
from climaf.site_settings import onCiclad

clog('critical')

cdef("project","example")
cdef("frequency","monthly")

if onCiclad:
   # 0 - define a dataset
   var_file  = ds(simulation='NPv3.1ada', variable='ua'   ,period='fx')
   pres_file = ds(simulation='NPv3.1ada', variable='pres' ,period='fx')
   #
   # 1 - Interpolate the variable from the model levels to the pressure levels
   var_on_pl = ml2pl(var_file,pres_file)
   cfile(var_on_pl)
   #
   # 2 - Compute a bias map for the zonal mean
   ref = ds(project='ref_climatos', variable='ua', product='ERAINT')
   climato_sim = time_average(var_on_pl)
   climato_ref = time_average(ref)
   #
   # 3 - Do the plot
   test_plot = plot(diff_zonmean(climato_sim,climato_ref),zonmean(climato_ref),
                    title='Zonal Mean Difference',contours='-20 -10 -5 -1 1 5 10 15 20 30 40',
                    min=-20,max=20,delta=2)

   if (cfile(test_plot) is None) : exit(1)
