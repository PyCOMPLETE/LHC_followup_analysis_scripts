def emittance_dictionary(filln=None, rescale=False, period = None):

    e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{}, 
          'sigma_corr_h':{}, 'sigma_corr_v':{},
          'rescale_sigma_h':{}, 'rescale_sigma_v':{}, 'scale_h': {}, 'scale_v': {}}
          
    if filln is None:
        raise ValueError('A fill number must be provided to select calibration!')
    
    print(('rescale = %s'%rescale ))
    print(('period = %s'%period ))

    #The "rescaling" is applied for the period between the BSRT calibration fill and the fill where the calibration factors change in timber. 
    #if rescale: #sigma_new=(scale_new/scale_old)*sigma_old
    #When applying the "rescaling" for a specific period of fills, take the LSF (e_dict['sigma_corr_']) and scale_new (e_dict['rescale_sigma_']) values after the fill for which the new calibration factors are applied in timber  

    if filln<5256:        

        for kk in list(e_dict.keys()):
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.1
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.3
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = 0.5277
        e_dict['sigma_corr_h'][6500][1] = 0.3025 
        e_dict['sigma_corr_v'][450][1] = 0.4369 
        e_dict['sigma_corr_v'][6500][1] = 0.2942
        e_dict['scale_h'][450][1] = .0431
        e_dict['scale_h'][6500][1] = .04457
        e_dict['scale_v'][450][1] = .0456
        e_dict['scale_v'][6500][1] = .04723
        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.6
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.1
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = 0.5178
        e_dict['sigma_corr_h'][6500][2] = 0.2986
        e_dict['sigma_corr_v'][450][2] = 0.6746
        e_dict['sigma_corr_v'][6500][2] = 0.2986
        e_dict['scale_h'][450][2] = .0545
        e_dict['scale_h'][6500][2] = .05128
        e_dict['scale_v'][450][2] = .0603
        e_dict['scale_v'][6500][2] = .05808

        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma
        e_dict['gamma'][450] = 479.6 
        e_dict['gamma'][6500] = 6927.6
        
        print('Using calibration 2016 A')


        
    elif filln>=5256 and filln<5405:

        for kk in list(e_dict.keys()):
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.1
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.3
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = .524
        e_dict['sigma_corr_h'][6500][1] = .318
        e_dict['sigma_corr_v'][450][1] = .680 # .59 #
        e_dict['sigma_corr_v'][6500][1] = .342 #.31 #
        e_dict['scale_h'][450][1] = 0.0427
        e_dict['scale_h'][6500][1] = 0.0432
        e_dict['scale_v'][450][1] = .05
        e_dict['scale_v'][6500][1] = .0478

        #e_dict['rescale_sigma_h'][450][1] = .977
        #e_dict['rescale_sigma_h'][6500][1] = 1.0232
        #e_dict['rescale_sigma_v'][450][1] = .94
        #e_dict['rescale_sigma_v'][6500][1] = .9375

        if rescale and period is '2016A':
            print('Rescale based on calibration 2016 A')
            e_dict['rescale_sigma_h'][450][1] = 0.0431/e_dict['scale_h'][450][1]
            e_dict['rescale_sigma_h'][6500][1] = 0.04457/e_dict['scale_h'][6500][1]
            e_dict['rescale_sigma_v'][450][1] = 0.0456/e_dict['scale_v'][450][1]
            e_dict['rescale_sigma_v'][6500][1] = 0.04723/e_dict['scale_v'][6500][1]
            e_dict['sigma_corr_h'][450][1] = 0.5277
            e_dict['sigma_corr_h'][6500][1] = 0.3025 
            e_dict['sigma_corr_v'][450][1] = 0.4369
            e_dict['sigma_corr_v'][6500][1] = 0.2942
        elif rescale and period is '2016C':
            print('Rescale based on calibration 2016 C')
            e_dict['rescale_sigma_h'][450][1] = 0.042/e_dict['scale_h'][450][1]
            e_dict['rescale_sigma_h'][6500][1] = 0.044/e_dict['scale_h'][6500][1]
            e_dict['rescale_sigma_v'][450][1] = 0.047/e_dict['scale_v'][450][1]
            e_dict['rescale_sigma_v'][6500][1] = 0.045/e_dict['scale_v'][6500][1]
            e_dict['sigma_corr_h'][450][1] = 0.5329
            e_dict['sigma_corr_h'][6500][1] = 0.3056
            e_dict['sigma_corr_v'][450][1] = 0.5887
            e_dict['sigma_corr_v'][6500][1] = 0.3069
        else:
            e_dict['rescale_sigma_h'][450][1] = 1.
            e_dict['rescale_sigma_h'][6500][1] = 1.
            e_dict['rescale_sigma_v'][450][1] = 1.
            e_dict['rescale_sigma_v'][6500][1] = 1.
            
        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.6
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.12
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = .472
        e_dict['sigma_corr_h'][6500][2] = .3194
        e_dict['sigma_corr_v'][450][2] = .48 #.640
        e_dict['sigma_corr_v'][6500][2] = .26 #.297
        e_dict['scale_h'][450][2] = .0521
        e_dict['scale_h'][6500][2] = .0488
        e_dict['scale_v'][450][2] = .058
        e_dict['scale_v'][6500][2] = .0561

  
        if rescale and period=='2016A':

            print ('Rescale based on calibration 2016 A')
            e_dict['rescale_sigma_h'][450][2] = 0.0545/e_dict['scale_h'][450][2]
            e_dict['rescale_sigma_h'][6500][2] = 0.05128/e_dict['scale_h'][6500][2]
            e_dict['rescale_sigma_v'][450][2] = 0.0603/e_dict['scale_v'][450][2]
            e_dict['rescale_sigma_v'][6500][2] = 0.05808/e_dict['scale_v'][6500][2]
            e_dict['sigma_corr_h'][450][2] = 0.5178
            e_dict['sigma_corr_h'][6500][2] = 0.2986
            e_dict['sigma_corr_v'][450][2] = 0.6746
            e_dict['sigma_corr_v'][6500][2] = 0.2986

        elif rescale and period=='2016C':
            print('Rescale based on calibration 2016 C')
            e_dict['rescale_sigma_h'][450][2] = 0.05267/e_dict['scale_h'][450][2]
            e_dict['rescale_sigma_h'][6500][2] = 0.05015/e_dict['scale_h'][6500][2]
            e_dict['rescale_sigma_v'][450][2] = 0.05567/e_dict['scale_v'][450][2]
            e_dict['rescale_sigma_v'][6500][2] = 0.05464/e_dict['scale_v'][6500][2]
            e_dict['sigma_corr_h'][450][2] = 0.4796
            e_dict['sigma_corr_h'][6500][2] = 0.3059
            e_dict['sigma_corr_v'][450][2] = 0.4803
            e_dict['sigma_corr_v'][6500][2] = 0.2614

        else:
            e_dict['rescale_sigma_h'][450][2] = 1.
            e_dict['rescale_sigma_h'][6500][2] = 1.
            e_dict['rescale_sigma_v'][450][2] = 1.
            e_dict['rescale_sigma_v'][6500][2] = 1.
            print('Using calibration 2016 B')

        e_dict['gamma'][450] = 479.6 
        e_dict['gamma'][6500] = 6927.6

        
    elif filln>=5405 and filln < 5690: 
        for kk in list(e_dict.keys()):
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.1
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.34
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = .5329
        e_dict['sigma_corr_h'][6500][1] = .3056
        e_dict['sigma_corr_v'][450][1] = .5887
        e_dict['sigma_corr_v'][6500][1] = .3069
        e_dict['scale_h'][450][1] = .04234
        e_dict['scale_h'][6500][1] = .04367
        e_dict['scale_v'][450][1] = .04746
        e_dict['scale_v'][6500][1] = .04469

        if rescale:
            e_dict['rescale_sigma_h'][450][1] = 0.0431/e_dict['scale_h'][450][1]
            e_dict['rescale_sigma_h'][6500][1] = 0.04457/e_dict['scale_h'][6500][1]
            e_dict['rescale_sigma_v'][450][1] = 0.0456/e_dict['scale_v'][450][1]
            e_dict['rescale_sigma_v'][6500][1] = 0.04723/e_dict['scale_v'][6500][1]
            e_dict['sigma_corr_h'][450][1] = 0.5277
            e_dict['sigma_corr_h'][6500][1] = 0.3025 
            e_dict['sigma_corr_v'][450][1] = 0.4369
            e_dict['sigma_corr_v'][6500][1] = 0.2942

        else:
            e_dict['rescale_sigma_h'][450][1] = 1.
            e_dict['rescale_sigma_h'][6500][1] = 1.
            e_dict['rescale_sigma_v'][450][1] = 1.
            e_dict['rescale_sigma_v'][6500][1] = 1. 

    # To rescale with the first period scale
        

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.64
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.12
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = .4796
        e_dict['sigma_corr_h'][6500][2] = .3059
        e_dict['sigma_corr_v'][450][2] = .4803
        e_dict['sigma_corr_v'][6500][2] = .2614
        e_dict['scale_h'][450][2] = .05267
        e_dict['scale_h'][6500][2] = .05015
        e_dict['scale_v'][450][2] = .05567
        e_dict['scale_v'][6500][2] = .05464

        if rescale:
            print('Rescale based on calibration 2016 A')
            e_dict['rescale_sigma_h'][450][2] = 0.0545/e_dict['scale_h'][450][2]
            e_dict['rescale_sigma_h'][6500][2] = 0.05128/e_dict['scale_h'][6500][2]
            e_dict['rescale_sigma_v'][450][2] = 0.0603/e_dict['scale_v'][450][2]
            e_dict['rescale_sigma_v'][6500][2] = 0.05808/e_dict['scale_v'][6500][2]
            e_dict['sigma_corr_h'][450][2] = 0.5178
            e_dict['sigma_corr_h'][6500][2] = 0.2986
            e_dict['sigma_corr_v'][450][2] = 0.6746
            e_dict['sigma_corr_v'][6500][2] = 0.2986


        else:
            e_dict['rescale_sigma_h'][450][2] = 1.
            e_dict['rescale_sigma_h'][6500][2] = 1.
            e_dict['rescale_sigma_v'][450][2] = 1.
            e_dict['rescale_sigma_v'][6500][2] = 1.
        print('Using calibration 2016 - C')


    # To rescale with the first period scale

        # gamma
        e_dict['gamma'][450] = 479.6 
        e_dict['gamma'][6500] = 6927.6 


    elif (filln>5690 and filln < 6053): # or filln>6400:        

        for kk in list(e_dict.keys()):
            e_dict[kk] = {450:{}, 6500:{}}

        ###Beam 1:
        e_dict['betaf_h'][450][1]           = 206.8 
        e_dict['betaf_h'][6500][1]          = 188.2 

        e_dict['betaf_v'][450][1]           = 287.3 
        e_dict['betaf_v'][6500][1]          = 301.  
        
        e_dict['sigma_corr_h'][450][1]      = 0.4109
        e_dict['sigma_corr_h'][6500][1]     = 0.2252
        
        e_dict['sigma_corr_v'][450][1]      = 0.6352
        e_dict['sigma_corr_v'][6500][1]     = 0.281 
        
        e_dict['scale_h'][450][1]           = 0.0247
        e_dict['scale_h'][6500][1]          = 0.02184
        
        e_dict['scale_v'][450][1]           = 0.0265
        e_dict['scale_v'][6500][1]          = 0.02284
        
        e_dict['rescale_sigma_h'][450][1]   = 1.
        e_dict['rescale_sigma_h'][6500][1]  = 1.
        
        e_dict['rescale_sigma_v'][450][1]   = 1.
        e_dict['rescale_sigma_v'][6500][1]  = 1.

        #### Beam 2:
        e_dict['betaf_h'][450][2]           = 193.1
        e_dict['betaf_h'][6500][2]          = 208.8
        
        e_dict['betaf_v'][450][2]           = 337.6
        e_dict['betaf_v'][6500][2]          = 340.3
        
        e_dict['sigma_corr_h'][450][2]      = 0.442
        e_dict['sigma_corr_h'][6500][2]     = 0.3352
        
        e_dict['sigma_corr_v'][450][2]      = 0.6291
        e_dict['sigma_corr_v'][6500][2]     = 0.32374
        
        e_dict['scale_h'][450][2]           = 0.0273
        e_dict['scale_h'][6500][2]          = 0.02948
        
        e_dict['scale_v'][450][2]           = 0.02888
        e_dict['scale_v'][6500][2]          = 0.03126

        e_dict['rescale_sigma_h'][450][2]   = 1.
        e_dict['rescale_sigma_h'][6500][2]  = 1.
        
        e_dict['rescale_sigma_v'][450][2]   = 1.
        e_dict['rescale_sigma_v'][6500][2]  = 1.

        # gamma
        e_dict['gamma'][450]                = 479.6 
        e_dict['gamma'][6500]               = 6927.6
        
        print('Using calibration A-2017')

    elif filln>=6054 and filln < 6309:
        for kk in list(e_dict.keys()):
            e_dict[kk] = {450:{}, 6500:{}}

        ###Beam 1:
        e_dict['betaf_h'][450][1]           = 206.8
        e_dict['betaf_h'][6500][1]          = 188.2

        e_dict['betaf_v'][450][1]           = 287.3
        e_dict['betaf_v'][6500][1]          = 301.
        
        e_dict['sigma_corr_h'][450][1]      = 0.44843
        e_dict['sigma_corr_h'][6500][1]     = 0.2527
        
        e_dict['sigma_corr_v'][450][1]      = 0.494
        e_dict['sigma_corr_v'][6500][1]     = 0.3218
        
        e_dict['scale_h'][450][1]           = 0.02626
        e_dict['scale_h'][6500][1]          = 0.023
        
        e_dict['scale_v'][450][1]           = 0.02648
        e_dict['scale_v'][6500][1]          = 0.0236
        
        e_dict['rescale_sigma_h'][450][1]   = 1.
        e_dict['rescale_sigma_h'][6500][1]  = 1.
        
        e_dict['rescale_sigma_v'][450][1]   = 1.
        e_dict['rescale_sigma_v'][6500][1]  = 1.

        #### Beam 2:
        e_dict['betaf_h'][450][2]           = 193.1
        e_dict['betaf_h'][6500][2]          = 208.8
        
        e_dict['betaf_v'][450][2]           = 337.6
        e_dict['betaf_v'][6500][2]          = 340.3
        
        e_dict['sigma_corr_h'][450][2]      = 0.38769
        e_dict['sigma_corr_h'][6500][2]     = 0.3323
        
        e_dict['sigma_corr_v'][450][2]      = 0.48528
        e_dict['sigma_corr_v'][6500][2]     = 0.29511
        
        e_dict['scale_h'][450][2]           = 0.02814
        e_dict['scale_h'][6500][2]          = 0.03016
        
        e_dict['scale_v'][450][2]           = 0.02898
        e_dict['scale_v'][6500][2]          = 0.0319

        e_dict['rescale_sigma_h'][450][2]   = 1.
        e_dict['rescale_sigma_h'][6500][2]  = 1.
        
        e_dict['rescale_sigma_v'][450][2]   = 1.
        e_dict['rescale_sigma_v'][6500][2]  = 1.

        # gamma
        e_dict['gamma'][450]                = 479.6 
        e_dict['gamma'][6500]               = 6927.6
        
        print('Using calibration B-2017')

	
    elif filln>=6309 and filln < 6420:
        for kk in list(e_dict.keys()):
            e_dict[kk] = {450:{}, 6500:{}}

        ###Beam 1:
        e_dict['betaf_h'][450][1]           = 206.8
        e_dict['betaf_h'][6500][1]          = 188.2

        e_dict['betaf_v'][450][1]           = 287.3
        e_dict['betaf_v'][6500][1]          = 301.
        
        e_dict['sigma_corr_h'][450][1]      = 0.45036
        e_dict['sigma_corr_h'][6500][1]     = 0.26283
        
        e_dict['sigma_corr_v'][450][1]      = 0.57683
        e_dict['sigma_corr_v'][6500][1]     = 0.40762
        
        e_dict['scale_h'][450][1]           = 0.02574
        e_dict['scale_h'][6500][1]          = 0.02379
        
        e_dict['scale_v'][450][1]           = 0.02684
        e_dict['scale_v'][6500][1]          = 0.02312
        
        e_dict['rescale_sigma_h'][450][1]   = 1.
        e_dict['rescale_sigma_h'][6500][1]  = 1.
        
        e_dict['rescale_sigma_v'][450][1]   = 1.
        e_dict['rescale_sigma_v'][6500][1]  = 1.

        #### Beam 2:
        e_dict['betaf_h'][450][2]           = 193.1
        e_dict['betaf_h'][6500][2]          = 208.8
        
        e_dict['betaf_v'][450][2]           = 337.6
        e_dict['betaf_v'][6500][2]          = 340.3
        
        e_dict['sigma_corr_h'][450][2]      = 0.3367
        e_dict['sigma_corr_h'][6500][2]     = 0.3158
        
        e_dict['sigma_corr_v'][450][2]      = 0.391 
        e_dict['sigma_corr_v'][6500][2]     = 0.2911
        
        e_dict['scale_h'][450][2]           = 0.02691
        e_dict['scale_h'][6500][2]          = 0.0289 
        
        e_dict['scale_v'][450][2]           = 0.02708
        e_dict['scale_v'][6500][2]          = 0.03001

        e_dict['rescale_sigma_h'][450][2]   = 1.
        e_dict['rescale_sigma_h'][6500][2]  = 1.
        
        e_dict['rescale_sigma_v'][450][2]   = 1.
        e_dict['rescale_sigma_v'][6500][2]  = 1.

        # gamma
        e_dict['gamma'][450]                = 479.6 
        e_dict['gamma'][6500]               = 6927.6
        
        print('Using calibration C-2017')

    # elif filln>=6372 and filln < 6420:  # ????  Stefania says its not there

    #     for kk in e_dict.keys():
    #         e_dict[kk] = {450:{}, 6500:{}}

    #     ###Beam 1:
    #     e_dict['betaf_h'][450][1]           = 206.8 
    #     e_dict['betaf_h'][6500][1]          = 200.76

    #     e_dict['betaf_v'][450][1]           = 287.3 
    #     e_dict['betaf_v'][6500][1]          = 329.87
        
    #     e_dict['sigma_corr_h'][450][1]      = 0.45036
    #     e_dict['sigma_corr_h'][6500][1]     = 0.3226 
        
    #     e_dict['sigma_corr_v'][450][1]      = 0.57683
    #     e_dict['sigma_corr_v'][6500][1]     = 0.56 # 
        
    #     e_dict['scale_h'][450][1]           = 0.02574
    #     e_dict['scale_h'][6500][1]          = 0.0232 
        
    #     e_dict['scale_v'][450][1]           = 0.02684
    #     e_dict['scale_v'][6500][1]          = 0.0253 
        
    #     e_dict['rescale_sigma_h'][450][1]   = 1.
    #     e_dict['rescale_sigma_h'][6500][1]  = 1.
        
    #     e_dict['rescale_sigma_v'][450][1]   = 1.
    #     e_dict['rescale_sigma_v'][6500][1]  = 1.

    #     #### Beam 2:
    #     e_dict['betaf_h'][450][2]           = 193.1
    #     e_dict['betaf_h'][6500][2]          = 200. 
        
    #     e_dict['betaf_v'][450][2]           = 337.6
    #     e_dict['betaf_v'][6500][2]          = 328.25
        
    #     e_dict['sigma_corr_h'][450][2]      = 0.3367
    #     e_dict['sigma_corr_h'][6500][2]     = 0.3227
        
    #     e_dict['sigma_corr_v'][450][2]      = 0.391 
    #     e_dict['sigma_corr_v'][6500][2]     = 0.402 
        
    #     e_dict['scale_h'][450][2]           = 0.02691
    #     e_dict['scale_h'][6500][2]          = 0.0285 
        
    #     e_dict['scale_v'][450][2]           = 0.02708 
    #     e_dict['scale_v'][6500][2]          = 0.0296 

    #     e_dict['rescale_sigma_h'][450][2]   = 1.
    #     e_dict['rescale_sigma_h'][6500][2]  = 1.
        
    #     e_dict['rescale_sigma_v'][450][2]   = 1.
    #     e_dict['rescale_sigma_v'][6500][2]  = 1.

    #     # gamma
    #     e_dict['gamma'][450]                = 479.6 
    #     e_dict['gamma'][6500]               = 2664.47
        
    #     print('Using calibration D-2017: 2.5TeV Runs!!!')
    elif filln>=6420  and filln <6500:
        for kk in list(e_dict.keys()):
            e_dict[kk] = {450:{}, 6500:{}}

        ###Beam 1:
        e_dict['betaf_h'][450][1]           = 206.8 
        e_dict['betaf_h'][6500][1]          = 188.2 

        e_dict['betaf_v'][450][1]           = 287.3 
        e_dict['betaf_v'][6500][1]          = 301.  
        
        e_dict['sigma_corr_h'][450][1]      = 0.45036 
        e_dict['sigma_corr_h'][6500][1]     = 0.26283 
        
        e_dict['sigma_corr_v'][450][1]      = 0.57683 
        e_dict['sigma_corr_v'][6500][1]     = 0.40762 
        
        e_dict['scale_h'][450][1]           = 0.02574 
        e_dict['scale_h'][6500][1]          = 0.02379 
        
        e_dict['scale_v'][450][1]           = 0.02684 
        e_dict['scale_v'][6500][1]          = 0.02312 
        
        e_dict['rescale_sigma_h'][450][1]   = 1.
        e_dict['rescale_sigma_h'][6500][1]  = 1.
        
        e_dict['rescale_sigma_v'][450][1]   = 1.
        e_dict['rescale_sigma_v'][6500][1]  = 1.

        #### Beam 2:
        e_dict['betaf_h'][450][2]           = 193.1
        e_dict['betaf_h'][6500][2]          = 208.8
        
        e_dict['betaf_v'][450][2]           = 337.6
        e_dict['betaf_v'][6500][2]          = 340.3
        
        e_dict['sigma_corr_h'][450][2]      = 0.3367
        e_dict['sigma_corr_h'][6500][2]     = 0.3158
        
        e_dict['sigma_corr_v'][450][2]      = 0.391
        e_dict['sigma_corr_v'][6500][2]     = 0.2911
        
        e_dict['scale_h'][450][2]           = 0.02691
        e_dict['scale_h'][6500][2]          = 0.0289
        
        e_dict['scale_v'][450][2]           = 0.02708
        e_dict['scale_v'][6500][2]          = 0.03001

        e_dict['rescale_sigma_h'][450][2]   = 1.
        e_dict['rescale_sigma_h'][6500][2]  = 1.
        
        e_dict['rescale_sigma_v'][450][2]   = 1.
        e_dict['rescale_sigma_v'][6500][2]  = 1.

        # gamma
        e_dict['gamma'][450]                = 479.6 
        e_dict['gamma'][6500]               = 6927.6
        
        print('Using calibration C-2017 - latest 6.5TeV for 2018-- Update!')

    #elif filln>6550 and filln < 6594:  # WTH??
    #
    #    for kk in e_dict.keys():
    #        e_dict[kk] = {450:{}, 6500:{}}
    #
    #    # Beam 1:
    #    e_dict['betaf_h'][450][1]       = 206.8  
    #    e_dict['betaf_h'][6500][1]      = 200.76 
    #    
    #    e_dict['betaf_v'][450][1]       = 287.328
    #    e_dict['betaf_v'][6500][1]      = 329.87
    #    
    #    e_dict['sigma_corr_h'][450][1]  = 450.276381 
    #    e_dict['sigma_corr_h'][6500][1] = 322.6

     #   e_dict['sigma_corr_v'][450][1]  = 576.818985
      #  e_dict['sigma_corr_v'][6500][1] = 560.

       # e_dict['scale_h'][450][1]       = 25.738338 
        #e_dict['scale_h'][6500][1]      = 23.2     

       # e_dict['scale_v'][450][1]       = 26.84 
       # e_dict['scale_v'][6500][1]      = 25.3 

       # e_dict['rescale_sigma_h'][450][1]  = 1.
       # e_dict['rescale_sigma_h'][6500][1] = 1.
       # e_dict['rescale_sigma_v'][450][1]  = 1.
       # e_dict['rescale_sigma_v'][6500][1] = 1.

        # Beam 2:
       # e_dict['betaf_h'][450][2]       = 193.1  
       # e_dict['betaf_h'][6500][2]      = 200.  
        
       # e_dict['betaf_v'][450][2]       = 337.6 
       # e_dict['betaf_v'][6500][2]      = 328.25 
        
       # e_dict['sigma_corr_h'][450][2]  = 336.7
       # e_dict['sigma_corr_h'][6500][2] = 322.7

       # e_dict['sigma_corr_v'][450][2]  = 391.0
       # e_dict['sigma_corr_v'][6500][2] = 402.0

       # e_dict['scale_h'][450][2]       = 26.91 
       # e_dict['scale_h'][6500][2]      = 28.5 

       # e_dict['scale_v'][450][2]       = 27.08
       # e_dict['scale_v'][6500][2]      = 29.6

       # e_dict['rescale_sigma_h'][450][2]  = 1.
       # e_dict['rescale_sigma_h'][6500][2] = 1.
       # e_dict['rescale_sigma_v'][450][2]  = 1.
       # e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma
       # e_dict['gamma'][450] = 479.6
       # e_dict['gamma'][6500] = 6927.6

        #print('Using calibration 2018 A')
    elif filln>=6544  and filln <6698: # changed on 04/06/2018
    #elif filln >= 6544: # changed on Friday 27/04/2018
	for kk in list(e_dict.keys()):
		e_dict[kk] = {450:{}, 6500:{}}
        
        e_dict['wrong_sigma_corr_units'] = True
        
        # Beam 1:    
        e_dict['betaf_h'][450][1]       = 205.05
        e_dict['betaf_h'][6500][1]      = 200.0
                
        e_dict['betaf_v'][450][1]       = 286.84
        e_dict['betaf_v'][6500][1]      = 300.0
                
        e_dict['sigma_corr_h'][450][1]  = 425.2
        e_dict['sigma_corr_h'][6500][1] = 197.610741088
  
        e_dict['sigma_corr_v'][450][1]  = 407.6
        e_dict['sigma_corr_v'][6500][1] = 212.403212946
                
        e_dict['scale_h'][450][1]       = 25.35
        e_dict['scale_h'][6500][1]      = 23.6943949343
                
        e_dict['scale_v'][450][1]       = 25.32
        e_dict['scale_v'][6500][1]      = 24.7305300188
                
        e_dict['rescale_sigma_h'][450][1]  = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1]  = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.
                
        # Beam 2:
        e_dict['betaf_h'][450][2]       = 196.71
        e_dict['betaf_h'][6500][2]      = 195.9
                
        e_dict['betaf_v'][450][2]       = 358.23
        e_dict['betaf_v'][6500][2]      = 359.9
                
        e_dict['sigma_corr_h'][450][2]  = 501.6
        e_dict['sigma_corr_h'][6500][2] = 274.082028528
                
        e_dict['sigma_corr_v'][450][2]  = 618.5
        e_dict['sigma_corr_v'][6500][2] = 249.872280702
               
        e_dict['scale_h'][450][2]       = 32.02
        e_dict['scale_h'][6500][2]      = 29.7324070175
                
        e_dict['scale_v'][450][2]       = 31.52
        e_dict['scale_v'][6500][2]      = 29.9482736842
                
        e_dict['rescale_sigma_h'][450][2]  = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2]  = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.
            
        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6


        print('Using calibration 2018-A')

    elif filln>=6699  and filln <=6749: # changed on 06/06/2018
        for kk in list(e_dict.keys()):
                e_dict[kk] = {450:{}, 6500:{}}
        
        e_dict['wrong_sigma_corr_units'] = True
        
        # Beam 1:   
        e_dict['betaf_h'][450][1]       = 205.05
        e_dict['betaf_h'][6500][1]      = 200.0
               
        e_dict['betaf_v'][450][1]       = 286.84
        e_dict['betaf_v'][6500][1]      = 300.0
               
        e_dict['sigma_corr_h'][450][1]  = 425.2
        e_dict['sigma_corr_h'][6500][1] = 197.3
 
        e_dict['sigma_corr_v'][450][1]  = 407.6
        e_dict['sigma_corr_v'][6500][1] = 212.8
               
        e_dict['scale_h'][450][1]       = 25.35
        e_dict['scale_h'][6500][1]      = 23.7
               
        e_dict['scale_v'][450][1]       = 25.32
        e_dict['scale_v'][6500][1]      = 24.78
        #The "rescaling" is applied for the period between the BSRT calibration fill and the fill where the calibration factors change in timber. 
        #if rescale: #sigma_new=(scale_new/scale_old)*sigma_old
        #When applying the "rescaling" for a specific period of fills, take the LSF (e_dict['sigma_corr_']) and scale_new (e_dict['rescale_sigma_']) values after the fill for which the new calibration factors are applied in timber  
        print('rescale B1 2018-B')
        e_dict['rescale_sigma_h'][450][1] = e_dict['scale_h'][450][1]/25.35
        e_dict['rescale_sigma_h'][6500][1] = e_dict['scale_h'][6500][1]/23.7
        e_dict['rescale_sigma_v'][450][1] = e_dict['scale_v'][450][1]/ 25.32
        e_dict['rescale_sigma_v'][6500][1] = e_dict['scale_v'][6500][1]/24.78
	'''
        else:
            e_dict['rescale_sigma_h'][450][1] = 1.
            e_dict['rescale_sigma_h'][6500][1] = 1.
            e_dict['rescale_sigma_v'][450][1] = 1.
            e_dict['rescale_sigma_v'][6500][1] = 1.
         '''      
        # Beam 2:
        e_dict['betaf_h'][450][2]       = 193.6
        e_dict['betaf_h'][6500][2]      = 195.9
               
        e_dict['betaf_v'][450][2]       = 343.3
        e_dict['betaf_v'][6500][2]      = 350.95
               
        e_dict['sigma_corr_h'][450][2]  = 599.0
        e_dict['sigma_corr_h'][6500][2] = 365.56
               
        e_dict['sigma_corr_v'][450][2]  = 718.0
        e_dict['sigma_corr_v'][6500][2] = 384.0
              
        e_dict['scale_h'][450][2]       = 31.62
        e_dict['scale_h'][6500][2]      = 30.71
               
        e_dict['scale_v'][450][2]       = 32.83
        e_dict['scale_v'][6500][2]      = 34.29
               
        #if rescale: #sigma_new=(scale_new/scale_old)*sigma_old
        print('rescale B2 2018-B')
        e_dict['rescale_sigma_h'][450][2] = e_dict['scale_h'][450][2]/32.02
        e_dict['rescale_sigma_h'][6500][2] = e_dict['scale_h'][6500][2]/29.85
        e_dict['rescale_sigma_v'][450][2] = e_dict['scale_v'][450][2]/31.52
        e_dict['rescale_sigma_v'][6500][2] = e_dict['scale_v'][6500][2]/29.92
	'''
        else:
            e_dict['rescale_sigma_h'][450][2] = 1.
            e_dict['rescale_sigma_h'][6500][2] = 1.
            e_dict['rescale_sigma_v'][450][2] = 1.
            e_dict['rescale_sigma_v'][6500][2] = 1.
	'''
           
        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6


        print('Using calibration 2018-B')

    elif filln>=6750 and filln <6913: # changed on 06/06/2018
        for kk in list(e_dict.keys()):
                e_dict[kk] = {450:{}, 6500:{}}
        e_dict['wrong_sigma_corr_units'] = True
        # Beam 1:   
        e_dict['betaf_h'][450][1]       = 205.05
        e_dict['betaf_h'][6500][1]      = 200.0
               
        e_dict['betaf_v'][450][1]       = 286.84
        e_dict['betaf_v'][6500][1]      = 300.0
               
        e_dict['sigma_corr_h'][450][1]  = 425.2
        e_dict['sigma_corr_h'][6500][1] = 197.3
 
        e_dict['sigma_corr_v'][450][1]  = 407.6
        e_dict['sigma_corr_v'][6500][1] = 212.8
               
        e_dict['scale_h'][450][1]       = 25.35
        e_dict['scale_h'][6500][1]      = 23.7
               
        e_dict['scale_v'][450][1]       = 25.32
        e_dict['scale_v'][6500][1]      = 24.78

        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.
               
        # Beam 2:
        e_dict['betaf_h'][450][2]       = 193.6
        e_dict['betaf_h'][6500][2]      = 195.9
               
        e_dict['betaf_v'][450][2]       = 343.3
        e_dict['betaf_v'][6500][2]      = 350.95
               
        e_dict['sigma_corr_h'][450][2]  = 599.0
        e_dict['sigma_corr_h'][6500][2] = 365.56
               
        e_dict['sigma_corr_v'][450][2]  = 718.0
        e_dict['sigma_corr_v'][6500][2] = 384.0
              
        e_dict['scale_h'][450][2]       = 31.62
        e_dict['scale_h'][6500][2]      = 30.71
               
        e_dict['scale_v'][450][2]       = 32.83
        e_dict['scale_v'][6500][2]      = 34.29
               
        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.
           
        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6


        print('Using calibration 2018-B')

    elif filln>=6913 and filln <=7030: # changed on 08/08/2018
        for kk in list(e_dict.keys()):
                e_dict[kk] = {450:{}, 6500:{}}
        e_dict['wrong_sigma_corr_units'] = True
        # Beam 1:   
        e_dict['betaf_h'][450][1]       = 205.05
        e_dict['betaf_h'][6500][1]      = 200.0
               
        e_dict['betaf_v'][450][1]       = 286.84
        e_dict['betaf_v'][6500][1]      = 300.0
               
        e_dict['sigma_corr_h'][450][1]  = 412.7
        e_dict['sigma_corr_h'][6500][1] = 232.6
 
        e_dict['sigma_corr_v'][450][1]  = 444.8
        e_dict['sigma_corr_v'][6500][1] = 253.7
               
        e_dict['scale_h'][450][1]       = 25.1048
        e_dict['scale_h'][6500][1]      = 25.1527
               
        e_dict['scale_v'][450][1]       = 25.6796
        e_dict['scale_v'][6500][1]      = 26.2339

        #The "rescaling" is applied for the period between the BSRT calibration fill and the fill where the calibration factors change in timber. 
        #if rescale: #sigma_new=(scale_new/scale_old)*sigma_old
        #When applying the "rescaling" for a specific period of fills, take the LSF (e_dict['sigma_corr_']) and scale_new (e_dict['rescale_sigma_']) values after the fill for which the new calibration factors are applied in timber  
        print('rescale B1 2018-C')
        e_dict['rescale_sigma_h'][450][1] = e_dict['scale_h'][450][1]/25.35
        e_dict['rescale_sigma_h'][6500][1] = e_dict['scale_h'][6500][1]/23.7
        e_dict['rescale_sigma_v'][450][1] = e_dict['scale_v'][450][1]/ 25.32
        e_dict['rescale_sigma_v'][6500][1] = e_dict['scale_v'][6500][1]/24.78
	'''
        else:
            e_dict['rescale_sigma_h'][450][1] = 1.
            e_dict['rescale_sigma_h'][6500][1] = 1.
            e_dict['rescale_sigma_v'][450][1] = 1.
            e_dict['rescale_sigma_v'][6500][1] = 1.
         '''      
               
        # Beam 2:
        e_dict['betaf_h'][450][2]       = 193.6
        e_dict['betaf_h'][6500][2]      = 195.9
               
        e_dict['betaf_v'][450][2]       = 343.3
        e_dict['betaf_v'][6500][2]      = 350.95
               
        e_dict['sigma_corr_h'][450][2]  = 493.8
        e_dict['sigma_corr_h'][6500][2] = 309.9
               
        e_dict['sigma_corr_v'][450][2]  = 551.0
        e_dict['sigma_corr_v'][6500][2] = 311.0
              
        e_dict['scale_h'][450][2]       = 31.3028
        e_dict['scale_h'][6500][2]      = 28.3114
               
        e_dict['scale_v'][450][2]       = 32.6934
        e_dict['scale_v'][6500][2]      = 31.9171              
        #if rescale: #sigma_new=(scale_new/scale_old)*sigma_old
        print('rescale B2 2018-C')
        e_dict['rescale_sigma_h'][450][2] = e_dict['scale_h'][450][2]/31.62
        e_dict['rescale_sigma_h'][6500][2] = e_dict['scale_h'][6500][2]/30.71
        e_dict['rescale_sigma_v'][450][2] = e_dict['scale_v'][450][2]/32.83
        e_dict['rescale_sigma_v'][6500][2] = e_dict['scale_v'][6500][2]/34.29
	'''
        else:
            e_dict['rescale_sigma_h'][450][2] = 1.
            e_dict['rescale_sigma_h'][6500][2] = 1.
            e_dict['rescale_sigma_v'][450][2] = 1.
            e_dict['rescale_sigma_v'][6500][2] = 1.
	'''
           
        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6


        print('Using calibration 2018-C')


    elif filln>=7031 and filln <=7220 : # changed on 08/08/2018
        for kk in list(e_dict.keys()):
                e_dict[kk] = {450:{}, 6500:{}}
        e_dict['wrong_sigma_corr_units'] = True
        # Beam 1:   
        e_dict['betaf_h'][450][1]       = 204.2
        e_dict['betaf_h'][6500][1]      = 201.5
               
        e_dict['betaf_v'][450][1]       = 292.4
        e_dict['betaf_v'][6500][1]      = 287.0
               
        e_dict['sigma_corr_h'][450][1]  = 412.7
        e_dict['sigma_corr_h'][6500][1] = 232.6
 
        e_dict['sigma_corr_v'][450][1]  = 444.8
        e_dict['sigma_corr_v'][6500][1] = 253.7
               
        e_dict['scale_h'][450][1]       = 25.1048
        e_dict['scale_h'][6500][1]      = 25.1527
               
        e_dict['scale_v'][450][1]       = 25.6796
        e_dict['scale_v'][6500][1]      = 26.2339

        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.
               
        # Beam 2:
        e_dict['betaf_h'][450][2]       = 193.6
        e_dict['betaf_h'][6500][2]      = 196.0
               
        e_dict['betaf_v'][450][2]       = 343.3
        e_dict['betaf_v'][6500][2]      = 351.0
               
        e_dict['sigma_corr_h'][450][2]  = 493.8
        e_dict['sigma_corr_h'][6500][2] = 309.9
               
        e_dict['sigma_corr_v'][450][2]  = 551.0
        e_dict['sigma_corr_v'][6500][2] = 311.0
              
        e_dict['scale_h'][450][2]       = 31.3028
        e_dict['scale_h'][6500][2]      = 28.3114
               
        e_dict['scale_v'][450][2]       = 32.6934
        e_dict['scale_v'][6500][2]      = 31.9171
               
        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6

        print('Using calibration 2018-C')


    elif filln>=7221 and filln <=7333 : # changed on 21/11/2018
    #B2 untouched during recalibration:New calibration data could be retro-applied to correct better previous data
    #B1 new calibration cannot be applied to previous fills (wrt Fill 7220)
        for kk in list(e_dict.keys()):
                e_dict[kk] = {450:{}, 6500:{}}
        e_dict['wrong_sigma_corr_units'] = True
        # Beam 1:   
        e_dict['betaf_h'][450][1]       = 204.2
        e_dict['betaf_h'][6500][1]      = 201.5
               
        e_dict['betaf_v'][450][1]       = 292.4
        e_dict['betaf_v'][6500][1]      = 287.0
               
        e_dict['sigma_corr_h'][450][1]  = 432.0
        e_dict['sigma_corr_h'][6500][1] = 271.0
 
        e_dict['sigma_corr_v'][450][1]  = 449.0
        e_dict['sigma_corr_v'][6500][1] = 313.0
               
        e_dict['scale_h'][450][1]       = 24.837
        e_dict['scale_h'][6500][1]      = 24.53

        e_dict['scale_v'][450][1]       = 25.842
        e_dict['scale_v'][6500][1]      = 24.421

	#The "rescaling" is applied for the period between the BSRT calibration fill and the fill where the calibration factors change in timber. 
        #if rescale: #sigma_new=(scale_new/scale_old)*sigma_old
        #When applying the "rescaling" for a specific period of fills, take the LSF (e_dict['sigma_corr_']) and scale_new (e_dict['rescale_sigma_']) values after the fill for which the new calibration factors are applied in timber  
        e_dict['rescale_sigma_h'][450][1] = e_dict['scale_h'][450][1]/25.1048
        e_dict['rescale_sigma_h'][6500][1] = e_dict['scale_h'][6500][1]/25.1527
        e_dict['rescale_sigma_v'][450][1] = e_dict['scale_v'][450][1]/25.6796
        e_dict['rescale_sigma_v'][6500][1] = e_dict['scale_v'][6500][1]/26.2339
            
        # Beam 2:
        e_dict['betaf_h'][450][2]       = 193.6
        e_dict['betaf_h'][6500][2]      = 196.0
               
        e_dict['betaf_v'][450][2]       = 343.3
        e_dict['betaf_v'][6500][2]      = 351.0
               
        e_dict['sigma_corr_h'][450][2]  = 496.0
        e_dict['sigma_corr_h'][6500][2] = 318.0
               
        e_dict['sigma_corr_v'][450][2]  = 544.0
        e_dict['sigma_corr_v'][6500][2] = 321.0
              
        e_dict['scale_h'][450][2]       = 30.694
        e_dict['scale_h'][6500][2]      = 29.86

        e_dict['scale_v'][450][2]       = 32.02
        e_dict['scale_v'][6500][2]      = 31.73

        print('rescale B2 2018-D')
        e_dict['rescale_sigma_h'][450][2] = e_dict['scale_h'][450][2]/31.3028
        e_dict['rescale_sigma_h'][6500][2] = e_dict['scale_h'][6500][2]/28.3114
        e_dict['rescale_sigma_v'][450][2] = e_dict['scale_v'][450][2]/32.6934
        e_dict['rescale_sigma_v'][6500][2] = e_dict['scale_v'][6500][2]/31.9171

        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6

        print('Using recalibration 2018-D for B2 and calibration 2018-D for B1')


    #after fill7334 the lsf and scales changed
    elif filln>=7334 and filln <=7426 : # changed on 21/11/2018
        for kk in list(e_dict.keys()):
                e_dict[kk] = {450:{}, 6500:{}}
        e_dict['wrong_sigma_corr_units'] = True
        # Beam 1:   
        e_dict['betaf_h'][450][1]       = 204.2
        e_dict['betaf_h'][6500][1]      = 201.5
               
        e_dict['betaf_v'][450][1]       = 292.4
        e_dict['betaf_v'][6500][1]      = 287.0
               
        e_dict['sigma_corr_h'][450][1]  = 432.0
        e_dict['sigma_corr_h'][6500][1] = 271.0
 
        e_dict['sigma_corr_v'][450][1]  = 449.0
        e_dict['sigma_corr_v'][6500][1] = 313.0
               
        e_dict['scale_h'][450][1]       = 24.837
        e_dict['scale_h'][6500][1]      = 24.53

        e_dict['scale_v'][450][1]       = 25.842
        e_dict['scale_v'][6500][1]      = 24.421

        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.
               
        # Beam 2:
        e_dict['betaf_h'][450][2]       = 193.6
        e_dict['betaf_h'][6500][2]      = 196.0
               
        e_dict['betaf_v'][450][2]       = 343.3
        e_dict['betaf_v'][6500][2]      = 351.0
               
        e_dict['sigma_corr_h'][450][2]  = 496.0
        e_dict['sigma_corr_h'][6500][2] = 318.0
               
        e_dict['sigma_corr_v'][450][2]  = 544.0
        e_dict['sigma_corr_v'][6500][2] = 321.0
              
        e_dict['scale_h'][450][2]       = 30.694
        e_dict['scale_h'][6500][2]      = 29.86

        e_dict['scale_v'][450][2]       = 32.02
        e_dict['scale_v'][6500][2]      = 31.73
               
        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6

        print('Using calibration 2018-D')

    elif filln>=7427: # (IE) - Ion period 2018 added on 21.11.2018

        for kk in list(e_dict.keys()):
                e_dict[kk] = {450:{}, 6500:{}}
        e_dict['wrong_sigma_corr_units'] = True
        # Beam 1:   
        e_dict['betaf_h'][450][1]       = 204.2
        e_dict['betaf_h'][6500][1]      = 201.5

        e_dict['betaf_v'][450][1]       = 292.4
        e_dict['betaf_v'][6500][1]      = 287.0

        e_dict['sigma_corr_h'][450][1]  = 432.0
        e_dict['sigma_corr_h'][6500][1] = 271.0
 
        e_dict['sigma_corr_v'][450][1]  = 449.0
        e_dict['sigma_corr_v'][6500][1] = 313.0

        e_dict['scale_h'][450][1]       = 24.837
        e_dict['scale_h'][6500][1]      = 24.53

        e_dict['scale_v'][450][1]       = 25.842
        e_dict['scale_v'][6500][1]      = 24.421

        e_dict['rescale_sigma_h'][450][1] = 1.
        e_dict['rescale_sigma_h'][6500][1] = 1.
        e_dict['rescale_sigma_v'][450][1] = 1.
        e_dict['rescale_sigma_v'][6500][1] = 1.

        # Beam 2:
        e_dict['betaf_h'][450][2]       = 193.6
        e_dict['betaf_h'][6500][2]      = 196.0

        e_dict['betaf_v'][450][2]       = 343.3
        e_dict['betaf_v'][6500][2]      = 351.0

        e_dict['sigma_corr_h'][450][2]  = 496.0
        e_dict['sigma_corr_h'][6500][2] = 318.0
               
        e_dict['sigma_corr_v'][450][2]  = 544.0
        e_dict['sigma_corr_v'][6500][2] = 321.0

        e_dict['scale_h'][450][2]       = 30.694
        e_dict['scale_h'][6500][2]      = 29.86

        e_dict['scale_v'][450][2]       = 32.02
        e_dict['scale_v'][6500][2]      = 31.73

        e_dict['rescale_sigma_h'][450][2] = 1.
        e_dict['rescale_sigma_h'][6500][2] = 1.
        e_dict['rescale_sigma_v'][450][2] = 1.
        e_dict['rescale_sigma_v'][6500][2] = 1.

        # gamma for Pb (82,208)
        e_dict['gamma'][450] = 190.49
        e_dict['gamma'][6500] = 2696.10 # for 6369 Z GeV/c

        print('Using calibration 2018-D for Ions')

    else:
        raise ValueError('What?!')

    if 'wrong_sigma_corr_units' in list(e_dict.keys()):
        if e_dict['wrong_sigma_corr_units']:
            for plane in ['h', 'v']:
                for energy in [450, 6500]:
                    for beam in [1,2]:
                        e_dict['sigma_corr_'+plane][energy][beam] *= 1e-3
    
    return(e_dict)
