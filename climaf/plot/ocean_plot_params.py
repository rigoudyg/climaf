# -*- coding: iso-8859-1 -*-
# Created : S.Sénési - nov 2015

dict_plot_params = {
        'wfo' : {
            'default' : { 'units' : 'mm/day' , 'color' : 'precip_diff_12lev', 'scale':86400., 'contours':1,'focus':'ocean'},
            'full_field'   : {'colors':"-15 -12 -10 -8 -6 -4 -3 -2 -1 0 1 2 3 4 6 8 10 12 15"},
            'bias'        : {'color':'precip_diff_12lev','colors': "-8 -6 -4 -2 -1 -0.5 0.5 1 2 4 6 8"},
            'model_model' : {'color':'precip_diff_12lev','colors': "-8 -6 -4 -2 -1 -0.5 0.5 1 2 4 6 8"},
        },
        'zos' : {
            'default' : { 'units' : 'm', 'color'  : 'matlab_jet' },
            'full_field'   : {'colors': "-2 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 2" },
            'bias'        : {'colors': "-2 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 2", 'color':'testcmap'},
            'model_model' : {'colors': "-1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1", 'color':'testcmap'},
        },
        'tos'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'full_field'   : {'colors' : "0. 0.5 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-10 -8 -6 -5 -4 -3 -2 -1 -0.5 0 0.5 1 2 3 4 5 6 8 10', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'to200'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'full_field'   : {'colors' : "0. 0.5 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-10 -8 -6 -5 -4 -3 -2 -1 -0.5 0 0.5 1 2 3 4 5 6 8 10', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'to1000'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'full_field'   : {'colors' : "0. 0.5 1 2 3 4 5 6 7 8 9 10 11 12 13"},
            'bias'        : {'colors' : '-5 -4 -3 -2.5 -2 -1.5 -1 -0.5 0 0.5 1 1.5 2 2.5 3 4 5', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'to2000'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'full_field'   : {'colors' : "0. 0.5 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16"},
            'bias'        : {'colors' : '-5 -4 -3 -2.5 -2 -1.5 -1 -0.5 0 0.5 1 1.5 2 2.5 3 4 5', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'sos'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'full_field'   : {'colors':'26 26.5 27 27.5 28 28.5 29 29.5 30 30.5 31 31.5 32 32.5 33 33.5 34 34.5 35 35.5 36 36.5 37 37.5 38 38.5 39 39.5 40'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-10 -5 -4 -3 -2 -1 -0.5 -0.25 0 0.25 0.5 1 2 3 4 5 10'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'so200'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'full_field'   : {'colors':'26 26.5 27 27.5 28 28.5 29 29.5 30 30.5 31 31.5 32 32.5 33 33.5 34 34.5 35 35.5 36 36.5 37 37.5 38 38.5 39 39.5 40'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-5 -4 -3 -2.5 -2 -1.5 -1 -0.5 -0.25 0 0.25 0.5 1 1.5 2 2.5 3 4 5'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'so1000'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'full_field'   : {'colors':'34 34.25 34.5 34.75 35 35.25 35.5 35.75 36 36.25 36.5'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-1.5 -1.25 -1 -0.75 -0.5 -0.25 -0.1 0.1 0.25 0.5 0.75 1 1.25 1.5'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'so2000'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'full_field'   : {'colors':'33 33.25 33.5 33.75 34 34.25 34.5 34.75 35 35.25 35.5 35.75 36 36.25 36.5 36.75 37'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-1.5 -1.25 -1 -0.75 -0.5 -0.25 -0.1 0.1 0.25 0.5 0.75 1 1.25 1.5'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'mlotst'  : {
            'default' : { 'color' : 'precip3_16lev' , 'units':'m', 'focus':'ocean'},
            'full_field'   : {'colors':"50 100 150 200 250 300 400 500 600 700 800 900 1000 1200 1500 2000"},
            'bias'        : {'color':'BlueDarkRed18','colors':"-1000 -750 -500 -400 -300 -250 -200 -150 -100 -75 -50 -10 10 50 75 100 150 200 250 300 400 500 750 1000"},
            'model_model' : {'color':'BlueDarkRed18','colors':"-250 -100 -75 -50 -25 -10 -5 -2 2 5 10 25 50 75 100 250"},
        },
        'hc300'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe', 'units':'J/m2', 'focus':'ocean'},
            'full_field'   : {'colors' : "-3 -2 -1 0 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-10 -8 -6 -5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5 6 8 10', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        # -- Sea ice variables
        'sic'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%', 'focus':'ocean'},
            'full_field'   : {'colors' : "15 20 25 30 40 50 60 70 80 85 90 95"},
            'bias'        : {'colors' : '-50 -40 -30 -25 -20 -15 -10 -5 -1 1 5 10 15 20 25 30 40 50', 'color': 'temp_diff_18lev'},
            'model_model' : {'colors' : '-50 -40 -30 -25 -20 -15 -10 -5 -1 1 5 10 15 20 25 30 40 50', 'color': 'temp_diff_18lev'},
        },
        'sit' : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%', 'focus':'ocean'},
            'full_field'   : {'colors' : "0.1 0.5 1 2 3 4 5 6 7 8 9"},
            'bias'        : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_diff_18lev'},
            'model_model' : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_diff_18lev'},
        },
        'sivolu' : {
            'default'  : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%', 'focus':'ocean'},
            'full_field'   : {'colors' : "0.1 0.5 1 2 3 4 5 6 7 8 9"},
            'bias'        : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_19lev'},
            'model_model' : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_19lev'},
        },
        # -- Surface Turbulent Fluxes
       'hfls' : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'full_field'   : {'colors':'0 20 40 60 80 100 120 140 160 180 200' , 'color':'precip3_16lev' },
            'bias'        : {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50' , 'color':'BlueDarkRed18' },
            'model_model' : {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 15 25 35 45 55', 'color':'BlueDarkRed18'},
        },
       'hfss' : {
            'default' : { 'color' : 'ViBlGrWhYeOrRe' , 'units':'W/m2'},
            'full_field'   : {'colors':'0 10 20 30 40 50 60 70 80 90 100 110 120' , 'color':'precip3_16lev'},
            'bias'        : {'colors': '-10 -8 -6 -4 -2 -1 1 2 4 6 8 10' , 'color':'BlueDarkRed18' },
            'model_model' : {'colors': '-10 -8 -6 -4 -2 -1 1 2 4 6 8 10', 'color':'BlueDarkRed18'},
        },
       'tauu' : {
            'default' : { 'color' : 'testcmap' , 'units':'N/m'},
            'full_field'   : {'colors':'-.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16' ,'color':'ViBlGrWhYeOrRe' },
            'bias'        : {'colors': '-1. -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 1.' , 'color':'ViBlGrWhYeOrRe' },
            'model_model' : {'colors': '-1. -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 1.'},

        },
       'tauv' : {
            'default' : { 'color' : 'testcmap' , 'units':'N/m'},
            'full_field'   : {'colors':'-0.1 -0.08 -0.06 -0.04 -0.02 -0.01 0.01 0.02 0.04 0.06 0.08 0.1' ,'color':'ViBlGrWhYeOrRe' },
            'bias'        : {'colors': '-0.05 -0.04 -0.03 -0.025 -0.02 -0.015 -0.01 -0.005 0.005 0.01 0.015 0.02 0.025 0.03 0.04 0.05' ,'color':'ViBlGrWhYeOrRe' },
            'model_model' : {'colors': '-1. -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 1.'},
        },
}
