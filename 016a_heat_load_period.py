
import time
import locale
import pylab as pl
from scipy.integrate import cumtrapz
import numpy as np
import LHCMeasurementTools.mystyle as ms
import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.TimestampHelpers as TH
import LHCMeasurementTools.LHC_BCT as BCT
import LHCMeasurementTools.LHC_Heatloads as HL
import LHCMeasurementTools.LHC_Energy as Energy
from LHCMeasurementTools.SetOfHomogeneousVariables import SetOfHomogeneousNumericVariables
from LHCMeasurementTools.LHC_Fills import Fills_Info
import argparse
import pickle
from data_folders import data_folder_list, recalc_h5_folder

from collections import OrderedDict


try:
    locale.setlocale(locale.LC_TIME, 'en_US')
except Exception as err:
    print('\nDid not manage to set locale. Got:')
    print(err)

empty_fills = [3888, 4032, 4055]
device_blacklist = [
#'QRLAA_33L5_QBS947_D3.POSST',
#'QRLAA_33L5_QBS947_D4.POSST',
]


# Specify plot settings
ax_norm_hl_ylim = 4e-13 #None#1e-14
int_cut_norm = 4e13
# defaults, can be overriden by args:
t_start_plot = '15-05-2017,08:00' ##
t_end_plot = '17-05-2017,08:00' ##


#Parse Args
parser = argparse.ArgumentParser()
parser.add_argument('--tstart', help='Format dd-mm-yyyy,hh:mm', default=t_start_plot)
parser.add_argument('--tend', help='Format dd-mm-yyyy,hh:mm', default=t_end_plot)
parser.add_argument('--notagfills', help='Do not show tags for fills.', action='store_true')
parser.add_argument('--noplotall', help='Do not plot all heat loads', action='store_true')
parser.add_argument('--noplotaverage', help='Do not plot average heat loads', action='store_true')
parser.add_argument('--varlists', help='Variable lists to plot. Choose from %s' % sorted(HL.heat_loads_plot_sets.keys()), nargs='+', default=['AVG_ARC'])
parser.add_argument('--plot-model', help='Plot model heat loads.', action='store_true')
parser.add_argument('--screen', help='Screen mode', choices=('small', 'CCC'), default='CCC')
parser.add_argument('--mode', help='What to plot in 3rd subplot.', choices=('norm_to_intensity', 'integrated'), default='norm_to_intensity')
parser.add_argument('--normlength', help='Normalization to length of', choices=('None', 'magnet', 'cryostat'), default='magnet')
parser.add_argument('--timein', help='ylabel of plots', choices=('datetime', 'h', 'd', 'hourtime'), default='datetime')
parser.add_argument('--hourtickspac', help='y tick spacing, specify "week" or a float', default='24')
parser.add_argument('--zeroat', help='Heat load offset at')
parser.add_argument('--use-recalc', help='Use recalculated heat loads.', action='store_true')
args = parser.parse_args()

t_start_plot = args.tstart
t_end_plot = args.tend

flag_filln = not args.notagfills
plot_all = not args.noplotall
plot_average = not args.noplotaverage
name_varlists_to_combine = args.varlists
plot_model = args.plot_model
mode = args.mode
zero_at = args.zeroat

if args.use_recalc:
    import GasFlowHLCalculator.qbs_fill as qf
    from GasFlowHLCalculator.h5_storage import H5_storage

normalization_to_length_of = args.normlength
if 'None' in normalization_to_length_of or 'none' in normalization_to_length_of:
    normalization_to_length_of = None
time_in = args.timein

screen_mode = args.screen
if screen_mode == 'small':
    fontsz = 14
    fontsz_leg = 14
    figsz = (6.4*1.9, 4.8*1.5)
elif screen_mode == 'CCC':
    fontsz = 14
    fontsz_leg = 14
    figsz = (6.4*1.9, 4.8*1.5)

t_plot_tick_h = args.hourtickspac
if t_plot_tick_h != 'week':
    t_plot_tick_h = float(t_plot_tick_h)

# End of parse args

hl_varlist = []
for name_varlist in name_varlists_to_combine:
    hl_varlist += HL.heat_loads_plot_sets[name_varlist]

