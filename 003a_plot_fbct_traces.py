import LHCMeasurementTools.mystyle as ms
import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.TimestampHelpers as th
import LHCMeasurementTools.LHC_BCT as BCT
import LHCMeasurementTools.LHC_BQM as BQM
import LHCMeasurementTools.LHC_FBCT as FBCT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mlc
import matplotlib.dates as mdt
import pickle, sys, time, string
import os

from LHCMeasurementTools.LHC_Fill_LDB_Query import load_fill_dict_from_json
from data_folders import data_folder_list, recalc_h5_folder

# merge jsons and add info on location
dict_fill_bmodes={}
for df in data_folder_list:
    this_dict_fill_bmodes = load_fill_dict_from_json(
            df+'/fills_and_bmodes.json')
    for kk in this_dict_fill_bmodes:
        this_dict_fill_bmodes[kk]['data_folder'] = df
    dict_fill_bmodes.update(this_dict_fill_bmodes)

if len(sys.argv)>1:
     print('--> Processing fill {:s}'.format(sys.argv[1]))
     filln = int(sys.argv[1])

t_ref = dict_fill_bmodes[filln]['t_startfill']
t_end = dict_fill_bmodes[filln]['t_endfill']
tref_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))

traces_times = np.linspace(0.1, (t_end-t_ref)/3600., 20)
i_bun_obs_list = np.arange(0,500)[::2]
# t_loss_ref = 1.97

N_traces_set = None

int_thresh = 2e10

if len(sys.argv)>1:

     if np.any([('--n_traces'in s) for s in sys.argv]):
        i_arg = int(np.where([('--n_traces'in s) for s in sys.argv])[0])
        arg_temp = sys.argv[i_arg]
        N_traces_set = int(arg_temp.split('=')[-1])
        traces_times = np.linspace(0.1, (t_end-t_ref)/3600., N_traces_set)

     if '--injection' in sys.argv:
        print('Scans in the INJPHYS-PRERAMP beam modes')
        t_start_INJPHYS = dict_fill_bmodes[filln]['t_start_INJPHYS']
        t_start_RAMP = dict_fill_bmodes[filln]['t_start_RAMP']
        if N_traces_set==None: N_traces_set=30
        traces_times = np.linspace((t_start_INJPHYS-t_ref)/3600., (t_start_RAMP-t_ref)/3600., N_traces_set)


     if '--highenergy' in sys.argv:
        print('Scans in the FLATTOP-STABLE beam modes')
        t_start_FLATTOP = dict_fill_bmodes[filln]['t_start_FLATTOP']
        t_start_STABLE = dict_fill_bmodes[filln]['t_start_STABLE']
        if N_traces_set==None: N_traces_set=30
        traces_times = np.linspace((t_start_FLATTOP-t_ref)/3600., (t_start_STABLE-t_ref)/3600.+0.5, N_traces_set)

     if '--stablebeams' in sys.argv:
        print('Scans in the STABLE BEAMS')
        t_start_STABLE = dict_fill_bmodes[filln]['t_start_STABLE']
        t_end_STABLE = dict_fill_bmodes[filln]['t_stop_STABLE']
        if N_traces_set==None: N_traces_set=30
        traces_times = np.linspace((t_start_STABLE-t_ref)/3600., (t_end_STABLE-t_ref)/3600.+0.5, N_traces_set)

     if '--ramp' in sys.argv:
        print('Scans in the RAMP')
        t_start_RAMP= dict_fill_bmodes[filln]['t_start_RAMP']
        t_end_RAMP = dict_fill_bmodes[filln]['t_stop_RAMP']
        if N_traces_set==None: N_traces_set=10
        traces_times = np.linspace((t_start_RAMP-t_ref)/3600., (t_end_RAMP-t_ref)/3600, N_traces_set)


     if np.any([('--interval'in s) for s in sys.argv]):
        i_arg = int(np.where([('--interval'in s) for s in sys.argv])[0])
        arg_temp = sys.argv[i_arg]
        t_start_man = float(arg_temp.split('=')[-1].split(',')[0])
        t_end_man = float(arg_temp.split('=')[-1].split(',')[1])
        print('Interval manually set: %.2fh to %.2fh'%(t_start_man, t_end_man))
        if N_traces_set==None: N_traces_set=30
        traces_times = np.linspace(t_start_man, t_end_man, N_traces_set)

     if np.any([('--twotraces'in s) for s in sys.argv]):
        i_arg = int(np.where([('--twotraces'in s) for s in sys.argv])[0])
        arg_temp = sys.argv[i_arg].split('=')[-1]
        temp_list = arg_temp.split(':')
        if len(temp_list) != 4:
            raise ValueError('twotraces option should be given in the form:\n--twotraces=slot_start:n_slots:t_h:Dt_min')
        flag_two_traces = True
        slot_start_2tr = int(temp_list[0])
        n_slots_2tr = int(temp_list[1])
        t_h_2tr = float(temp_list[2])
        Dt_min_2tr = float(temp_list[3])
     else:
        flag_two_traces = False
        



     if '--notrace' in sys.argv:
        traces_times = []



