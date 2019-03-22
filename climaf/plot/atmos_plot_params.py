#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created : S.Sénési - nov 2015
# Adapter : J.Servonnat - april 2016

dict_plot_params = {
    'pr': {
        'default': {'scale': 86400., 'color': 'precip_11lev', 'contours': 1},
        'full_field': {'colors': '0.5 1 2 3 4 6 8 10 12 14'},
        'bias': {'color': 'MPL_BrBG', 'colors': '-5 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 5'},
        'model_model': {'color': 'precip_diff_12lev', 'colors': '-5 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 5'},
    },
    'pme': {
        'default': {'scale': 86400., 'color': 'precip_diff_12lev', 'contours': 1},
        'full_field': {'colors': '-14 -12 -10 -8 -6 -4 -3 -2 -1 -0.5 0.5 1 2 3 4 6 8 10 12 14'},
        'bias': {'color': 'precip_diff_12lev', 'colors': '-5 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 5'},
        'model_model': {'color': 'precip_diff_12lev', 'colors': '-5 -2 -1 -0.5 -0.2 -0.1 0.1 0.2 0.5 1 2 5'},
    },
    'hurs': {
        'default': {'focus': 'ocean'},
        'full_field': {'colors': '72 74 76 78 80 82 84 86 88 90 92', 'color': 'precip_11lev'},
        'bias': {'colors': '-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10', 'color': 'precip_diff_12lev'},
        'model_model': {'colors': '-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10',
                        'color': 'precip_diff_12lev'},
    },
    'rstt': {
        'full_field': {'colors': '0 20 40 60 80 100 120 140 160 180 200 220 240 260 280 300 320',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rlut': {
        'full_field': {'colors': '150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300 310',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rlus': {
        'full_field': {'colors': '120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 440 480',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -1 1 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rsus': {
        'full_field': {'colors': '10 20 30 40 50 60 70 80 90 100 110 120 130 140 150',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -1 1 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rsuscs': {
        'full_field': {'colors': '20 30 40 50 60 70 80 90 100 110 120 130 140 150', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -1 1 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rsds': {
        'full_field': {'colors': '80 100 120 140 160 180 200 220 240 260 280 300 320',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rlds': {
        'full_field': {'colors': '100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rsdscs': {
        'full_field': {'colors': '80 100 120 140 160 180 200 220 240 260 280 300 320',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rldscs': {
        'full_field': {'colors': '100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },

    'rtt': {
        'full_field': {'colors': '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50 60 70 80 90 100',
                       'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crest': {
        'full_field': {'colors': '-120 -110 -100 -90 -80 -70 -60 -50 -40 -30 -20 -10'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crett': {
        'full_field': {'colors': '-60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'hfns': {
        'full_field': {'colors': '-200 -150 -100 -50 0 50 100 150 200 -75 -25 25 75'},
        'bias': {'colors': '-80 -60 -40 -20 -10 10 20 40 60 80', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-80 -60 -40 -20 -10 10 20 40 60 80'},
    },
    'hfss': {
        'default': {'focus': 'ocean'},
        'full_field': {'colors': '0 10 20 30 40 50 60 70 80 90 100 110 120', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 15 25 35 45 55', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 15 25 35 45 55'},
    },
    'hfls': {
        'default': {'focus': 'ocean'},
        'full_field': {'colors': '0 20 40 60 80 100 120 140 160 180 200', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 15 25 35 45 55', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 15 25 35 45 55'},
    },
    'tas': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed'},
        'full_field': {'colors': '-60 -50 -40 -35 -30 -25 -20 -15 -10 -6 0 6 10 14 18 22 26 24 27 28 30',
                       'offset': -273.15},
        'bias': {'colors': '-8 -4 -2 -1 -0.5 0.5 1 2 4 8', 'color': 'BlueWhiteOrangeRed', 'offset': 0},
        'model_model': {'colors': '-8 -4 -2 -1 -0.5 0.5 1 2 4 8', 'color': 'BlueWhiteOrangeRed', 'offset': 0},
    },
    'tauu': {
        'default': {'focus': 'ocean', 'mpCenterLonF': 200},
        'full_field': {
            'colors': '-.16 -0.14 -0.12 -0.1 -0.08 -0.06 -0.04 -0.02 0 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16',
            'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': '-0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-0.1 -0.08 -0.06 -0.04 -0.02 0.02 0.04 0.06 0.08 0.1'},
    },
    'tauv': {
        'default': {'focus': 'ocean', 'mpCenterLonF': 200},
        'full_field': {'colors': '-0.1 -0.08 -0.06 -0.04 -0.02 -0.01 0.01 0.02 0.04 0.06 0.08 0.1',
                       'color': 'BlueWhiteOrangeRed'},
        'bias': {'colors': '-0.05 -0.04 -0.03 -0.02 -0.01 0.01 0.02 0.03 0.04 0.05', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-0.05 -0.04 -0.03 -0.02 -0.01 0.01 0.02 0.03 0.04 0.05',
                        'color': 'BlueWhiteOrangeRed'},
    },
    'psl': {
        'default': {'scale': 0.01, 'units': 'hPa', 'color': 'cmp_b2r', 'mpCenterLonF': 200},
        'full_field': {'colors': '990 995 1000 1002 1004 1006 1008 1010 1012 1014 1016 1020 1025 1030 1040'},
        'bias': {'colors': '-100 -50 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 7 8 9 10 25 50 100',
                 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-100 -50 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 7 8 9 10 25 50 100',
                        'color': 'BlueWhiteOrangeRed'},
    },
    'zg500': {
        'full_field': {
            'colors': '4900 4950 5000 5050 5100 5150 5200 5250 5300 5350 5400 5450 5500 5550 5600 5650 5700 5750 5800'},
        'bias': {
            'colors': '-260 -230 -200 -180 -160 -140 -120 -100 -80 -60 -40 -20 -10 10 20 40 60 80 '
                      '100 120 140 160 180 200 230 260',
            'color': 'BlueWhiteOrangeRed'},
        'model_model': {
            'colors': '-260 -230 -200 -180 -160 -140 -120 -100 -80 -60 -40 -20 -10 10 20 40 60 80 '
                      '100 120 140 160 180 200 230 260',
            'color': 'BlueWhiteOrangeRed'},
    },
    'rsah': {
        'full_field': {'colors': '10 20 30 40 50 60 70 80 90 100 110 120 130', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rsahcs': {
        'full_field': {'colors': '10 20 30 40 50 60 70 80 90 100 110 120 130', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rsahcre': {
        'full_field': {'colors': '-20 -16 -12 -10 -8 -6 -4 -2 2 4 6 8 10 12 16 20'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rlah': {
        'full_field': {'colors': '160 180 200 220 240 260 280 300 320 340 360 380 400 420 460',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rlahcs': {
        'full_field': {
            'colors': '-260 -250 -240 -230 -220 -210 -200 -190 -180 -170 -160 -150 '
                      '-140 -130 -120 -110 -100 -90 -80 -70'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -1 1 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -1 1 5 10 20 30 40 50'},
    },
    'rlahcre': {
        'full_field': {'colors': '220 240 260 280 300 320 340 360 380 400 420 460 480 500 540 580',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rah': {
        'full_field': {'colors': '160 180 200 220 240 260 280 300 320 340 360 380 400 420 460',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rahcs': {
        'full_field': {'colors': '-160 -150 -140 -130 -120 -110 -100 -90 -80 -70 -60 -50 -40 -30 -20'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rahcre': {
        'full_field': {'colors': '240 260 280 300 320 340 360 380 400 420 460 480 500 540 580',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 0 5 10 20 30 40 50'},
    },
    'rsts': {
        'full_field': {
            'colors': '0 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 '
                      '190 200 210 220 230 240 250 260 270 280 290 300 310 320 330',
            'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'rsut': {
        'full_field': {'colors': '50 60 70 80 90 100 110 120 130 140 150 160 180', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'rsutcs': {
        'full_field': {'colors': '10 30 50 60 70 80 90 100 110 120 130 140 150 160 180',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'rlutcs': {
        'full_field': {'colors': '150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300 310 ',
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'albs': {
        'full_field': {'colors': '5 10 15 20 25 30 35 40 45 50 55 60 65 70 80 90 100', 'scale': 100,
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed', 'scale': 100},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'scale': 100,
                        'color': 'BlueWhiteOrangeRed'},
    },
    'albt': {
        'full_field': {'colors': '5 10 15 20 25 30 35 40 45 50 55 60 65 70 80 90 100', 'scale': 100,
                       'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed', 'scale': 100},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'scale': 100,
                        'color': 'BlueWhiteOrangeRed'},
    },
    # -- CRE
    'cress': {
        'full_field': {'colors': '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60 70 80 90 100'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crels': {
        'full_field': {'colors': '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60 70 80 90 100'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crets': {
        'full_field': {'colors': '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60 70 80 90 100'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crest': {
        'full_field': {'colors': '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60 70 80 90 100'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crelt': {
        'full_field': {'colors': '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60 70 80 90 100'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crett': {
        'full_field': {'colors': '-100 -90 -80 -70 -60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60 70 80 90 100'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'rts': {
        'full_field': {'colors': '-20 0 20 40 60 80 100 120 140 160 180 200', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'crelt': {
        'full_field': {'colors': '0 5 10 15 20 25 30 35 40 45 50 55 60 65 70', 'color': 'WhiteBlueGreenYellowRed'},
        'bias': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50', 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'colors': '-50 -40 -30 -20 -10 -5 -2 2 5 10 20 30 40 50'},
    },
    'cltcalipso': {
        'full_field': {'colors': '20 25 30 35 40 45 50 55 60 70 80 90 100', 'color': 'precip_11lev'},
        'bias': {'colors': '-70 -40 -30 -20 -10 -5 5 10 20 30 40 70', 'color': 'precip_diff_12lev'},
        'model_model': {'colors': '-70 -40 -35 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 35 40 70',
                        'color': 'precip_diff_12lev'},
    },
    'clhcalipso': {
        'full_field': {'colors': '0 2 4 6 8 10 20 30 40 50 60 70 80 90 100', 'color': 'precip_11lev'},
        'bias': {'colors': '-70 -40 -35 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 35 40 70',
                 'color': 'precip_diff_12lev'},
        'model_model': {'colors': '-70 -40 -35 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 35 40 70',
                        'color': 'precip_diff_12lev'},
    },
    'clmcalipso': {
        'full_field': {'colors': '2 4 6 8 10 20 30 40 50 60', 'color': 'precip_11lev'},
        'bias': {'colors': '-70 -40 -35 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 35 40 70',
                 'color': 'precip_diff_12lev'},
        'model_model': {'colors': '-70 -40 -35 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 35 40 70',
                        'color': 'precip_diff_12lev'},
    },
    'cllcalipso': {
        'full_field': {'colors': '5 10 20 30 40 50 60 70 80 90 100', 'color': 'precip_11lev'},
        'bias': {'colors': '-70 -40 -35 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 35 40 70',
                 'color': 'precip_diff_12lev'},
        'model_model': {'colors': '-70 -40 -35 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 35 40 70',
                        'color': 'precip_diff_12lev'},
    },
    'ua': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-40 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 40'},
        # 'bias'        : {'min':-14,'max':14,'delta':2},
        'bias': {'colors': '-6 -5.5 -5 -4.5 -4 -3.5 -3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1},
    },
    'va': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {
            'colors': '-2 -1.8 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 -0.1 -0.05 0.05 '
                      '0.1 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8 2'},
        'bias': {'min': -1, 'max': 1, 'delta': 0.05},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05},
    },
    'ta': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': '-70 -50 -40 -30 -20 -10 0 5 10 15 20 25 30 25'},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'vitu': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-40 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 40'},
        # 'bias'        : {'min':-14,'max':14,'delta':2},
        'bias': {'colors': '-6 -5.5 -5 -4.5 -4 -3.5 -3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1},
    },
    'vitv': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {
            'colors': '-2 -1.8 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 -0.1 -0.05 0.05 0.1 '
                      '0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8 2'},
        'bias': {'min': -1, 'max': 1, 'delta': 0.05},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05},
    },
    'vitw': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'min': -0.05, 'max': 0.05, 'delta': 0.005},
        # 'colors':'-2 -1.8 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 -0.1 -0.05 0.05 0.1
        #           0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8 2'},
        'bias': {'min': -1, 'max': 1, 'delta': 0.05},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05},
    },

    'temp': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': '-70 -50 -40 -30 -20 -10 0 5 10 15 20 25 30 25'},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },

    'hur': {
        'default': {'color': 'precip_11lev', 'units': 'g/g'},
        'full_field': {'colors': '0.1 1 5 10 20 30 40 60 80 100'},
        'bias': {'min': -25, 'max': 25, 'delta': 5, 'color': 'MPL_BrBG'},
        'model_model': {'min': -0.001, 'max': 0.001, 'delta': 0.0001, 'color': 'MPL_BrBG'},
    },
    'hus': {
        'default': {'color': 'precip_11lev', 'units': 'g/g'},
        'full_field': {
            'colors': '0.00001 0.0001 0.0005 0.001 0.002 0.003 0.004 0.006 0.008 0.01 0.012 0.014 0.016 0.02'},
        'bias': {'min': -0.002, 'max': 0.002, 'delta': 0.0002, 'color': 'MPL_BrBG'},
        'model_model': {'min': -0.001, 'max': 0.001, 'delta': 0.0001, 'color': 'MPL_BrBG'},
    },
    'uas': {
        'default': {'color': 'BlueYellowRed', 'units': 'm/s', 'mpCenterLonF': 200, 'contours': 1},
        'full_field': {'colors': '-10 -8 -6 -4 -2 -1 0 1 2 4 6 8 10'},
        # 'bias'        : {'min':-3.5, 'max':3.5, 'delta':0.5},
        # 'model_model' : {'colors':'-3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3'},
        # 'default' : { 'color' : 'BlueWhiteOrangeRed' , 'units':'m/s'},
        # 'full_field'   : {'colors':'-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 7 8 9 10'},
        'bias': {'colors': '-3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3', 'color': 'BlueWhiteOrangeRed'},
        # 'model_model' : {'colors':'-3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3'},
    },
    'vas': {
        'default': {'color': 'BlueYellowRed', 'units': 'm/s', 'mpCenterLonF': 200, 'contours': 1},
        'full_field': {'colors': '-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10'},
        'bias': {'colors': '-3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3', 'color': 'BlueWhiteOrangeRed'},
        # 'bias'        : {'min':-3,'max':3,'delta':0.5},
        'model_model': {'min': -5, 'max': 5, 'delta': 0.5},
    },
    'ua_Atl_sect': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-40 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 40'},
        'bias': {'min': -20, 'max': 20, 'delta': 2},
        'model_model': {'min': -10, 'max': 10, 'delta': 1},
    },
    'ua850': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-20 -15 -10 -5 -2 2 5 10 15 20'},
        'bias': {'min': -6, 'max': 6, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'ua700': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-20 -15 -10 -5 -2 2 5 10 15 20'},
        'bias': {'min': -8, 'max': 8, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'ua500': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-25 -20 -15 -10 -5 -2 2 5 10 15 20 25'},
        'bias': {'min': -8, 'max': 8, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'ua200': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-40 -30 -25 -20 -15 -10 -5 -2 2 5 10 15 20 25 30 40'},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'color': 'BlueWhiteOrangeRed'},
    },
    'va850': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-10 -8 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 8 10'},
        'bias': {'min': 5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'va700': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-10 -8 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 8 10'},
        'bias': {'min': 5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'va500': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-10 -8 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 8 10'},
        'bias': {'min': 5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'va200': {
        'default': {'color': 'BlueWhiteOrangeRed', 'units': 'm/s'},
        'full_field': {'colors': '-10 -8 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 8 10'},
        'bias': {'min': 5, 'max': 5, 'delta': 0.5, 'color': 'BlueWhiteOrangeRed'},
        'model_model': {'min': -1, 'max': 1, 'delta': 0.05, 'color': 'BlueWhiteOrangeRed'},
    },
    'ta850': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': '-40 -30 -20 -10 0 5 10 15 20 25'},
        'bias': {'min': -5, 'max': 5, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'ta700': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': '-40 -30 -20 -10 0 5 10 15 20 25'},
        'bias': {'min': -5, 'max': 5, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'ta500': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': '-40 -30 -20 -10 0 5 10 15 20 25'},
        'bias': {'min': -5, 'max': 5, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'ta200': {
        'default': {'units': 'degC', 'color': 'BlueWhiteOrangeRed', 'offset': -273.15},
        'full_field': {'colors': '-70 -65 -60 -58 -56 -54 -52 -50 -45 -40'},
        'bias': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
        'model_model': {'min': -10, 'max': 10, 'delta': 1, 'offset': 0},
    },
    'curltau': {'default': {},
                'full_field': dict(min=-1e-6, max=1e-6, delta=1e-7, focus='ocean', contours=1),
                }

}
