# -*- coding: iso-8859-1 -*-
# Created : S.Sénési - nov 2015

"""
Une fonction qui rend des paramètres régissant l'apparence de
graphiques, en fonction de la variable géophysique et du contexte

Encore au stade de brouilllon ; peu de variables traitées

"""

def plot_params(variable,context) :
    """
    Return plot parameters as a dict(), according to LMDZ habits , for a given
    variable and a context (among fullfield, bias, model_model)

    """

    defaults = { 
        'contours' : 1 ,
        'color'    :'matlab_jet',
    }

    per_variable = {
        # -- General atmosphere surface variables
        'tas' : {
            'default' : { 'units' : 'degC' , 'color' : 'BlueDarkRed18' },
            'fullfield'   : {'colors':'-60 -50 -40 -30 -25 -20 -18 -14 -10 -6 0 6 10 14 18 20 22 26 27 28 30', 'offset':-273.15},
            'bias'        : {'color':'hotcold_18lev','colors': '-8 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 8 ','offset':0.0},
            'model_model' : {'color':'hotcold_18lev', 'min':-5,'max':5,'delta':0.5,'offset':0.0},
        },
        'psl' : {
            'default' : { 'scale'  : 0.01 , 'units' : 'hPa', 'color'  : 'matlab_jet' },
            'fullfield'   : {'colors': "975 980 985 990 995 1000 1005 1010 1015 1020 1025 1030 1040 1050 1070 1100" },
            'bias'        : {'colors': "-100 -90 -80 -70 -60 -50 -40 -30 -20 -17.5 -15 -12.5 -10 -7.5 -5 -2.5 -1 -0.5 0.5 1 2.5 5 7.5 10 12.5 15 17.5 20 30 40 50 60 70 80 90 100", 'color':'testcmap'},
            'model_model' : {'colors': "-20 -17.5 -15 -12.5 -10 -7.5 -5 -2.5 -1 -0.5 0.5 1 2.5 5 7.5 10 12.5 15 17.5 20", 'color':'testcmap'},
        },
        'wfo' : {
            'default' : { 'units' : 'mm/day' , 'color' : 'precip_diff_12lev', 'scale':86400., 'contours':1},
            'fullfield'   : {'colors':"-15 -12 -10 -8 -6 -4 -3 -2 -1 0 1 2 3 4 6 8 10 12 15"},
            'bias'        : {'color':'precip_diff_12lev','colors': "-8 -6 -4 -2 -1 -0.5 0.5 1 2 4 6 8"},
            'model_model' : {'color':'precip_diff_12lev','colors': "-8 -6 -4 -2 -1 -0.5 0.5 1 2 4 6 8"},
        },
        'zos' : {
            'default' : { 'units' : 'm', 'color'  : 'matlab_jet' },
            'fullfield'   : {'colors': "-2 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 2" },
            'bias'        : {'colors': "-2 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 2", 'color':'testcmap'},
            'model_model' : {'colors': "-1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1", 'color':'testcmap'},
        },
        'pr' : {
            'default' : { 'units' : 'mm/day' , 'color' : 'precip_11lev', 'scale':86400., 'contours':1},
            'fullfield'   : {'colors':"0.5 1 1.5 2 3.5 4 5 6 7 8 10 12 14"},
            'bias'        : {'color':'precip_diff_12lev','colors': "-5 -4 -3 -2 -1 -0.5 -0.1 0.1 0.5 1 2 3 4 5"},
            'model_model' : {'color':'precip_diff_12lev','colors': "-2 -1.5 -1 -0.5 -0.1 0.1 0.5 1 1.5 2"},
        },
        'uas'  : {
            'default' : { 'color' : 'testcmap' , 'units':'m/s'},
            'fullfield'   : {'colors':'-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 7 8 9 10'},
            'bias'        : {'min':-10,'max':10,'delta':1},
            'model_model' : {'min':-5,'max':5,'delta':0.5},
        },
        'vas'  : {
            'default' : { 'color' : 'testcmap' , 'units':'m/s'},
            'fullfield'   : {'colors':'-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 7 8 9 10'},
            'bias'        : {'min':-10,'max':10,'delta':1},
            'model_model' : {'min':-5,'max':5,'delta':0.5},
        },
        'huss'  : {
            'default' : { 'color' : 'precip_11lev' , 'units':'g/g'},
            'fullfield'   : {'colors':'0 0.002 0.004 0.006 0.008 0.01 0.012 0.014 0.016 0.018 0.02'},
            'bias'        : {'min':-0.005,'max':0.005,'delta':0.0005, 'color':'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-0.001,'max':0.001,'delta':0.0001 , 'color':'ViBlGrWhYeOrRe'},
        },
        'sfcWind'  : {
            'default' : { 'color' : 'WhiteBlueGreenYellowRed' , 'units':'m/s', 'focus':'ocean'},
            'fullfield'   : {'colors':'0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6 6.5 7 7.5 8 8.5 9 9.5 10 11 12 '},
            'bias'        : {'min':-5,'max':5,'delta':0.5, 'color':'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-2.5,'max':2.5,'delta':0.2 , 'color':'ViBlGrWhYeOrRe'},
        },
        'ua'  : {
            'default' : { 'color' : 'ViBlGrWhYeOrRe' , 'units':'m/s'},
            'fullfield'   : {'colors':'-40 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 40'},
            'bias'        : {'min':-20,'max':20,'delta':2},
            'model_model' : {'min':-10,'max':10,'delta':1},
        },
        'va'  : {
            'default' : { 'color' : 'ViBlGrWhYeOrRe' , 'units':'m/s'},
            'fullfield'   : {'colors':'-5 -4 -3 -2 -1.5 -1 -0.5 -0.2 -0.1 -0.05 0.05 0.1 0.2 0.5 1 1.5 2 3 4 5'},
            'bias'        : {'min':-1,'max':1,'delta':0.05},
            'model_model' : {'min':-1,'max':1,'delta':0.05},
        },
        'ta' : {
            'default' : { 'units' : 'degC' , 'color' : 'BlueDarkRed18', 'offset':-273.15 },
            'fullfield'   : {'colors':'-70 -50 -40 -30 -20 -10 0 5 10 15 20 25 30 25'},
            'bias'        : {'min':-10,'max':10,'delta':1,'offset':0.0},
            'model_model' : {'min':-10,'max':10,'delta':1,'offset':0.0},
        },
        'hus'  : {
            'default' : { 'color' : 'precip_11lev' , 'units':'g/g'},
            'fullfield'   : {'colors':'0.00001 0.0001 0.0005 0.001 0.002 0.003 0.004 0.006 0.008 0.01 0.012 0.014 0.016 0.02'},
            'bias'        : {'min':-0.005,'max':0.005,'delta':0.0005, 'color':'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-0.001,'max':0.001,'delta':0.0001 , 'color':'ViBlGrWhYeOrRe'},
        },


        # -- Surface Ocean variables
        'tos'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'fullfield'   : {'colors' : "0. 0.5 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-10 -8 -6 -5 -4 -3 -2 -1 -0.5 0 0.5 1 2 3 4 5 6 8 10', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'to200'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'fullfield'   : {'colors' : "0. 0.5 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-10 -8 -6 -5 -4 -3 -2 -1 -0.5 0 0.5 1 2 3 4 5 6 8 10', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'to1000'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'fullfield'   : {'colors' : "0. 0.5 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-5 -4 -3 -2.5 -2 -1.5 -1 -0.5 0 0.5 1 1.5 2 2.5 3 4 5', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'to2000'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'offset': -273.15 , 'units':'degC', 'focus':'ocean'},
            'fullfield'   : {'colors' : "0. 0.5 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-5 -4 -3 -2.5 -2 -1.5 -1 -0.5 0 0.5 1 1.5 2 2.5 3 4 5', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        'sos'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'fullfield'   : {'colors':'26 26.5 27 27.5 28 28.5 29 29.5 30 30.5 31 31.5 32 32.5 33 33.5 34 34.5 35 35.5 36 36.5 37 37.5 38 38.5 39 39.5 40'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-10 -5 -4 -3 -2 -1 -0.5 -0.25 0 0.25 0.5 1 2 3 4 5 10'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'so200'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'fullfield'   : {'colors':'26 26.5 27 27.5 28 28.5 29 29.5 30 30.5 31 31.5 32 32.5 33 33.5 34 34.5 35 35.5 36 36.5 37 37.5 38 38.5 39 39.5 40'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-5 -4 -3 -2.5 -2 -1.5 -1 -0.5 -0.25 0 0.25 0.5 1 1.5 2 2.5 3 4 5'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'so1000'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'fullfield'   : {'colors':'26 26.5 27 27.5 28 28.5 29 29.5 30 30.5 31 31.5 32 32.5 33 33.5 34 34.5 35 35.5 36 36.5 37 37.5 38 38.5 39 39.5 40'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-2.5 -2 -1.5 -1 -0.5 -0.25 -0.1 0 0.1 0.25 0.5 1 1.5 2 2.5'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'so2000'  : {
            'default' : { 'color' : 'matlab_jet' , 'units':'psu', 'focus':'ocean'},
            'fullfield'   : {'colors':'26 26.5 27 27.5 28 28.5 29 29.5 30 30.5 31 31.5 32 32.5 33 33.5 34 34.5 35 35.5 36 36.5 37 37.5 38 38.5 39 39.5 40'},
            'bias'        : {'color':'BlueDarkRed18','colors' : '-5 -4 -3 -2.5 -2 -1.5 -1 -0.5 -0.25 0 0.25 0.5 1 1.5 2 2.5 3 4 5'},
            'model_model' : {'color':'BlueDarkRed18','colors' : '-2 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 2'},
        },
        'mlotst'  : {
            'default' : { 'color' : 'precip3_16lev' , 'units':'m', 'focus':'ocean'},
            'fullfield'   : {'colors':"5 10 25 50 100 150 200 300 400 600 800 1000 1500 2000"},
            'bias'        : {'color':'BlueGreen14','colors':"-250 -100 -75 -50 -25 -10 -5 -2 2 5 10 25 50 75 100 250"},
            'model_model' : {'color':'BlueGreen14','colors':"-250 -100 -75 -50 -25 -10 -5 -2 2 5 10 25 50 75 100 250"},
        },
        'hc300'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe', 'units':'J/m2', 'focus':'ocean'},
            'fullfield'   : {'colors' : "-3 -2 -1 0 1 2 3 4 6 8 10 12 14 16 18 20 22 24 26 28 30"},
            'bias'        : {'colors' : '-10 -8 -6 -5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5 6 8 10', 'color': 'temp_19lev', 'offset':0},
            'model_model' : {'colors' : '-5 -3 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 3 5', 'color': 'temp_19lev', 'offset':0},
        },
        # -- Sea ice variables
        'sic'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%', 'focus':'ocean'},
            'fullfield'   : {'colors' : "15 20 25 30 40 50 60 70 80 85 90 95"},
            'bias'        : {'colors' : '-50 -40 -30 -25 -20 -15 -10 -5   0   5 10 15 20 25 30 40 50', 'color': 'temp_19lev'},
            'model_model' : {'colors' : '-50 -40 -30 -25 -20 -15 -10 -5 2 0 2 5 10 15 20 25 30 40 50', 'color': 'temp_19lev'},
        },
        'sithic' : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%', 'focus':'ocean'},
            'fullfield'   : {'colors' : "0.1 0.5 1 2 3 4 5 6 7 8 9"},
            'bias'        : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_19lev'},
            'model_model' : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_19lev'},
        },
        #'sivolu' : {
        #    'default'  : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%', 'focus':'ocean'},
        #    'fullfield'   : {'colors' : "0.1 0.5 1 2 3 4 5 6 7 8 9"},
        #    'bias'        : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_19lev'},
        #    'model_model' : {'colors' : '-5 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 5', 'color': 'temp_19lev'},
        #},
        # -- Surface Turbulent Fluxes
        'hfls'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' :'0 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200' },
            'bias'        : {'min':-40, 'max':40, 'delta':5, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-10, 'max':10, 'delta':1, 'color': 'ViBlGrWhYeOrRe'},
        },
        'hfss'  : {
            'default' : { 'color' : 'ViBlGrWhYeOrRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50 60 70 80 90 100' },
            'bias'        : {'min':-40, 'max':40, 'delta':5 },
            'model_model' : {'min':-10, 'max':10, 'delta':2 },
        },
        'tauu'  : {
            'default' : { 'color' : 'testcmap' , 'units':'N/m'},
            'fullfield'   : {'colors':'-0.2 -0.18 -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 0.18 0.2'},
            'bias'        : {'min':-0.1,'max':0.1,'delta':0.01},
            'model_model' : {'min':-0.1,'max':0.1,'delta':0.01},
        },
        'tauv'  : {
            'default' : { 'color' : 'testcmap' , 'units':'N/m'},
            'fullfield'   : {'colors':'-0.2 -0.18 -0.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 0.18 0.2'},
            'bias'        : {'min':-0.1,'max':0.1,'delta':0.01},
            'model_model' : {'min':-0.1,'max':0.1,'delta':0.01},
        },

        # -- Clouds
        'clt'  : {
            'default' : { 'color' : 'precip_11lev' , 'units':'Fract.'},
            'fullfield'   : {'colors' : '20 30 40 50 60 70 80 90 100 110'},
            'bias'        : {'min':-30, 'max':30, 'delta':5, 'color': 'precip_diff_12lev'},
            'model_model' : {'min':-50, 'max':50, 'delta':5, 'color': 'precip_diff_12lev'},
        },
        'cldl'  : {
            'default' : { 'color' : 'precip_11lev' , 'units':'Fract.'},
            'fullfield'   : {'colors' : '20 30 40 50 60 70 80 90 100 110'},
            'bias'        : {'min':-30, 'max':30, 'delta':5, 'color': 'precip_diff_12lev'},
            'model_model' : {'min':-50, 'max':50, 'delta':5, 'color': 'precip_diff_12lev'},
        },
        'cldm'  : {
            'default' : { 'color' : 'precip_11lev' , 'units':'Fract.'},
            'fullfield'   : {'colors' : '20 30 40 50 60 70 80 90 100 110'},
            'bias'        : {'min':-30, 'max':30, 'delta':5, 'color': 'precip_diff_12lev'},
            'model_model' : {'min':-50, 'max':50, 'delta':5, 'color': 'precip_diff_12lev'},
        },
        'cldh'  : {
            'default' : { 'color' : 'precip_11lev' , 'units':'Fract.'},
            'fullfield'   : {'colors' : '20 30 40 50 60 70 80 90 100 110'},
            'bias'        : {'min':-30, 'max':30, 'delta':5, 'color': 'precip_diff_12lev'},
            'model_model' : {'min':-50, 'max':50, 'delta':5, 'color': 'precip_diff_12lev'},
        },

        # -- TOA Radiative variables
        'rlut'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors':'110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300 310 320' },
            'bias'        : {'min':-40, 'max':40, 'delta':5, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-10, 'max':10, 'delta':1, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rlutcs'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors':'110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300 310 320' },
            'bias'        : {'min':-40, 'max':40, 'delta':5, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-10, 'max':10, 'delta':1, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rsut'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200' },
            'bias'        : {'min':-50, 'max':50, 'delta':5, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-10, 'max':10, 'delta':1, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rsutcs'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200' },
            'bias'        : {'min':-50, 'max':50, 'delta':5, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-10, 'max':10, 'delta':1, 'color': 'ViBlGrWhYeOrRe'},
        },
        # -- Surface Radiative variables
        'rlds'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '10 30 50 70 90 110 130 150 170 190 210 230 250 270 290 310 330 350 370 390 410' },
            'bias'        : {'min':-100, 'max':100, 'delta':10, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rsds'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '10 30 50 70 90 110 130 150 170 190 210 230 250 270 290 310 330 350 370 390 410' },
            'bias'        : {'min':-100, 'max':100, 'delta':10, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rldscs'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '40 60 80 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460' },
            'bias'        : {'min':-110, 'max':100, 'delta':10, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rsdscs'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '40 60 80 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460' },
            'bias'        : {'min':-100, 'max':100, 'delta':10, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rlus'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '40 60 80 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460' },
            'bias'        : {'min':-100, 'max':100, 'delta':10, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rsus'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '40 60 80 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460' },
            'bias'        : {'min':-100, 'max':100, 'delta':10, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        'rsuscs'  : {
            'default' : { 'color' : 'WhBlGrYeRe' , 'units':'W/m2'},
            'fullfield'   : {'colors' : '40 60 80 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460' },
            'bias'        : {'min':-100, 'max':100, 'delta':10, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        
        'alb'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%'},
            'fullfield'   : {'colors' : '0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100' },
            'bias'        : {'min':-50, 'max':50, 'delta':5, 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'min':-20, 'max':20, 'delta':2, 'color': 'ViBlGrWhYeOrRe'},
        },
        'alb_oce'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%'},
            'fullfield'   : {'colors':'2 3 4 4.5 5 5.5 6 6.5 7 8 9 10 15 20 50' },
            'bias'        : {'colors':'-10 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 10', 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'colors':'-10 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 10', 'color': 'ViBlGrWhYeOrRe'},
        },
         'alb_ter'  : {
            'default' : { 'color' : 'WhViBlGrYeOrRe' , 'units':'%'},
            'fullfield'   : {'colors':'10 15 20 25 30 35 40 45 50 55 60 70 100' },
            'bias'        : {'colors':'-10 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 10', 'color': 'ViBlGrWhYeOrRe'},
            'model_model' : {'colors':'-10 -1 -0.5 -0.25 -0.1 0.1 0.25 0.5 1 10', 'color': 'ViBlGrWhYeOrRe'},
        },

    }
    #
    rep=defaults.copy()
    if variable in per_variable : 
        var_entry=per_variable[variable]
        for cont in [ 'default', context ] :
            if cont in var_entry : rep.update(var_entry[cont])
    return rep
        
