from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *
from env.site_settings import *
from env.clogging import clogger
from climaf import __path__ as cpath
from climaf.operators import cscript, fixed_fields

scriptpath = cpath[0] + "/../scripts/"
binpath = cpath[0] + "/../bin/"


def load_plot_operators():

    cscript('plotmap',
            'python3 ' + scriptpath + 'plotmap.py '
            '--projection=${proj} '
            '--projection_option="${proj_options}" '
            '--title="${title}" '
            '--feature_name=${feature_name} '
            '--feature_color=${feature_color} '
            '--output_file=${out} '
            '--coordinates="${coord}" '
            '--format="${format}" '
            '--savefig_options="${savefig_options}" '
            # Colored map
            '--colored_map_file="${in_1}" '
            '--colored_map_variable="${var_1}" '
            '--colored_map_levels=${coll} '
            '--colored_map_colors="${colc}" '
            '--colored_map_transform=${colt} '
            '--colored_map_transform_options="${colto}" '
            # Contour map
            '--contours_map_file="${in_2}" '
            '--contours_map_variable="${var_2}" '
            '--contours_map_levels=${conl} '
            '--contours_map_colors="${conc}" '
            '--contours_map_transform=${cont} '
            '--contours_map_transform_options="${conto}" '
            # Vector map
            '--vector_map_ufile="${in_3}" '
            '--vector_map_vfile="${in_4}" '
            '--vector_map_u_variable="${var_3}" '
            '--vector_map_v_variable="${var_4}" '
            '--vector_map_type="${vecty}" '
            '--vector_map_options="${veco}" '
            '--vector_map_transform=${vect} '
            '--vector_map_transform_options="${vecto}" '
            # Shade map
            '--shade_map_file="${in_5}" '
            '--shade_map_variable="${var_5}" '
            '--shade_map_levels="${shal}" '
            '--shade_map_hatches="${shah}" '
            '--shade_map_transform=${shat} '
            '--shade_map_transform_options="${shato}" '
            # 2nd Shade map
            '--shad2_map_file="${in_6}" '
            '--shad2_map_variable="${var_6}" '
            '--shad2_map_levels="${sh2l}" '
            '--shad2_map_hatches="${sh2h}" '
            '--shad2_map_transform=${sh2t} '
            '--shad2_map_transform_options="${sh2to}" '
            # Annotations
            '--lines="${lines}" '
            '--texts="${texts}" ', format="graph")
