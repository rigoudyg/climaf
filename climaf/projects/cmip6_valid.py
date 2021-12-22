from env.environment import cprojects
    
    
def set_CMIP6_valid_values(project):

    # No list of valid values for : root, realization, version

    proj = cprojects[project]
    
    proj.cvalid('institute', [ 'AS-RCEC', 'CCCma', 'CSIRO-ARCCSS', 'INM', 'MPI-M',
                          'NIMS-KMA', 'UA', 'AWI', 'CCCR-IITM', 'E3SM-Project',
                          'IPSL', 'MRI', 'NOAA-GFDL', 'BCC', 'CMCC', 'EC-Earth-Consortium',
                          'KIOST', 'NASA-GISS,' 'NUIST', 'CAMS', 'CNRM-CERFACS',
                          'FIO-QLNM', 'MIROC', 'NCAR', 'SNU',' CAS', 'CSIRO',
                          'HAMMOZ-Consortium', 'MOHC', 'NCC', 'THU' ] )
    proj.cvalid('model', [ "UKESM1-0-LL", "HadGEM3-GC31-LL", "MRI-ESM2-0",
                      "EC-Earth3", "EC-Earth3-AerChem", "ACCESS-ESM1-5", "ACCESS-CM2",
                      "MIROC6", "CNRM-CM6-1", "CNRM-ESM2-1", "MPI-ESM1-2-LR", "MPI-ESM-1-2-HAM",
                      "NorESM2-LM", "NorESM2-MM", "GFDL-ESM4", "GFDL-CM4", "IPSL-CM6A-LR",
                      "4AOP-v1-5", "IPSL-CM6A-LR-INCA", "CESM2-WACCM", "CESM2", "GISS-E2-1-G",
                      "CanESM5", "CMCC-ESM2", "CMCC-CM2-SR5", "FIO-ESM-2-0", "MIROC-ES2L",
                      "TaiESM1-TIMCOM", "FGOALS-f3-L", "CAS-ESM2-0", "CanESM5-CanOE",
                      "HadGEM3-GC31-MM", "BCC-CSM2-MR", "MPI-ESM1-2-HR", "NorCPM1",
                      "CESM1-1-CAM5-CMIP5", "BCC-ESM1", "MIROC-ES2H-NB", "IPSL-CM5A2-INCA",
                      "AWI-CM-1-1-MR", "MCM-UA-1-0", "CAMS-CSM1-0", "E3SM-1-1", "EC-Earth3-CC",
                      "EC-Earth3-Veg-LR", "EC-Earth3-Veg", "NESM3", "KACE-1-0-G",
                      "CNRM-CM6-1-HR", "KIOST-ESM", "IITM-ESM", "INM-CM5-0", "INM-CM4-8",
                      "CIESM", "FGOALS-g3", "TaiESM1", "GISS-E2-1-H", "GISS-E2-2-G",
                      "AWI-ESM-1-1-LR", "EC-Earth3-LR", "NorESM1-F", "E3SM-1-1-ECA",
                      "GISS-E2-1-G-CC", "CMCC-CM2-HR4", "E3SM-1-0", "EC-Earth3P-VHR",
                      "SAM0-UNICON", "MIROC-ES2H", "GFDL-AM4", "CESM2-WACCM-FV2",
                      "CESM2-FV2", "CMCC-CM2-VHR4", "EC-Earth3P", "EC-Earth3P-HR",
                      "BCC-CSM2-HR", "NICAM16-7S", "NICAM16-8S", "ECMWF-IFS-MR", "ECMWF-IFS-LR",
                      "ECMWF-IFS-HR", "MPI-ESM1-2-XR", "INM-CM5-H", "IPSL-CM6A-ATM-HR",
                      "IPSL-CM7A-ATM-LR", "IPSL-CM7A-ATM-HR", "CESM1-CAM5-SE-LR", "CESM1-CAM5-SE-HR"])
    proj.cvalid('mip', ['AerChemMIP', 'C4MIP', 'CDRMIP', 'CFMIP', 'CMIP', 'DAMIP', 'DCPP',
                        'GeoMIP', 'GMMIP', 'HighResMIP', 'LS3MIP', 'LUMIP', 'OMIP', 'PAMIP',
                        'PMIP', 'RFMIP', 'ScenarioMIP' ])
    proj.cvalid('grid', ["gr", "gn", "gr1", "gr2"])
    proj.cvalid('experiment', ["piClim-lu", "piClim-ghg", "piClim-anthro", "piClim-4xCO2", "piClim-control", "piClim-histghg", "piClim-histaer", "piClim-aer", "piClim-histall", "piClim-histnat", "piClim-spAer-aer", "piClim-spAer-histall", "piClim-spAer-anthro", "hist-spAer-all", "rad-irf", "omip1", "dcppB-forecast", "dcppA-hindcast", "dcppA-assim", "dcppC-amv-neg", "dcppC-amv-pos", "dcppC-ipv-neg", "dcppC-ipv-NexTrop-neg", "dcppC-pac-control", "dcppC-amv-ExTrop-neg", "dcppC-ipv-NexTrop-pos", "dcppC-pac-pacemaker", "dcppC-atl-pacemaker", "dcppC-amv-Trop-pos", "dcppC-ipv-pos", "dcppC-atl-control", "dcppC-amv-Trop-neg", "dcppC-amv-ExTrop-pos", "ssp370", "hist-piAer", "ssp370-lowNTCF", "piClim-2xdust", "piClim-NH3", "piClim-BC", "piClim-OC", "piClim-2xss", "piClim-SO2", "amip-hist-EXT", "amip-TIP", "amip-hist", "ssp119", "ssp245", "ssp534-over", "ssp585", "ssp434", "ssp126", "ssp460", "pdSST-pdSIC", "pdSST-futArcSIC", "piSST-piSIC", "pdSST-piAntSIC", "futSST-pdSIC", "pdSST-futBKSeasSIC", "pdSST-piArcSIC", "piSST-pdSIC", "pdSST-futAntSIC", "pdSST-futOkhotskSIC", "G6sulfur", "G1", "G7cirrus", "G6solar", "amip-piForcing", "abrupt-2xCO2", "amip", "abrupt-0p5xCO2", "aqua-p4K", "piSST-4xCO2", "piSST", "piSST-pxK", "a4SSTice", "amip-4xCO2", "amip-p4K", "abrupt-solp4p", "amip-m4K", "amip-a4SST-4xCO2", "piSST-4xCO2-rad", "a4SSTice-4xCO2", "a4SST", "aqua-p4K-lwoff", "aqua-control", "aqua-4xCO2", "aqua-control-lwoff", "abrupt-solm4p", "amip-p4K-lwoff", "amip-future4K", "amip-piForcing-EXT", "amip-lwoff", "hist-GHG", "hist-aer", "hist-nat", "hist-stratO3", "ssp245-GHG", "ssp245-nat", "land-hist-cruNcep", "land-hist", "amip-lfmip-rmLC", "amip-lfmip-pdLC", "hist-noLu", "ssp370-ssp126Lu", "ssp126-ssp370Lu", "deforest-globe", "land-noLu", "land-cCO2", "past1000", "midHolocene", "lig127k", "lgm", "midPliocene-eoi400", "1pctCO2-rad", "esm-ssp585", "1pctCO2-bgc", "ssp534-over-bgc", "hist-bgc", "ssp585-bgc", "abrupt-4xCO2", "historical", "esm-hist", "piControl", "esm-piControl", "1pctCO2", "historical-EXT", "piControl-spinup", "esm-ssp534-over", "hist-1950", "highresSST-present", "spinup-1950", "control-1950", ])
    proj.cvalid('table', ['3hr', '6hrLev', '6hrPlev', '6hrPlevPt', 'AERday', 'AERhr', 'AERmon', 'AERmonZ', 'Amon', 'CF3hr', 'CFday', 'CFmon', 'CFsubhr', 'day', 'E1hr', 'E3hr', 'Eday', 'EdayZ', 'Efx', 'Emon', 'EmonZ', 'fx', 'LImon', 'Lmon', 'Oday', 'Ofx', 'Omon', 'SIday', 'SImon'])
