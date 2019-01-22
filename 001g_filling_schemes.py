import pickle

import LHCMeasurementTools.TimestampHelpers as th
import LHCMeasurementTools.lhc_log_db_query as lldb

t_start_string = '2017_05_01 00:00:00'
t_stop_string = '2017_12_31 00:00:00'
filepath =  './filling_patterns_2017.csv'
fills_pkl_name = '/afs/cern.ch/project/spsecloud/LHC_2017_operation/LHC_2017_operation/fills_and_bmodes.pkl'


# t_start_string = '2018_04_01 00:00:00'
# t_stop_string = '2018_12_31 00:00:00'
# filepath =  './filling_patterns_2018.csv'
# fills_pkl_name = '../LHC_2018_followup/fills_and_bmodes.pkl'


with open(fills_pkl_name, 'rb') as fid:
    dict_fill_bmodes = pickle.load(fid)

varlist = ['LHC:INJECTION_SCHEME']


fills = sorted(dict_fill_bmodes.items())
t_start = fills[0][1]['t_startfill']
t_end = fills[-1][1]['t_endfill']

t_start = th.localtime2unixstamp(t_start_string)
t_stop = th.localtime2unixstamp(t_stop_string)

lldb.dbquery(varlist, t_start, t_stop, filepath)
