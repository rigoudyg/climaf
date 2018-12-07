from climaf.api import *

# -- easyCMIP_functions contains an ensemble of functionalities for
# -- an easy access and exploration of CMIP data, especially on Ciclad/CLIMERI



def ensemble_one_keyword(req_dict):
    '''
    ensemble_one_keyword takes a dictionary containing the same arguments
    as ds() or eds(), but it is possible to set EITHER:
       - model='*'
       - simulation='*'
       - member='*'
    It returns a CliMAF ensemble with all the datasets matching the request.
    
    Example:
    >>> req_dict = dict(project='CMIP5',
                        model='*',
                        experiment='historical',
                        variable='pr',
                        period='1980',
                        frequency='monthly',
                        )
    >>> my_ens = ensemble_one_keyword(req_dict)
    >>> summary(my_ens)
    
    '''
    # -- Check the wildcards
    #keys = []
    key=None
    for elt in req_dict:
        if req_dict[elt]=='*':
            key = elt
    req = ds(**req_dict)
    if not key:
        return req

    # -- Get unique values
    members = []
    #for key in keys:
    # -- 1. On recupere toutes les valeurs disponibles
    if key=='model': index_kw = 6
    if key in ['simulation','member']: index_kw = 11
    for pathfilename in str.split(req.baseFiles(),' '):
        value = str.split(pathfilename,'/')[index_kw]
        if value not in members: members.append(value)
    #
    # -- If models, on refait la requete avec eds()
    if members:
        ens_req_dict = req_dict.copy()
        ens_req_dict.update({key:members})
    ens_req = eds(**ens_req_dict)

    return ens_req



