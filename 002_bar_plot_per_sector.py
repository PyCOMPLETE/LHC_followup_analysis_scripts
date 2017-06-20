import sys, time, os
sys.path.append("../")

import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.SetOfHomogeneousVariables as shv
import LHCMeasurementTools.LHC_Heatloads as hl
import LHCMeasurementTools.mystyle as ms

from data_folders import data_folder_list

import GasFlowHLCalculator.qbs_fill as qf

import argparse
import pickle
import numpy as np
import pylab as plt

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Save plots on disk.', action='store_true')
parser.add_argument('--fromcsv', help='Load heatloads from csvs. By default, use recalculated.', action='store_true')
parser.add_argument('--t', help='Time at which you plot the heat loads in hours.', type=float)
parser.add_argument('--min-hl-scale', help='Minimum of plot.', type=float)
parser.add_argument('--max-hl-scale', help='Maximum of plot.', type=float)
parser.add_argument('--t-offset', help='Time within the fill which sets heat loads to 0 in hours.', type=float)
parser.add_argument('--no-plot-model', help='Plot imp. SR contribution to heat loads.', action='store_true')
parser.add_argument('--tag', help='Tag of plot windows.', default='')
parser.add_argument('-v', help='Verbose.', action='store_true')
parser.add_argument('--legend', help='Plot a legend for Imp/SR', action='store_true')

parser.add_argument('--filln',type=int, default=None)

args = parser.parse_args()
from_csv = args.fromcsv

filln = 5029
t1 = 0.2#2.65
min_hl_scale = -5
max_hl_scale = 250
t_offset = None
plot_model = True

filln = 5386
t1 = 2.
min_hl_scale = -10
max_hl_scale = 80
t_offset = None
plot_model = True
tagfname = ''

#~ filln = 4511
#~ t1 = 6.5
#~ min_hl_scale = -10
#~ max_hl_scale = 80
#~ t_offset = 2.5
#~ plot_model = True
#~ tagfname = '100ns_high_energy'

#~ filln = 4246
#~ t1 = 4
#~ min_hl_scale = -10
#~ max_hl_scale = 80
#~ t_offset = 1.6
#~ plot_model = True
#~ tagfname = '50ns_high_energy'

#~ filln = 4246
#~ t1 = 4
#~ min_hl_scale = -5
#~ max_hl_scale = 10
#~ t_offset = 1.6
#~ plot_model = True
#~ tagfname = '50ns_high_energy_zoom'

#~ filln = 4525
#~ t1 = 5.
#~ min_hl_scale = -10
#~ max_hl_scale = 80
#~ t_offset = 1.25
#~ plot_model = True
#~ tagfname = '8b4e_high_energy'

#~ filln = 5386
#~ t1 = 2.2
#~ min_hl_scale = -10
#~ max_hl_scale = 80
#~ t_offset = 0.7
#~ plot_model = True
#~ tagfname = '25ns600b_high_energy'

#~ filln = 5219
#~ t1 = 1.8
#~ min_hl_scale = -10
#~ max_hl_scale = 250
#~ t_offset = 0.15
#~ plot_model = True
#~ tagfname = '25ns2040b_high_energy'

#~ filln = 5393
#~ t1 = 2.2
#~ min_hl_scale = -10
#~ max_hl_scale = 250
#~ t_offset = .8
#~ plot_model = True
#~ tagfname = '25ns2200b_high_energy'

#~ filln = 4565
#~ t1 = 3.5
#~ min_hl_scale = -10
#~ max_hl_scale = 250
#~ t_offset = 1.
#~ plot_model = True
#~ tagfname = '25ns2244b_high_energy'

if args.filln:
    filln = args.filln

if args.t:
    t1 = args.t

if args.min_hl_scale:
    min_hl_scale = args.min_hl_scale

if args.max_hl_scale:
    max_hl_scale = args.max_hl_scale

if args.t_offset:
    t_offset = args.t_offset

if args.tag:
    tagfname = args.tag

plot_model = not args.no_plot_model

