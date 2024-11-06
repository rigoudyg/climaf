from __future__ import print_function, division, unicode_literals, absolute_import

import sys
from env.environment import *
from env.site_settings import *
from env.clogging import clogger
from climaf import __path__ as cpath
from climaf import operators
from climaf.operators import cscript, fixed_fields 

scriptpath = cpath[0] + '/../scripts/'
binpath = cpath[0] + '/../bin/'


def load_plot_operators():

    cscript("plotmap",
            "python3 " + scriptpath + "plotmap.py "
            "--projection=${proj} "
            "--projection_option='${proj_options}' "
            "--features='${features}' "
            "--axis_methods='${axis_methods}' "
            "--gv_methods='${gv_methods}' "
            "--plt_methods='${plt_methods}' "
            "--output_file=${out} "
            "--format=${format} "
            "--debug='${debug}' "
            "--figure_options='${figure_options}' "
            "--savefig_options='${savefig_options}' "
            "--title_options='${title_options}' "
            "--show='${show}' "
            #
            # Colored map
            #
            "--colored_map_file='${in_1}' "
            "--colored_map_variable='${var_1}' "
            "--colored_map_levels='${colored_map_levels}' "
            "--colored_map_levels='${clrl}' "
            "--colored_map_levels='${levels}' "
            "--colored_map_levels='${colors}' "
            "--colored_map_cmap='${colored_map_cmap}' "
            "--colored_map_cmap='${cmap}' "
            "--colored_map_cmap='${color}' "
            "--colored_map_transform=${colored_map_transform} "
            "--colored_map_transform=${clrt} "
            "--colored_map_transform_options='${colored_map_transform_options}' "
            "--colored_map_transform_options='${clrto}' "
            "--colored_map_selection_options='${colored_map_selection_options}' "
            "--colored_map_selection_options='${clrso}' "
            "--colored_map_engine=${colored_map_engine} "
            "--colored_map_engine=${clre} "
            "--colored_map_engine_options='${colored_map_engine_options}' "
            "--colored_map_engine_options='${clreo}' "
            "--colored_map_min='${colored_map_min}' "
            "--colored_map_min='${clrn}' "
            "--colored_map_min=${min} "
            "--colored_map_max='${colored_map_max}' "
            "--colored_map_max='${clrx}' "
            "--colored_map_max=${max} "
            "--colored_map_delta=${colored_map_delta} "
            "--colored_map_delta=${delta} "
            "--colored_map_scale='${colored_map_scale}' "
            "--colored_map_scale='${clrs}' "
            "--scale=${scale} "
            "--colored_map_offset='${colored_map_offset}' "
            "--colored_map_offset='${clro}' "
            "--offset=${offset} "
            "--colored_map_methods='${colored_map_methods}' "
            "--colored_map_methods='${clrm}' "
            "--vcb='${vcb}' "
            "--colorbar_options='${colorbar_options}' "
            "--colorbar_options='${clrco}' "
            #
            # Contour map
            #
            "--contours_map_file='${in_2}' "
            "--contours_map_variable='${var_2}' "
            "--contours_map_levels='${contours_map_levels}' "
            "--contours_map_levels='${contours}' "
            "--contours_map_colors='${contours_map_colors}' "
            "--contours_map_colors='${cntc}' "
            "--contours_map_transform=${contours_map_transform} "
            "--contours_map_transform=${cntt} "
            "--contours_map_transform_options='${contours_map_transform_options}' "
            "--contours_map_transform_options='${cntto}' "
            "--contours_map_selection_options='${contours_map_selection_options}' "
            "--contours_map_selection_options='${cntso}' "
            "--contours_map_engine_options='${contours_map_engine_options}' "
            "--contours_map_engine_options='${cnteo}' "
            "--contours_map_min='${contours_map_min}' "
            "--contours_map_min='${cntn}' "
            "--contours_map_max='${contours_map_max}' "
            "--contours_map_max='${cntx}' "
            "--contours_map_scale='${contours_map_scale}' "
            "--contours_map_scale='${cnts}' "
            "--contours_map_offset='${contours_map_offset}' "
            "--contours_map_offset='${cnto}' "
            #
            # Vector map
            #
            "--vectors_map_u_file='${in_3}' "
            "--vectors_map_v_file='${in_4}' "
            "--vectors_map_u_variable='${var_3}' "
            "--vectors_map_v_variable='${var_4}' "
            "--vectors_map_type=${vectors_map_type} "
            "--vectors_map_type=${vecty} "
            "--vectors_map_options='${vectors_map_options}' "
            "--vectors_map_options='${veco}' "
            "--vectors_map_transform=${vectors_map_transform} "
            "--vectors_map_transform=${vect} "
            "--vectors_map_transform_options='${vectors_map_transform_options}' "
            "--vectors_map_transform_options='${vecto}' "
            "--vectors_map_selection_options='${vectors_map_selection_options}' "
            "--vectors_map_selection_options='${vecso}' "
            "--vectors_map_scale='${vectors_map_scale}' "
            "--vectors_map_scale='${vecs}' "
            "--vectors_map_gridsizes='${vectors_map_gridsizes}' "
            "--vectors_map_gridsizes='${vecg}' "
            #
            # Shade map
            #
            "--shaded_map_file='${in_5}' "
            "--shaded_map_variable='${var_5}' "
            "--shaded_map_levels='${shaded_map_levels}' "
            "--shaded_map_levels='${shdl}' "
            "--shaded_map_hatches='${shaded_map_hatches}' "
            "--shaded_map_hatches='${shdh}' "
            "--shaded_map_transform=${shaded_map_transform} "
            "--shaded_map_transform=${shdt} "
            "--shaded_map_transform_options='${shaded_map_transform_options}' "
            "--shaded_map_transform_options='${shdto}' "
            "--shaded_map_min='${shaded_map_min}' "
            "--shaded_map_min='${shdn}' "
            "--shaded_map_max='${shaded_map_max}' "
            "--shaded_map_max='${shdx}' "
            "--shaded_map_scale='${shaded_map_scale}' "
            "--shaded_map_scale='${shds}' "
            "--shaded_map_offset='${shaded_map_offset}' "
            "--shaded_map_offset='${shdo}' "
            #
            # 2nd Shade map
            #
            "--shade2_map_file='${in_6}' "
            "--shade2_map_variable='${var_6}' "
            "--shade2_map_levels='${shade2_map_levels}' "
            "--shade2_map_levels='${shdl}' "
            "--shade2_map_hatches='${shade2_map_hatches}' "
            "--shade2_map_hatches='${shdh}' "
            "--shade2_map_transform=${shade2_map_transform} "
            "--shade2_map_transform=${shdt} "
            "--shade2_map_transform_options='${shade2_map_transform_options}' "
            "--shade2_map_transform_options='${shdto}' "
            "--shade2_map_min='${shade2_map_min}' "
            "--shade2_map_min='${shdn}' "
            "--shade2_map_max='${shade2_map_max}' "
            "--shade2_map_max='${shdx}' "
            "--shade2_map_scale='${shade2_map_scale}' "
            "--shade2_map_scale='${shds}' "
            "--shade2_map_offset='${shade2_map_offset}' "
            "--shade2_map_offset='${shdo}' "
            #
            # gplot.ncl compatibility
            #
            "--title=${title} "
            "--trim='${trim}' "
            "--resolution=${resolution} "
            "--dpi=${dpi} "
            "--focus=${focus} "
            "--units=${units} "
            "--date=${date} "
            "--time=${time} "
            "--level=${level} "
            "--print_time=${print_time} "
            "--xpolyline=${xpolyline} "
            "--ypolyline=${ypolyline} "
            "--polyline_options='${polyline_options}' ",
            format='graph')