def ensemble_request(req_dict):
    '''
    ensemble_request takes a dictionary containing the same arguments
    as ds() or eds(), but it is possible to set:
       - model, simulation, member to '*' or a list
       - variable, period to a list (not to '*')
    It returns a CliMAF ensemble with all the datasets matching the request.
    
    Example:
    >>> req_dict = dict(project='CMIP5',
                        model='*',
                        experiment='historical',
                        variable=['tas','pr'],
                        period=['1980','1990'],
                        frequency='monthly',
                        )
    >>> my_ens = ensemble_request(req_dict)
    >>> summary(my_ens)
    
    '''
    
    keys = []
    for elt in req_dict:
        if req_dict[elt]=='*' or isinstance(req_dict[elt],list):
            keys.append(elt)
    #
    wreq_dict = req_dict.copy()

    # -- Traitement de multiples periodes et variables
    period_variable_dict = dict()
    if 'period' in keys:
        periods = req_dict['period']
        if periods=='*':
            print "Sorry, but period='*' is not allowed. Provide either one period or a list of periods."
            return ""
        wreq_dict.update(dict(period=req_dict['period'][0]))
    else:
        periods = [req_dict['period']]
    if 'variable' in keys:
        variables = req_dict['variable']
        wreq_dict.update(dict(variable=req_dict['variable'][0]))
        if variables=='*':
            print "Sorry, but variable='*' is not allowed. Provide either one variable or a list of variables."
            print "If you want to check the available variables for your request, do it on only one "
            print "model, simulation and period using summary( ds(**req_dict) ) or ds(**req_dict).baseFiles()"
            return ""
    else:
        variables = [req_dict['variable']]
    #
    if 'period' in keys or 'variable' in keys:
        for period in periods:
            for variable in variables:
                period_variable_name = ''
                if 'variable' in keys:
                    period_variable_name = variable
                    if 'period' in keys:
                        period_variable_name += '_'+str(period)
                else:
                    period_variable_name = str(period)
                period_variable_dict.update({period_variable_name:dict(period=str(period), variable=variable)})

    if 'model' in keys:
        if 'simulation' in wreq_dict:
            wreq_dict.pop('simulation')
        if 'member' in wreq_dict:
            wreq_dict.pop('member')           
        available_models = ensemble_one_keyword(wreq_dict).order
    else:
        available_models = [req_dict['model']]
    #
    
    total_ens = None
    total_ens_names = []
    #
    # On va faire une boucle sur tous les modeles trouves (un seul si on n'a pas demande tous les modeles)
    for model in available_models:
        # Si on a demande plusieurs simulations/members, on fait une requete sur tout l'existant
        # Sinon, on utilise celle qui est passee par l'utilisateur, ou on utilise celle par defaut
        # si elle n'est pas renseignee (donc, on ne modifie pas wreq_dict)
        if 'simulation' in keys or 'member' in keys:
            if 'simulation' in keys: member_kw = 'simulation'
            if 'member' in keys: member_kw = 'member'
            wreq_dict.update({'model':model, member_kw:'*'})
        else:
            wreq_dict.update({'model':model})
        #
        # On fait la requete, et on recuperera tous les membres correspondant a la requete,
        # cad soit un, soit une liste, soit tous
        tmp_sub_ens = ensemble_one_keyword(wreq_dict)
        if len(available_models)>1 and isinstance(tmp_sub_ens, cens):
            sub_ens = add_prefix_suffix_to_ens_req(tmp_sub_ens, prefix=model+'_')
        else:
            sub_ens = tmp_sub_ens
        #
        multi_periods_variables_sub_ens_dict = dict()
        multi_periods_variables_sub_ens_names = []                
        #
        # On fait maintenant une boucle sur tous les membres si on a demande plusieurs
        # periodes, variables
        if period_variable_dict:
            for member in sub_ens:
                for period_variable in period_variable_dict:
                    tmp_dict = sub_ens[member].kvp
                    tmp_dict.update(**period_variable_dict[period_variable])
                    multi_periods_variables_sub_ens_names.append(member+'_'+period_variable)
                    multi_periods_variables_sub_ens_dict.update({member+'_'+period_variable:ds(**tmp_dict)})
            multi_periods_variables_sub_ens = cens(multi_periods_variables_sub_ens_dict,
                                                   order=multi_periods_variables_sub_ens_names)
            if multi_periods_variables_sub_ens_dict:
                sub_ens = multi_periods_variables_sub_ens
        if total_ens:
            if isinstance(sub_ens,cens):
                total_ens.update(sub_ens)
                total_ens_names = total_ens_names + sub_ens.order
            else:
                total_ens.update({model:sub_ens})
                total_ens_names.append(model)
        else:
            if isinstance(sub_ens,cens):
                total_ens = sub_ens.copy()
                total_ens_names = sub_ens.order
            else:
                total_ens = {model:sub_ens}
                total_ens_names = [model]
    if isinstance(total_ens,dict):
        total_ens = cens(total_ens, order=total_ens_names)
    if isinstance(total_ens,cens):
        total_ens.set_order(total_ens_names)

    return total_ens

def save_req_file(ens_obj, filename = 'test.txt', separator = ' '):
    '''
    save_req_file is used to save the list of netcdf files associated with a CliMAF ensemble
    in a txt or json file, tagged with their names from the ensemble.
    It takes as arguments: a CliMAF ensemble, a filename (optional), and a separator (only for txt)
    
    Examples:
    >>> my_ens = ensemble_request(req_dict) # -- see help(ensemble_request)
    >>> save_req_file(my_ens, filename='my_pretreated_files.txt')
    >>> save_req_file(my_ens, filename='my_pretreated_files_bis.txt', separator=';')
    >>> save_req_file(my_ens, filename='my_pretreated_files.json')

    '''
    if '.txt' in filename:
        file = open(filename,"w") 
        for elt in ens_obj.order:
            print elt+separator+cfile(ens_obj[elt])
            file.write(elt+separator+cfile(ens_obj[elt])+' \n') 
        file.close()
    if '.json' in filename:
        import json
        json_dict = dict()
        for elt in ens_obj.order:
            print elt+separator+cfile(ens_obj[elt])
            json_dict.update({elt:cfile(ens_obj[elt])})
        with open(filename, 'w') as outfile:
            json.dump(json_dict, outfile, indent = 4) 

