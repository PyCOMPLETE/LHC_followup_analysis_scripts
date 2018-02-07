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

pl.rcParams['lines.linewidth'] = 2


# BSRT scan parameters
filln = 4979
list_scan_times = np.linspace(1.7, 2.25, 20)

scan_thrld = 70
plot_emittance = True
average_repeated_meas = True

if len(sys.argv)>1:
     print '--> Processing fill {:s}'.format(sys.argv[1])
     filln = int(sys.argv[1])

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
n_traces = 5



#for 4947
#~ list_scan_times_before_blowup = np.linspace(6.0, 6.5, n_traces)
#~ list_scan_times_after_blowup = np.linspace(11.0, 11.5, n_traces)


#for 4958
#~ list_scan_times_before_blowup = np.linspace(3.0, 3.5, n_traces)
#~ list_scan_times_after_blowup = np.linspace(6.0, 6.5, n_traces)

#for 4961
#~ list_scan_times_before_blowup = np.linspace(2.6, 3.1, n_traces)
#~ list_scan_times_after_blowup = np.linspace(6.0, 6.5, n_traces)

#~ #for 4964
#~ list_scan_times_before_blowup = np.linspace(2.6, 3.1, n_traces)
#~ list_scan_times_after_blowup = np.linspace(6.0, 6.5, n_traces)

#for 4965
#~ list_scan_times_before_blowup = np.linspace(5.0, 5.5, n_traces)
#~ list_scan_times_after_blowup = np.linspace(9.0, 9.5, n_traces)

#for 4979
#~ list_scan_times_before_blowup = np.linspace(4, 4.5, n_traces)
#~ list_scan_times_after_blowup = np.linspace(10.0, 10.5, n_traces)

#for 4080
#~ list_scan_times_before_blowup = np.linspace(8, 8.5, n_traces)
#~ list_scan_times_after_blowup = np.linspace(12., 12.5, n_traces) 

if len(sys.argv)>1:

     if np.any(map(lambda s: ('--n_traces'in s), sys.argv)):
        i_arg = np.where(map(lambda s: ('--n_traces'in s), sys.argv))[0]
        arg_temp = sys.argv[i_arg]
        n_traces = float(arg_temp.split('=')[-1])

        list_scan_times = np.linspace((t_start_fill-t_ref)/3600., (t_end_fill-t_ref)/3600., n_traces)
         
     if '--injection' in sys.argv:
                print 'Scans in the INJPHYS-PRERAMP beam modes'
                t_start_INJPHYS = dict_fill_bmodes[filln]['t_start_INJPHYS']
                t_start_RAMP = dict_fill_bmodes[filln]['t_start_RAMP']
                list_scan_times = np.linspace((t_start_INJPHYS-t_ref)/3600., (t_start_RAMP-t_ref)/3600., n_traces)


     if '--highenergy' in sys.argv:
                print 'Scans in the FLATTOP-STABLE beam modes'
                t_start_FLATTOP = dict_fill_bmodes[filln]['t_start_FLATTOP']
                t_start_STABLE = dict_fill_bmodes[filln]['t_start_STABLE']
                list_scan_times = np.linspace((t_start_FLATTOP-t_ref)/3600., (t_start_STABLE-t_ref)/3600.+0.5, n_traces)

     if '--stablebeams' in sys.argv:
                print 'Scans in the STABLE BEAMS'
                t_start_STABLE = dict_fill_bmodes[filln]['t_start_STABLE']
                t_end_STABLE = dict_fill_bmodes[filln]['t_stop_STABLE']
                list_scan_times = np.linspace((t_start_STABLE-t_ref)/3600., (t_end_STABLE-t_ref)/3600.+0.5, n_traces)

     if '--sigma' in sys.argv:
                plot_emittance=False
                
     if '--avgrep' in sys.argv:
            average_repeated_meas = True

     if np.any(map(lambda s: ('--interval'in s), sys.argv)):
        i_arg = np.where(map(lambda s: ('--interval'in s), sys.argv))[0]
        arg_temp = sys.argv[i_arg]
        t_start_man = float(arg_temp.split('=')[-1].split(',')[0])
        t_end_man = float(arg_temp.split('=')[-1].split(',')[1])
        print 'Interval manually set: %.2fh to %.2fh'%(t_start_man, t_end_man)
        list_scan_times = np.linspace(t_start_man, t_end_man, n_traces)

     if '--notrace' in sys.argv:
        list_scan_times = []


fill_dict = {}
if os.path.isdir(data_folder_fill+'/fill_basic_data_csvs'):
    # 2016 structure
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_basic_data_csvs/basic_data_fill_%d.csv'%filln, verbose=True))
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_bunchbybunch_data_csvs/bunchbybunch_data_fill_%d.csv'%filln, verbose=True))
else:
    # 2015 structure
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_csvs/fill_%d.csv'%filln, verbose=True))
        

sp_sigma_h = None
sp_t = None
pl.close('all')
ms.mystyle_arial(fontsz=16, dist_tick_lab=5)

