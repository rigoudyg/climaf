from CM_atlas import *


# -- Function for ORCHIDEE

def derive_var_PFT(var, project='IGCM_OUT'):
    dum = str.split(var, 'PFT')
    wvariable = str.replace(dum[0], '_', '')
    dumPFTnumber = dum[len(dum) - 1]
    if dumPFTnumber == '_tot':
        derive(project, var, 'ccdo', wvariable, operator='vertsum -selname,' + wvariable)
    else:
        dum2 = str.split(dumPFTnumber, '_')
        PFTnumbers = dum2[1:len(dum2)]
        for PFTnumber in PFTnumbers:
            if PFTnumber == PFTnumbers[0]:
                selection = '-d veget,' + str(int(PFTnumber) - 1)
            else:
                selection = selection + ' -d veget,' + str(int(PFTnumber) - 1)
        #
        if len(PFTnumbers) > 1:
            derive(project, 'dum_' + var, 'select_veget_types', wvariable, selection=selection)
            derive(project, var, 'ccdo', 'dum_' + var, operator='vertsum -selname,dum_' + var)
        else:
            derive(project, var, 'select_veget_types', wvariable, selection=selection)
