from LHCMeasurementTools.LHC_Fill_LDB_Query import load_fill_dict_from_json
from data_folders import data_folder_list, recalc_h5_folder

filln = 6740
#~ filln = 6055

# merge jsons and add info on location
dict_fill_bmodes={}
for df in data_folder_list:
    this_dict_fill_bmodes = load_fill_dict_from_json(
            df+'/fills_and_bmodes.json')
    for kk in this_dict_fill_bmodes:
        this_dict_fill_bmodes[kk]['data_folder'] = df
    dict_fill_bmodes.update(this_dict_fill_bmodes)

import pytimber
ldb = pytimber.LoggingDB(source='nxcals')
#ldb = pytimber.LoggingDB(source='ldb')


device_name = {1:'5R4', 2:'5L4'}
event = {450:'t_stop_INJPHYS', 6500:'t_start_STABLE'}


e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{},
      'sigma_corr_h':{}, 'sigma_corr_v':{},
      'rescale_sigma_h':{}, 'rescale_sigma_v':{}, 'scale_h': {}, 'scale_v': {}}
for kk in list(e_dict.keys()):
    e_dict[kk] = {450:{}, 6500:{}}

e_dict['gamma'][450]                = 479.6
e_dict['gamma'][6500]               = 6927.6


for ene in [450, 6500]:
    t_ref = dict_fill_bmodes[filln][event[ene]]


    for beam in [1, 2]:

        data = {}
        data.update(ldb.get([
                        'LHC.BSRT.%s.B%d:LSF_H'%(device_name[beam], beam),
                        'LHC.BSRT.%s.B%s:LSF_V'%(device_name[beam], beam),
                        'LHC.BSRT.%s.B%d:BETA_H'%(device_name[beam], beam),
                        'LHC.BSRT.%s.B%s:BETA_V'%(device_name[beam], beam)
                        ],
                        t1=t_ref, t2='last'))

        e_dict['betaf_h'][ene][beam] = data['LHC.BSRT.%s.B%d:BETA_H'%(device_name[beam], beam)][1][0]
        e_dict['betaf_v'][ene][beam] = data['LHC.BSRT.%s.B%d:BETA_V'%(device_name[beam], beam)][1][0]
        e_dict['sigma_corr_h'][ene][beam] = data['LHC.BSRT.%s.B%d:LSF_H'%(device_name[beam], beam)][1][0]*1e-3
        e_dict['sigma_corr_v'][ene][beam] = data['LHC.BSRT.%s.B%d:LSF_V'%(device_name[beam], beam)][1][0]*1e-3
        e_dict['rescale_sigma_h'][ene][beam] = 1.
        e_dict['rescale_sigma_v'][ene][beam] = 1.

print(e_dict)

