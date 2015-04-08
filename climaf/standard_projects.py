"""
Management of CliMAF standard projects

"""

import climaf
from climaf.classes import cproject, cprojects

def init_standard_projects():
    """ 
    Define CliMAF standard projects : CMIP5, EM, OCMIP5_Ciclad, OBS4MIPS
    Invoked by standard CliMAF setup

    The cprojects list also show in variable 'cprojects'
    """
    cprojects=dict()
    cproject("CMIP5"   ,"model","rip","frequency","table","realm","version")
    cproject("OCMIP5"                ,"frequency"                          )
    cproject("EM"                    ,"frequency"                          )
    cproject("OBS_CAMI"                                                    )
    cproject("OBS4MIPS"              ,"frequency"                          )
