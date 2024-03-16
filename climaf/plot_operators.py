from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *
from env.site_settings import *
from env.clogging import clogger
from climaf import __path__ as cpath
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
