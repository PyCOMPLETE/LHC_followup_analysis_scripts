
def emittance_dictionary(filln=None):

    e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{}, 
          'sigma_corr_h':{}, 'sigma_corr_v':{},
          'rescale_sigma_h':{}, 'rescale_sigma_v':{}, 'scale_h': {}, 'scale_v': {}}
          
    if filln is None:
        raise ValueError('A fill number must be provided to select calibration!')
    
    if filln<5256:

        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.1
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.3
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = 0.528
        e_dict['sigma_corr_h'][6500][1] = 0.303 
        e_dict['sigma_corr_v'][450][1] = 0.437
        e_dict['sigma_corr_v'][6500][1] = 0.294
        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.6
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.1
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = 0.518
        e_dict['sigma_corr_h'][6500][2] = 0.299
        e_dict['sigma_corr_v'][450][2] = 0.675
        e_dict['sigma_corr_v'][6500][2] = 0.299
        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma
        e_dict['gamma'][450] = 479.6 
        e_dict['gamma'][6500] = 6927.6
        
        print 'Using calibration A'


        
    elif filln>=5256 and filln<5405:

        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.1
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.3
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = .53
        e_dict['sigma_corr_h'][6500][1] = .31
        e_dict['sigma_corr_v'][450][1] = .59
        e_dict['sigma_corr_v'][6500][1] = .31
        e_dict['rescale_sigma_h'][450][1] = .977
        e_dict['rescale_sigma_h'][6500][1] = 1.0232
        e_dict['rescale_sigma_v'][450][1] = .94
        e_dict['rescale_sigma_v'][6500][1] = .9375

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.6
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.1
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = .48
        e_dict['sigma_corr_h'][6500][2] = .31
        e_dict['sigma_corr_v'][450][2] = .48
        e_dict['sigma_corr_v'][6500][2] = .26
        e_dict['rescale_sigma_h'][450][2] = 1.0192
        e_dict['rescale_sigma_h'][6500][2] = 1.0204
        e_dict['rescale_sigma_v'][450][2] = .9655
        e_dict['rescale_sigma_v'][6500][2] = .9821

        # gamma
        e_dict['gamma'][450] = 479.6 
        e_dict['gamma'][6500] = 6927.6
        print 'Using calibration B'
        
    elif filln>=5405 and filln<5600: 
        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.11
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.34
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = .53
        e_dict['sigma_corr_h'][6500][1] = .306
        e_dict['sigma_corr_v'][450][1] = .59
        e_dict['sigma_corr_v'][6500][1] = .307
        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.64
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.12
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = .48
        e_dict['sigma_corr_h'][6500][2] = .306
        e_dict['sigma_corr_v'][450][2] = .48
        e_dict['sigma_corr_v'][6500][2] = .261
        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma
        e_dict['gamma'][450] = 479.6 
        e_dict['gamma'][6500] = 6927.6 
        print 'Using calibration C'
        
    elif filln>=5601 and filln<=5690: 
        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 203.4
        e_dict['betaf_h'][6500][1] = 200.7
        e_dict['betaf_v'][450][1] = 317.54
        e_dict['betaf_v'][6500][1] = 329.9
        e_dict['sigma_corr_h'][450][1] = .74
        e_dict['sigma_corr_h'][6500][1] = .415
        e_dict['sigma_corr_v'][450][1] = .646
        e_dict['sigma_corr_v'][6500][1] = .346
        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.6
        e_dict['betaf_h'][6500][2] = 200.0
        e_dict['betaf_v'][450][2] = 328.1
        e_dict['betaf_v'][6500][2] = 328.2
        e_dict['sigma_corr_h'][450][2] = .709
        e_dict['sigma_corr_h'][6500][2] = .489
        e_dict['sigma_corr_v'][450][2] = .661
        e_dict['sigma_corr_v'][6500][2] = .305
        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma
        e_dict['gamma'][450] = 479.6 
        e_dict['gamma'][6500] = 6927.6 
        print 'Using 2017 preliminary calibration!'
     
    elif filln>5690 and filln<6055:        

        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1]           = 206.8 #-- updated 5839 203.4 #203.4
        e_dict['betaf_h'][6500][1]          = 188.2 #-- updated 5839 188.2 #200.7 #200.7
        e_dict['betaf_v'][450][1]           = 287.3 #-- updated 5839 317.54 #317.54
        e_dict['betaf_v'][6500][1]          = 301.  #-- updated 5839 301.0 #329.9 #329.9        
        e_dict['sigma_corr_h'][450][1]      = 0.4109 #-- updated 5839 0.74#0.7400
        e_dict['sigma_corr_h'][6500][1]     = 0.2252 #-- updated 5839 0.2252 #0.415#0.4150         
        e_dict['sigma_corr_v'][450][1]      = 0.6352#-- updated 5839 0.646#0.6460 
        e_dict['sigma_corr_v'][6500][1]     = 0.281 #-- updated 5839 0.281 #0.346#0.3460        
        #e_dict['scale_h'][450][1]           = 0.0247 #-- updated 5839 0.0274#0.0274
        #e_dict['scale_h'][6500][1]          = 0.02184 #-- updated 5839 0.02184#0.0283#0.0283       
        #e_dict['scale_v'][450][1]           = 0.0265 #-- updated 5839 0.0272#0.0272
        #e_dict['scale_v'][6500][1]          = 0.02284 #-- updated 5839 0.02284 #0.0246#0.0246      
        e_dict['rescale_sigma_h'][450][1]   = 1.
        e_dict['rescale_sigma_h'][6500][1]  = 1.      
        e_dict['rescale_sigma_v'][450][1]   = 1.
        e_dict['rescale_sigma_v'][6500][1]  = 1.

        # Beam 2:
        e_dict['betaf_h'][450][2]           = 193.1 #-- updated 5839 200.6 #200.6
        e_dict['betaf_h'][6500][2]          = 208.8 #-- updated 5839 208.8#200.0 #200. 
        e_dict['betaf_v'][450][2]           = 337.6#-- updated 5839 328.1 #328.1
        e_dict['betaf_v'][6500][2]          = 340.3#-- updated 5839 340.3#328.2 #328.2
        e_dict['sigma_corr_h'][450][2]      = 0.442#-- updated 5839 0.709#0.7090
        e_dict['sigma_corr_h'][6500][2]     = 0.3352#-- updated 5839 0.3352 #0.489 #0.4890
        e_dict['sigma_corr_v'][450][2]      = 0.6291 #-- updated 5839 0.661#0.6610
        e_dict['sigma_corr_v'][6500][2]     = 0.32374#-- updated 5839 0.32374#0.305#0.3050
        #e_dict['scale_h'][450][2]           = 0.0273 #-- updated 5839 0.0301#0.0301
        #e_dict['scale_h'][6500][2]          = 0.02948#-- updated 5839 0.02948#0.0403#0.0403
        #e_dict['scale_v'][450][2]           = 0.02888 #-- updated 5839 0.0285#0.0285
        #e_dict['scale_v'][6500][2]          = 0.03126 #-- updated 5839 0.03126 #0.0315#0.0315
        e_dict['rescale_sigma_h'][450][2]   = 1.
        e_dict['rescale_sigma_h'][6500][2]  = 1.
        e_dict['rescale_sigma_v'][450][2]   = 1.
        e_dict['rescale_sigma_v'][6500][2]  = 1.

        # gamma
        e_dict['gamma'][450]                = 479.6 
        e_dict['gamma'][6500]               = 6927.6
        
        print 'Using calibration A-2017'
        
    elif filln>=6055 and filln<6611:        

        # From Nikos 15-08-2017
        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        ###Beam 1:
        e_dict['betaf_h'][450][1]           = 206.8 #-- updated 5839 203.4 #203.4
        e_dict['betaf_h'][6500][1]          = 188.2 #-- updated 5839 188.2 #200.7 #200.7

        e_dict['betaf_v'][450][1]           = 287.3 #-- updated 5839 317.54 #317.54
        e_dict['betaf_v'][6500][1]          = 301.  #-- updated 5839 301.0 #329.9 #329.9
        
        e_dict['sigma_corr_h'][450][1]      = 0.44843 #updated 6055 #0.4109 #-- updated 5839 0.74#0.7400
        e_dict['sigma_corr_h'][6500][1]     = 0.2527 #updated 6055 #0.2252 #-- updated 5839 0.2252 #0.415#0.4150 
        
        e_dict['sigma_corr_v'][450][1]      = 0.494 #updated 6055 #0.6352#-- updated 5839 0.646#0.6460 
        e_dict['sigma_corr_v'][6500][1]     = 0.3218 #updated 6055 #0.281 #-- updated 5839 0.281 #0.346#0.3460
        
        e_dict['scale_h'][450][1]           = 0.02626 #updated 6055 #0.0247 #-- updated 5839 0.0274#0.0274
        e_dict['scale_h'][6500][1]          = 0.023 #updated 6055 #0.02184 #-- updated 5839 0.02184#0.0283#0.0283
        
        e_dict['scale_v'][450][1]           = 0.02648 #updated 6055 #0.0265 #-- updated 5839 0.0272#0.0272
        e_dict['scale_v'][6500][1]          = 0.0236 #updated 6055 #0.02284 #-- updated 5839 0.02284 #0.0246#0.0246
        
        e_dict['rescale_sigma_h'][450][1]   = 1.
        e_dict['rescale_sigma_h'][6500][1]  = 1.
        
        e_dict['rescale_sigma_v'][450][1]   = 1.
        e_dict['rescale_sigma_v'][6500][1]  = 1.

        #### Beam 2:
        e_dict['betaf_h'][450][2]           = 193.1 #-- updated 5839 200.6 #200.6
        e_dict['betaf_h'][6500][2]          = 208.8 #-- updated 5839 208.8#200.0 #200.
        
        e_dict['betaf_v'][450][2]           = 337.6#-- updated 5839 328.1 #328.1
        e_dict['betaf_v'][6500][2]          = 340.3#-- updated 5839 340.3#328.2 #328.2
        
        e_dict['sigma_corr_h'][450][2]      = 0.38769 #updated 6055 #0.442#-- updated 5839 0.709#0.7090
        e_dict['sigma_corr_h'][6500][2]     = 0.3323 #updated 6055 #0.3352#-- updated 5839 0.3352 #0.489 #0.4890
        
        e_dict['sigma_corr_v'][450][2]      = 0.48528 #updated 6055 #0.6291 #-- updated 5839 0.661#0.6610
        e_dict['sigma_corr_v'][6500][2]     = 0.29511 #updated 6055 #0.32374#-- updated 5839 0.32374#0.305#0.3050
        
        e_dict['scale_h'][450][2]           = 0.02814 #updated 6055 #0.0273 #-- updated 5839 0.0301#0.0301
        e_dict['scale_h'][6500][2]          = 0.03016 #updated 6055 #0.02948#-- updated 5839 0.02948#0.0403#0.0403
        
        e_dict['scale_v'][450][2]           = 0.02898 #updated 6055 #0.02888 #-- updated 5839 0.0285#0.0285
        e_dict['scale_v'][6500][2]          = 0.0319#updated 6055 #0.03126 #-- updated 5839 0.03126 #0.0315#0.0315

        e_dict['rescale_sigma_h'][450][2]   = 1.
        e_dict['rescale_sigma_h'][6500][2]  = 1.
        
        e_dict['rescale_sigma_v'][450][2]   = 1.
        e_dict['rescale_sigma_v'][6500][2]  = 1.

        # gamma
        e_dict['gamma'][450]                = 479.6 
        e_dict['gamma'][6500]               = 6927.6
        
        print 'Using calibration B-2017'
        
    elif filln>=6611:
        e_dict = {
        'betaf_h': {450: {1: 205.05000000000001, 2: 196.71000000000001},
          6500: {1: 200.0, 2: 195.90000000000001}},
         'betaf_v': {450: {1: 286.83999999999997, 2: 358.23000000000002},
          6500: {1: 300.0, 2: 359.89999999999998}},
         'gamma': {450: 479.6, 6500: 6927.6},
         'rescale_sigma_h': {450: {1: 1.0, 2: 1.0}, 6500: {1: 1.0, 2: 1.0}},
         'rescale_sigma_v': {450: {1: 1.0, 2: 1.0}, 6500: {1: 1.0, 2: 1.0}},
         'scale_h': {450: {}, 6500: {}},
         'scale_v': {450: {}, 6500: {}},
         'sigma_corr_h': {450: {1: 0.42520000000000002, 2: 0.50160000000000005},
          6500: {1: 0.1973, 2: 0.27410000000000001}},
         'sigma_corr_v': {450: {1: 0.40760000000000002, 2: 0.61850000000000005},
          6500: {1: 0.21280000000000002, 2: 0.24940000000000001}}}
        print 'Using calibration A-2018'
    else:         
        raise ValueError('What?!')     
    
         
    
    return(e_dict)