for varname in hl_varlist:
    if varname in device_blacklist:
        hl_varlist.remove(varname)


# get magnet lengths for normalization_to_length_of
if normalization_to_length_of == 'magnet':
    norm_length_dict = HL.get_dict_magnet_lengths()
if normalization_to_length_of == 'cryostat':
    norm_length_dict = HL.get_dict_cryostat_lengths()

t_start_unix =  time.mktime(time.strptime(t_start_plot, '%d-%m-%Y,%H:%M'))
t_end_unix =  time.mktime(time.strptime(t_end_plot, '%d-%m-%Y,%H:%M'))
t_ref_unix = t_start_unix
tref_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref_unix))

time_conv = TH.TimeConverter(time_in, t_ref_unix, t_plot_tick_h=t_plot_tick_h)
tc = time_conv.from_unix



# merge pickles and add info on location
dict_fill_bmodes={}
for df in data_folder_list:
    with open(df+'/fills_and_bmodes.pkl', 'rb') as fid:
        this_dict_fill_bmodes = pickle.load(fid)
        for kk in this_dict_fill_bmodes:
            this_dict_fill_bmodes[kk]['data_folder'] = df
        dict_fill_bmodes.update(this_dict_fill_bmodes)

fill_info = Fills_Info(dict_fill_bmodes)
fill_list = fill_info.fills_in_time_window(t_start_unix, t_end_unix)

# find offset to remove
if zero_at is not None:
    print('Evaluating offsets')
    if ':' in zero_at:
        t_zero_unix = time.mktime(time.strptime(zero_at, '%d-%m-%Y,%H:%M'))
    else:
        t_zero_unix  = t_ref_unix + float(zero_at)*3600.
    filln_offset = fill_info.filln_at_time(t_zero_unix)

    data_folder_fill = dict_fill_bmodes[filln_offset]['data_folder']

    try:
        fill_dict = tm.timber_variables_from_h5(data_folder_fill+'/heatloads_fill_h5s/heatloads_all_fill_%d.h5'%filln_offset)
        print('From h5!')
    except IOError:
        print("h5 file not found, using h5s :-P")
        fill_dict = {}
        fill_dict.update(tm.CalsVariables_from_h5(
            data_folder_fill + ('/fill_basic_data_h5s/'
                'basic_data_fill_%d.h5'%filln_offset)))
        fill_dict.update(tm.CalsVariables_from_h5(
            data_folder_fill + ('/fill_heatload_data_h5s/'
                'heatloads_fill_%d.h5'%filln_offset)))

    if args.use_recalc:
        fill_dict.update(qf.get_fill_dict(filln_offset,
             h5_storage=H5_storage(recalc_h5_folder),
             use_dP=True))


    dict_offsets={}
    for kk in hl_varlist:
        dict_offsets[kk] = np.interp(t_zero_unix, np.float_(np.array(fill_dict[kk].t_stamps)), fill_dict[kk].float_values())


pl.close('all')
ms.mystyle_arial(fontsz=fontsz, dist_tick_lab=9)
fig = pl.figure(1, figsize=figsz)
fig.patch.set_facecolor('w')
ax1 = fig.add_subplot(311)
ax11 = ax1.twinx()
ax2 = fig.add_subplot(312, sharex=ax1)
ax3 = fig.add_subplot(313, sharex=ax1)
ms.sciy()

N_fills = len(fill_list)

t_for_integrated = []
hl_for_integrated = []

first_fill = True