if from_csv:
    fill_file = 'fill_heatload_data_csvs/hl_all_cells_fill_%d.csv'%filln
    hid = tm.parse_timber_file(fill_file, verbose=args.v)
else:
    hid = qf.get_fill_dict(filln)


varlist = hl.arcs_varnames_static

hid_set = shv.SetOfHomogeneousNumericVariables(varlist, hid)

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

t_fill_st = dict_fill_bmodes[filln]['t_startfill']
t_fill_end = dict_fill_bmodes[filln]['t_endfill']
t_ref=t_fill_st
tref_string=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))


# to plot impedance and synchrotron radiation
if plot_model:

    from LHCMeasurementTools.LHC_FBCT import FBCT
    from LHCMeasurementTools.LHC_BCT import BCT
    from LHCMeasurementTools.LHC_BQM import blength

    import HeatLoadCalculators.impedance_heatload as ihl
    import HeatLoadCalculators.synchrotron_radiation_heatload as srhl
    import HeatLoadCalculators.FillCalculator as fc

    fill_dict = {}
    if os.path.isdir(data_folder_fill+'/fill_basic_data_csvs'):
        # 2016 structure
        fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_basic_data_csvs/basic_data_fill_%d.csv'%filln, verbose=args.v))
        fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_bunchbybunch_data_csvs/bunchbybunch_data_fill_%d.csv'%filln, verbose=args.v))
    else:
        # 2015 structure
        fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_csvs/fill_%d.csv'%filln, verbose=args.v))

    fbct_bx = {}
    bct_bx = {}
    blength_bx = {}
    for beam_n in [1,2]:
        fbct_bx[beam_n] = FBCT(fill_dict, beam = beam_n)
        bct_bx[beam_n] = BCT(fill_dict, beam = beam_n)
        blength_bx[beam_n] = blength(fill_dict, beam = beam_n)

    hli_calculator  = ihl.HeatLoadCalculatorImpedanceLHCArc()
    hlsr_calculator  = srhl.HeatLoadCalculatorSynchrotronRadiationLHCArc()

    hl_imped_fill = fc.HeatLoad_calculated_fill(fill_dict, hli_calculator, bct_dict=bct_bx, fbct_dict=fbct_bx, blength_dict=blength_bx)
    hl_sr_fill = fc.HeatLoad_calculated_fill(fill_dict, hlsr_calculator, bct_dict=bct_bx, fbct_dict=fbct_bx, blength_dict=blength_bx)

    hl_imped_t1 = hl.magnet_length['AVG_ARC'][0]*np.interp(t1, (hl_imped_fill.t_stamps-t_ref)/3600,  hl_imped_fill.heat_load_calculated_total)
    hl_sr_t1 = hl.magnet_length['AVG_ARC'][0]*np.interp(t1, (hl_imped_fill.t_stamps-t_ref)/3600,  hl_sr_fill.heat_load_calculated_total)





plt.close('all')
ms.mystyle_arial(fontsz=12,dist_tick_lab=3)
width = 0.6
show_labels = True

sectors = hl.sector_list()

