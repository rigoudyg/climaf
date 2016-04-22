import numpy as np
from climaf.api import *
from climaf.site_settings import onCiclad, atTGCC, onSpip
from plot_params import plot_params
from reference import variable2reference
import os
from getpass import getuser
from climaf.html import *

clog('critical')


def IGCM_syntax_to_CliMAF_facets(simulations):
    #
    dict = {
        'JobName':'simulation',
        'TagName':'model'
    }
    #
    for simulation in simulations:
        for kwd in dict:
            print kwd
            if kwd in simulation:
                print simulation[kwd]
                print dict[kwd]
                test = {dict[kwd]:simulations[kwd]}
                simulations.update(test)
    return simulations



def bias(dat1,dat2):
    """
    Computes the bias between dat1 and dat2.
    Returns a scalar (using cvalue)
    """
    return cvalue(compute_bias(dat1,dat2))


def CRMSE(dat1,dat2,variable=None):
    """
    Computes the Centered RMSE between dat1 and dat2 (RMSE with bias removed, as in a Taylor Diagram)
    Returns a scalar (using cvalue)
    """
    #cscript('compute_RMSE','cdo sqrt fldmean -timmean -sqr -sub -selvar,${var} ${in} -selvar,${var} ${in_2} ${out}')
    #cscript('compute_RMSE','cdo fldmean ${in} ${out}')
    meandat1 = str(cvalue(ccdo(dat1,operator='fldmean')))
    print '-- Average of dat1 = '+meandat1
    meandat2 = str(cvalue(ccdo(dat2,operator='fldmean')))
    print '-- Average of dat2 = '+meandat2
    # -- retrieve the mean of the field
    anomdat1 = ccdo(dat1,operator='subc,'+meandat1)
    anomdat2 = ccdo(dat2,operator='subc,'+meandat2)
    # -- Compute the difference and apply the square operator
    tmp = ccdo(minus(anomdat1,anomdat2),operator='sqr')
    # -- compute the mean
    tmp2 = ccdo(tmp,operator='fldmean')
    # -- And finally apply the square root
    return cvalue(ccdo(tmp2,operator='sqrt'))


# -- Normalized RMSE
def NRMSE(dat1,dat2):
    """
    Computes the Normalized Centered RMSE between dat1 and dat2 (normalized by the standard deviation of dat2)
    """
    # Centered RMSE normalized by the spatial standard deviation of the reference
    # -> Valid only for spatial fields!!! 
    std_dat = ccdo(dat2,operator='fldstd')
    return float(CRMSE(dat1,dat2))/float(cvalue(std_dat))



kwargs = {}

dataset_specs = {
    'climatology' : 'annual_mean'
    }#end dataset_specs
kwargs.update(dataset_specs)


diag_specs = {
    # -- Model-reference bias or model-model difference?
    #'context' : 'bias', # - model_model
    
    # -- Do you want the climatology next to the bias plot (True) or just the bias plots (False)?
    # -> Set to False if you have more than 5 simulations
    'plot_climato' : True,
    'plot_bias'    : True,
    'Metrics'      : False,
    'ref_contours' : False,
    
    # -- Display the plots in portrait or landscape
    'orientation' : 'landscape',
    'nrow':None,
    'ncol':None,
    
    
    }#end diag_specs
kwargs.update(diag_specs)


plot_specs = {
    ## -- CLIMATOLOGY
    # -- Plot Main Title
    'ClimPlotMainTitle' : 'Climatology ${variable} ${simulation}',
    
    # -- Plot Upper right title
    'ClimUpperRightTitle' : '${climatology}',
    
    # -- Plot Upper left title
    'ClimUpperLeftTitle' : '${period}',
    
    # -- Plot Center title
    'ClimCenterTitle' : '',

    ## -- BIAS PLOT
    # -- Plot Main Title
    'BiasPlotMainTitle' : '${simulation}',
    
    # -- Plot Upper right title
    'BiasUpperRightTitle' : '${climatology}',
    
    # -- Plot Upper left title
    'BiasUpperLeftTitle' : '${period}',
    
    # -- Plot Center title
    'BiasCenterTitle' : '',

    'mpCenterLonF':0,
    'vcb':False,                  # -> if True (False), color bar is vertical (horizontal)
    'tiMainFontHeightF':0.035,    # -> Font size for the title ; default is 0.025
    'gsnStringFontHeightF':0.022, # -> Font size of the subtitle ; default is 0.012
    'resolution':'1500x1500',     # -> Default resolution: 1024x1024
    'aux_options':None,           # -> NCL options to be passed to plot for an auxilliary field (used in the bias plot)
    'default_aux_options':None,   # -> Default aux_options that will be common to all the plots
    'options':None,               # -> NCL options to be passed to plot for the main field
    'default_options':None,       # -> Default options that will be common to all the plots
  
    # -- General plot specifs
    'plot_specs' : {
        },

}#end plot_specs
kwargs.update(plot_specs)


page_specs = {
    # -- Page title
    'page_title' : 'Bias map: ${variable} (vs ${product})',
    
    # -- Specifs affichage
    'title_specs' : {
        'gravity':'NorthWest',
        'ybox':80, 'pt':30,
        'x':30, 'y':40, 
        'font':'Waree-Bold',
        },#end title_specs 
    # pt => between ybox/4 and ybox/2
    # Interesting fonts : Waree-Bold, DejaVu-Sans-Condensed, Unikurd-Web-Regular,
    # UnDotum-Regular, PakTypeNaqsh-Regular, Nimbus-Sans-Bold, Nimbus-Mono-Bold,
    # FreeSans-Gras, Jomolhari-Regular, Khmer-OS-System-Regular
    
    }#end page_specs
kwargs.update(page_specs)


ref_specs = {
    'ref_project' : 'ref_climatos',
    
    # - If you want to specify a simulation as a reference, describe it in reference{} the same way as simulations
    # - If you don't just leave 'reference':{}
    'reference' : {},
    
    # -- Specify the remapping method
    #'remappingMethod':'remapbil' # Default == remapbil
    #'cdogrid'
    
    # -- Remap the simulation on the reference? Or inverse? (if cdogrid 
    'remapSimOnRef':True
    }#end ref_specs
kwargs.update(ref_specs)


