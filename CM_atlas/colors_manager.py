# -- Color palettes for time series, dots, //coordinates
# -- R
cesmep_R_colors      = ['dodgerblue3','firebrick1','green4','darkturquoise','goldenrod1',
                        'navyblue','green2','steelblue','deeppink',
                        'blue','darkgoldenrod2','yellowgreen','darkorchid3','darkgoldenrod','darkgreen',
                        'orchid3','slategray', 'gold','green','saddlebrown','tan',
                        'coral','violetred','aquamarine2','firebrick']
# -- python
cesmep_python_colors = ['royalblue', 'red', 'green', 'mediumturquoise', 'orange',
                        'navy', 'limegreen', 'steelblue', 'fuchsia',
                        'blue', 'goldenrod', 'yellowgreen', 'blueviolet', 'darkgoldenrod', 'darkgreen',
                        'mediumorchid', 'lightslategray', 'gold', 'chartreuse', 'saddlebrown', 'tan',
                        'tomato', 'mediumvioletred', 'mediumspringgreen', 'firebrick',
                        ]

# -- add more default colors
from matplotlib import colors as mcolors
mpcolors = sorted(mcolors.CSS4_COLORS.keys())
# -- Remove white-ish colors
mpcolors.remove('white')
#mpcolors.remove('w')
mpcolors.remove('snow')
mpcolors.remove('seashell')
mpcolors.remove('floralwhite')
mpcolors.remove('cornsilk')
mpcolors.remove('ivory')
mpcolors.remove('beige')
mpcolors.remove('lightyellow')
mpcolors.remove('lightgoldenrodyellow')
mpcolors.remove('honeydew')
mpcolors.remove('mintcream')
mpcolors.remove('azure')
mpcolors.remove('aliceblue')
mpcolors.remove('ghostwhite')
mpcolors.remove('lavender')
mpcolors.remove('lavenderblush')
mpcolors.remove('linen')
mpcolors.remove('whitesmoke')
mpcolors.remove('oldlace')
mpcolors.remove('lemonchiffon')
mpcolors.remove('lightcyan')
mpcolors.remove('papayawhip')
mpcolors.remove('blanchedalmond')
mpcolors.remove('bisque')
mpcolors.remove('antiquewhite')
mpcolors.remove('palegoldenrod')
mpcolors.remove('wheat')
mpcolors.remove('thistle')

# and duplicates
mpcolors.remove('dimgrey')
mpcolors.remove('grey')
mpcolors.remove('lightgrey')
mpcolors.remove('darkgrey')
mpcolors.remove('lightslategrey')
mpcolors.remove('slategrey')
mpcolors.remove('darkslategrey')

for tmpcolor in mpcolors:
   if tmpcolor in cesmep_python_colors: mpcolors.remove(tmpcolor)

cesmep_python_colors = cesmep_python_colors + mpcolors

import matplotlib

def colors_manager(dataset_list,default_colors, colors_list=[], method='start_with_colors_list'):
    '''colors_manager returns a list of colors that combines default '''
    '''colors specified for the C-ESM-EP and user specified colors.  '''
    '''                                                              '''
    ''' It is typically used in the context of the C-ESM-EP:         '''
    '''    - the user provides a list of datasets, like models       '''
    '''      as first argument                                       '''
    '''    - the second argument is the default palette to be used.  '''
    '''      By default we use python colors (cesmep_python_colors)  '''
    '''      but we can use R colors (cesmep_R_colors) or any user   '''
    '''      specified list of colors.                               '''
    '''    - it is also possible to provide a list of colors to      '''
    '''      to start with (only used for the //coordinates plots)   '''
    ''' colors_manager automatically handles duplicate color names   '''
    ''' and gives priority to the user specified colors.             '''
    '''                                                              '''
    hashcolor = []
    for dumcolor in default_colors:
        hashcolor.append(str(matplotlib.colors.cnames[dumcolor]))

    # -- dataset_list is usually called models or Wmodels in the C-ESM-EP
    # -- Loop on the dataset list
    i=0
    wcolors_list = []
    for dumcolor in colors_list:
        wcolors_list.append(str(matplotlib.colors.cnames[dumcolor]))
    #
    color_status = ['default']*len(wcolors_list)
    for dat_dict in dataset_list:
        # -- No color provided by the user
        if not 'color' in dat_dict:
            # -- If the ith default color is already in use, we search for the next one that is not in colors_list
            while hashcolor[i] in wcolors_list: i = i + 1
            tmp_color = hashcolor[i]
            tmp_color_status = 'default'
        else:
            user_color = dat_dict['color']
            if user_color=='blue': user_color=1
            if user_color=='red': user_color=2
            if user_color=='green': user_color=3

            # -- The color provided by the user is either a color name (red, blue...)
            # -- or a number in the default list of colors (works in both R and python colors lists)
            # -- 1. If the color provided is in the form of 'color1', we remove color from the color name
            #if 'color' in user_color: user_color = str.replace(user_color,'color','')
            # -- 2. If the user provided a color number:
            try:
                tmp_color = hashcolor[int(user_color)-1]
            except:
                tmp_color = str(matplotlib.colors.cnames[user_color])
            #
            # -- if tmp_color (provided by the user) is already in the list, we search for the next color
            # -- that is not already in use and change the color in colors_list for this default color
            #tmp_color = str(matplotlib.colors.cnames[tmp_color])
            if tmp_color in wcolors_list:
                if color_status[wcolors_list.index(tmp_color)]=='default':
                   while hashcolor[i] in wcolors_list: i = i + 1
                   replacement_color = hashcolor[i]
                   wcolors_list[wcolors_list.index(tmp_color)] = replacement_color
            #
            tmp_color_status = 'user'
            #
        wcolors_list.append(tmp_color)
        color_status.append(tmp_color_status)
    if method=='end_with_colors_list':
       wcolors_list = wcolors_list[len(colors_list):] + wcolors_list[0:len(colors_list)]
    #
    #hashcolor = []
    #for dumcolor in wcolors_list:
    #    hashcolor.append(str(matplotlib.colors.cnames[dumcolor]))
    return wcolors_list