def swap_even_odd(vect):
    temp_list = []
    for ii in xrange(len(vect)//2):
        temp_list.append(vect[2*ii+1])
        temp_list.append(vect[2*ii])
    return np.array(temp_list)

	
        

for i, s in enumerate(sectors[:]):

    sect_str = str(s)
    R_part = 'R'+sect_str[0]
    L_part = 'L'+sect_str[1]

    # Find values at t1 and t2 for each cell.
    val1 = []
    cells = []
    for cell in hid.keys():
        if '_D2' in cell or '_D3' in cell or '_D4' in cell or '_Q1' in cell:
            continue
        if R_part not in cell and L_part not in cell:
            continue
        try:
            ind1 = np.argmin(np.abs((np.array(hid[cell].t_stamps) - t_ref)/3600 - t1))
        except ValueError as e:
            print('Got Error %s, skipping cell %s' % (e, cell))
            continue
        cellname = cell.split('_')[1]+'_'+cell.split('.POSST')[0][-1]
        if int(cellname[:2])<11: continue # skip LSS and DS

        if cellname=='11L1_3': print cell, cellname
        cells.append(cellname)


        # remove offset
        if t_offset is not None:
            ind_offset = np.argmin(np.abs((np.array(hid[cell].t_stamps) - t_ref)/3600 - t_offset))
            val_offset = float(hid[cell].values[ind_offset])
            offset_info = ', no beam at %.2fh'%t_offset
        else:
            val_offset = 0.
            offset_info = ''

        val1.append(float(hid[cell].values[ind1]) - val_offset)

    val1 = np.array(val1)
    cells = np.array(cells)

    # Sort everything
    # it's R(IP) 09, 10, 11, ... L(IP+1) 33, 32, ...
    msk_l = (np.char.find(cells, 'L') > -1)
    cells_lip = cells[msk_l]
    cells_rip = cells[~msk_l]

    #~ print val1.shape
    #~ print msk_l.shape
    val1_lip = val1[msk_l]
    val1_rip = val1[~msk_l]

    ind_sort = (np.argsort(cells_lip))[::-1]
    cells_lip = cells_lip[ind_sort]
    val1_lip = val1_lip[ind_sort]
    ind_sort = swap_even_odd(np.argsort(cells_rip))
    cells_rip = cells_rip[ind_sort]
    val1_rip = val1_rip[ind_sort]
    
    # swap 3 and 7 to recover the right order


    
    cells = np.append(cells_rip, cells_lip)
    val1 = np.append(val1_rip, val1_lip)


    #single sector plot
    fig_sect = plt.figure(1000+i, figsize=(12,4.5), tight_layout=False)
    fig_sect.patch.set_facecolor('w')
    ax1_sect = fig_sect.add_subplot(111)

    if plot_model:
        if args.legend:
            label1, label2 = 'Imp', 'SR'
        else:
            label1, label2 = None, None
        ax1_sect.axhspan(ymin=0, ymax=hl_imped_t1, color='grey', alpha=0.5, label=label1)
        ax1_sect.axhspan(ymin=hl_imped_t1, ymax=hl_imped_t1+hl_sr_t1, color='green', alpha=0.5, label=label2)
        if args.legend:
            ax1_sect.legend(bbox_to_anchor=(1,1), loc='upper left')




    ind = np.arange(len(cells))
    bar = ax1_sect.bar(ind, val1, width, color='b', label='%.1f h after start of fill'%t1, alpha=0.5)


    ax1_sect.set_ylabel('Heatload [W/hc]')
    ax1_sect.set_ylim(min_hl_scale, max_hl_scale)
    #ax1_sect.legend(loc='upper right')
    ax1_sect.set_xticks(ind+width)
    #~ ax1_sect.xaxis.set_major_formatter(plt.NullFormatter())
    if show_labels:
        ax1_sect.set_xticklabels(cells, rotation=90)
    #~ plt.setp(ax1_sect.get_xticklabels(), visible=False)
    ax1_sect.set_xlim(ind[0]-2*width, ind[-1]+4*width)

    if show_labels:
        fig_sect.subplots_adjust(left=.06, right=.96, top=0.83, hspace=0.15, bottom=0.19)
    else:
        fig_sect.subplots_adjust(left=.06, right=.96, top=0.83, hspace=0.15, bottom=0.05)
    fig_sect.suptitle('Fill. %d started on %s\n(t=%.2fh, %s%s)\nSector %d, %d cells, %s'%(filln, tref_string,
                        t1, tagfname, offset_info, s, len(cells), {False:'recalc. values', True:'DB values'}[from_csv]))
    #plt.subplots_adjust(top=.83, left=.05)
    plt.grid('on')

    if args.o:
        plt.savefig('cell_by_cell_plots/cellbycell_fill%d_t%.2fh_%s_sector%d.png'%(filln, t1, tagfname, s), dpi=200)

plt.show()
