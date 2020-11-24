import LHCMeasurementTools.LHC_BQM as BQM
import LHCMeasurementTools.TimestampHelpers as th
import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.LHC_FBCT as FBCT
import LHCMeasurementTools.mystyle as ms
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mlc
import matplotlib.dates as mdt
import pickle, sys, time, string

plt.rcParams.update({'axes.labelsize': 18,
                     'axes.linewidth': 2,
                     'xtick.labelsize': 'large',
                     'ytick.labelsize': 'large',
                     'xtick.major.pad': 14,
                     'ytick.major.pad': 14})

format_datetime = mdt.DateFormatter('%m-%d %H:%M')

ylim = False
cmap = 'jet_r'
t_inter = 60. #seconds
bint_thresh = 8e9
totint_thresh = 2e11
color_scale_limits = (0.65, 1.0)


pkl_name = 'fills_and_bmodes.pkl'
with open(pkl_name, 'rb') as fid:
    dict_fill_bmodes = pickle.load(fid)


if len(sys.argv)>1:
    print('--> Processing fill {:s}'.format(sys.argv[1]))
    filln = int(sys.argv[1])
    print((sys.argv))

    if np.any([('--cmap' in s) for s in sys.argv]):
        i_arg = np.where([('--cmap' in s) for s in sys.argv])[0][0]
        v_arg = sys.argv[i_arg]
        cmap = str(v_arg.split('=')[-1])

    if np.any([('--clim' in s) for s in sys.argv]):
        i_arg = np.where([('--clim' in s) for s in sys.argv])[0][0]
        v_arg = sys.argv[i_arg]
        clim = v_arg.split('=')[-1]
        color_scale_limits = list(map(float, clim.split(',')))

    if np.any([('--ylim' in s) for s in sys.argv]):
        i_arg = np.where([('--ylim' in s) for s in sys.argv])[0][0]
        v_arg = sys.argv[i_arg]
        ylim = v_arg.split('=')[-1]
        ylim = list(map(float, ylim.split(',')))

    # if '--injection' in sys.argv:
    #     print 'Scans in the INJPHYS-PRERAMP beam modes'
    #     t_start_INJPHYS = dict_fill_bmodes[filln]['t_start_INJPHYS']
    #     t_start_RAMP = dict_fill_bmodes[filln]['t_start_RAMP']
    #     list_scan_times = np.linspace((t_start_INJPHYS-t_ref)/3600., (t_start_RAMP-t_ref)/3600., n_traces)

    # if '--highenergy' in sys.argv:
    #     print 'Scans in the FLATTOP-STABLE beam modes'
    #     t_start_FLATTOP = dict_fill_bmodes[filln]['t_start_FLATTOP']
    #     t_start_STABLE = dict_fill_bmodes[filln]['t_start_STABLE']
    #     list_scan_times = np.linspace((t_start_FLATTOP-t_ref)/3600., (t_start_STABLE-t_ref)/3600.+0.5, n_traces)

    # if '--stablebeams' in sys.argv:
    #     print 'Scans in the STABLE BEAMS'
    #     t_start_STABLE = dict_fill_bmodes[filln]['t_start_STABLE']
    #     t_end_STABLE = dict_fill_bmodes[filln]['t_stop_STABLE']
    #     list_scan_times = np.linspace((t_start_STABLE-t_ref)/3600., (t_end_STABLE-t_ref)/3600.+0.5, n_traces)

else:
    filln = max(dict_fill_bmodes.keys())
    print('--> Processing latest fill: %d'%filln)


t_ref = dict_fill_bmodes[filln]['t_startfill']
tref_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))

fill_dict = {}
fill_dict.update(tm.parse_timber_file('fill_bunchbybunch_data_csvs/bunchbybunch_data_fill_%d.csv'%filln, verbose=False))