plt.rcParams.update({'axes.labelsize': 18,
                     'axes.linewidth': 2,
                     'xtick.labelsize': 'large',
                     'ytick.labelsize': 'large',
                     'xtick.major.pad': 14,
                     'ytick.major.pad': 14})

format_datetime = mdt.DateFormatter('%m-%d %H:%M')

# get location of current data
data_folder_fill = dict_fill_bmodes[filln]['data_folder']
fill_dict = {}
if os.path.isdir(data_folder_fill+'/fill_basic_data_csvs'):
    # 2016 structure
    fill_dict.update(tm.parse_timber_file(data_folder_fill
        +'/fill_basic_data_csvs/basic_data_fill_%d.csv'%filln,
        verbose=True))
    fill_dict.update(tm.parse_timber_file(data_folder_fill
        +'/fill_bunchbybunch_data_csvs/bunchbybunch_data_fill_%d.csv'%filln
        , verbose=True))
elif os.path.isdir(data_folder_fill+'/fill_basic_data_h5s'):
    fill_dict.update(tm.CalsVariables_from_h5(data_folder_fill
        +'/fill_basic_data_h5s/basic_data_fill_%d.h5'%filln,
        ))
    fill_dict.update(tm.CalsVariables_from_h5(data_folder_fill
        +'/fill_bunchbybunch_data_h5s/bunchbybunch_data_fill_%d.h5'%filln))
else:
    raise ValueError('This mode is discontinous')
    # # 2015 structure
    # fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_csvs/fill_%d.csv'%filln, verbose=True))

n_traces = len(traces_times)
bint_thresh = 8e9

sp_t = None

