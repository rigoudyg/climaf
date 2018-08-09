from climaf.api import derive, calias

# -- LMDZ

# -- Radiative SW Total at TOA
derive('*','rstt','minus','rsdt','rsut')
derive('*','rst','minus','rsdt','rsut')
# -- Radiative SW Total at surface
derive('*','rsts','minus','rsds','rsus')
# -- Radiative LW Total at surface
derive('*','rlts','minus','rlds','rlus')
# -- Radiative LW Total at surface - CS
derive('*','rltscs','minus','rldscs','rluscs')
# -- Radiative SW Total at surface - CS
derive('*','rstscs','minus','rsdscs','rsuscs')
# -- Radiative SW Total at TOA - CS
derive('*','rsttcs','minus','rsdt'  ,'rsutcs')

# -- Radiative Total at TOA
derive('*','rtt','minus','rstt','rlut')
derive('*','rt','minus','rstt','rlut')
# -- Radiative Total at surface
derive('*','rts','plus','rsts','rlts')


# -- Cloud radiative effect SW at surface
derive('*','cress','minus','rsds','rsdscs')
# -- Cloud radiative effect SW at surface
derive('*','crels','minus','rlds','rldscs')
# -- Cloud radiative effect Total at surface
derive('*','crets','plus','cress','crels')

# -- Cloud radiative effect SW at TOA
derive('*','crest','minus','rsutcs','rsut')
derive('*','rstcre','minus','rsutcs','rsut')
# -- Cloud radiative effect LW at TOA
derive('*','crelt','minus','rlutcs','rlut')
derive('*','rltcre','minus','rlutcs','rlut')
# -- Cloud radiative effect Total at TOA
derive('*','crett','plus','crest','crelt')
derive('*','rtnetcre','plus','crest','crelt')

# -- Total Non-radiative Heat Fluxes at surface
derive('*','hfns','plus','hfls','hfss')
# -- Radiative budget at surface
derive('*','bil' ,'minus','rts','hfns')
derive('*','tsmtas','minus','ts','tas')

# -- Atm. LW Heat
derive('*','rlah','minus','rlut','rlts')
# -- Atm. LW Heat - CS (rlahcs)
derive('*','rtmp','plus','rldscs','rlutcs')
derive('*','rlahcs','minus','rlus','rtmp')
# -- Atm. LW Heat - CRE
derive('*','rlahcre','minus','rlah','rlahcs')
#
# -- Atm. SW Heat
derive('*','rsah','minus','rstt','rsts')
# -- Atm. SW Heat - CS (rlahcs)
derive('*','rsahcs','minus','rsttcs','rstscs')
# -- Atm. SW Heat - CRE
derive('*','rsahcre','minus','rsah','rsahcs')

# -- Atm. Total Heat
derive('*','rah','plus','rsah','rlah')
# -- Atm. Total Heat - CS (rlahcs)
derive('*','rahcs','plus','rsahcs','rlahcs')
# -- Atm. Total Heat - CRE
derive('*','rahcre','minus','rah','rahcs')

# -- Planetary albedo at TOA
derive('*','albt','divide','rsut','rsdt')
# -- Planetary albedo at surface
derive('*','albs','divide','rsus','rsds')

# -- Atmosphere Curl Tau
derive('*','curltau','curl_tau_atm','tauu','tauv')

# -- P - E
calias('IGCM_OUT', 'hflsevap', 'hfls', scale=-1./2.5e6, filenameVar='histmth')
derive('IGCM_OUT', 'pme', 'minus', 'pr' ,'hflsevap')
calias('CMIP5', 'hflsevap', 'hfls', scale=1./2.5e6 )
derive('CMIP5', 'pme', 'minus', 'pr' ,'hflsevap')