i_fig = 0
plt.close('all')
# Loop over beams
beam_col = ['b','r']
for beam in [1, 2]:
    print('\nPreparing plot beam %d...' %beam)

    fbct = FBCT.FBCT(fill_dict, beam=beam)
    fbct_t_all, fbct_v_all = fbct.uniform_time()
    nslots = fbct_v_all.shape[1]

    # Remove time without beam
    mask_beam_presence = np.float_(fbct.totint > totint_thresh)

    # Identify fills within file
    i_start_fills = np.where(np.diff(mask_beam_presence) == 1)[0]
    i_stop_fills = np.where(np.diff(mask_beam_presence) == -1)[0] + 1
    n_fills = len(i_start_fills)

    # Loop over fills
    for fill_curr in range(n_fills):
        i_fig += 1
        i_start_fill = i_start_fills[fill_curr]
        if len(i_stop_fills) == 0:
            i_stop_fill = -1
        else:
            try:
                i_stop_fill = i_stop_fills[fill_curr]
            except IndexError as idxErr:
                print(idxErr)
                i_stop_fill = -1
        fbct_v = fbct_v_all[i_start_fill:i_stop_fill,:]
        fbct_t = fbct_t_all[i_start_fill:i_stop_fill]

        # Get bunches
        mask_bunches = np.ma.masked_greater(fbct_v, bint_thresh).mask
        list_nbunches = np.sum(mask_bunches, axis=1)
        i_bunches = np.where(list_nbunches > 0)
        nbunches = np.max(list_nbunches)
        i_nbunches = np.max(np.argmax(list_nbunches))
        is_bunch = mask_bunches[i_nbunches,:]

        # Normalize
        fbct_norm = np.copy(fbct_v)
        for i in range(nslots):
            if is_bunch[i]:
                fbct_norm[:,i] /= max(fbct_norm[:,i])
            else:
                fbct_norm[:,i] = 0

        # Get injections
        i_inj = []
        for i in range(nslots):
            cnt = 0
            while cnt < len(fbct_t) and fbct_v[cnt,i] == 0:
                cnt += 1
            i_inj.append(cnt)
        # Roll to injections
        for i in range(nslots):
            # fbct_v[:,i] = np.roll(fbct_v[:,i], -i_inj[i])
            fbct_norm[:,i] = np.roll(fbct_norm[:,i], -i_inj[i])

        # Colormap and normalisations
        xx, yy = np.meshgrid((fbct_t - fbct_t[0])/3600., np.arange(fbct_v.shape[1]))
        zz = np.ma.masked_array(fbct_norm, mask = fbct_norm==0)[1:]

        # Filling scheme
        ms.mystyle()
        fig1 = plt.figure(i_fig, figsize=(16, 7), tight_layout=False)
        fig1.patch.set_facecolor('w')
        ax1 = plt.subplot(111)


        norm = mlc.Normalize(*color_scale_limits)

        pl1 = ax1.pcolormesh(yy, xx, zz.T, cmap=cmap, edgecolors='face', norm=norm)
        ax1.set_ylabel('Time after injection [h]')
        ax1.set_xlabel('25 ns slot')
        ax1.set_xlim((0, 3500))
        # ax1.set_ylim((0, 1.1*np.amax(xx)))
        if ylim:
            ax1.set_ylim(ylim)
        bcol = beam_col[beam-1]
        ax1.text(0.975, 0.9, nbunches, transform=ax1.transAxes,
                 horizontalalignment='right', verticalalignment='top',
                 fontsize=32, color=bcol, fontweight='bold', alpha=.5,
                 bbox=dict(boxstyle='round, pad=.5', facecolor='w', edgecolor=bcol))

        from mpl_toolkits.axes_grid.inset_locator import inset_axes
        axins1 = inset_axes(ax1, width="100%", height="5%", loc=9)
        locator = axins1.get_axes_locator()
        locator.set_bbox_to_anchor((0, 0, 1, 0.92), ax1.transAxes)
        locator.borderpad = -4

        cbar = plt.gcf().colorbar(pl1, cax=axins1, format='%.2g', orientation='horizontal')
        cbar.set_ticks(list(np.arange(0.5, 1.1, 0.05)))
        cbar.ax.tick_params(labelsize=16)
        cbar.ax.get_xaxis().labelpad = -60 #-72
        cbar.ax.set_xlabel('Intensity normalized to intensity at injection', fontsize=16)

        plt.subplots_adjust(top=0.75, bottom=0.15, right=0.95,
                            left=0.1, hspace=0.2, wspace=0.3)
        if n_fills > 1:
            subfill_str = string.ascii_lowercase[fill_curr]
            fig1.suptitle('Fill %d: B%d, subfill %s, started on %s'%(filln, beam, subfill_str, tref_string), fontsize=20)
        else:
            fig1.suptitle('Fill %d: B%d, started on %s'%(filln, beam, tref_string), fontsize=20)

plt.show()