i_fig = 0
plt.close('all')
ms.mystyle_arial(fontsz=16, dist_tick_lab=5)
beam_col = ['b','r']
fig_list = []
figures_2traces={}
for beam in [1,2]:
    fbct = FBCT.FBCT(fill_dict, beam=beam)
    bct = BCT.BCT(fill_dict, beam=beam)

    fig1 = plt.figure(i_fig, figsize=(14, 8))
    fig1.patch.set_facecolor('w')
    fig_list.append(fig1)
    ax0 = plt.subplot(211, sharex=sp_t)
    sp_t = ax0
    ax1 = plt.subplot(212)


    ax0.plot((bct.t_stamps-t_ref)/3600., bct.values, color=beam_col[beam-1], lw=2)
    for i in range(0, n_traces):
        t_cut_h = traces_times[i]
        t_curr = t_ref+t_cut_h*3600.
        fbct_curr, t_fbct_curr = fbct.nearest_older_sample(t_curr, flag_return_time=True)

        ax1.plot(fbct_curr, color=ms.colorprog(i, n_traces),
                     label='%.2f h'%((t_fbct_curr-t_ref)/3600.))
        ax0.axvline((t_fbct_curr-t_ref)/3600., lw=1.5, color=ms.colorprog(i, n_traces))

    ax1.set_xlabel('25 ns slot')
    ax1.set_xlim(0, 3500)
    ax1.set_ylabel('Bunch intensity [p$^+$]')
    ax1.grid('on')
    ax0.set_xlabel('Time [h]')
    ax0.set_ylabel('Beam intensity [p]')
    ax0.grid('on')
    ax0.set_ylim(bottom=0)
    plt.subplots_adjust(top=0.9, bottom=0.1, right=0.95,
                        left=0.1, hspace=0.3, wspace=0.4)
    fig1.suptitle('Fill %d: B%d, started on %s'%(filln, beam, tref_string), fontsize=20)
    i_fig += 1

    #plot bunch by bunch losses
    fig3 = plt.figure(i_fig, figsize=(14, 8))
    fig3.patch.set_facecolor('w')
    fig_list.append(fig3)
    ax30 = plt.subplot(211, sharex=sp_t)
    #sp_t = ax30
    ax31 = plt.subplot(212)

    #find the filled slots
    mask_bunches = np.ma.masked_greater(fbct.bint, bint_thresh).mask
    list_nbunches = np.sum(mask_bunches, axis=0)
    i_bunches = np.where(list_nbunches > 0)[0]
    i_bunches_sel = list(set(i_bunches) & set(i_bun_obs_list))

    ax30.plot((bct.t_stamps-t_ref)/3600., bct.values, color=beam_col[beam-1], lw=2)
    #fbct_old = np.zeros(len(list_nbunches))
    for i in range(0, n_traces): #(0,1)
        t_cut_h = traces_times[i]
        t_curr = t_ref+t_cut_h*3600.
        t_delta = 10./60. #10 minutes
        fbct_curr, t_fbct_curr = fbct.nearest_older_sample(t_curr, flag_return_time=True)
        fbct_old, t_fbct_curr = fbct.nearest_older_sample(t_curr-t_delta*3600, flag_return_time=True)
        fbct_losses = np.zeros(len(list_nbunches))
        for i_b in i_bunches:
            if fbct_old[i_b] != 0.:
                loss = (fbct_old[i_b]-fbct_curr[i_b])/(fbct_old[i_b]*t_delta)
                fbct_losses[i_b] = loss
        ax31.plot(fbct_losses, color=ms.colorprog(i, n_traces),
                     label='%.2f h'%((t_fbct_curr-t_ref)/3600.))
        ax30.axvline((t_fbct_curr-t_ref)/3600., lw=1.5, color=ms.colorprog(i, n_traces))
        #fbct_old = fbct_curr
        
    ax31.set_xlabel('25 ns slot')
    ax31.set_xlim(0, 3500)
    ax31.set_ylabel('Loss rate [%/h]')
    ax31.grid('on')
    ax30.set_xlabel('Time [h]')
    ax30.set_ylabel('Beam intensity [p]')
    ax30.grid('on')
    ax30.set_ylim(bottom=0)
    plt.subplots_adjust(top=0.9, bottom=0.1, right=0.95,
                        left=0.1, hspace=0.3, wspace=0.4)
    fig3.suptitle('Fill %d: B%d, started on %s'%(filln, beam, tref_string), fontsize=20)
    i_fig += 1

    # #find the filled slots
    # mask_bunches = np.ma.masked_greater(fbct.bint, bint_thresh).mask
    # list_nbunches = np.sum(mask_bunches, axis=0)
    # i_bunches = np.where(list_nbunches > 0)[0]

    N_bunches = len(i_bunches)
    figbbb = plt.figure(100+i_fig, figsize=(14, 10))
    figbbb.patch.set_facecolor('w')
    axbbb_bct = plt.subplot(211, sharex=sp_t)
    axbbb_traces = plt.subplot(212, sharex=axbbb_bct)

    #figlosref = plt.figure(200+i_fig, figsize=(14, 8), tight_layout=False)
    #figlosref.patch.set_facecolor('w')
    #axlref_bct = plt.subplot(211)
    #axlref_traces = plt.subplot(212, sharex=axbbb_bct)

    i_bunches_sel = list(set(i_bunches) & set(i_bun_obs_list))

    #totint_at_loss_ref = bct.nearest_older_sample(t_ref+t_loss_ref*3600)

    axbbb_bct.plot((bct.t_stamps-t_ref)/3600., bct.values, color=beam_col[beam-1], lw=2)
    for i_line, i_bun in enumerate(i_bunches_sel):
        if np.max(fbct.bint[:, i_bun])<int_thresh:
            continue
        axbbb_traces.plot((fbct.t_stamps-t_ref)/3600., 1.-fbct.bint[:, i_bun]/np.max(fbct.bint[:, i_bun]),
        color=ms.colorprog(i_line, len(i_bunches_sel)))
    axbbb_bct.grid('on')
    axbbb_traces.grid('on')
    axbbb_bct.set_ylabel('Beam intensity [p]')
    axbbb_bct.set_xlabel('Time [h]')
    axbbb_traces.set_ylabel('Lost bunch fraction')
    axbbb_traces.set_xlabel('Time [h]')
    
    if flag_two_traces:
        fig2traces = plt.figure(200 + beam)
        fig2traces.set_facecolor('w')
        sp2tr = fig2traces.add_subplot(111)

        t_first_trace = t_ref+ t_h_2tr*3600.
        t_second_trace = t_first_trace + Dt_min_2tr*60
        inten_first, t_real_first = fbct.nearest_sample(t_first_trace, flag_return_time=True)
        inten_second, t_real_second = fbct.nearest_sample(t_second_trace, flag_return_time=True)
        
        mask_2tr = inten_first[slot_start_2tr : slot_start_2tr + n_slots_2tr] > 1e10

        sp2tr.plot(inten_first[slot_start_2tr : slot_start_2tr + n_slots_2tr] * np.float_(mask_2tr), 'b', linewidth=2)
        sp2tr.plot(inten_second[slot_start_2tr : slot_start_2tr + n_slots_2tr] * np.float_(mask_2tr), 'r', linewidth=2)
        sp2tr.set_xlim(0, n_slots_2tr)
        sp2tr.set_ylabel('Bunch intensity [p]')
        sp2tr.set_xlabel('Bunch slot')
        sp2tr.grid(True)

        fig2traces.suptitle('Fill %d: B%d, started on %s\nt_h = %.3f, Dt= %.1f min, slot =%d'%(
            filln, beam, tref_string, t_h_2tr, Dt_min_2tr, slot_start_2tr))
        fig2traces.subplots_adjust(top=.84)

        figures_2traces[beam] = fig2traces

plt.show()