for i_fill, filln in enumerate(fill_list):

    print('Fill %d, %d/%d'%(filln, i_fill+1, N_fills))
    if filln in empty_fills:
        print('Fill blacklisted!')
        continue

    t_startfill = fill_info.dict_fill_bmodes[filln]['t_startfill']
    t_endfill = fill_info.dict_fill_bmodes[filln]['t_endfill']

    data_folder_fill = dict_fill_bmodes[filln]['data_folder']

    try:
        fill_dict = tm.timber_variables_from_h5(data_folder_fill+'/heatloads_fill_h5s/heatloads_all_fill_%d.h5'%filln)
        print('From h5!')
    except IOError:
        print("h5 file not found, using h5s :-P")
        fill_dict = {}
        fill_dict.update(tm.CalsVariables_from_h5(
            data_folder_fill + ('/fill_basic_data_h5s/'
                'basic_data_fill_%d.h5'%filln)))
        fill_dict.update(tm.CalsVariables_from_h5(data_folder_fill +
            '/fill_heatload_data_h5s/heatloads_fill_%d.h5'%filln))
    except Exception as err:
        print('Skipped! Got:')
        print(err)
        continue

    if args.use_recalc:
        try:
            fill_dict.update(qf.get_fill_dict(filln,
                h5_storage=H5_storage(recalc_h5_folder),
                use_dP=True))
        except ValueError:
            'Skipped due to ValueError'

    if plot_model:
        try:
            fill_dict.update(tm.timber_variables_from_h5(data_folder_fill+'/heatloads_fill_h5s/imp_and_SR_fill_%i.h5' % filln))
        except IOError:
            print("model datafile not found")


    bct_b1 = BCT.BCT(fill_dict, beam=1)
    bct_b2 = BCT.BCT(fill_dict, beam=2)
    energy = Energy.energy(fill_dict, beam=1, t_start_fill=t_startfill, t_end_fill=t_endfill)
    ax1.plot(tc(bct_b1.t_stamps), bct_b1.values*1e-14, lw=2, c='b', label = 'Intensity B1' if i_fill==0 else "")
    ax1.plot(tc(bct_b2.t_stamps), bct_b2.values*1e-14, lw=2, c='r', label = 'Intensity B2' if i_fill==0 else "")
    ax11.plot(tc(energy.t_stamps), energy.energy/1e3, c='black', lw=1.5, alpha=0.2,label='Energy' if i_fill==0 else "") #was alpha=.5

    heatloads = SetOfHomogeneousNumericVariables(variable_list=hl_varlist, timber_variables=fill_dict)


    # remove offset
    if zero_at is not None:
        for device in hl_varlist:
            heatloads.timber_variables[device].values = heatloads.timber_variables[device].values - dict_offsets[device]

    # normalize to the length
    if normalization_to_length_of is not None:
        for device in hl_varlist:
            heatloads.timber_variables[device].values = heatloads.timber_variables[device].values/norm_length_dict[device]
    if plot_all:
        for ii, kk in enumerate(heatloads.variable_list):

            #if '13L5' in kk and ('D2' in kk or 'D3' in kk):
            #    continue
            colorcurr = ms.colorprog(i_prog=ii, Nplots=len(heatloads.variable_list))

            kwplt = {}
            # # Enhance S12
            # if 'S12' in kk:
            #     kwplt = {'zorder':10}
            #     colorcurr = tk'


            # Labels
            if first_fill:
                label = ''
                for st in kk.split('.POSST')[0].split('_'):
                    if 'QRL' in st or 'QBS' in st or 'AVG' in st or 'ARC' in st:
                        pass
                    else:
                        label += st + ' '
                label = label[:-1]
            else:
                label = None

            ax2.plot(tc(heatloads.timber_variables[kk].t_stamps), heatloads.timber_variables[kk].values,
                       '-', color=colorcurr, lw=2., label=label, **kwplt)

            if mode == 'norm_to_intensity':
                t_curr = heatloads.timber_variables[kk].t_stamps
                hl_curr = heatloads.timber_variables[kk].values
                bct1_int = np.interp(t_curr, bct_b1.t_stamps, bct_b1.values)
                bct2_int = np.interp(t_curr, bct_b2.t_stamps, bct_b2.values)
                hl_norm = hl_curr/(bct1_int+bct2_int)
                hl_norm[(bct1_int+bct2_int)<int_cut_norm] = 0.
                ax3.plot(tc(t_curr), hl_norm,'-', color=colorcurr, lw=2., **kwplt)


    if plot_model and 'AVG_ARC' in name_varlists_to_combine:
        try:
            heatloads_model = SetOfHomogeneousNumericVariables(variable_list=['imp_arc_wm', 'sr_arc_wm'], timber_variables=fill_dict)
            model_time = heatloads_model.timber_variables['imp_arc_wm'].t_stamps
            model_hl = heatloads_model.timber_variables['sr_arc_wm'].values + heatloads_model.timber_variables['imp_arc_wm'].values
            model_hl *= 53.45

            if normalization_to_length_of is not None:
                model_hl = model_hl/norm_length_dict[device]

        except Exception as err:
            print('Cannot plot model heat loads because')
            print(err)
        else:
            if first_fill:
                label='Imp.+SR'
            else:
                label=None
            ax2.plot(tc(model_time), model_hl, '--', color='grey', lw=2., label=label)
    if plot_average or mode == 'integrated':
        hl_ts, hl_aver = heatloads.mean()

    if plot_average:
        ax2.plot(tc(hl_ts), hl_aver,'k-', lw=2.)

    if mode == 'integrated':
        t_for_integrated += list(hl_ts)
        hl_for_integrated += list(hl_aver)

    if flag_filln and t_startfill>t_start_unix-15*60:
        # Fill number labeling
        fds = tc(t_startfill)
        trans = ax1.get_xaxis_transform()
        ax1.axvline(fds, c='grey', ls='dashed', lw=2, alpha=0.4)
        ax2.axvline(fds, c='grey', ls='dashed', lw=2, alpha=0.4)
        ax3.axvline(fds, c='grey', ls='dashed', lw=2, alpha=0.4)
        try:x_fn = fds[0] #in case we are using the date
        except IndexError: x_fn = fds
        ax1.annotate('%d'%filln, xy=(x_fn, 1.01), xycoords=trans,
                            horizontalalignment='left', verticalalignment='bottom',
                            rotation=67.5, color='grey', alpha=0.8)


    first_fill = False


