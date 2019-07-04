from climaf.api import *
import os
import copy

# -- Si je veux choisir ma periode, et qu'elle soit la meme entre les TS et les climato
#    -> frequency='monthly', period='1980-2000'
# -- Si je veux utiliser les SE:
#    -> frequency='seasonal', clim_period='1980_1989'
# -- Si je veux utiliser les SE pour les climatos, et choisir ma periode pour les TS:
#    -> frequency='seasonal', clim_period='1980_1989', ts_period='full'
# -- Si je veux le dernier SE pour les climatos, et choisir ma periode pour les TS:
#    -> frequency='seasonal', clim_period='last', ts_period='full'
# -- Si je veux toute la periode pour les TS, et seulement une selection pour les climatos (ne pas tout utiliser)
#    -> frequency='monthly', clim_period='last_30Y', ts_period='full'
#    -> frequency='monthly', clim_period='1980_2005', ts_period='full'

# -- En amont du diag, il faut faire la difference entre diag 'clim' ou diag 'TS'
import copy


def period_for_diag_manager(DAT_DICT, diag=''):
    """ In a python dictionary dat_dict defining a CliMAF dataset, """
    ''' this function updates:                                     '''
    '''   - period with dat_dict[diag+'_period']                   '''
    '''   - ts_period with dat_dict[diag+'_ts_period']             '''
    '''   - clim_period with dat_dict[diag+'_clim_period']         '''
    ''' In the context of a CliMAF atlas, it allows choosing the   '''
    ''' period for each diagnostic.                                '''
    '''                                                            '''
    ''' Returns the updated dictionary.                            '''

    def period_update_dict(DAT_DICT, diag):
        wdat_dict = copy.deepcopy(DAT_DICT)
        if diag + '_frequency' in wdat_dict:
            wdat_dict.update(dict(frequency=wdat_dict[diag + '_frequency']))
        if diag + '_period' in wdat_dict:
            wdat_dict.update(dict(period=wdat_dict[diag + '_period']))
        if diag + '_clim_period' in wdat_dict:
            wdat_dict.update(dict(clim_period=wdat_dict[diag + '_clim_period']))
        if diag + '_ts_period' in wdat_dict:
            wdat_dict.update(dict(ts_period=wdat_dict[diag + '_ts_period']))
        return wdat_dict

    print ''
    if isinstance(DAT_DICT, dict):
        return period_update_dict(dat_dict, diag)
    if isinstance(DAT_DICT, list):
        WDAT_DICT = copy.deepcopy(DAT_DICT)
        for dat_dict in WDAT_DICT:
            dat_dict.update(period_update_dict(dat_dict, diag))
        return WDAT_DICT


def base_variable_of_derived_variable(tested_variable, project='*'):
    """ Returns one of the variables used to compute a derived variable """
    project_derived_variables = copy.deepcopy(derived_variables['*'])
    if project in derived_variables:
        project_derived_variables.update(derived_variables[project])
    while tested_variable in project_derived_variables.keys():
        for elt in project_derived_variables[tested_variable]:
            if isinstance(elt, list):
                base_var = elt[0]
        tested_variable = base_var
    return tested_variable


def frequency_manager_for_diag(model, diag='TS'):
    if 'frequency' in model:
        # -- Diagnostics on TS
        if diag.upper() == 'TS':
            model.update(dict(diag=diag))
            if 'ts_period' in model:
                model.update(dict(period=model['ts_period']))
            if 'ts_frequency' in model:
                model['frequency'] = model['ts_frequency']
            else:
                model['frequency'] = 'monthly'
        # -- Diagnostics on SE
        if diag.upper() in ['SE', 'CLIM']:
            model.update(dict(diag=diag))
            # -- Fix to avoid errors when clim_period contains a - instead of _
            if 'clim_period' in model:
                model.update(dict(clim_period=str.replace(model['clim_period'], '-', '_')))
                # -- If frequency=='monthly' or 'yearly', we use clim_period for period
                if model['frequency'] in ['daily', 'monthly', 'yearly']:
                    if 'SE' in model['clim_period']:
                        model.update({'frequency': 'seasonal'})
                    else:
                        model.update(dict(period=model['clim_period']))
    print "model in frequency_manager = ", model
    return ''


