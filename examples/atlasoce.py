#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import


from optparse import OptionParser

from climaf.api import *
from climaf.chtml import *
from climaf import cachedir


# This example does work only on Ciclad
if not onCiclad and not onSpirit:
    exit(0)

desc = "\n\nProto d'atlas océanique (Nemo) en CliMAF (CMIP5 seulement pour l'instant)"

parser = OptionParser(desc)
parser.set_usage("%%prog [-h]\n%s" % desc)
parser.add_option("-s", "--simulation",
                  help="simulation to process ",
                  action="store", default="historical")
parser.add_option("-i", "--index",
                  help="html index filename",
                  action="store", default="index_oce.html")
parser.add_option("-d", "--directory",
                  help="destination directory ", action="store")
parser.add_option("-a", "--alt_dir_name",
                  help="disguise links to another dir ", action="store")
parser.add_option("-u", "--root_url",
                  help="Root url for option -a",
                  default="https://vesg.ipsl.upmc.fr", action="store")
parser.add_option("-p", "--period",
                  help="period after CliMAF syntax, as e.g. 1980-1987",
                  action="store", default="1980")
parser.add_option("-v", "--variables",
                  help="variables list(comma separated)",
                  action="store", default="thetao,so")
#
(opts, args) = parser.parse_args()

# Some settings about data used (model and obs)
#######################################################
# Scaling de la MOC modèle pour homogénéité avec obs RAPID
calias("CMIP5", "msftmyz", scale=1.e-3)

# Obs de MOC RAPID (Il a fallu bricoler les données d'origine pour la dimension time au début et unlim)
dataloc(project="ref_pcmdi", organization="generic",
        url=['/home/esanchez/data_climaf/${variable}_vertical_unlim.nc', ])
calias('ref_pcmdi', 'moc', 'stream_function_mar', filenameVar='moc')

model = dict(project='CMIP5', model='CNRM-CM5', frequency="mon",
             realm="ocean", table="Omon", version="latest",
             period=opts.period, experiment=opts.simulation, simulation="r1i1p1")
levitus = dict(project="ref_pcmdi", product='NODC-Levitus', clim_period='*')


