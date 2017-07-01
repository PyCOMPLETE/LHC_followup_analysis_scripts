import sys, os
import pickle
import time
import argparse

import pylab as pl
import numpy as np

import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.LHC_Energy as Energy
import LHCMeasurementTools.mystyle as ms
from LHCMeasurementTools.LHC_FBCT import FBCT
from LHCMeasurementTools.LHC_BCT import BCT
from LHCMeasurementTools.LHC_BQM import blength
import LHCMeasurementTools.LHC_Heatloads as HL
from LHCMeasurementTools.SetOfHomogeneousVariables import SetOfHomogeneousNumericVariables
import LHCMeasurementTools.savefig as sf

import HeatLoadCalculators.impedance_heatload as ihl
import HeatLoadCalculators.synchrotron_radiation_heatload as srhl
import HeatLoadCalculators.FillCalculator as fc

import GasFlowHLCalculator.qbs_fill as qf
from data_folders import data_folder_list

parser = argparse.ArgumentParser(description='Plot the heat loads for one LHC fill')
parser.add_argument('filln', metavar='FILLN', type=int, help='LHC fill number')
parser.add_argument('--varlists', help='Variable lists to plot. Choose from %s' % sorted(HL.heat_loads_plot_sets.keys()), nargs='+', default=['AVG_ARC'])
parser.add_argument('--zeroat', metavar='T_0', type=float, help='Calculate offset at this point', default=None)
parser.add_argument('--noblength', help='Do not show a plot with bunch length vs time.', action='store_true')
parser.add_argument('--noaverage', help='Do not show an average heat load.', action='store_true')
parser.add_argument('--fbct', help='Show fbct intensity, too!', action='store_true')
parser.add_argument('--noplotmodel', help='Do not plot the model heat load', action='store_true')
parser.add_argument('--savefig', help='Save figures in pdijksta dir', action='store_true')
parser.add_argument('--beam-events', help='Show when is begin of squeeze etc.', action = 'store_true')
parser.add_argument('--use-recalc', help='Recalculated heat loads from Gasflow.', action = 'store_true')
parser.add_argument('--normtointensity', help='Normalize to beam intensity', action='store_true')
parser.add_argument('--add-csv-to-fill-dict', nargs='+', default=[])
parser.add_argument('--full-varname-in-legend', help='Do not shorten varnames.', action='store_true')
parser.add_argument('--colormap', help='chose between hsv and rainbow', default='hsv')

parser.add_argument('--custom_vars', help='Custom list of variables to plot', nargs='+', default=[])

parser.add_argument('-v', help='Verbose parsing of timber files.', action = 'store_true')

#parser.add_argument('--time', metavar='TIME', type=str, nargs='*')

args = parser.parse_args()

filln = args.filln
t_zero = args.zeroat
flag_bunch_length = not args.noblength
flag_average = not args.noaverage
flag_fbct = args.fbct
plot_model = not args.noplotmodel
plot_t_arr = True
use_recalculated = args.use_recalc
group_names = args.varlists
normtointen = args.normtointensity
added_csvs = args.add_csv_to_fill_dict

int_cut_norm = 1e13

myfontsz = 14
pl.close('all')
ms.mystyle_arial(fontsz=myfontsz, dist_tick_lab=8)

blacklist = [
'QRLAA_33L5_QBS947_D4.POSST',
#~ 'QRLAA_13R4_QBS947_D2.POSST',
'QRLAA_33L5_QBS947_D3.POSST',
#'QRLEC_05L1_QBS947.POSST',
#'QRLEA_05L8_QBS947.POSST',
#'QRLEA_06L8_QBS947.POSST',
#'QRLEA_05R8_QBS947.POSST']
#'S78_QBS_AVG_ARC.POSST']
]

beams_list = [1,2]
first_correct_filln = 4474
arc_correction_factor_list = HL.arc_average_correction_factors()
colstr = {}
colstr[1] = 'b'
colstr[2] = 'r'

dict_hl_groups = HL.heat_loads_plot_sets

# handle custom list
if len(args.custom_vars)>0:
    group_names.append('Custom')
    dict_hl_groups['Custom'] = args.custom_vars
    


# merge pickles and add info on location
dict_fill_bmodes={}
for df in data_folder_list:
    with open(df+'/fills_and_bmodes.pkl', 'rb') as fid:
        this_dict_fill_bmodes = pickle.load(fid)
        for kk in this_dict_fill_bmodes:
            this_dict_fill_bmodes[kk]['data_folder'] = df
        dict_fill_bmodes.update(this_dict_fill_bmodes)


# get location of current data
data_folder_fill = dict_fill_bmodes[filln]['data_folder']


