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
pl.rc('font', weight='bold')

# BSRT scan parameters
filln = 4979
list_scan_times = np.linspace(1.7, 2.25, 20)

scan_thrld = 70
plot_emittance = True

average_repeated_meas = False

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
n_traces = 1.



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
                list_scan_times = np.linspace(10, 11, n_traces)
                #list_scan_times = np.linspace((t_start_STABLE-t_ref)/3600., (t_end_STABLE-t_ref)/3600.+0.5, n_traces)

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

fig_list = []
for beam in [2]:
    energy = Energy.energy(fill_dict, beam=beam)
    bct = BCT.BCT(fill_dict, beam=beam)
    bsrt_calib_dict = BSRT_calib.emittance_dictionary(filln=filln)
    bsrt  = BSRT.BSRT(fill_dict, beam=beam, calib_dict=bsrt_calib_dict, average_repeated_meas=average_repeated_meas)
    if plot_emittance:
        bsrt.calculate_emittances(energy)

    # START PLOT
    fig_h = pl.figure(beam, figsize=(12,10))
    fig_h.patch.set_facecolor('w')
   
    # Sigma and emittance      
    N_scans = len(list_scan_times)
    
    sp_emih = pl.subplot2grid((2,2), (0, 0))
    sp_emiv = pl.subplot2grid((2,2), (1, 0))
    sp_sigma_h = pl.subplot2grid((2,2), (0, 1), sharex = sp_sigma_h)
    sp_sigma_v = pl.subplot2grid((2,2), (1, 1), sharex = sp_sigma_h)
    
    t_offset = (t_start_STABLE-t_ref)/3600. 
        
    sp_emih.plot(((bsrt.t_stamps - t_ref)/3600.)-t_offset, bsrt.norm_emit_h, '.', markersize=.5, color='b')
    sp_emih.grid('on')
    sp_emih.set_ylabel('Hor. emittance [um]')
    sp_emih.set_xlim(0, None)
    sp_emih.set_ylim(0, 8)
    sp_emih.set_xlabel('Collision time [h]')
   
    sp_emiv.plot(((bsrt.t_stamps - t_ref)/3600.)-t_offset, bsrt.norm_emit_v, '.', markersize=.5, color='b')    
    sp_emiv.grid('on')
    sp_emiv.set_ylabel('Vert. emittance [um]')
    sp_emiv.set_xlim(0, None)
    sp_emiv.set_ylim(0, 8)
    sp_emiv.set_xlabel('Collision time [h]')
   

    for jj in xrange(N_scans):
        ii=N_scans-1-jj
        #colorcurr = hsv_to_rgb(float(ii)/float(N_scans), 0.9, 1.)
        colorcurr = ['b'][ii]#[pl.cm.rainbow(k) for k in np.linspace(0.1, 1, N_scans)][ii]

        t_start_requested = list_scan_times[ii]*3600. + t_ref
        try:
            scan = bsrt.find_closest_scan(t_start_requested, scan_thrld)
        except IndexError as err:
                        print 'Stop plotting! Got:'
                        print err
                        continue

        if plot_emittance:
  
            sp_sigma_h.plot(scan.bunch_n, scan.norm_emit_h, '.', color=colorcurr, 
                        label='%.1f'%((scan.t_start - t_ref)/3600.))
            sp_sigma_v.plot(scan.bunch_n, scan.norm_emit_v, '.', color=colorcurr)

        
        else:
            sp_sigma_h.plot(scan.bunch_n, scan.sigma_h, '.', color=colorcurr,
                        label='%.1f'%((scan.t_start - t_ref)/3600.))
            sp_sigma_v.plot(scan.bunch_n, scan.sigma_v, '.', color=colorcurr)
        
        #~ legend = sp_sigma_h.legend(bbox_to_anchor=(1.05, 1.03),  
                    #~ loc='upper left', 
                    #~ title='Time after stable beam \nstarted [h]', 
                    #~ prop={'size':14}, 
                    #~ ncol=2, 
                    #~ borderpad=0.5, 
                    #~ columnspacing=0.9, 
                    #~ handlelength=0.16)
        #~ pl.setp(legend.get_title(), multialignment='center') 
    

        
        #~ sp_emih.axvspan((scan.t_start-t_ref)/3600.-t_offset, (scan.t_stop - t_ref)/3600.-t_offset, 
                            #~ facecolor=colorcurr, alpha=0.6, linewidth=0)
        #~ sp_emiv.axvspan((scan.t_start - t_ref)/3600.-t_offset, (scan.t_stop - t_ref)/3600.-t_offset, 
                    #~ facecolor=colorcurr, alpha=0.6, linewidth=0)
    
    sp_sigma_h.set_xlim(1050, 1550)
    sp_sigma_v.set_xlim(1050, 1550)
    sp_sigma_h.set_ylim(0, 8)
    sp_sigma_v.set_ylim(0, 8)
    sp_sigma_h.set_xlabel('Bunch slot')
    sp_sigma_v.set_xlabel('Bunch slot')
    sp_sigma_h.grid('on')
    sp_sigma_v.grid('on')

    sp_sigma_h.set_ylabel('Hor. emittance [um]')
    sp_sigma_v.set_ylabel('Vert. emittance [um]')
    plot_str = 'emittance'

    tref_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))
    title = fig_h.suptitle('Fill %d: B%d, started on %s'%(filln, bsrt.beam, tref_string), fontsize=18)
    fig_h.subplots_adjust(top=0.9,right=0.9, left=0.1, hspace=0.3, wspace=0.3)
    
    fig_list.append(fig_h)
    fig_h.savefig('beam%d.png'%beam, dpi=300, 
        bbox_inches='tight', bbox_extra_artists=[title])


pl.show()
