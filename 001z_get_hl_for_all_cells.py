import sys, time
sys.path.append("../")

import LHCMeasurementTools.lhc_log_db_query as lldb
import LHCMeasurementTools.LHC_Heatloads as HL


import pickle
import numpy as np

# filln = 4485

if len(sys.argv) > 1:
     filln = int(sys.argv[1])

fills_pkl_name = '../fills_and_bmodes.pkl'
with open(fills_pkl_name, 'rb') as fid:
    dict_fill_bmodes = pickle.load(fid)
    
t_start_fill = dict_fill_bmodes[filln]['t_startfill']
t_end_fill = dict_fill_bmodes[filln]['t_endfill']


sector_list = HL.sector_list()
variable_list = HL.sector_all_variables(sector_list)
#variable_list=['CMS:LUMI_TOT_INST','S12_QBS_AVG_ARC.POSST']

fill_file = 'hl_all_cells_fill_%d.csv'%filln

lldb.dbquery(variable_list, t_start_fill, t_end_fill, fill_file)