#load data
if os.path.isdir(data_folder_fill+'/fill_basic_data_csvs'):
    # 2016+ structure
    fill_dict = {}
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_basic_data_csvs/basic_data_fill_%d.csv'%filln, verbose=True))
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_bunchbybunch_data_csvs/bunchbybunch_data_fill_%d.csv'%filln, verbose=True))
    if use_recalculated:
        print 'Using recalc data'
        fill_dict.update(qf.get_fill_dict(filln))
    else:
        fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_heatload_data_csvs/heatloads_fill_%d.csv'%filln, verbose=False))
else:
    # 2015 structure
    fill_dict = {}
    fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_csvs/fill_%d.csv'%filln, verbose=True))

    if use_recalculated:
        print 'Using recalc data'
        # remove db values from dictionary (for 2015 cases)
        for kk in fill_dict.keys():
            if 'QBS' in kk and '.POSST'in kk:
                fill_dict[kk] = 'Not recalculated'
        fill_dict.update(qf.get_fill_dict(filln))
 
# Handle additional csvs 
for csv in added_csvs:
    fill_dict.update(tm.parse_timber_file(csv), verbose=True)


dict_beam = fill_dict
dict_fbct = fill_dict

energy = Energy.energy(fill_dict, beam=1)

t_fill_st = dict_fill_bmodes[filln]['t_startfill']
t_fill_end = dict_fill_bmodes[filln]['t_endfill']
t_fill_len = t_fill_end - t_fill_st
t_min = dict_fill_bmodes[filln]['t_startfill']-0*60.
t_max = dict_fill_bmodes[filln]['t_endfill']+0*60.

t_ref=t_fill_st
tref_string=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))

fbct_bx = {}
bct_bx = {}
blength_bx = {}

for beam_n in beams_list:
    fbct_bx[beam_n] = FBCT(fill_dict, beam = beam_n)
    bct_bx[beam_n] = BCT(fill_dict, beam = beam_n)
    if flag_bunch_length:
        blength_bx[beam_n] = blength(fill_dict, beam = beam_n)
    else:
        blength_bx = None


N_figures = len(group_names)
figs = []
sp1 = None




