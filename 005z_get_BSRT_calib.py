import sys, os
BIN = os.path.expanduser("../LHC_fullRun2_analysis_scripts/")
sys.path.append(BIN)

import pickle

filln = 6638
#~ filln = 6055

fills_pkl_name = '../LHC_2018_followup/fills_and_bmodes.pkl'
with open(fills_pkl_name, 'rb') as fid:
    dict_fill_bmodes = pickle.load(fid)

import pytimber
ldb = pytimber.LoggingDB()


device_name = {1:'5R4', 2:'5L4'}
event = {450:'t_stop_INJPHYS', 6500:'t_start_STABLE'}


e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{}, 
      'sigma_corr_h':{}, 'sigma_corr_v':{},
      'rescale_sigma_h':{}, 'rescale_sigma_v':{}, 'scale_h': {}, 'scale_v': {}}
for kk in e_dict.keys():
    e_dict[kk] = {450:{}, 6500:{}}
    
e_dict['gamma'][450]                = 479.6 
e_dict['gamma'][6500]               = 6927.6


for ene in [450, 6500]:
    t_ref = dict_fill_bmodes[filln][event[ene]]


    for beam in [1, 2]:

        data = {}
        data.update(ldb.get([
                        u'LHC.BSRT.%s.B%d:LSF_H'%(device_name[beam], beam),
                        u'LHC.BSRT.%s.B%s:LSF_V'%(device_name[beam], beam),
                        u'LHC.BSRT.%s.B%d:BETA_H'%(device_name[beam], beam),
                        u'LHC.BSRT.%s.B%s:BETA_V'%(device_name[beam], beam)
                        ],
                        t1=t_ref, t2='last'))
                        
        e_dict['betaf_h'][ene][beam] = data['LHC.BSRT.%s.B%d:BETA_H'%(device_name[beam], beam)][1][0]
        e_dict['betaf_v'][ene][beam] = data['LHC.BSRT.%s.B%d:BETA_V'%(device_name[beam], beam)][1][0]
        e_dict['sigma_corr_h'][ene][beam] = data['LHC.BSRT.%s.B%d:LSF_H'%(device_name[beam], beam)][1][0]*1e-3
        e_dict['sigma_corr_v'][ene][beam] = data['LHC.BSRT.%s.B%d:LSF_V'%(device_name[beam], beam)][1][0]*1e-3
        e_dict['rescale_sigma_h'][ene][beam] = 1.
        e_dict['rescale_sigma_v'][ene][beam] = 1.
        
print e_dict

