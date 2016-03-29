from climaf.api import *
from climaf.html import * 
from climaf import cachedir

desc="\n\nProto d'atlas oceanique (Nemo) en CliMAF (CMIP5 seulement pour l'instant)"
from optparse import OptionParser
parser = OptionParser(desc) ; parser.set_usage("%%prog [-h]\n%s" % desc)
parser.add_option("-s", "--simulation", 
                  help="simulation a traiter ",
                  action="store",default="historical")
parser.add_option("-p", "--period", 
                  help="period after CliMAF syntax, as e.g. 1980-1987",
                  action="store",default="1980")
parser.add_option("-v", "--variables", 
                  help="liste des variables (separees par des virgules)", action="store",default="thetao,so")
#parser.add_option("-o", "--pdf", 
#                  help="nom du pdf de sortie (default: atlas_<SIMU>_<SAISON>.pdf)", action="store")
(opts, args) = parser.parse_args()
if opts.simulation is None :
    print "Must provide a simulation "
    exit(0)

model=dict(project='CMIP5',model='CNRM-CM5', frequency="mon", 
           realm="ocean", table="Omon", version="latest", 
           period=opts.period, experiment=opts.simulation,simulation="r1i1p1")
levitus=dict(project="ref_pcmdi", product='NODC-Levitus',clim_period='*')

# Obs de MOC RAPID 
# (Il a fallu bricoler les donnees d'origine pour la dimension time au debut et unlim)
dataloc(project="ref_pcmdi",organization="generic",
        url='/home/esanchez/data_climaf/${variable}_vertical_unlim.nc')
calias('ref_pcmdi','moc','stream_function_mar',filenameVar='moc')

# Scaling de la MOC modele pour homogeneite avec obs RAPID
calias("CMIP5","msftmyz",scale=1.e-3)


def model_vs_obs_profile_oce(variable,model,obs,masks='/data/esanchez/Atlas/oce/mask'):
    """
    Given two dataset specifications, and an oceanic variable name,
    create a figure for profile for the variable in both sources

    dataset specifications are dictionnaries
    
    specifics : 
     - space averaging uses cdftools for model variable, on grid T
     - obs data are supposed to be an annual cycle

    Example :
    >>> model=dict(project="CMIP5", model='CNRM-CM5', frequency='mon',
    >>>       realm='ocean', table='Omon',
    >>>       experiment='historical', period='1980-1981')
    >>> obs=dict(project="ref_pcmdi", product='NODC-Levitus',clim_period='*')
    >>> fig=model_vs_obs_profile_oce('thetao',model,obs)

    """
    modvar=ds(variable=variable,**model)
    obsvar=ds(variable=variable,**obs)
    
    #- Compute temporal means 
    tmean_modvar=ccdo(modvar,operator='timavg -yearmonmean')
    tmean_obsvar=ccdo(obsvar,operator='yearmonmean') 
    
    #- Compute vertical profiles 
    fixed_fields('ccdfmean_profile',
             ('mask.nc',    masks+'/ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',masks+'/ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',masks+'/ORCA1_mesh_zgr.nc'))
    cscript("rename_time","ncrename -d time,time_counter ${in} ${out}")
    aux=rename_time(tmean_modvar)
    vertprof_modvar=ccdfmean_profile(aux,pos_grid='T')
    vertprof_obsvar=ccdo(tmean_obsvar,operator='mermean -zonmean')

    #- Plot vertical profile of model & obs data
    myplot=plot( vertprof_obsvar, vertprof_modvar, title='MOD&OBS - '+variable, 
                 y="index",aux_options="xyLineColor='red'",invXY=False)
    
    return(myplot)


def plot_atl_moc(model, variable="msftmyz", rank=1):
    # Plot a model MOC slice
    moc_model=ds(variable=variable, **model)
    moc_model_mean=time_average(moc_model)
    # extraire le bassin de rang 'rank' (def: Atlantique=1)
    moc_model_mean_atl=slice(moc_model_mean, dim='x', num=rank)
    # masquer les valeurs 
    moc_model_mean_atl_mask=mask(moc_model_mean_atl,miss=0.0)
    # Plot
    plot_moc_slice=plot(moc_model_mean_atl_mask, title="MOC", y="index",
                        min=-10.,max=30.,delta=1.,scale=1e-3,units="Sv",options="trXMinF=-30.")
    return(plot_moc_slice)


# Profil de MOC, vs Obs RAPID
def moc_profile_vs_obs_rapid(model,variable="msftmyz",rank=1): 
    # Comparer les profil de MOC modele/RAPID a la latitude 26
    mod=model.copy()
    mod.update({'variable': variable})
    moc_model=ds(**mod)
    moc_model_mean=time_average(moc_model)
    #extraire le bassin Atlantique de la MOC modele
    moc_model_mean_atl=slice(moc_model_mean, dim='x', num=rank)
    #masquer les valeurs et extraire la latitude 26
    moc_model_mean_atl_mask=mask(moc_model_mean_atl,miss=0.0)
    moc_model_26=slice(moc_model_mean_atl_mask, dim='lat', num=26.5)
    #
    moc_obs=ds(project="ref_pcmdi",variable='moc')
    moc_obs_mean=time_average(moc_obs)
    #
    plot_profile_obs=plot(moc_model_26,moc_obs_mean, title='RAPID', 
                          y="lin", units="Sv", aux_options="xyLineColor='red'")
    return plot_profile_obs

#pdffile="atlas_"+opts.simulation+"_"+opts.season+".pdf"
#pdfargs=["pdfjam","--landscape","-o ",pdffile]

# Initialisation de l'index html
index= header("Nemo CliMAF Atlas for "+opts.simulation+ " and period "+opts.period) 
#index += cell('PDF',pdffile)
index += section("ocean", level=4)
index += open_table()

index+=open_line('VARIABLE')+cell('profile')+cell('map')+close_line()
lvars=opts.variables.split(',')

atlas_dir=os.path.expanduser(cachedir+'/../atlas')
for variable  in lvars :
    profile=model_vs_obs_profile_oce(variable,model,levitus)
    index+=open_line(variable)+\
            cell("",cfile(profile),thumbnail="70*70", hover=True, dirname=atlas_dir)
    close_line()
index += close_table()

index += vspace(2)

moc_profile=moc_profile_vs_obs_rapid(model)
moc_atl=plot_atl_moc(model)
index+=line({"moc_profile":cfile(moc_profile), "moc_atl":cfile(moc_atl)},title="Autres:   ", hover=True, dirname=atlas_dir)


index += trailer()
out="index_example.html"
with open(out,"w") as filout : filout.write(index)
import os,os.path ; 
print("Attendez un bon peu : lancemement de firefox sur Ciclad....")
os.system("firefox file://"+os.path.abspath(os.path.curdir)+"/"+out+"&")




# Example for defining a data organization in a project
cproject("dmc", "root")
cdef("root","/data/mcheval")
dataloc(project="dmc",organization="generic",url="${root}/${simulation}/${simulation}_1m_YYYYMMDD_YYYYMMDD_grid_${variable}.nc")
calias("dmc", 'tos',filenameVar='T')
tos=ds(project='dmc',simulation='O1IAF01',variable='tos',period='1980')