for beam in [1,2]:
    
    dict_beams = {'sigma_v_before_blowup':[],
                'sigma_v_after_blowup':[],
                'bunch_n':[]}
    
    energy = Energy.energy(fill_dict, beam=beam)
    bct = BCT.BCT(fill_dict, beam=beam)
    bsrt_calib_dict = BSRT_calib.emittance_dictionary(filln=filln)
    bsrt  = BSRT.BSRT(fill_dict, beam=beam, calib_dict=bsrt_calib_dict, average_repeated_meas=average_repeated_meas)

    if plot_emittance:
        bsrt.calculate_emittances(energy)
    
    fill = BSRT.Masked(bsrt, t_start_fill, t_end_fill)
    
    # Figure setting up
    pl.figure(beam, figsize=(12,10)) 
    sp_emittance_ev = pl.subplot2grid((2,2), (0, 0))
    sp_bunch = pl.subplot2grid((2,2), (1, 0))
    sp_sigma_v_before_blowup = pl.subplot2grid((2,2), (0, 1))
    sp_sigma_v_after_blowup = pl.subplot2grid((2,2), (1, 1))
    sp_emittance_ev.set_ylim(0,8)
    sp_sigma_v_before_blowup.set_ylim(0,8)
    sp_sigma_v_after_blowup.set_ylim(0,8)
    
    # We start playing ....
    #----------------------------------
    sp_emittance_ev.plot(((bsrt.t_stamps - t_ref)/3600.), bsrt.norm_emit_v, '.', markersize=.5, color='b')
    
    mask_scan = fill.t_stamps > t_ref
    sp_bunch.plot((fill.t_stamps[mask_scan] - t_ref)/3600., fill.bunch_n[mask_scan], 'b')
    bsrt.find_start_scans(scan_thrld)

    
    # Check the emittance BEFORE the instability development
    N_scans_before_blowup = len(list_scan_times_before_blowup)
    
    sigma_before_blowup_scans = []
    for ii in xrange(N_scans_before_blowup):
        colorcurr = [pl.cm.rainbow(k) for k in np.linspace(0, 0.5, N_scans_before_blowup)][ii]
        
        t_start_requested_before_blowup = list_scan_times_before_blowup[ii]*3600. + t_ref
        try:
            scan_before_blowup = bsrt.find_closest_scan(t_start_requested_before_blowup, scan_thrld)
        except IndexError as err:
                        print 'Stop plotting! Got:'
                        print err
                        continue
        
        sigma_before_blowup_scans.append(scan_before_blowup.norm_emit_v)
        
        sp_sigma_v_before_blowup.plot(scan_before_blowup.bunch_n, scan_before_blowup.norm_emit_v, '.', 
                    color=colorcurr)
        sp_emittance_ev.axvspan((scan_before_blowup.t_start - t_ref)/3600., (scan_before_blowup.t_stop - t_ref)/3600., 
                facecolor=colorcurr, alpha=0.6, linewidth=0)
        sp_bunch.axvspan((scan_before_blowup.t_start - t_ref)/3600., (scan_before_blowup.t_stop - t_ref)/3600., 
                facecolor=colorcurr, alpha=0.6, linewidth=0)
     

    # Check the emittance AFTER the instability development
    sigma_after_blowup_scans = []
    N_scans_after_blowup = len(list_scan_times_after_blowup) 
    for jj in xrange(N_scans_after_blowup):
        colorcurr = [pl.cm.rainbow(k) for k in np.linspace(0.5, 1, N_scans_after_blowup)][jj]
        
        t_start_requested_after_blowup = list_scan_times_after_blowup[jj]*3600. + t_ref
        try:
            scan_after_blowup = bsrt.find_closest_scan(t_start_requested_after_blowup, scan_thrld)
        except IndexError as err:
                        print 'Stop plotting! Got:'
                        print err
                        continue
        
        sigma_after_blowup_scans.append(scan_after_blowup.norm_emit_v)

        sp_sigma_v_after_blowup.plot(scan_after_blowup.bunch_n, scan_after_blowup.norm_emit_v, '.', color=colorcurr)
        sp_emittance_ev.axvspan((scan_after_blowup.t_start - t_ref)/3600., (scan_after_blowup.t_stop - t_ref)/3600., 
                facecolor=colorcurr, alpha=0.6, linewidth=0)
        sp_bunch.axvspan((scan_after_blowup.t_start - t_ref)/3600., (scan_after_blowup.t_stop - t_ref)/3600., 
                facecolor=colorcurr, alpha=0.6, linewidth=0)
                                                

    avg_sigma_before_blowup = np.mean(sigma_before_blowup_scans, axis=0)
    avg_sigma_after_blowup = np.mean(sigma_after_blowup_scans, axis=0)
    
    delta_sigma_v = (avg_sigma_after_blowup - avg_sigma_before_blowup)/avg_sigma_before_blowup
    dict_beams['sigma_v_before_blowup'].append(avg_sigma_before_blowup)
    dict_beams['sigma_v_after_blowup'].append(avg_sigma_after_blowup)
    dict_beams['bunch_n'].append(scan_after_blowup.bunch_n)

    import scipy.io as sio
    sio.savemat('bbb_emi_dict%dB%d.mat'%(filln, beam),
            {'sigma_v_before_blowup':dict_beams['sigma_v_before_blowup'],
            'sigma_v_after_blowup':dict_beams['sigma_v_after_blowup'],
            'bunch_n':dict_beams['bunch_n']}, oned_as='row')
      
pl.show()
