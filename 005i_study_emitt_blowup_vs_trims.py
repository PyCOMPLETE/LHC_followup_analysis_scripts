import LHCMeasurementTools.LHC_BCT as BCT
import LHCMeasurementTools.LHC_Energy as Energy
import LHCMeasurementTools.LHC_BSRT as BSRT
import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.mystyle as ms
import BSRT_calib 
import numpy as np
import pylab as pl
import pickle
import sys, time
from colorsys import hsv_to_rgb
import os

import pytimber
ldb = pytimber.LoggingDB()


t_step_resample_s = 2*60.

filln = 6071
t_cut_delay_h = 0
beam = 1

DT_Demitt_s = 3600.


scan_thrld = 70

average_repeated_meas = False

if len(sys.argv)>1:
     print '--> Processing fill {:s}'.format(sys.argv[1])
     filln = int(sys.argv[1])

##################
## Data loading ##
##################

# merge pickles and add info on location
from data_folders import data_folder_list
dict_fill_bmodes={}
for df in data_folder_list:
    with open(df+'/fills_and_bmodes.pkl', 'rb') as fid:
        this_dict_fill_bmodes = pickle.load(fid)
        for kk in this_dict_fill_bmodes:
            this_dict_fill_bmodes[kk]['data_folder'] = df
        dict_fill_bmodes.update(this_dict_fill_bmodes)
        
# get location of current data
data_folder_fill = dict_fill_bmodes[filln]['data_folder']


t_start_fill = dict_fill_bmodes[filln]['t_startfill']
t_end_fill = dict_fill_bmodes[filln]['t_endfill']
t_fill_len = t_end_fill - t_start_fill
t_ref = t_start_fill
n_traces = 50.


fill_dict = {}
if os.path.isdir(data_folder_fill+'/fill_basic_data_csvs'):
    # 2016 structure
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_basic_data_csvs/basic_data_fill_%d.csv'%filln, verbose=True))
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_bunchbybunch_data_csvs/bunchbybunch_data_fill_%d.csv'%filln, verbose=True))
else:
    # 2015 structure
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_csvs/fill_%d.csv'%filln, verbose=True))
        
beam_col = ['k', 'b','r']

sp_sigma_h = None
sp_t = None


###################
## Data from LDB ##
###################

print 'Get tunes from LDB...'
data = {}
data.update(ldb.getScaled(['LHC.BOFSU:TUNE_B%d_H'%beam, 'LHC.BOFSU:TUNE_B%d_V'%beam, 'RPMBB.RR13.ROF.A81B%d:I_MEAS'%beam],
 			t_start_fill, t_end_fill, scaleAlgorithm='AVG', scaleInterval='SECOND',scaleSize='30'))
            
            
            
print 'Done'



##################
## Data manip   ##
##################

bsrt_calib_dict = BSRT_calib.emittance_dictionary(filln=filln)

energy = Energy.energy(fill_dict, beam=beam)
bct = BCT.BCT(fill_dict, beam=beam)
bsrt  = BSRT.BSRT(fill_dict, beam=beam, calib_dict=bsrt_calib_dict, average_repeated_meas=average_repeated_meas)
bsrt.calculate_emittances(energy)

dict_bunches, t_bbb, emit_h_bbb, emit_v_bbb, bunch_n_un = bsrt.get_bbb_emit_evolution()

#resample with uniform time step
resampled_emit_h_bbb = []
resampled_emit_v_bbb = []

t_resampled = np.arange(t_start_fill, t_end_fill, t_step_resample_s)

for i_b in xrange(len(emit_h_bbb)):
    resampled_emit_h_bbb.append(np.interp(t_resampled, t_bbb[i_b], emit_h_bbb[i_b]))
    resampled_emit_v_bbb.append(np.interp(t_resampled, t_bbb[i_b], emit_v_bbb[i_b]))
    
    resampled_emit_h_bbb[i_b][t_resampled<t_bbb[i_b][0]] = np.nan
    resampled_emit_v_bbb[i_b][t_resampled<t_bbb[i_b][0]] = np.nan
    
    resampled_emit_h_bbb[i_b][t_resampled<t_ref+t_cut_delay_h*3600.] = np.nan
    resampled_emit_v_bbb[i_b][t_resampled<t_ref+t_cut_delay_h*3600.] = np.nan
    