def get_period_manager(dat_dict):
    # -- dealing with the Time Series : period = 'full', 'first_??Y', 'last_??Y'
    if 'frequency' not in dat_dict:
        ds_dat_dict = ds(**dat_dict)
        dat_dict.update(dict(frequency=ds_dat_dict.kvp['frequency']))
    if dat_dict['frequency'] in ['daily', 'monthly', 'yearly']:
        # if 'period' in dat_dict:
        #  period = dat_dict['period']
        # else:
        if 'diag' in dat_dict:
            if dat_dict['diag'].upper() in ['SE', 'CLIM'] and 'clim_period' in dat_dict:
                period = dat_dict['clim_period']
            else:
                if 'ts_period' in dat_dict:
                    period = dat_dict['ts_period']
                else:
                    period = dat_dict['period']
        else:
            if 'ts_period' in dat_dict:
                period = dat_dict['ts_period']
            else:
                period = dat_dict['period']
        if period.upper() == 'FULL' or 'LAST_' in period.upper() or 'FIRST_' in period.upper():
            # -- request for all the files
            req_dict = dat_dict.copy()
            # -> Check if the variable is a derived variable; if yes, returns one variable it is based on
            # -> Will be used only for the request
            tested_variable = req_dict['variable']
            req_dict.update(dict(variable=base_variable_of_derived_variable(tested_variable, req_dict['project'])))
            req_dict.update(dict(period='0001-9998'))
            req = ds(**req_dict)

            # -- Files found
            if not req.baseFiles():
                print 'No File found for ', req_dict
            else:
                # -- Get the syntax
                # syntax = req['kwp']['filename_syntax']
                # file_separator = req['kwp']['filename_separator']
                # period_separator = req['kwp']['period_separator']
                # test = str.split(syntax, file_separator)
                # for test_elt in test:
                #  if '${start_year}' in test_elt:
                #     index_start_year = test.index(test_elt)
                #  if '${end_year}' in test_elt:
                #     index_end_year = test.index(test_elt)
                # -- Si c'est le meme, il faut utiliser period_separator
                # -- Si il n'y a pas de period_separator, on coupe la string en deux, et on prend les 4 premiers
                # characteres de chaque moitie
                # -- puis on se sert des index pour extraire les periodes.
                # -- Sinon, on recupere la periode en lisant dans le fichier?
                files = list(set(str.split(req.baseFiles(), ' ')))
                # -- Find the last period covered by an annual cycle
                start_periods = []
                end_periods = []
                for file in files:
                    # Get the file name
                    filename = os.path.basename(file)
                    # Find the period
                    # !!! SOLUTION A LA MAIN, IGCM_OUT
                    filename_elts = str.split(filename, '_')
                    if 'MIP' in dat_dict['project']:
                        tmpperiod = str.replace(filename_elts[len(filename_elts) - 1], '.nc', '')
                        start_period = str.split(tmpperiod, '-')[0]
                        end_period = str.split(tmpperiod, '-')[1]
                    else:
                        start_period = filename_elts[1]
                        end_period = filename_elts[2]
                    start_periods.append(int(start_period[0:4]))
                    end_periods.append(int(end_period[0:4]))
                #
                # -- Sort the results to find the last start date
                sorted_end_periods = sorted(end_periods, reverse=True)
                last_end_period = sorted_end_periods[0]
                sorted_start_periods = sorted(start_periods)
                first_start_period = sorted_start_periods[0]
                sorted_start_periods_2 = sorted(start_periods, reverse=True)
                last_start_period = sorted_start_periods_2[0]
                # If period='full':
                if period.upper() == 'FULL':
                    dat_dict['period'] = str(first_start_period) + '_' + str(last_end_period)
                # If period='last_??Y':
                if 'LAST_' in period.upper():
                    prd_lgth = int(str.replace(str.replace(period.upper(), 'LAST_', ''), 'Y', ''))
                    # first_start_period = last_end_period - prd_lgth + 1
                    # first_start_period = max([last_end_period - prd_lgth + 1, last_start_period])
                    wfirst_start_period = max([last_end_period - prd_lgth + 1, first_start_period])
                    dat_dict['period'] = str(wfirst_start_period) + '_' + str(last_end_period)
                # If period='first_??Y':
                if 'FIRST_' in period.upper():
                    prd_lgth = int(str.replace(str.replace(period.upper(), 'FIRST_', ''), 'Y', ''))
                    last_end_period = first_start_period + prd_lgth - 1
                    dat_dict['period'] = str(first_start_period) + '_' + str(last_end_period)
    print 'dat_dict in get_period_manager = ', dat_dict
    #
    if dat_dict['frequency'] in ['seasonal', 'annual_cycle']:
        if 'clim_period' not in dat_dict:
            dat_dict.update(dict(clim_period='*'))
        else:
            clim_period = dat_dict['clim_period']
            if 'LAST' in clim_period.upper() or 'FIRST' in clim_period.upper():
                # -- request for all the files
                req_dict = dat_dict.copy()
                # -> Check if the variable is a derived variable; if yes, returns one variable it is based on
                # -> Will be used only for the request
                tested_variable = req_dict['variable']
                req_dict.update(dict(variable=base_variable_of_derived_variable(tested_variable, req_dict['project'])))
                req_dict.update(dict(clim_period='????_????'))
                req = ds(**req_dict)
                # -- Files found
                if not req.baseFiles():
                    print 'No File found for ', req_dict
                else:
                    files = list(set(str.split(req.baseFiles(), ' ')))
                    # -- Find the last period covered by an annual cycle
                    start_periods = []
                    for file in files:
                        # Get the file name
                        filename = os.path.basename(file)
                        # Find the period
                        # !!! SOLUTION A LA MAIN, uniquement pour IGCM_OUT
                        filename_elts = str.split(filename, '_')
                        start_period = filename_elts[2]
                        start_periods.append(int(start_period))
                    #
                    # -- Sort the results to find the last start date
                    sorted_start_periods = sorted(start_periods, reverse=True)
                    first_period = sorted_start_periods[len(sorted_start_periods) - 1]
                    last_period = sorted_start_periods[0]
                    # -- Treat either first or last file
                    if clim_period.upper() in ['LAST', 'LAST_SE']:
                        last_file = []
                        for file in files:
                            if '_' + str(last_period) + '_' in file:
                                last_file.append(file)
                        # -- If we found more than one file, we print an error (but don't stop)
                        if len(last_file) > 1:
                            print '--- Warning: found ', len(last_file), ' for last file'
                            print 'last_file = ', last_file
                        filename = os.path.basename(last_file[0])
                        filename_elts = str.split(filename, '_')
                        last_clim_period = filename_elts[2] + '_' + filename_elts[3]
                        dat_dict['clim_period'] = last_clim_period
                    if clim_period.upper() in ['FIRST', 'FIRST_SE']:
                        first_file = []
                        for file in files:
                            if '_' + str(first_period) + '_' in file:
                                first_file.append(file)
                        # -- If we found more than one file, we print an error (but don't stop)
                        if len(first_file) > 1:
                            print '--- Warning: found ', len(first_file), ' files for first file'
                            print 'first_file = ', first_file
                        filename = os.path.basename(first_file[0])
                        filename_elts = str.split(filename, '_')
                        first_clim_period = filename_elts[2] + '_' + filename_elts[3]
                        dat_dict['clim_period'] = first_clim_period
                        #
    # Garde fou
    if 'period' in dat_dict:
        if 'LAST' in dat_dict['period'].upper() or 'FIRST' in dat_dict['period'].upper() or\
                'FULL' in dat_dict['period'].upper():
            dat_dict['period'] = 'fx'
    return ''