def plot(*largs, forbid_plotmap=False, **kwargs):
    """ 
    A replacement for old CliMAF plot operator, which uses plotmap, 
    simplifies the plot if needed, and keep tracks of arguments not managed by plotmaps
    """
    caller = sys._getframe().f_back.f_code.co_name
    
    if not env.environment.plot_use_plotmap or forbid_plotmap:
        rep = operators.plot(*largs,**kwargs)
        clogger.info("Plotmap warning: using old plot for %s. Caller is :%s"%(rep.crs,caller))
        return(rep)
    
    # Should check that input data has two horizontal dimensions ...
    
    # Transfer positional arguments (input fields)
    main=largs[0]
    if len(largs)>1 :
        aux = largs[1]
    else:
        aux = ""                
    if len(largs)>3 :
        u = largs[2]
        v = largs[3]
    else:
        u = ""
        v = ""
    if len(largs)>4 :
        shade2 = largs[4]
    else:
        shade2 = ""
    
    compatible_args = [ "title", "trim", "resolution", "format", "focus", "proj", 
                        "xpolyline", "ypolyline", "date", "time", "level", "color",
                        "min", "max", "delta", "colors", "scale", "offset", "units",
                        "contours", "options", "aux_options", "scale_aux", "offset_aux"]
    
    incompatible_args = [ "y" ]
    
    unmanaged_args    = [ "fmt", "reverse", "rotation", 
                          "shading_options", "shade2_options", "polyline_options", 
                          "shade_below", "shade_above", "shade2_below", "shade2_above",
                          "vcRefLengthF", "vcRefMagnitudeF", "vcMinDistanceF", "vcLineArrowColor", ]
    
    compatible_projections = [ "Orthographic", "Stereographic", "AzimuthalEquidistant",
                               "Gnomonic", "Mercator", "LambertConformal", "Robinson",
                               "Hammer", "Mollweide", "PlateCarree"]
    must_use_old_plot = False
    
    # shade_above et al. : a affiner
    outargs=dict()
    for arg in kwargs.keys() :
        if arg in compatible_args :
            outargs[arg] = kwargs[arg]
            #
            # Title may include Ncl escape characters ~
            if arg == "title" and "~" in kwargs[arg]:
                clogger.info("Plotmap warning: Title has NCL control characters: %s"%kwargs[arg] +\
                             ". Caller is %s:"%caller)
                
            # Resolution may be a paper format name (e.g. A4), not managed by plotmap
            if arg == "resolution" and \
               any([ str.isalpha(x) and x != "x" for x in kwargs[arg]]):
                clogger.info("Plotmap warning: Cannot handle required format %s"%kwargs[arg] +\
                             ". Caller is :%s"%caller)
                outargs.pop(arg)

            # "proj" : change Ncl names in  Cartopy's , when applicable
            if arg == "proj":
                proj = kwargs["proj"]
                if proj[0:2] in [ "NH", "SH" ] :
                    pass
                elif proj in compatible_projections :
                    pass
                else:
                    clogger.info(f"Plotmap warning: Projection {proj} is "\
                                 f"not (yet) managed. Caller is :{caller}")
                    outargs.pop(arg)

            # polylines: change syntax
            if arg [1:] == "polyline":
                outargs[arg] = kwargs[arg].replace(","," ")
                
            # color : forbid lists of color names (criterion : has ",")
            if arg == "color" and "," in kwargs[arg] :
                clogger.info("Plotmap warning: Cannot handle list of colors in color=%s"%kwargs[arg] +\
                             ". Caller is %s:"%caller)
                outargs.pop(arg)
                
            # contours : change ”230 240 250” to [230, 240, 250]
            if arg == "contours" and kwargs["contours"] != 1:
                outargs[arg] = kwargs[arg].split(" ")

            if arg == "options" :
                outargs.pop(arg)
                options = kwargs["options"].split("|")
                for option in options:
                    if "=" in option:
                        param,value=option.split("=")
                        if param == "gsnAddCyclic" :
                            pass  # This is automatic in plotmap
                        elif param == "mpProjection":
                            if value in compatible_projections:
                                outargs["proj"] = value                        
                        else:
                            clogger.info(f"Plotmap warning: Option {param} is not managed "+\
                                         f"(value is {kwargs[arg]}). Caller is : {caller}")
                
            if arg == "aux_options" :
                outargs.pop(arg)
                aux_options = kwargs["aux_options"].split("|")
                if "contours_map_engine_options" not in outargs:
                    outargs["contours_map_engine_options"] = dict()
                for option in aux_options:
                    if "=" in option:
                        param,value=option.split("=")
                        if param == "cnLineThicknessF" :
                            outargs["contours_map_engine_options"]["linewidths"] = int(value)
                        else:
                            clogger.info(f"Plotmap warning: aux_option {param} is not managed" +\
                                         ". Caller is :%s"%caller)
                            
        elif arg in unmanaged_args :
            clogger.info(f"Plotmap warning: Unmanaged arg {arg} = {kwargs[arg]}" +\
                         ". Caller is :%s"%caller)

        elif arg in incompatible_args :
            clogger.info(f"Plotmap warning: Incompatible arg {arg} = {kwargs[arg]}" +\
                         ". Caller is :%s"%caller)
            #clogger.info(f"Plotmap warning: -> will use old plot")
            must_use_old_plot = True

        elif arg == "vcGlyphStyle":
            oarg= 'vectors_map_type'
            style = kwargs[arg]
            if style in [ "LineArrow", "FillArrow" ]:
                outargs[oarg] = 'quiver'
            elif style == "WindBarb":
                outargs[oarg] = 'barbs'
            elif style == "CurlyVector":
                outargs[oarg] = 'streamplot'

        elif arg.lower() == "mpcenterlonf":
            outargs["proj_options"] = {'central_longitude' : kwargs[arg]}

        elif arg == "gsnLeftString":
            if "title_options" not in outargs:
                outargs["title_options"] = dict()
            if "lefttitle" in outargs["title_options"]:
                center_title = outargs["title_options"]["lefttitle"] 
                outargs["title_options"]["lefttitle"] = kwargs[arg] + " / " + center_title
            else:
                outargs["title_options"]["lefttitle"] = kwargs[arg]

        elif arg == "gsnCenterString":
            if "title_options" not in outargs:
                outargs["title_options"] = dict()
            if "lefttitle" in outargs["title_options"]:
                left_title = outargs["title_options"]["lefttitle"] 
                outargs["title_options"]["lefttitle"] = left_title + " / " + kwargs[arg]
            else:
                outargs["title_options"]["lefttitle"] = kwargs[arg]
                
        elif arg == "gsnRightString":
            if "title_options" not in outargs:
                outargs["title_options"] = dict()
            outargs["title_options"]["righttitle"] = kwargs[arg]
            
        elif arg == "gsnStringFontHeightF":
            if "title_options" not in outargs:
                outargs["title_options"] = dict()
            outargs["title_options"]["righttitlefontsize"] = 1000. * kwargs[arg]
            outargs["title_options"]["lefttitlefontsize"] = 1000. * kwargs[arg]
            
        elif arg == "tiMainFontHeightF":
            if "title_options" not in outargs:
                outargs["title_options"] = dict()
            outargs["title_options"]["maintitlefontsize"] = 1000. * kwargs[arg]

        elif arg == "scale_aux":
            outargs.pop(arg)
            outargs["contours_map_scale"] = kwargs[arg]

        elif arg == "offset_aux":
            outargs.pop(arg)
            outargs["contours_map_offset"] = kwargs[arg]

        else:
            clogger.info(f"Plotmap warning: Unknown arg {arg} (= {kwargs[arg]})" +\
                         ". Caller is %s:"%caller)
            outargs[arg] = kwargs[arg]
            
    # if 'proj' not in outargs:
    #     outargs["proj"] = "PlateCarree"

    if must_use_old_plot :
        rep = operators.plot(*largs,**kwargs)
        clogger.info("Plotmap warning: using old plot for %s"%rep.crs + \
                     ". Caller is :%s"%caller)
        return(rep)

    rep=operators.plotmap(main, aux, u, v, shade2, **outargs)
    if env.environment.teach_me_plotmap :
        print("Plotmap call: %s"%rep.crs)
    return(rep)
            
                  