# Basic functions
#######################
def model_vs_obs_profile_oce(variable, model, obs, masks='/data/esanchez/Atlas/oce/mask'):
    """
    Given two dataset specifications, and an oceanic variable name,
    create a figure for profile for the variable in both sources

    dataset specifications are dictionaries

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
    modvar = ds(variable=variable, **model)
    obsvar = ds(variable=variable, **obs)

    # - Compute temporal means
    tmean_modvar = ccdo(modvar, operator='timavg -yearmonmean')
    tmean_obsvar = ccdo(obsvar, operator='yearmonmean')

    # - Compute model profile using CdfTools (this requires some pre-processing)
    fixed_fields('ccdfmean_profile',
                 ('mask.nc', masks + '/ORCA1_mesh_mask.nc'),
                 ('mesh_hgr.nc', masks + '/ORCA1_mesh_hgr.nc'),
                 ('mesh_zgr.nc', masks + '/ORCA1_mesh_zgr.nc'))
    vertprof_modvar = ccdfmean_profile(tmean_modvar, pos_grid='T')

    # Obs profile is simpler to compute, thanks to a regular grid
    vertprof_obsvar = ccdo(tmean_obsvar, operator='mermean -zonmean')

    # - Plot vertical profile of model & obs data
    myplot = plot(vertprof_obsvar, vertprof_modvar, title='MOD&OBS - ' + variable,
                  y="index", aux_options="xyLineColor='red'", invXY=False)

    return myplot


def plot_basin_moc(model, variable="msftmyz", basin=1):
    # Plot a model MOC slice
    moc_model = ds(variable=variable, **model)
    moc_model_mean = time_average(moc_model)
    # extraire le bassin de rang 'basin' (def: Atlantique=1)
    moc_model_mean_atl = cslice_average(moc_model_mean, dim='x', min=basin, max=basin)
    # masquer les valeurs
    moc_model_mean_atl_mask = mask(moc_model_mean_atl, miss=0.0)
    # Plot
    plot_moc_slice = plot(moc_model_mean_atl_mask, title="MOC", y="lin",
                          min=-10., max=30., delta=1., scale=1e-3, units="Sv", options="trXMinF=-30.")
    return plot_moc_slice


# Profil de MOC, vs Obs RAPID
def moc_profile_vs_obs_rapid(model, variable="msftmyz", basin=1):
    """
    Model is a dict defining the model dataset (except variable)
    """
    # Comparer les profils de MOC modèle/RAPID a la latitude 26
    mod = model.copy()
    mod.update({'variable': variable})
    moc_model = ds(**mod)
    moc_model_mean = time_average(moc_model)
    # extraire le bassin Atlantique de la MOC modele
    moc_model_mean_atl = cslice_average(moc_model_mean, dim='x', min=basin, max=basin)
    # masquer les valeurs et extraire la latitude 26
    moc_model_mean_atl_mask = mask(moc_model_mean_atl, miss=0.0)
    moc_model_26 = cslice_average(moc_model_mean_atl_mask, dim='lat', min=26.5, max=26.5)
    #
    moc_obs = ds(project="ref_pcmdi", variable='moc')
    moc_obs_mean = time_average(moc_obs)
    #
    plot_profile_obs = plot(moc_model_26, moc_obs_mean, title='RAPID',
                            y="lin", units="Sv", aux_options="xyLineColor='red'")
    return plot_profile_obs


# Init html index
#########################################################################
# if opts.directory : atlas_dir=os.path.expanduser(opts.directory)

index = header("Nemo CliMAF Atlas for " + opts.simulation + " and period " + opts.period)
index += section("ocean", level=4)

# A table with one line per variable, showing its global average profile
#########################################################################
index += open_table()

# Table title line
index += open_line('VARIABLE') + cell('profile') + cell('map') + close_line()
lvars = opts.variables.split(',')

# Loop on variables, one per line
for variable in lvars:
    profile = model_vs_obs_profile_oce(variable, model, levitus)
    index += open_line(variable) + cell("", cfile(profile), thumbnail="70*70", hover=True, altdir=opts.alt_dir_name)
    close_line()
index += close_table()

# Some more plots
#########################################################################
index += vspace(2)
moc_profile = moc_profile_vs_obs_rapid(model)
moc_atl = plot_basin_moc(model, basin=1)
index += line({"moc_profile": cfile(moc_profile), "moc_atl": cfile(moc_atl)},
              title="Autres:   ", hover=True, altdir=opts.alt_dir_name)

index += trailer()

out = opts.index
if opts.alt_dir_name:
    outfile = cachedir + "/" + out
    with open(outfile, "w") as filout:
        filout.write(index)
    print("index actually writtten as : " + outfile)
    print("may be seen at " + opts.root_url + outfile.replace(cachedir, opts.alt_dir_name))
else:
    with open(out, "w") as filout:
        filout.write(index)
    print("The atlas is ready as %s" % out)
    # print("You may copy it using : scp -r "+os.system("uname -n")+":%s ...."%(atlas_dir))
    # print("Attendez un bon peu : lancemement de firefox sur Ciclad....")
    # os.system("firefox file://"+os.path.abspath(os.path.curdir)+"/"+out+"&")


def spare_code():
    # Example for defining a data organization in a project
    cproject("dmc", "root")
    cdef("root", "/data/mcheval")
    dataloc(project="dmc", organization="generic",
            url="${root}/${simulation}/${simulation}_1m_YYYYMMDD_YYYYMMDD_grid_${variable}.nc")
    calias("dmc", 'tos', filenameVar='T')
    tos = ds(project='dmc', simulation='O1IAF01', variable='tos', period='1980')
    print(tos)