def add_str_to_list_elements(my_list, my_str):
    '''
    This function adds a string (second argument) to all the elements of a list (first argument)
    
    Example:
    >>> my_list = ['model1','model2']
    >>> add_str_to_list_elements(my_list, '_tas')
    '''
    new_list = []
    for elt in my_list: new_list.append(elt+my_str)
    return new_list

def add_prefix_suffix_to_ens_req(ens_obj, prefix='', suffix=''):
    '''
    add_prefix_suffix_to_ens_req adds a prefix and/or a suffix string to
    the names of the members of a CliMAF ensemble. It is very useful to rename
    the members of an ensemble.
    It returns the renamed ensemble.
    
    Example:
    >>> my_ens = ensemble_request(req_dict) # -- see help(ensemble_request)
    >>> renamed_ens = add_prefix_suffix_to_ens_req(my_ens, prefix='tas_', suffix='_myperiod')
    '''
    new_ens_dict =dict()
    new_names = []
    for elt in ens_obj.order:
        new_names.append( prefix+elt+suffix )
        new_ens_dict.update( {prefix+elt+suffix: ens_obj[elt]} )
    new_ens = cens(new_ens_dict, order=new_names)
    new_ens.set_order(new_names)
    
    return new_ens


def merge_climaf_ensembles(ens_list=[]):
    '''
    Simply merges a list ens_list of CliMAF ensembles, keeping the order of the members
    in the order of the list.
    
    Example:
    >>> my_hist_ens = ensemble_request(hist_dict) # -- see help(ensemble_request)
    >>> my_rcp85_ens = ensemble_request(rcp85_dict) # -- see help(ensemble_request)
    >>> my_merged_ens = merge_climaf_ensembles(ens_list=[my_hist_ens,my_rcp85_ens])
    '''
    if ens_list:
        merged_ens = ens_list[0].copy()
        merged_names = ens_list[0].order
        for ens in ens_list[1:len(ens_list)]:
            merged_ens.update(ens)
            merged_names += ens.order
        merged_ens.set_order(merged_names)
        return merged_ens
    else:
        print 'Provide a list of ensembles to merge together'
        

def check_time_consistency_CMIP(dat, return_available_period=False):
    ''' Check if the period found by CliMAF actually covers the request period
        If yes, returns True.
        If not, returns False.
        If not, and return_available_period=True, returns the period actually available in your request.
    '''
    #
    # -- First, get the period available among the listed files
    startyears = []
    endyears = []
    for tmpf in str.split(dat.baseFiles(),' '):
        dum = str.split(tmpf,'_')
        tmpf_period = str.replace(dum[-1],'.nc','')
        startdate = str.split(tmpf_period,'-')[0]
        enddate = str.split(tmpf_period,'-')[1]
        startyears.append(int(startdate[0:4]))
        endyears.append(int(enddate[0:4]))
    first_available_year = sorted(startyears)[0]
    last_available_year = sorted(endyears)[-1]
    #
    # -- Then, get the start year and end year of the request
    req_period = str.replace(str(dat.period),'_','-')
    #
    start_req_date = str.split(req_period,'-')[0]
    end_req_date = str.split(req_period,'-')[1]
    #
    start_req_year = int(start_req_date[0:4])
    end_req_year = int(end_req_date[0:4])
    #
    # -- Eventually, check if the requested period is covered by the listed files
    #    -> If yes, return True
    #    -> If not, return False
    if start_req_year>=first_available_year and end_req_year<=last_available_year:
        check=True
        if return_available_period:
            return req_period
    else:
        check=False
        if return_available_period:
            if start_req_year<=first_available_year:
                available_period = str(first_available_year)
            else:
                available_period = str(start_req_year)
            if end_req_year>=last_available_year:
                available_period += '-'+str(last_available_year)
            else:
                available_period += '-'+str(end_req_year)
            return available_period
    return check


