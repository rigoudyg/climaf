def variable2reference(variable, project=None) :
    if not project:
        if variable in ['pr','prw','rlut', 'rsut' , 'rlutcs', 'rsutcs', 'rlus', 'rsus' , 'rluscs', 'rsuscs', 'rlds', 'rsds',
                        'rsdscs','rldscs','tas', 'ta', 'ua', 'va', 'psl', 'uas', 'vas', 'tos', 'sos', 'zos','hus','mlotst','alb',
                        'to','so','so200','so1000','so2000','to200','to1000','to2000','sic','wfo']:
            project='ref_climatos'
        else:
            project='ref_ts'
    
    refs = {
        'ref_climatos' : {
            'CERES'  : [ 'rlut', 'rsut' , 'rlutcs', 'rsutcs', 'rlus', 'rsus' , 'rluscs', 'rsuscs', 'rlds', 'rsds', 'rsdscs','rldscs' ] ,
            'ERAINT' : [ 'tas', 'ta', 'psl', 'uas', 'vas' ,'hus','huss', 'ua', 'va','wfo'],
            'RSS'    : [ 'prw' ],
            'GPCP'   : ['pr'],
            'NSIDC'  : ['sic'],
            #'UKMETOFFICE-HadISST-v1-1' : [ 'tos' ],
            'WOA13-v2': ['to','tos','to200','to1000','to2000'],
            'NODC-WOA09' : [ 'sos'],
            'NODC-Levitus': ['so','so200','so1000','so2000'],
            'CNES-AVISO-L4': [ 'zos' ],
            'DeBoyerM' : ['mlotst','omlmax'],
            'CLARA-A1-1deg': ['alb'],
        },
        'ref_ts' : {
            'ERAInterim' : [ 'tas', 'psl' , 'uas' , 'vas', 'cldl', 'cldm', 'cldh' ], 
            'GPCP'   : [ 'pr'], 
            'CERES'  : [ 'rlut'  ,  'rsut'  ,      'rlutcs',   'rsutcs' ],
            'NCEP'   : [ 'huss' ],
            'MODIS-L3-C5' : ['clt'],
            'CLARA-A1-1deg': ['alb'],
            'NSIDC' : ['sic'],
        }
    }
    if project in refs :
        for product in refs[project] :
            if variable in refs[project][product] :
                return {'project':project,'product':product,'variable':variable}