resampled_emit_h_bbb = np.array(resampled_emit_h_bbb)
resampled_emit_v_bbb = np.array(resampled_emit_v_bbb)

mean_h = np.nanmean(resampled_emit_h_bbb, axis=0)
mean_v = np.nanmean(resampled_emit_v_bbb, axis=0)

std_h = np.nanstd(resampled_emit_h_bbb, axis=0)
std_v = np.nanstd(resampled_emit_v_bbb, axis=0)

# Find max intensity
t_maxint = bct.t_stamps[np.argmax(bct.values)]

emitt_end_inj_h = np.interp(t_maxint, t_resampled, mean_h)
emitt_end_inj_v = np.interp(t_maxint, t_resampled, mean_v)

Demitt_h_Dt_um_h = (np.interp(t_maxint + DT_Demitt_s, t_resampled, mean_h) - emitt_end_inj_h)/DT_Demitt_s*3600.
Demitt_h_Dt_um_v = (np.interp(t_maxint + DT_Demitt_s, t_resampled, mean_v) - emitt_end_inj_v)/DT_Demitt_s*3600.


pl.close('all')
lw=2
ms.mystyle_arial(fontsz=14, dist_tick_lab=5)

# Time manipulation
import LHCMeasurementTools.TimestampHelpers as th
time_conv = th.TimeConverter(time_in='hourtime')
tc = time_conv.from_unix

fig1 = pl.figure(1, figsize=(8*1.1,6*1.5))
fig1.set_facecolor('w')
sp1 = pl.subplot(4,1,1)
pl.plot(tc(bct.t_stamps), bct.values, lw=lw, color = {1:'b', 2:'r'}[beam])
sp1.set_ylim(bottom=0.)
sp1.set_ylabel('Intensity [p]')

sp2 = pl.subplot(4,1,2, sharex=sp1)
pl.plot(tc(t_resampled), mean_h, 'b')
pl.fill_between(x=tc(t_resampled),y1=np.nan_to_num(mean_h-std_h),y2=np.nan_to_num(mean_h+std_h), color = 'b', alpha=.3, lw=lw)
pl.plot(tc(t_resampled), mean_v, 'g')
pl.fill_between(x=tc(t_resampled),y1=np.nan_to_num(mean_v-std_v),y2=np.nan_to_num(mean_v+std_v), color = 'g', alpha=.3, lw=lw)
sp2.set_ylim(1, 3.5)
sp2.set_ylabel('Emittance [um]')

sp3 = pl.subplot(4,1,3, sharex=sp1)
var = 'LHC.BOFSU:TUNE_B%d_H'%beam;sp3.plot(tc(data[var][0]), data[var][1], color='b', lw=lw)
var = 'LHC.BOFSU:TUNE_B%d_V'%beam;sp3.plot(tc(data[var][0]), data[var][1], color='g', lw=lw)
sp3.set_ylabel('Tunes')


sp4 = pl.subplot(4,1,4, sharex=sp1)
var = 'RPMBB.RR13.ROF.A81B%d:I_MEAS'%beam;sp4.plot(tc(data[var][0]), data[var][1], lw=lw, color='grey')
sp4.set_ylim(0, 50)

sp4.set_xlim(tc(t_resampled)[0], tc(t_resampled)[-1])
sp4.set_ylabel('I oct [A]')


for sp in [sp1, sp2, sp3, sp4]:
    sp.grid('on')
    sp.axvspan(tc(t_maxint), tc(t_maxint+ DT_Demitt_s), color='grey', alpha = .3)

time_conv.set_x_for_plot(fig1, sp1)

tref_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))


pl.tight_layout()
fig1.subplots_adjust(top=.82)

summary_string = \
'After the last injection:\n'+\
'H: emittance = %.2f um growth = %.2f um/h\n'%(emitt_end_inj_h, Demitt_h_Dt_um_h)+\
'V: emittance = %.2f um growth = %.2f um/h\n'%(emitt_end_inj_v, Demitt_h_Dt_um_v)
fig1.suptitle('Fill %d: B%d, started on %s\n\n'%(filln, bsrt.beam, tref_string)+summary_string)

pl.show()