# -- Potential Temperature and salinity @ 200m, 1000m and 2000m in depth
derive('*','so_onevar','cncks','so')
derive('*','thetao_onevar','cncks','thetao')
#derive('*','so200','ccdo','so_onevar',operator='intlevel,200')
#derive('*','so1000','ccdo','so_onevar',operator='intlevel,1000')
#derive('*','so2000','ccdo','so_onevar',operator='intlevel,2000')
#derive('*','to200','ccdo','thetao_onevar',operator='intlevel,200')
#derive('*','to1000','ccdo','thetao_onevar',operator='intlevel,1000')
#derive('*','to2000','ccdo','thetao_onevar',operator='intlevel,2000')
derive('*','so200','ccdo','so',operator='intlevel,200')
derive('*','so1000','ccdo','so',operator='intlevel,1000')
derive('*','so2000','ccdo','so',operator='intlevel,2000')
derive('*','to200','ccdo','thetao',operator='intlevel,200')
derive('*','to1000','ccdo','thetao',operator='intlevel,1000')
derive('*','to2000','ccdo','thetao',operator='intlevel,2000')



# -- Biogeochemistry
derive('*','NO3_onevar','cncks','NO3')
derive('*','NO3_surf','ccdo','NO3_onevar',operator='sellevidx,1')
derive('*','NO3_300m','ccdo','NO3_onevar',operator='intlevel,300')
derive('*','NO3_1000m','ccdo','NO3_onevar',operator='intlevel,1000')
derive('*','NO3_2500m','ccdo','NO3_onevar',operator='intlevel,2500')

derive('*','PO4_onevar','cncks','PO4')
derive('*','PO4_surf','ccdo','PO4_onevar',operator='sellevidx,1')
derive('*','PO4_300m','ccdo','PO4_onevar',operator='intlevel,300')
derive('*','PO4_1000m','ccdo','PO4_onevar',operator='intlevel,1000')
derive('*','PO4_2500m','ccdo','PO4_onevar',operator='intlevel,2500')

derive('*','O2_onevar','cncks','O2')
derive('*','O2_surf','ccdo','O2_onevar',operator='sellevidx,1')
derive('*','O2_300m','ccdo','O2_onevar',operator='intlevel,300')
derive('*','O2_1000m','ccdo','O2_onevar',operator='intlevel,1000')
derive('*','O2_2500m','ccdo','O2_onevar',operator='intlevel,2500')

derive('*','Si_onevar','cncks','Si')
derive('*','Si_surf','ccdo','Si_onevar',operator='sellevidx,1')
derive('*','Si_300m','ccdo','Si_onevar',operator='intlevel,300')
derive('*','Si_1000m','ccdo','Si_onevar',operator='intlevel,1000')
derive('*','Si_2500m','ccdo','Si_onevar',operator='intlevel,2500')

derive('*','tod','ccdo','thetao_onevar',operator='intlevel,50,100,250,500,1000,2000')
derive('*','sod','ccdo','so_onevar',operator='intlevel,50,100,250,500,1000,2000')



# -- Land surfaces
derive("IGCM_OUT", 'auto_resp', 'plus', 'growth_resp', 'maint_resp')
derive("IGCM_OUT", 'autoresp', 'plus', 'growth_resp', 'maint_resp')

# -- GPP total ready for comparison with obs
#calias("IGCM_OUT", 'cfracgpp', 'gpp' ,filenameVar='stomate_ipcc_history')
#derive("IGCM_OUT", 'gpptot', 'divide', 'cfracgpp','Contfrac')
# -> alias for the obs
#calias("ref_climatos", 'gpptot', 'gpp')

# -- Atmospheric Variables on vertical levels
for tmpvar in ['ua', 'va', 'ta', 'hus', 'hur', 'zg']:
    for tmplev in ['850', '700', '500', '200']:
        derive('*', tmpvar+tmplev, 'ccdo', tmpvar, operator='intlevel,'+tmplev+'00')

# ua, va et ta sur moyenne sectorielle Atl
Atl_sect = '-60,-15,-90,90'
derive('*', 'ua_Atl_sect', 'ccdo', 'ua', operator='sellonlatbox,'+Atl_sect)
derive('*', 'va_Atl_sect', 'ccdo', 'va', operator='sellonlatbox,'+Atl_sect)
derive('*', 'ta_Atl_sect', 'ccdo', 'ta', operator='sellonlatbox,'+Atl_sect)
derive('*', 'hus_Atl_sect', 'ccdo', 'hus', operator='sellonlatbox,'+Atl_sect)