for ii, group_name in enumerate(group_names):
    fig_h = pl.figure(ii, figsize=(8*1.4, 6*1.4))
    figs.append(fig_h)
    fig_h.patch.set_facecolor('w')

    sptotint = pl.subplot(3,1,1, sharex=sp1)
    sp1 = sptotint
    #if flag_bunch_length:
    spavbl = pl.subplot(3,1,3, sharex=sp1)
    sphlcell = pl.subplot(3,1,2, sharex=sp1)
    spenergy = sptotint.twinx()

    spenergy.plot((energy.t_stamps-t_ref)/3600., energy.energy/1e3, c='black', lw=2., label='Energy')
    spenergy.set_ylabel('Energy [TeV]')
    spenergy.set_ylim(0,7)

    if args.beam_events:
            keys_labels = [('t_start_INJPHYS', 'Injection'),
                    ('t_start_RAMP',    'Ramp'),
                    ('t_start_FLATTOP', 'Flat top'),
                    ('t_start_SQUEEZE', 'Squeeze'),
                    ('t_start_ADJUST',  'Adjust'),
                    ('t_start_STABLE',  'Stable beams')
                    ]
            for ctr, (key, label) in enumerate(keys_labels):
                color = ms.colorprog(ctr, len(keys_labels)+1)
                tt = (dict_fill_bmodes[filln][key] - t_ref)/3600.
                spenergy.axvline(tt, ls='-', color=color, label=label)

    for beam_n in beams_list:

        if flag_fbct: sptotint.plot((fbct_bx[beam_n].t_stamps-t_ref)/3600., fbct_bx[beam_n].totint, '.--', color=colstr[beam_n])
        sptotint.plot((bct_bx[beam_n].t_stamps-t_ref)/3600., bct_bx[beam_n].values, '-', color=colstr[beam_n], lw=2., label='Intensity B%i' % beam_n)
        sptotint.set_ylabel('Total intensity [p+]')
        sptotint.grid('on')
        sptotint.set_ylim(0, None)

        if flag_bunch_length and not normtointen:
            spavbl.plot((blength_bx[beam_n].t_stamps-t_ref)/3600., blength_bx[beam_n].avblen/1e-9, '.-', color=colstr[beam_n])
            spavbl.set_ylabel('Bunch length [ns]')
            spavbl.set_ylim(0.8,1.8)
        spavbl.grid('on')
        spavbl.set_xlabel('Time [h]')

    ms.comb_legend(sptotint, spenergy, bbox_to_anchor=(1.1, 1),  loc='upper left', prop={'size':myfontsz})

    group_name = group_names[ii]
    if use_recalculated:
        string = 'Recalculated data'
    else:
        string = 'Logged data'
    pl.suptitle(' Fill. %d started on %s\n%s (%s)'%(filln, tref_string, group_name, string))
    fig_h.canvas.set_window_title(group_name)

    hl_var_names = dict_hl_groups[group_name][:]
    hl_var_names_copy = dict_hl_groups[group_name][:]
    for varname in hl_var_names_copy:
        if varname in blacklist:
            hl_var_names.remove(varname)

    heatloads = SetOfHomogeneousNumericVariables(variable_list=hl_var_names, timber_variables=fill_dict, skip_not_found=True)

    # CORRECT ARC AVERAGES
    if not use_recalculated and (group_name == 'Arcs' or group_name == 'AVG_ARC') and filln < first_correct_filln:
        hl_corr_factors = []
        for ii, varname in enumerate(dict_hl_groups[group_name]):
            if varname not in blacklist:
                hl_corr_factors.append(arc_correction_factor_list[ii])
        heatloads.correct_values(hl_corr_factors)

    if flag_average:
        hl_ts_curr, hl_aver_curr  = heatloads.mean()
    for ii, kk in enumerate(heatloads.variable_list):
        colorcurr = ms.colorprog(i_prog=ii, Nplots=len(heatloads.variable_list), cm=args.colormap)
        if t_zero is not None:
            offset = np.interp(t_ref+t_zero*3600, heatloads.timber_variables[kk].t_stamps, heatloads.timber_variables[kk].values)
        else:
            offset=0.

        if args.full_varname_in_legend:
            label = kk
        else:
            label = ''
            for st in kk.split('.POSST')[0].split('_'):
                if 'QRL' in st or 'QBS' in st or 'AVG' in st or 'ARC' in st:
                    pass
                else:
                    label += st + ' '
            label = label[:-1]

        sphlcell.plot((heatloads.timber_variables[kk].t_stamps-t_ref)/3600, heatloads.timber_variables[kk].values-offset,
            '-', color=colorcurr, lw=2., label=label)#.split('_QBS')[0])
            
        if normtointen:
            t_curr = heatloads.timber_variables[kk].t_stamps
            hl_curr = heatloads.timber_variables[kk].values
            bct1_int = np.interp(t_curr, bct_bx[1].t_stamps, bct_bx[1].values)
            bct2_int = np.interp(t_curr, bct_bx[2].t_stamps, bct_bx[2].values)
            hl_norm = (hl_curr-offset)/(bct1_int+bct2_int)
            hl_norm[(bct1_int+bct2_int)<int_cut_norm] = 0.
            spavbl.plot((t_curr-t_ref)/3600, hl_norm,'-', color=colorcurr, lw=2.)

    if plot_model and (group_name == 'Arcs' or group_name == 'AVG_ARC'):
        hli_calculator  = ihl.HeatLoadCalculatorImpedanceLHCArc()
        hlsr_calculator  = srhl.HeatLoadCalculatorSynchrotronRadiationLHCArc()

        hl_imped_fill = fc.HeatLoad_calculated_fill(fill_dict, hli_calculator, bct_dict=bct_bx, fbct_dict=fbct_bx, blength_dict=blength_bx)
        hl_sr_fill = fc.HeatLoad_calculated_fill(fill_dict, hlsr_calculator, bct_dict=bct_bx, fbct_dict=fbct_bx, blength_dict=blength_bx)
        label='Imp.+SR (recalc.)'
        sphlcell.plot((hl_imped_fill.t_stamps-t_ref)/3600,
            (hl_imped_fill.heat_load_calculated_total+hl_sr_fill.heat_load_calculated_total)*HL.magnet_length['AVG_ARC'][0],
            '--', color='grey', lw=2., label=label)

        #~ kk = 'LHC.QBS_CALCULATED_ARC.TOTAL'
        #~ label='Imp.+SR'
        #~ sphlcell.plot((hl_model.timber_variables[kk].t_stamps-t_ref)/3600., hl_model.timber_variables[kk].values,
            #~ '--', color='grey', lw=2., label=label)

    if flag_average:
        if t_zero is not None:
            offset = np.interp(t_ref+t_zero*3600, hl_ts_curr, hl_aver_curr)
        else:
            offset=0.
        sphlcell.plot((hl_ts_curr-t_ref)/3600., hl_aver_curr-offset, 'k', lw=2, label='Average')
    sphlcell.set_ylabel('Heat load [W]')

    #~ sphlcell.set_xlabel('Time [h]')
    sphlcell.legend(prop={'size':myfontsz}, bbox_to_anchor=(1.15, 1.0),  loc='upper left')
    sphlcell.grid('on')
    
    if normtointen:
         spavbl.set_ylabel('Normalized heat load [W/p+]')

    pl.subplots_adjust(right=0.65, wspace=0.35, hspace=.26)
    #~ fig_h.set_size_inches(15., 8.)

if args.savefig:
    sf.saveall_pdijksta()


pl.show()
