import pickle

import LHCMeasurementTools.TimestampHelpers as th
import LHCMeasurementTools.lhc_log_db_query as lldb

t_start_string = '2017_05_01 00:00:00'
t_stop_string = '2017_12_31 00:00:00'
filepath =  './filling_patterns_2017.csv'


# t_start_string = '2018_04_01 00:00:00'
# t_stop_string = '2018_12_31 00:00:00'
# filepath =  './filling_patterns_2018.csv'

varlist = ['LHC:INJECTION_SCHEME']

t_start = th.localtime2unixstamp(t_start_string)
t_stop = th.localtime2unixstamp(t_stop_string)

lldb.dbquery(varlist, t_start, t_stop, filepath)