atlas_specs = {
    # -- append the result with an existing atlas
    'append':False,                    # -- Set to True to append the result to an existing pdf file (either keep the same
                                       #    pdffile or use main_atlas_pdf, so you can use pdffile to give an explicit name to
                                       #    your intermediate atlases
    'remove_intermediate_atlas':False, # -- Removes the intermediate atlases
    'pdffile':'atlas.pdf',             # -- Name of the pdffile produced by the present call of the explorer
    'main_atlas_pdf':'main_atlas.pdf', # -- if main_atlas_pdf is different of pdffile, append will use main_atlas_pdf as
                                       #    the name of the final concatenated atlas
    'outdir' :'',                       # -- Output directory (default: current working directory)
    'hover':False
}
kwargs.update(atlas_specs)

kwargs.update({'thumbnail_size':400})

kwargs.update({'dods_cp':True})

kwargs.update({'significance_field':[]})
# shade_below, shade_above

kwargs.update({'add_wind_vectors':False})
# if True, we use ds() to get uas and vas to plot the vectors:
# - we get the files
# - compute the climatologies
# - remap the fields (if necessary)
# - add them to the plot instead of the auxillary file
# - need to pass also some options to control the vectors

def check_kwargs(kwargs):
    """
    Prints the pairs keyword - values defined in a kwargs dictionary
    """
    for k in kwargs:
        print '-- '+k
        print kwargs[k]


# -- Atlas explorer functions

# -- Function to create the multiplot page from a set of simulations
def create_fig_lines(panels,plot_climato=True,orientation='portrait',nrow=None,ncol=None):
    """
    Returns an array that will be typically used in cpage as fig_lines.
    """
    npanels = len(panels)
    if plot_climato:
        if orientation=='portrait':
            ncol = 2
            nrow = npanels
        if orientation=='landscape':
            nrow = 2
            ncol = npanels
    else:
        from math import ceil
        if orientation=='portrait':
            if not ncol:
                if npanels<=2:
                    ncol=1
                if npanels>2 and npanels<=10:
                    ncol=2
                if npanels>10:
                    ncol=3
            nrow = int(ceil(npanels / ncol))
        if orientation=='landscape':
            if not nrow:
                if npanels<=2:
                    nrow=1
                if npanels>2 and npanels<=10:
                    nrow=2
                if npanels>10:
                    nrow=3
            ncol = int(ceil(float(npanels) / float(nrow)))
    tmp = [[ None for i in range(ncol)] for j in range(nrow)]
    return tmp


def replace_facet_in_string(strg,values={}):
    """
    The function replace_facet_in_string replaces a facet like ${variable} in a character string with
    a value defined in values like values={'variable':'tas'}
    
    Example:
    >>> replace_facet_in_string('The variable is ${variable}',values={'variable':'tas'})
    'The variable is tas'
    
    """
    facet_values={'model':'','simulation':'','period':'','variable':'','product':'','CustomName':''}
    facet_values.update(values)
    for facet in facet_values:
        tmpfacet='${'+facet+'}'
        if tmpfacet in strg:
            strg = str.replace(strg,tmpfacet,facet_values[facet])
    return strg


def check_ds(simulations, variables, return_file=False):
    """
    check_ds is used to check the datasets associated with a 'simulations' list and 'variables' list.
    If you want to write the files, set return_file=True
    """
    for variable in variables:
        for simulation in simulations:
            print simulation
            sim = ds(variable=variable, **simulation)

            print '-- simulation = '+sim.simulation
            print '-- model = '+sim.model
            if 'clim_period' in simulation or sim.kvp['frequency'] in ['seasonal','annual_cycle']:
                tmp_period = sim.kvp['clim_period']
            else:
                tmp_period = str(sim.period)
            print summary(sim)
            if return_file:
                file = cfile(sim)
                print file

#
    