ax1.set_xlim(tc(t_start_unix), tc(t_end_unix))
ax11.set_ylim(0, 7)
ax1.set_ylim(0, None)
ax1.grid('on')
ax1.set_ylabel('Total intensity\n[10$^{14}$ p$^+$]')
ax11.set_ylabel('Energy [TeV]')
time_conv.set_x_for_plot(fig, ax1)


ms.comb_legend(ax1,ax11, bbox_to_anchor=(1.1, 1.05),  loc='upper left', prop={'size':fontsz_leg})

if normalization_to_length_of is None:
    ax2.set_ylabel('Heat load\n[W]')
else:
    ax2.set_ylabel('Heat load\n[W/m]')
ax2.legend(bbox_to_anchor=(1.1, 1.05),  loc='upper left', prop={'size':fontsz_leg})#, frameon=False)
#ax2.set_ylim(0, None)
ax2.grid('on')

if mode == 'integrated':
    hl_for_integrated = np.array(hl_for_integrated)
    hl_for_integrated[hl_for_integrated<0.] = 0.
    t_for_integrated = np.array(t_for_integrated)
    hl_for_integrated[t_for_integrated < t_start_unix] = 0.
    integrated_hl = cumtrapz(hl_for_integrated, t_for_integrated)
    ax3.plot(tc(t_for_integrated[:-1]), integrated_hl,'b-', lw=2.)
    if normalization_to_length_of is None:
        ax3.set_ylabel('Integrated heat load\n[J]')
    else:
        ax3.set_ylabel('Integrated heat load\n[J/m]')
elif mode == 'norm_to_intensity':
    if normalization_to_length_of is None:
        ax3.set_ylabel('Normalized heat load\n[W/p+]')
    else:
        ax3.set_ylabel('Normalized heat load\n[W/m/p+]')
    try:
        ax3.set_ylim(0, ax_norm_hl_ylim)
    except NameError:
        ax3.set_ylim(0, None)
ax3.grid('on')


if time_in == 'd' or time_in == 'h':
    ax3.set_xlabel('Time [%s]' % time_in)

pl.suptitle('From ' + tref_string)
fig.subplots_adjust(left=.1, right=.76, hspace=.28, top=.89)
pl.savefig('plot.png', dpi=200)
pl.show()

axint = ax1
axene = ax11
axhl = ax2
axhl2 = ax3
