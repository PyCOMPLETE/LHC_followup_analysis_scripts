import pickle

import LHCMeasurementTools.TimestampHelpers as th
import LHCMeasurementTools.lhc_log_db_query as lldb

filepath =  './filling_patterns.csv'

fills_pkl_name = '../LHC_2017_operation/fills_and_bmodes.pkl'
with open(fills_pkl_name, 'rb') as fid:
    dict_fill_bmodes = pickle.load(fid)

varlist = ['LHC:INJECTION_SCHEME']


fills = sorted(dict_fill_bmodes.items())
t_start = fills[0][1]['t_startfill']
t_end = fills[-1][1]['t_endfill']

t_start_string = '2015_01_01 00:00:00'
t_stop_string = '2017_12_31 09:00:00'

t_start = th.localtime2unixstamp(t_start_string)
t_stop = th.localtime2unixstamp(t_stop_string)

lldb.dbquery(varlist, t_start, t_stop, filepath)
