from CM_atlas.plot_CM_atlas import *
from climaf.api import *
from climaf.html import *
from reference import variable2reference
from LMDZ_SE_atlas.lmdz_SE import *
from time_manager import *
from climaf import __path__ as cpath
import os
from climaf import cachedir
import shutil

StringFontHeight = 0.019

# main_cesmep_path

hover = False

# -- Set a blank space
# -----------------------------------------------------------------------------------
blank_cell = os.path.dirname(__file__) + '/Empty.png'

# -- Add the variable and get the dataset
wdat = dat.copy()
wdat.update(dict(variable=variable))
# -- Apply the frequency and time manager (IGCM_OUT)
frequency_manager_for_diag(wdat, diag='SE')
get_period_manager(wdat)
print wdat


# -- Function to produce a section of 2D maps (both atmosphere and ocean variables)
# -----------------------------------------------------------------------------------
def section_WaterBudget(models, main_cesmep_path, safe_mode=True):
    #
    # -- Upper band at the top of the section
    index = section(section_title, level=4)
    #
    # -- Open the html table of this section
    index += open_table()
    #
    # -- Start the line with the title
    if not line_title:
        wline_title = varlongname(variable) + ' (' + variable + ') ; season = ' + season
    else:
        wline_title = line_title
    index += start_line(wline_title)
    #
    # -- Loop on the models and compute the difference against the reference
    for model in models:
        # -- Compute the water budget for model; save in a json file (or dictionary)
        # -- Do the figures: get the template and edit a copy
        # --   - Summary
        # --   - LMDz
        # --   - NEMO
        # --   - ORCHIDEE
        index += cell("", model_diff, thumbnail=thumbN_size, hover=hover, **alternative_dir)
        #
    # -- Close the line
    close_line()
    index += close_table()
    #
    # -- Close the table of the section
    return index