def climbias_explorer(panels, pages, show_last_plot=True, **kwargs):
    """    
    The function climbias_explorer() returns a pdf document composed of pages showing several simulations
    for one variable (and one variable per page), or several variables for one simulation (and one
    simulation per page).
    
    It offers many possibilities; among the most interesting, the user can:
        - easily create an inter-atlas (atlas to compare several simulations) for multiple variables
        - plot either the climatology, or the bias map, or both
        - plot differences against a reference or another chosen simulation
        - iterate on multiple time steps / periods to see the diagnostic
          evoluting with time (via the definition of the simulations)
        - plot the four seasons on the same page (via the definition of the simulations)
    
    climbias_explorer computes the climatology, regrids the model on the reference and creates the multiplot,
    depending on the number of panels.
    It uses:
        - plot_params.py to find the default plotting parameters per variable and type of plot
          (full_field, bias, or model_model)
        - reference.py to find a default reference for a variable (function variable2reference)
    
    
    The main strengths of climbias_explorer come from:
        - the definition of the datasets with the CliMAF datasets; it allows selecting the period, using different
          organization of data (projects), loop on the variables...
        - the CliMAF plot() function that takes a great amount of arguments
        - using python dictionaries to pass arguments
    
    
    Some other automatic interesting features/behaviours:
        - If the user asks for ua, va, ta or hus, climbias_explorer automatically
          computes the zonal mean (lat/pressure) field.
        - If the variable is an ocean variable (tos, sos...), both model and ref are regridded on a 1deg grid
    
    climbias_explorer takes as a third argument kwargs (used like this: **kwargs). The user can control
    many parameters with kwargs.
        kwargs is defined in the atlas_explorer_functions.py file. It is a dictionary with default values
        for a set of parameters (to control the page, the panels, the plots themselves...) that the user
        can control like this:
        We recommand to first making a copy of kwargs like this:
          >>> wkwargs = kwargs.copy()
        and then work with wkwargs.
        The user can modify wkwargs by updating as many parameters as he wants, like this:
        >>> wkwargs.update({ 'parameter1':user_defined_value1, 'parameter2':user_defined_value2 }) 
        !!! It is also possible to pass parameters in the dictionary of a variable in the same way as in kwargs.
            Notably a season (DJF, JJA...), a projection (NH, SH...).
            This feature allows controlling the plotting parameters independantly for each variable.
    
    Example (strict minimum to be done):
    >>> from atlas_explorer import *
    >>> wkwargs = kwargs.copy()
    >>> simulations = [
            {'project':'CMIP5','model':'IPSL-CM5A-LR','period':'1980-2000','experiment':'historical'},
            {'project':'CMIP5','model':'CNRM-CM5','period':'1980-2000','experiment':'historical'}
         ]
    >>> variables = ['tas','pr','tos','sos']
    >>> climbias_explorer(simulations, variable, **kwargs)
    --> climbias_explorer returns a pdf file atlas.pdf in the current working directory.
    
    Example with the choice of a season and a CustomName for the title of the panels,
    and plotting the sea ice concentration for the NH and the SH (plotting only the climatologies, not the bias):
    (Note that it is also possible to define the season via the dictionary of the variable)
    >>> from atlas_explorer import *
    >>> wkwargs = kwargs.copy()
    >>> wkwargs.update({'plot_bias':False}) # - Switch off the plot of the bias maps
    >>> simulations = [
            {'project':'CMIP5','model':'IPSL-CM5A-LR','period':'1980-2000','experiment':'historical',
             'climatology':'March','CustomName':'CM5A-LR'},
            {'project':'CMIP5','model':'IPSL-CM5A-LR','period':'1980-2000','experiment':'historical',
             'climatology':'September','CustomName':'CM5A-LR'}
         ]
    >>> variables = [{'variable':'sic','proj':'NH'},{'variable':'sic','proj':'SH'}]
    >>> climbias_explorer(simulations, variable, **kwargs)
     
    # ------------------------------------------------------------------------------------------------------------ #
    Parameters that can be controlled with wkwargs (and their associated default values defined in kwargs):
    ** Note that you can use ${model}, ${simulation}, ${period}, ${season}, ${product}, ${variable} or ${CustomName}
    in the values of the parameters; they will be automatically replaced by the values associated with the
    dataset and/or the product used as reference (${product} returns the facet simulation if the reference is
    a simulation)
    
        'climatology' : 'annual_mean'  # -- Note you can use 'season', 'clim' or 'climato' instead of 'climatology'
        'plot_climato' : True
        'plot_bias'    : True
        'Metrics'      : False         # -- If True, it displays the metrics associated with the plot
        'ref_contours' : False         # -- If True, displays the contours of the reference over the bias map
                                       #    It uses the contours defined in plot_params as 'colors' for 'full_field'
        'orientation' : 'landscape'    # -- Either 'landscape' or 'portrait'
        'nrow':None                    # -- Controls the number of rows of the multiplot
        'ncol':None                    # -- Controls the number of columns of the multiplot
        
        ## -- PLOT OF THE CLIMATOLOGY
        'ClimPlotMainTitle' : 'Climatology ${variable} ${simulation}' # -- Plot Main Title
        'ClimUpperRightTitle' : '${climatology}'                      # -- Plot Upper right title
        'ClimUpperLeftTitle' : '${period}'                            # -- Plot Upper left title
        'ClimCenterTitle' : ''                                        # -- Plot Center title
        ## -- BIAS PLOT
        'BiasPlotMainTitle' : '${simulation}'         # -- Plot Main Title
        'BiasUpperRightTitle' : '${climatology}'      # -- Plot Upper right title
        'BiasUpperLeftTitle' : '${period}'            # -- Plot Upper left title
        'BiasCenterTitle' : ''                        # -- Plot Center title

        'mpCenterLonF':0              # -> Longitude centered in the map
        'vcb':False                   # -> if True (False), color bar is vertical (horizontal)
        'tiMainFontHeightF':0.035     # -> Font size for the title ; default is 0.025
        'gsnStringFontHeightF':0.022  # -> Font size of the subtitle ; default is 0.012
        'resolution':'1500x1500'      # -> Default resolution: 1024x1024
        'aux_options':None            # -> NCL options to be passed to plot for an auxilliary field (used in the bias plot)
        'default_aux_options':None    # -> Default aux_options that will be common to all the plots
        'options':None                # -> NCL options to be passed to plot for the main field
        'default_options':None        # -> Default options that will be common to all the plots
        
        # -- General plot specifs: this dictionary allows the user to pass potential parameters to plot
        # -- that are not in the list of defined parameters in kwargs
        'plot_specs' : {}

        # -- Page title
        'page_title' : 'Bias map: ${variable} (vs ${product})'

        # -- Display specifications
        'title_specs' : {
            'gravity':'NorthWest',
            'ybox':80, 'pt':30,
            'x':30, 'y':40, 
            'font':'Waree-Bold',
            }#end title_specs 
        # pt => between ybox/4 and ybox/2
        # Interesting fonts : Waree-Bold, DejaVu-Sans-Condensed, Unikurd-Web-Regular,
        # UnDotum-Regular, PakTypeNaqsh-Regular, Nimbus-Sans-Bold, Nimbus-Mono-Bold,
        # FreeSans-Gras, Jomolhari-Regular, Khmer-OS-System-Regular

        # - If you want to specify a simulation as a reference, describe it in reference{} the same way as simulations
        # - If you don't just leave 'reference':{},
        # - and climbias_explorer will get a default reference with variable2reference.
        'reference' : {}
    
        # -- Specify the remapping method
        # -- By default, they are not defined in kwargs. The default values are thus only shown as examples.
        'remappingMethod':'remapbil' # Default == remapbil
        'cdogrid':'r360x180'
    
        # -- Remap the simulation on the reference? Or inverse? (if cdogrid
        'remapSimOnRef':True

        # -- append the result with an existing atlas
        'append':False                     # -- Set to True to append the result to an existing pdf file (either keep the same
                                           #    pdffile or use main_atlas_pdf, so you can use pdffile to give
                                           #    an explicit name to your intermediate atlases
        'remove_intermediate_atlas':False  # -- Removes the intermediate atlases
        'pdffile':'atlas.pdf'              # -- Name of the pdffile produced by the present call of the explorer
        'main_atlas_pdf':'main_atlas.pdf'  # -- if main_atlas_pdf is different of pdffile, append will use main_atlas_pdf as
                                           #    the name of the final concatenated atlas
        'outdir' :''                       # -- Output directory (default: current working directory)
        
    # ------------------------------------------------------------------------------------ #
    Parameters that can be controlled with the dictionary of a variable:
        'climatology'
        'ref_contours'
        and all plotting parameters that plot() can take as argument.
        options and aux_options can also be passed for one given variable (they overwrite the values in kwargs)
    
    
    """
    #
    #
    # ------------------------------------------------------------------------------------------------ #
    # -- General parameters for the pdf document
    # -- Name of the pdf file that will contain the atlas
    pdffile        = kwargs['pdffile']          # -> Name of the pdf file produced by the present call of climbias_explorer
    main_atlas_pdf = kwargs['main_atlas_pdf']   # -> Name of the pdf file that will gather several pdfs produced with explorer
    orientation    = kwargs['orientation']      # -> orientation of the pdf
    pdf_outdir     = kwargs['outdir']           # -> output directory for the atlas
    if pdf_outdir=='':
        pdf_outdir='./'
    else:
        if pdf_outdir[len(pdf_outdir)-1]!='/': pdf_outdir = pdf_outdir+'/'
    pdf_pathandfilename = pdf_outdir+pdffile
    
    if orientation=='landscape':
        pdf_orientation=orientation
    else:
        pdf_orientation='no-landscape'
    #
    import os
    # -- Si on precise 'append':True et que le fichier que l'on veut concatener existe deja, soit:
    # --    - on fait une copie du fichier existant (qui porte le nom du fichier final) et on lui donne un nom de fichier tmp
    # --    - on a un nom de fichier main_atlas_pdf different de pdffile renseigne par l'utilisateur,
    # --      et on utilise pdffile pour le fichier interm
    if kwargs['append'] and os.path.isfile(pdf_pathandfilename):
        if main_atlas_pdf!=pdffile:
            tmp_pdf_pathandfilename = pdf_pathandfilename
            pdf_pathandfilename = pdf_outdir+main_atlas_pdf
        else:
            # Creer un nouveau nom de fichier pour pdf_pathandfilename
            tmp_pdf_pathandfilename = pdf_pathandfilename.replace('.pdf','-'+str(time.time()).replace('.','')+'.pdf')
            # Faire un mv
            os.rename(pdf_pathandfilename, tmp_pdf_pathandfilename)
        # mettre le pdf_pathandfilename renomme dans la commande 
        pdfcmd = 'pdfjam --'+pdf_orientation+' -o '+pdf_pathandfilename+' '+tmp_pdf_pathandfilename
    else:    
        pdfcmd = 'pdfjam --'+pdf_orientation+' -o '+pdf_pathandfilename
    #
    # -- End General parameters for pdf file
    # ------------------------------------------------------------------------------------------------ #
    #
    #
    # ------------------------------------------------------------------------------------------------ #
    # -- Initialize the html index
    index= header("Atlas Explorer")
    #index += cell('PDF',pdffile)
    index += open_table()
    thumbnail_size = kwargs['thumbnail_size']
    init_line = 0
    accumulated_pages = 1
    ntot_pages = len(pages)
    tmp_line = []

    # -- End Initialize the html index
    # ------------------------------------------------------------------------------------------------ #
    #
    #
    # -- Get some general graph specs to be used later on
    plot_climato = kwargs['plot_climato']
    plot_bias = kwargs['plot_bias']
    #
    #
    # ----------------------------------------------- #
    # -----> STARTING LOOP ON THE PAGES            -- #
    # ----------------------------------------------- #
    for page in pages:
        
        # -- Create the multiplot device with create_fig_lines
        nrow = kwargs['nrow']
        ncol = kwargs['ncol']
        if plot_climato and plot_bias:
            fig_lines = create_fig_lines(panels,orientation=orientation,plot_climato=True,nrow=nrow,ncol=ncol)
        else:
            fig_lines = create_fig_lines(panels,orientation=orientation,plot_climato=False,nrow=nrow,ncol=ncol)
        nrow = np.shape(fig_lines)[0]
        ncol = np.shape(fig_lines)[1]
        byColumn=False
        byRow=True
        # -- Initialize the loop on the columns (j) and rows (i)
        i=0
        j=0
        #
        #
        # ----------------------------------------------- #
        # -----> STARTING LOOP ON THE PANELS           -- #
        # ----------------------------------------------- #
        # -- Loop on the panels
        for panel in panels:
            #
            # -- Identifies whether page is a dataset or a variable
            if ('model' or 'simulation' or 'login') in page:
                print 'Dataset = ',page
                dataset = page
                print 'variable = ',panel
                tmpvariable = panel
            else:
                print 'Dataset = ',panel
                dataset = panel
                print 'variable = ',page
                tmpvariable = page
            # -- Here, we check if variable is a dictionary -> If yes, it potentially contains
            # -- plotting parameters, and/or a season/climatology
            if isinstance(tmpvariable,dict):
                variable = tmpvariable['variable']
                # --> Here is the mechanism to get the pairs keyword/value from a dictionary
                # --> to pass plotting arguments to the plot (variable_plot_specs)
                variable_plot_specs = dict(tmpvariable.items())
                variable_plot_specs.pop('variable')
                for tmpclimarg in ['clim','season','climato','climatology']:
                    if tmpclimarg in variable_plot_specs:
                        dataset.update({'climatology':variable_plot_specs[tmpclimarg]})
                        variable_plot_specs.pop(tmpclimarg)
            else:
                # -- If tmpvariable is not a dictionary, it is simply a string ; then variable_plot_specs
                # -- is an empty dictionary
                variable = tmpvariable
                variable_plot_specs = {}
            #
            #
            # -- facet_values is a dictionary containing some facets that will be replaced with
            # -- their values; it allows using ${variable}, ${model}, ${simulation}, ${product},
            # -- ${period} and ${CustomName} to get their values
            facet_values = {'variable':variable}
            #
            # ------------------------------------------------------------------------------------------------ #
            # -- In this section, we see if we need to get a reference or not (i.e. if we ask for a bias map,
            # -- or not.
            # --> if plot_bias: If we don't plot the bias, we do not get the reference
            if 'ref_contours' not in variable_plot_specs:
                variable_plot_specs.update({'ref_contours':kwargs['ref_contours']})
            if plot_bias or variable_plot_specs['ref_contours']:
                # -- It is possible to define a simulation as a reference via kwargs['reference']
                # -- The user defines it like a casual CliMAF dataset (a dictionary making sense with ds() )
                # -- If kwargs['reference'] is an empty dictionary (the default value), it will get
                # -- a reference dataset defined in reference.py via the function variable2reference(variable).
                # -- Otherwise it gets the dataset defined with kwargs['reference'].
                if kwargs['reference']=={}:
                    if not variable2reference(variable):
                        print '!!!'
                        print '!!! No reference defined in variable2reference for variable '+variable
                        print '!!! Edit reference.py in the atlas_explorer module to define a reference'
                        print '!!!'
                    ref = ds(**variable2reference(variable))
                    summary(ref)
                    difftype='bias' #; context = difftype
                else:
                    reference = kwargs['reference'].copy()
                    difftype='model_model'
                    reference.update({'variable':variable})
                    ref = ds(**reference)
                #if any(kwd in ref.kvp for kwd in ['model','simulation','login']) and ref.kvp['simulation']!=:
                if 'product' not in ref.kvp:
                    facet_values.update({'product':ref.kvp['simulation']})
                else:
                    facet_values.update({'product':ref.kvp['product']})
                if 'clim_period' in ref.kvp:
                    tmp_period = ref.kvp['clim_period']
                else:
                    tmp_period = str(ref.period)
                facet_values.update({'period':tmp_period})
                print summary(ref)
            # ------------------------------------------------------------------------------------------------ #
            #
            # ------------------------------------------------------------------------------------------------ #
            #  -- We add variable to the dictionary defining the dataset, before passing it to ds()
            dataset.update({'variable':variable})
            dat = ds(**dataset)
            # ------------------------------------------------------------------------------------------------ #
            #
            # ------------------------------------------------------------------------------------------------ #
            # -- Get the time period
            if 'clim_period' in dataset or dat.kvp['frequency'] in ['seasonal','annual_cycle']:
                tmp_period = dat.kvp['clim_period']
            else:
                tmp_period = str(dat.period)
            # ------------------------------------------------------------------------------------------------ #
            #
            #
            # ------------------------------------------------------------------------------------------------ #
            # --> Case of dat is a reference dataset!!
            # --> This step here is only to feed the facet_values dictionary with the right facets and values
            # -- Here, it is a simulation
            if 'product' not in dataset:
                print '-- simulation = '+dat.simulation
                print '-- model = '+dat.model
                facet_values.update({'model':dat.model,'simulation':dat.simulation,'period':tmp_period})
                if 'CustomName' in dataset:
                    facet_values.update({'CustomName':dataset['CustomName']})
            else:
                # -- And here, it is a reference product
                print '-- product = '+dat.product
                facet_values.update({'product':dat.product,'period':tmp_period})
                if 'CustomName' in dataset:
                    facet_values.update({'CustomName':dataset['CustomName']})                
            print summary(dat)
            print ''
            # ------------------------------------------------------------------------------------------------ #
            #
            #
            # ------------------------------------------------------------------------------------------------ #
            # -- Compute the climatologies
            # -- We use clim_average() to compute the climatologies.
            climarg = 'climatology'
            for tmpclimarg in ['clim','season','climato']:
                if tmpclimarg in dataset:
                    climarg = tmpclimarg
            if climarg in dataset:
                tmp_climatology = dataset[climarg]
            else:
                tmp_climatology = kwargs['climatology']
            if tmp_climatology in 'annual_mean':
                tmp_climatology='ANM'
            climato_dat = clim_average(dat,tmp_climatology)
            if plot_bias or variable_plot_specs['ref_contours']:
                climato_ref = clim_average(ref,tmp_climatology)
            # -- Update facet_values
            facet_values.update({'climatology':tmp_climatology})
            # ------------------------------------------------------------------------------------------------ #
            #
            #
            # ------------------------------------------------------------------------------------------------ #
            # --> plot_specs will be passed to plot
            # --> It is the dictionary with all the plotting specifications.
            # --  !!! This is a heavy step in terms of code lines...
            # ------------------------------------------------------------------------------------------------ #
            # --> We merge the arguments passed with the dictionary of the variable
            plot_specs = dict(kwargs['plot_specs'].items())
            plot_specs.update({'mpCenterLonF':kwargs['mpCenterLonF']})
            plot_specs.update({'vcb':kwargs['vcb']})
            plot_specs.update({'tiMainFontHeightF':kwargs['tiMainFontHeightF']})
            plot_specs.update({'gsnStringFontHeightF':kwargs['gsnStringFontHeightF']})
            plot_specs.update({'resolution':kwargs['resolution']})
            #
            # -------------------------------------------------------------------------------- #
            # --> Treatment of aux_options: argument to pass NCL plotting options to plot()  - #
            # --> aux_options applies to the auxillary file, i.e. the reference (that we     - #
            # --> generally plot with contours)                                              - #
            # -------------------------------------------------------------------------------- #
            # -- This is the default set of aux_options (see plot())
            # --> The user can pass a default_aux_options that will be used for all the plots
            # --  even the user defines additionnal aux_options via the dictionary of the variable
            if kwargs['default_aux_options']:
                default_aux_options = kwargs['default_aux_options']
            else:
                default_aux_options = ['cnLineThicknessF=1.5','cnLineLabelsOn=True','cnLineLabelFontHeightF=0.009']
            #
            # -- And kwargs_aux_options is the aux_options passed via kwargs
            # -- We also check whether the used has passed aux_options
            # -- via the dictionary of the variable (variable_plot_specs)
            # --> If yes, we use this one instead of aux_options passed with 
            if 'aux_options' in variable_plot_specs:
                kwargs_aux_options = variable_plot_specs['aux_options']
                variable_plot_specs.pop('aux_options')
            else:
                kwargs_aux_options = kwargs['aux_options']
            # --> Here, we build a list of the options that will be incorporated to aux_options,
            # --  first by constructing a list of options avoiding duplicating arguments between default_aux_options
            # --  and kwargs_aux_options
            if kwargs_aux_options:
                if isinstance(kwargs_aux_options,str):
                    tmp_kwargs_aux_options = str.split(kwargs_aux_options,'|')
                    kwargs_aux_options = tmp_kwargs_aux_options
                list_aux_options = list(default_aux_options)
                for default_arg in default_aux_options:
                    for arg in kwargs_aux_options:
                        kw = str.split(arg,'=')[0]
                        if kw in default_arg:
                            list_aux_options.remove(default_arg)
                            list_aux_options.append(arg)
            else:
                list_aux_options = default_aux_options
            # -- Then, we build the aux_options character string that will be passed to plot()
            aux_options=list_aux_options[0]
            for elt in list_aux_options[1:len(list_aux_options)]:
                aux_options = aux_options + '|' + elt
            plot_specs.update({'aux_options':aux_options})
            #
            # --> The user can pass a default_aux_options that will be used for all the plots
            # --  even the user defines additionnal aux_options via the dictionary of the variable
            if kwargs['default_options']:
                default_options = kwargs['default_options']
            else:
                default_options = ''
            #
            # -------------------------------------------------------------------------------- #
            # --> Treatment of options: argument to pass NCL plotting options to plot()      - #
            # --> options applies to the main field, i.e. the colors that we display.        - #
            # -------------------------------------------------------------------------------- #
            # -- And kwargs_aux_options is the aux_options passed via kwargs
            # -- We also check whether the used has passed aux_options
            # -- via the dictionary of the variable (variable_plot_specs)
            # --> If yes, we use this one instead of aux_options passed with 
            if 'options' in variable_plot_specs:
                kwargs_options = variable_plot_specs['options']
                variable_plot_specs.pop('options')
            else:
                kwargs_options = kwargs['options']
            # --> Here, we build a list of the options that will be incorporated to aux_options,
            # --  first by constructing a list of options avoiding duplicating arguments between default_aux_options
            # --  and kwargs_aux_options
            if kwargs_options:  # -- If kwargs_options has been defined by the user...
                if isinstance(kwargs_options,str):  # -- It can be one character tring with |, so we split it to make a list
                    tmp_kwargs_options = str.split(kwargs_options,'|')
                    kwargs_options = tmp_kwargs_options
                # -- If the user has defined some default_options common to all the plots, we do:
                if default_options:
                    list_options = list(default_options)
                    for default_arg in default_options:
                        for arg in kwargs_options:
                            kw = str.split(arg,'=')[0]
                            if kw in default_arg:
                                list_options.remove(default_arg)
                                list_options.append(arg)
                else: # -- Otherwise, we set directly list_options to kwargs_options
                    list_options = kwargs_options
            else:
                # -- If no kwargs_options has been defined by the user, we set list_options to the
                # -- default_options ; if default_options is '', nothing will be done at the next 'if' statement
                list_options = default_options
            # -- Then, we build the aux_options character string that will be passed to plot()
            # -- if list_options is not ''
            if list_options:
                options=list_options[0]
                for elt in list_options[1:len(list_options)]:
                    options = options + '|' + elt
                plot_specs.update({'options':options})
            #
            # -- Finally, we can add the plots specifications associated
            # -- with the variable variable_plot_specs to plot_specs (so it will be used by plot) 
            plot_specs.update(variable_plot_specs)
            #
            # --> If we work on ocean variables, we set the center of the figure to 200 deg in longitude
            # --> to have the Pacific ocean centered in the plot
            ocean_variables = ['tos','sos','zos']
            if variable in ocean_variables and plot_specs['mpCenterLonF']==0:
                plot_specs.update({'mpCenterLonF':200})
            #
            # -- End definition of plot_specs !!!                                                          -- #
            # ----------------------------------------------------------------------------------------------- #
            #
            #
            # ----------------------------------------------------------------------------------------------- #
            # -- Compute the zonal mean for ua, va, ta or hus                                              -- #
            zonmean_variables = ['ua','va','ta','hus']
            if variable in zonmean_variables:
                climato_dat = zonmean(climato_dat)
                if plot_bias or variable_plot_specs['ref_contours']:
                    climato_ref = zonmean(climato_ref)
            # --                                                                                           -- #
            # ----------------------------------------------------------------------------------------------- #
            #
            #
            # ----------------------------------------------------------------------------------------------- #
            # -- Compute the bias map                                                                      -- #
            # -- and deals with the remapping                                                              -- #
            # -- The user can pass 'cdogrid' and/or 'remappingMethod' via kwargs                           -- #
            # -- or the dictionary of the variable.                                                        -- #
            # -- By default:
            # --    - an atmospheric variable is regridded on the ref
            # --    - a 3D atmospheric variable is regridded and vertically interpolated with
            # --      diff_zonmean
            # --    - ocean variables are interpolated on 1deg grid (r360x180)
            variablekwargs = dict(kwargs.items())
            variablekwargs.update(variable_plot_specs)
            if plot_bias or variable_plot_specs['ref_contours']:
                if variable in zonmean_variables:
                    # -- Remapping vertical
                    # -- Remapping horizontal
                    bias_field = diff_zonmean(climato_dat,climato_ref)
                else:
                    # -- Default
                    if 'cdogrid' not in variablekwargs and 'remappingMethod' not in variablekwargs:
                        if variable in ocean_variables:
                            climato_ref = regridn(climato_ref,cdogrid="r360x180")
                            climato_dat = regridn(climato_dat,cdogrid="r360x180")
                        else:
                            if variablekwargs['remapSimOnRef'] or 'remapSimOnRef' not in variablekwargs:
                                climato_dat = regrid(climato_dat,climato_ref)
                            else:
                                climato_ref = regrid(climato_ref,climato_dat)
                    else:
                        remappingMethod = variablekwargs.get('remappingMethod','remapbil')
                        #if 'remappingMethod' in variablekwargs:
                        #    remappingMethod = variablekwargs['remappingMethod']
                        cdogrid = "r360x180"
                        if 'cdogrid' in variablekwargs:
                            cdogrid = variablekwargs['cdogrid']
                            climato_ref = regridn(climato_ref,cdogrid=cdogrid,option=remappingMethod)
                            climato_dat = regridn(climato_dat,cdogrid=cdogrid,option=remappingMethod)
                        else:
                            if variablekwargs['remapSimOnRef']:
                                climato_dat = regridn(climato_dat,climato_ref,option=remappingMethod)
                            else:
                                climato_ref = regridn(climato_ref,climato_dat,option=remappingMethod)
                    bias_field = minus(climato_dat,climato_ref)
            # --                                                                                           -- #
            # -- End computing the climatology and remapping                                               -- #
            # ----------------------------------------------------------------------------------------------- #
            #
            #
            # ----------------------------------------------------------------------------------------------- #
            # -- Do we want metrics on the climato and bias maps?                                          -- #
            Metrics = kwargs['Metrics']
            if 'Metrics' in variable_plot_specs:
                Metrics = variable_plot_specs['Metrics']
            # --                                                                                           -- #
            # ----------------------------------------------------------------------------------------------- #
            #
            #
            # --------------------------------------- #
            # -- Start the plot of the climatology -- #
            # --------------------------------------- #
            if plot_climato:
                # -- This step is to set the main title of the plot PlotMainTitle to CustomName
                # -- if CustomName is defined in dataset, and if kwargs['ClimPlotMainTitle']
                # -- has its default value (i.e. it has not been changed by the user)
                if 'CustomName' in dataset and kwargs['ClimPlotMainTitle'] == 'Climatology ${variable} ${simulation}':
                    PlotMainTitle = dataset['CustomName']
                else:
                    PlotMainTitle = kwargs['ClimPlotMainTitle']
                UpperLeftTitle = kwargs['ClimUpperLeftTitle']
                UpperRightTitle = kwargs['ClimUpperRightTitle']
                CenterTitle = kwargs['ClimCenterTitle']

                # --> Do we want metrics on the climatology map?
                if Metrics:
                    climato_min_value = '%s' % float('%.3g' % cvalue(ccdo(climato_dat,operator='fldmin')) )
                    climato_mean_value = '%s' % float('%.3g' % cvalue(ccdo(climato_dat,operator='fldavg')) )
                    climato_max_value = '%s' % float('%.3g' % cvalue(ccdo(climato_dat,operator='fldmax')) )
                    UpperRightTitle='min='+climato_min_value+' ; mean='+climato_mean_value+' ; max='+climato_max_value
                    UpperLeftTitle='${climatology}'
                    CenterTitle=''
                #
                # -- Here, we get the default plot params specified in plot_params.py
                # -- We create tmp_plot_climato_specifs that will be passed to plot() for the climato
                # -- and we add the plot_specs
                print 'variable_plot_specs = ',variable_plot_specs
                print 'plot_specs = ',plot_specs
                tmp_plot_climato_specifs = plot_params(variable,'full_field') ; tmp_plot_climato_specifs.update(plot_specs)
                #
                # -- Here, we give the possibility to pass arguments that are specific to a variable with kwargs
                if 'custom_plot_specs' in kwargs:
                    if variable in kwargs['custom_plot_specs']:
                        if 'full_field' in kwargs['custom_plot_specs'][variable]:
                            tmp_plot_climato_specifs.update(kwargs['custom_plot_specs'][variable]['full_field'])
                #
                # -- Print the arguments and do the plot
                if plot_specs['ref_contours']:
                    params_full_field = plot_params(variable,'full_field')
                    if 'offset' in params_full_field:
                        offset = params_full_field['offset']
                    else:
                        offset = 0.0
                    if 'scale' in params_full_field:
                        scale  = params_full_field['scale']
                    else:
                        scale = 1.0
                    # -- We apply the scale and offset with apply_scale_offset()
                    aux_ref = apply_scale_offset(climato_ref,scale,offset)
                    #
                    # -- We add the contours defined in plot_params for the full_field with 'colors'
                    # -- to the dictionary of specifs for the bias plot
                    if 'contours' in variable_plot_specs:
                        tmp_plot_climato_specifs.update({'contours':variable_plot_specs['contours']})
                    else:
                        tmp_plot_climato_specifs.update({'contours':params_full_field['colors']})
                    if 'ref_contours' in tmp_plot_climato_specifs:
                        tmp_plot_climato_specifs.pop('ref_contours')
                    climato_plot      = plot(climato_dat, aux_ref,
                                             title           = replace_facet_in_string(PlotMainTitle,facet_values),
                                             gsnLeftString   = replace_facet_in_string(UpperLeftTitle,facet_values),
                                             gsnRightString  = replace_facet_in_string(UpperRightTitle,facet_values),
                                             gsnCenterString = replace_facet_in_string(CenterTitle,facet_values),
                                             **tmp_plot_climato_specifs)
                else:
                    if 'ref_contours' in tmp_plot_climato_specifs:
                        tmp_plot_climato_specifs.pop('ref_contours')
                    climato_plot      = plot(climato_dat,
                                             title           = replace_facet_in_string(PlotMainTitle,facet_values),
                                             gsnLeftString   = replace_facet_in_string(UpperLeftTitle,facet_values),
                                             gsnRightString  = replace_facet_in_string(UpperRightTitle,facet_values),
                                             gsnCenterString = replace_facet_in_string(CenterTitle,facet_values),
                                             **tmp_plot_climato_specifs)

            # --------------------------------------- #
            # -- End plot of the climatology       -- #
            # --------------------------------------- #
            #
            #
            # --------------------------------------- #
            # -- Start the plot of the bias map    -- #
            # --------------------------------------- #
            # -- Plot the bias
            if plot_bias:
                # -- This step is to set the main title of the plot PlotMainTitle to CustomName
                # -- if CustomName is defined in dataset, and if kwargs['BiasPlotMainTitle']
                # -- has its default value (i.e. it has not been changed by the user)
                if 'CustomName' in dataset and kwargs['BiasPlotMainTitle'] == '${simulation}':
                    PlotMainTitle = dataset['CustomName']
                else:
                    PlotMainTitle = kwargs['BiasPlotMainTitle']
                UpperLeftTitle = kwargs['BiasUpperLeftTitle']
                UpperRightTitle = kwargs['BiasUpperRightTitle']
                CenterTitle = kwargs['BiasCenterTitle']   
                
                # -- Do we want to draw the contours of the reference?
                # -- Two steps here:
                # --   - First, we get the default value from kwargs
                # --   - then, we update with the possible value passed with the dictionary of a variable
                draw_ref_contours = kwargs['ref_contours']
                if 'ref_contours' in variable_plot_specs:
                    draw_ref_contours = variable_plot_specs['ref_contours']
                    plot_specs.pop('ref_contours')

                # -- Metrics on the bias map
                if Metrics:
                    bias_min_value = '%s' % float('%.3g' % cvalue(ccdo(bias_field,operator='fldmin')) )
                    bias_max_value = '%s' % float('%.3g' % cvalue(ccdo(bias_field,operator='fldmax')) )
                    bias_value = '%s' % float('%.3g' % cvalue(ccdo(bias_field,operator='fldmean')) )
                    crmse_value = '%s' % float('%.3g' % CRMSE(climato_dat,climato_ref) )
                    UpperRightTitle='min='+bias_min_value+'; max='+bias_max_value+'; bias='+bias_value+'; CRMSE='+crmse_value
                    UpperLeftTitle='${climatology}'
                    CenterTitle=''
                #
                # -- Here, we get the default plot params specified in plot_params.py
                # -- We create tmp_plot_bias_specifs that will be passed to plot() for the bias
                # -- and we add the plot_specs
                tmp_plot_bias_specifs = plot_params(variable,difftype) ; tmp_plot_bias_specifs.update(plot_specs)
                #
                # -- Here, we give the possibility to pass arguments that are specific to a variable with kwargs                
                if 'custom_plot_specs' in kwargs:
                    if variable in kwargs['custom_plot_specs']:
                        if difftype in kwargs['custom_plot_specs'][variable]:
                            tmp_plot_bias_specifs.update(kwargs['custom_plot_specs'][variable][difftype])
                #
                # -- If we want to add the contours of the ref to the bias map:
                # --    - we get the contours from 'colors' specified in plot_params for full_field
                # --    - because those contours are defined after applying an offset and/or scale,
                # --      we have to apply the offset and scale to ref to display it
                if draw_ref_contours:
                    params_full_field = plot_params(variable,'full_field')
                    if 'offset' in params_full_field:
                        offset = params_full_field['offset']
                    else:
                        offset = 0.0
                    if 'scale' in params_full_field:
                        scale  = params_full_field['scale']
                    else:
                        scale = 1.0
                    # -- We apply the scale and offset with apply_scale_offset()
                    aux_ref = apply_scale_offset(climato_ref,scale,offset)
                    #
                    # -- We add the contours defined in plot_params for the full_field with 'colors'
                    # -- to the dictionary of specifs for the bias plot
                    if 'contours' in variable_plot_specs:
                        tmp_plot_bias_specifs.update({'contours':variable_plot_specs['contours']})
                    else:
                        tmp_plot_bias_specifs.update({'contours':params_full_field['colors']})
                    if 'ref_contours' in tmp_plot_bias_specifs:
                        tmp_plot_bias_specifs.pop('ref_contours')
                    bias_plot     = plot(bias_field, aux_ref,
                                         title           = replace_facet_in_string(PlotMainTitle,facet_values),
                                         gsnLeftString   = replace_facet_in_string(UpperLeftTitle,facet_values),
                                         gsnRightString  = replace_facet_in_string(UpperRightTitle,facet_values),
                                         gsnCenterString = replace_facet_in_string(CenterTitle,facet_values),
                                         **tmp_plot_bias_specifs)
                else:
                    if 'ref_contours' in tmp_plot_bias_specifs:
                        tmp_plot_bias_specifs.pop('ref_contours')
                    bias_plot     = plot(bias_field,
                                         title           = replace_facet_in_string(PlotMainTitle,facet_values),
                                         gsnLeftString   = replace_facet_in_string(UpperLeftTitle,facet_values),
                                         gsnRightString  = replace_facet_in_string(UpperRightTitle,facet_values),
                                         gsnCenterString = replace_facet_in_string(CenterTitle,facet_values),
                                         **tmp_plot_bias_specifs)
            #
            # --------------------------------------- #
            # -- End plot of the bias map          -- #
            # --------------------------------------- #
            #
            # ------------------------------------------ #
            # -- Now, we fill the multiplot device... -- #
            # ------------------------------------------ #
            if plot_climato and plot_bias:
                if orientation=='portrait': 
                    fig_lines[i][0] = climato_plot
                    fig_lines[i][1] = bias_plot
                if orientation=='landscape':
                    fig_lines[0][i] = climato_plot
                    fig_lines[1][i] = bias_plot
                i=i+1
            else:
                if plot_climato:
                    fig = climato_plot
                if plot_bias:
                    fig = bias_plot
                fig_lines[i][j] = fig
                if byRow:
                    if i==(nrow-1):
                        i=-1 ; j = j+1
                    i = i+1
                if byColumn:
                    if j==(ncol-1):
                        j=-1 ; i = i+1
                    j = j+1
            # ------------------------------------------ #
            # -- End fill the multiplot device        -- #
            # ------------------------------------------ #
        #
        #
        # ----------------------------------- #
        # -- Do the multiplot with cpage() -- #
        # ----------------------------------- #
        page_title = kwargs['page_title']
        title_specs = kwargs['title_specs']
        multiplot = cpage(fig_lines, orientation=orientation, fig_trim=True, page_trim=True,
                          title = replace_facet_in_string(page_title,facet_values), format='png',
                          **title_specs)
        # ----------------------------------- #
        # -- End multiplot with cpage()    -- #
        # ----------------------------------- #
        #
        #
        # --------------------------------------------------------------------- #
        # -- Prepare the PDF command to produce the multi-page PDF document
        pdfcmd = pdfcmd+' '+cfile(multiplot)
        #
        #
        # --------------------------------------------------------------------- #
        # -- Build the line of thumbnails for the html index
        if accumulated_pages <= ntot_pages:
            init_line = init_line + 1
            tmp_line.append({'label':kwargs['page_title'],'file':cfile(multiplot)})
            if init_line==3 or accumulated_pages == ntot_pages:
                if init_line==1:
                    index+=open_line('')+\
                        cell(tmp_line[0]['label'],tmp_line[0]['file'],thumbnail=thumbnail_size,hover=kwargs['hover'])
                    close_line()
                if init_line==2:
                    index+=open_line('')+\
                        cell(tmp_line[0]['label'],tmp_line[0]['file'],thumbnail=thumbnail_size,hover=kwargs['hover'])+\
                        cell(tmp_line[1]['label'],tmp_line[1]['file'],thumbnail=thumbnail_size,hover=kwargs['hover'])
                    close_line()
                if init_line==3:
                    index+=open_line('')+\
                        cell(tmp_line[0]['label'],tmp_line[0]['file'],thumbnail=thumbnail_size,hover=kwargs['hover'])+\
                        cell(tmp_line[1]['label'],tmp_line[1]['file'],thumbnail=thumbnail_size,hover=kwargs['hover'])+\
                        cell(tmp_line[2]['label'],tmp_line[2]['file'],thumbnail=thumbnail_size,hover=kwargs['hover'])
                    close_line()
                    init_line = 0
                    tmp_line = []
            accumulated_pages = accumulated_pages + 1
        #
    #
    #
    # ------------------------- #
    # -- Create the pdf page -- #
    # ------------------------- #
    print pdfcmd
    os.system(pdfcmd)
    if kwargs['append'] and kwargs['remove_intermediate_atlas'] and os.path.isfile(tmp_pdf_pathandfilename):
        os.remove(tmp_pdf_pathandfilename)
    #
    #
    # ------------------------------- #
    # -- Copy on dods (open space) -- #
    # ------------------------------- #
    if kwargs['dods_cp']:
        if atTGCC:
            dods_dir = '/ccc/work/cont003/dods/public/'+getuser()+'/atlas_explorer/'
        if onCiclad:
            print 'dods_cp -> TBD on Ciclad'
    #
    #
    # ----------------------------- #
    # -- Finalize the html index -- #
    # ----------------------------- #
    index += close_table()
    index += trailer()
    out="index_atlas.html"
    with open(out,"w") as filout : filout.write(index)
    #
    #
    # ----------------------------------------------------------- #
    # -- Show the last plot or return the name of the pdf file -- #
    # ----------------------------------------------------------- #
    if show_last_plot:
        return iplot(multiplot)
    else:
        return pdf_pathandfilename
    # -->
    # -->
    # --> End of climbias_explorer!!




