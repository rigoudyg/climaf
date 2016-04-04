def varlongname(variable):
   """
   Returns the long name of variable
   """
   longvarname = variable
   if variable=='tos':
        longvarname  = 'Sea Surface Temperature'
   if variable=='sos':
        longvarname  = 'Sea Surface Salinity'
   if variable=='to200':
        longvarname  = 'Potential Temperature at 200m'
   if variable=='to1000':
        longvarname  = 'Potential Temperature at 1000m'
   if variable=='to2000':
        longvarname  = 'Potential Temperature at 2000m'
   if variable=='so200':
        longvarname  = 'Salinity at 200m'
   if variable=='so1000':
        longvarname  = 'Salinity at 1000m'
   if variable=='so2000':
        longvarname  = 'Salinity at 2000m'
   if variable=='mlotst':
        longvarname  = 'MLD (SigmaT 0.03)'
   if variable=='wfo':
        longvarname  = 'E-P Budget'
   if variable=='tauu':        
        longvarname  = 'Zonal Wind Stress'
   if variable=='tauv':        
        longvarname  = 'Meridional Wind Stress'
   if variable=='hfls':        
        longvarname  = 'Latent Heat Flux'
   if variable=='hfss':        
        longvarname  = 'Sensible Heat Flux'
   if variable=='sic':        
        longvarname  = 'Sea Ice Concentration'
   #
   return longvarname