def find_common_period(models, common_period_variable, common_clim_period):
    last_available_periods = []
    startyear_last_available_periods = []
    common_period_models = []
    for model in models:
        wmodel = model.copy()
        if 'clim_period' in model:
            if model['clim_period'] == 'common_clim_period':
                wmodel.update(dict(variable=common_period_variable, clim_period=common_clim_period))
                frequency_manager_for_diag(wmodel, diag='SE')
                get_period_manager(wmodel)
                cp_model = ''
                if 'model' in wmodel:
                    cp_model = wmodel['model'] + ' '
                if 'simulation' in wmodel:
                    cp_model = cp_model + wmodel['simulation']
                common_period_models.append(cp_model)
                if model['frequency'] == 'monthly':
                    wperiod = wmodel['period']
                if model['frequency'] == 'seasonal':
                    wperiod = wmodel['clim_period']
                print wmodel
                print wperiod
                last_available_periods.append(wperiod)
                startyear_last_available_periods.append(int(wperiod[0:4]))
    #
    # -- find the last available period
    sorted_periods = sorted(startyear_last_available_periods)
    last_available_period = last_available_periods[startyear_last_available_periods.index(sorted_periods[0])]
    #
    # -- Now update the model dictionaries with the common period that we found:
    for model in models:
        if 'clim_period' in model:
            if model['clim_period'] == 'common_clim_period':
                model.update(dict(clim_period=last_available_period))
        print '--> Updated model with common period found accross all simulations:'
        print model
    #
    print '==> Model with earliest last available clim_period = ' + common_period_models[
        startyear_last_available_periods.index(sorted_periods[0])]
    return models
