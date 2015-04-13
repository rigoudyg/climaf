"""
Management of CliMAF standard projects

"""

import climaf
from climaf.classes import cproject, cprojects

def init_standard_projects():
    """ 
    Define attributes (above experiment, variable, domain, period ) for CliMAF 
    standard projects : CMIP5, EM, OCMIP5_Ciclad, OBS4MIPS, OBS_CAMI

    Invoked by standard CliMAF API setup

    The cprojects list also show in variable :ref:`~climaf.classes.cprojects`
    """
    cproject("CMIP5"   ,"model","rip","frequency","table","realm","version")
    cproject("OCMIP5"                ,"frequency"                          )
    cproject("OBS4MIPS"              ,"frequency"                          )
    cproject("CAMIOBS"                                                     , separator="_")
    cproject("EM"                    ,"frequency",        "realm"          )
    cproject("example"               ,"frequency"                          )


