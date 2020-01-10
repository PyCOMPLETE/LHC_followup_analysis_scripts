import sys, time, os
sys.path.append("../")
sys.path.append("../LHC_fullRun2_analysis_scripts/")
import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.SetOfHomogeneousVariables as shv
import LHCMeasurementTools.LHC_Heatloads as hl
import LHCMeasurementTools.mystyle as ms
import scipy.stats as stats

from data_folders import data_folder_list, recalc_h5_folder

import GasFlowHLCalculator.qbs_fill as qf
from GasFlowHLCalculator.h5_storage import H5_storage

import cell_by_cell_plot_helpers as cch

import argparse
import pickle
import numpy as np
import pylab as plt



# defaults
t_offset_h = None
min_hl_scale = None
max_hl_scale = None
tagfname = ''


# parse arguments
parser = argparse.ArgumentParser(epilog='Example: 002b_bar_plot_per_sector_multiple_fills.py --at filln:5108!t_h:2.5!t_offs_h:0.05 filln:5108!t_h:3.5!t_offs_h:0.05')
parser.add_argument('-o', help='Save plots on disk.', action='store_true')
parser.add_argument('--savein', help='Specify folder to save the output', default='cell_by_cell_plots')
parser.add_argument('--fromcsv', help='Load heatloads from csvs. By default, use recalculated.', action='store_true')
parser.add_argument('--min-hl-scale', help='Minimum of plot.', type=float)
parser.add_argument('--max-hl-scale', help='Maximum of plot.', type=float)
parser.add_argument('--no-plot-model', help='Plot imp. SR contribution to heat loads.', action='store_true')
parser.add_argument('--tag', help='Tag of plot windows.', default='')
parser.add_argument('-v', help='Verbose.', action='store_true')
parser.add_argument('--legend', help='Plot a legend for Imp/SR', action='store_true')
parser.add_argument('--normtointensity', help='Normalize to beam intensity', action='store_true')
parser.add_argument('--first-cell', help='First cell to be plotted', type=float, default=11)
parser.add_argument('--minhist', help='Minimum in histogram scales', type=float)
parser.add_argument('--maxhist', help='Minimum in histogram scales', type=float)


parser.add_argument('--at', help="Snapshots in the form: filln:5108!t_h:2.5!t_offs_h:0.05 filln:5108!t_h:3.5!t_offs_h:0.05", nargs='+')




args = parser.parse_args()

if args.min_hl_scale:
    min_hl_scale = args.min_hl_scale
if args.max_hl_scale:
    max_hl_scale = args.max_hl_scale
if args.tag:
    tagfname = args.tag

plot_model = not args.no_plot_model

from_csv = args.fromcsv
normtointen = args.normtointensity


#histogram parameters
if not normtointen:
    minhist = -5
    maxhist = 300
    nbinhist = 20
    distr_bw = 10
else:
    minhist = -.2e-13
    maxhist = 300/6e14
    nbinhist = 20
    distr_bw = 10/6e14

if args.maxhist:
    maxhist = args.maxhist

if args.minhist:
    minhist = args.minhist

try:
    import locale
    locale.setlocale(locale.LC_TIME, 'en_US')
except Exception as err:
    print '\nDid not manage to set locale. Got:'
    print err



# build snapshots dicts
snapshots = []
for strin in args.at:
    dd = {}
    for ss in strin.split('!'):
        kk, value=ss.split(':')
        if kk=='filln':
            dd[kk] = int(value)
        elif kk=='t_h' or kk=='t_offs_h':
            dd[kk] = float(value)
        else:
            raise ValueError("Input not recognized\n"+strin)

    if 't_offs_h' not in dd.keys():
        dd['t_offs_h'] = None

    snapshots.append(dd)



# merge pickles and add info on location
dict_fill_bmodes={}
for df in data_folder_list:
    with open(df+'/fills_and_bmodes.pkl', 'rb') as fid:
        this_dict_fill_bmodes = pickle.load(fid)
        for kk in this_dict_fill_bmodes:
            this_dict_fill_bmodes[kk]['data_folder'] = df
        dict_fill_bmodes.update(this_dict_fill_bmodes)



N_snapshots = len(snapshots)

for i_snapshot in xrange(N_snapshots):

    filln = snapshots[i_snapshot]['filln']
    t_sample_h = snapshots[i_snapshot]['t_h']
    t_offset_h = snapshots[i_snapshot]['t_offs_h']

    if from_csv:
        fill_file = 'fill_heatload_data_csvs/hl_all_cells_fill_%d.csv'%filln
        hid = tm.parse_timber_file(fill_file, verbose=args.v)
    else:
        hid = qf.get_fill_dict(filln, h5_storage=H5_storage(recalc_h5_folder))

    # get location of current data
    data_folder_fill = dict_fill_bmodes[filln]['data_folder']
    t_fill_st = dict_fill_bmodes[filln]['t_startfill']
    t_fill_end = dict_fill_bmodes[filln]['t_endfill']
    t_ref=t_fill_st
    tref_string=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))
    tref_string_short=time.strftime("%d %b %Y %H:%M", time.localtime(t_ref))

    # extract standard fill data
    fill_dict = {}
    if os.path.isdir(data_folder_fill+'/fill_basic_data_csvs'):
        # 2016 structure
        fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_basic_data_csvs/basic_data_fill_%d.csv'%filln, verbose=args.v))
        fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_bunchbybunch_data_csvs/bunchbybunch_data_fill_%d.csv'%filln, verbose=args.v))
    else:
        # 2015 structure
        fill_dict.update(tm.parse_timber_file(data_folder_fill+'/fill_csvs/fill_%d.csv'%filln, verbose=args.v))

    #sample standard fill data at right moment
    intensity_b1, intensity_b2, bl_ave_b1, bl_ave_b2, n_bunches_b1, n_bunches_b2, energy_GeV, hl_imped_sample, hl_sr_sample = cch.extract_and_compute_extra_fill_data(fill_dict, t_ref, t_sample_h, thresh_bint=3e10)

    # extract heat load data
    dict_hl_cell_by_cell = cch.sample_and_sort_cell_by_cell(hid, t_ref=t_ref, t_sample_h=t_sample_h, t_offset_h=t_offset_h, first_cell=args.first_cell)

    snapshots[i_snapshot]['intensity_b1'] = intensity_b1
    snapshots[i_snapshot]['intensity_b2'] = intensity_b2
    snapshots[i_snapshot]['bl_ave_b1'] = bl_ave_b1
    snapshots[i_snapshot]['bl_ave_b2'] = bl_ave_b2
    snapshots[i_snapshot]['n_bunches_b1'] = n_bunches_b1
    snapshots[i_snapshot]['n_bunches_b2'] = n_bunches_b2
    snapshots[i_snapshot]['energy_GeV'] = energy_GeV
    snapshots[i_snapshot]['dict_hl_cell_by_cell'] = dict_hl_cell_by_cell
    snapshots[i_snapshot]['hl_imped_sample'] = hl_imped_sample
    snapshots[i_snapshot]['hl_sr_sample'] = hl_sr_sample
    snapshots[i_snapshot]['tref_string_short'] = tref_string_short

    if t_offset_h is None:
        snapshots[i_snapshot]['t_offs_h_str'] = '-'
    else:
        snapshots[i_snapshot]['t_offs_h_str'] = '%.2f'%snapshots[i_snapshot]['t_offs_h']

# check consistency in cell naming
for i_snapshot in xrange(N_snapshots):
    for s in hl.sector_list():
        if len(snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]['cell_names'])!=len(snapshots[0]['dict_hl_cell_by_cell'][s]['cell_names']):
            raise ValueError('Found inconsistency type 1 in dict!')
        for c1, c2 in zip(snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]['cell_names'], snapshots[0]['dict_hl_cell_by_cell'][s]['cell_names']):
            if c1!=c2:raise ValueError('Found inconsistency type 2 in dict!')


# Plots!
plt.close('all')
myfontsz = 13
ms.mystyle_arial(fontsz=13,dist_tick_lab=3)
if N_snapshots==1:
    width = 0.6
else:
    width = 0.8
spshare = None
spsharehist = None
colorlist = ['b','r','g']
colorleglist = ['#7F7FFF', '#FF7F7F', '#7FBF7F']
x_hist = np.linspace(minhist, maxhist, 1000)
y_list = []
figlist = []

for i, s in enumerate(hl.sector_list()):


    #single sector plot
    fig_sect = plt.figure(1000+i, figsize=(12,8.5), tight_layout=False)
    fig_sect.patch.set_facecolor('w')
    ax1_sect = plt.subplot2grid((2,2), (0,0), colspan=2, sharey=spshare)
    axhist = plt.subplot2grid((2,2), (1,0), colspan=1, sharey=spsharehist, sharex=spsharehist)
    spsharehist = axhist

    sptable =  plt.subplot2grid((2,2), (1,1), colspan=1, sharey=spsharehist, sharex=spsharehist)

    spshare = ax1_sect


    y_list.append([])
    for i_snapshot in xrange(N_snapshots):

        this_hld = snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]
        cells = this_hld['cell_names']
        hl_cells = this_hld['heat_loads'].copy()

        # normalize to intensity
        if normtointen:
            totintnorm = (snapshots[i_snapshot]['intensity_b1']+snapshots[i_snapshot]['intensity_b2'])
        else:
            totintnorm = 1.

        if N_snapshots==1:
            if plot_model:
                if args.legend:
                    label1, label2 = 'Imp', 'SR'
                else:
                    label1, label2 = None, None

                hl_imped_t1 = snapshots[i_snapshot]['hl_imped_sample']
                hl_sr_t1 = snapshots[i_snapshot]['hl_sr_sample']

                ax1_sect.axhspan(ymin=0, ymax=hl_imped_t1/totintnorm, color='grey', alpha=0.5, label=label1)
                ax1_sect.axhspan(ymin=hl_imped_t1/totintnorm, ymax=(hl_imped_t1+hl_sr_t1)/totintnorm, color='green', alpha=0.5, label=label2)
                if args.legend:
                    ax1_sect.legend(bbox_to_anchor=(1,1), loc='upper left')
        else:
            if plot_model:
                print('Info: the model line is plotted only when running with a single snapshot')

        if normtointen:
            hl_cells/= totintnorm

        ind = np.arange(len(cells))
        #alternating grey background
        if i_snapshot==0:
            for igrey in ind[1::2]:
                ax1_sect.axvspan(igrey-0.5, igrey+0.5, color='k', alpha=.1)

        #barplot
        #~ ax1_sect.bar(ind-width/2+i_snapshot*width/N_snapshots, hl_cells, width/N_snapshots,
            #~ color=colorleglist[i_snapshot], edgecolor=colorleglist[i_snapshot], linewidth = 0)
        ax1_sect.bar(ind-width/2+i_snapshot*width/N_snapshots, hl_cells, width/N_snapshots,
            color=colorlist[i_snapshot], alpha=.5)

        if normtointen:
            ax1_sect.set_ylabel('Norm. heat load [W/hc/p+]')
        else:
            ax1_sect.set_ylabel('Heat load [W/hc]')


        ax1_sect.set_ylim(min_hl_scale, max_hl_scale)

        ax1_sect.set_xticks(ind)
        ax1_sect.set_xticklabels(cells, rotation=90)

        ax1_sect.set_xlim(ind[0]-2*width, ind[-1]+2*width)

        fig_sect.subplots_adjust(left=.06, right=.96, top=0.9, hspace=0.35, bottom=0.07)

        ax1_sect.yaxis.grid(True)

        # histogram
        histval, binedges = np.histogram(hl_cells, bins=nbinhist, range=(minhist, maxhist))

        normhist = histval/(len(hl_cells)*np.mean(np.diff(binedges)))
        axhist.bar(left=binedges[:-1], width=np.diff(binedges), height=normhist, alpha=0.5, color=colorlist[i_snapshot], edgecolor='none')

        if normtointen:
            axhist.set_xlabel('Norm. heat load [W/hc/p+]')
        else:
            axhist.set_xlabel('Heat load [W/hc]')
        axhist.set_ylabel('Normalized distribution')

        import statsmodels.api as sm
        mask_nan = ~np.isnan(hl_cells)
        obstat = sm.nonparametric.KDEUnivariate(hl_cells[mask_nan])
        obstat.fit()
        obstat.fit(bw=distr_bw)
        density = obstat.evaluate
        tempy = density(x_hist)
        axhist.plot(x_hist, tempy, linewidth=3, color=colorlist[i_snapshot], alpha=0.8)
        axhist.grid('on')
        axhist.set_xlim(minhist, maxhist)
        axhist.ticklabel_format(style='sci', scilimits=(0,0),axis='y')

        y_list[-1].append(tempy)

    to_table = []
    to_table.append(['Fill'] + ['%d'%snapshots[i_snapshot]['filln'] for i_snapshot in xrange(N_snapshots)])
    to_table.append(['Started on'] + [snapshots[i_snapshot]['tref_string_short'] for i_snapshot in xrange(N_snapshots)])
    to_table.append(['T_sample [h]'] + ['%.2f'%snapshots[i_snapshot]['t_h'] for i_snapshot in xrange(N_snapshots)])
    to_table.append(['Energy [GeV]'] + ['%.0f'%(snapshots[i_snapshot]['energy_GeV']) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['N_bunches (B1/B2)'] + ['%d/%d'%(snapshots[i_snapshot]['n_bunches_b1'],snapshots[i_snapshot]['n_bunches_b2']) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['Intensity (B1/B2) [p]'] + [('%.2e/%.2e'%(snapshots[i_snapshot]['intensity_b1'],snapshots[i_snapshot]['intensity_b2'])).replace('+', '') for i_snapshot in xrange(N_snapshots)])
    to_table.append(['Bun.len. (B1/B2) [ns]'] + ['%.2f/%.2f'%(snapshots[i_snapshot]['bl_ave_b1']/1e-9,snapshots[i_snapshot]['bl_ave_b2']/1e-9) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['H.L. S%d (avg) [W]'%s] + ['%.2f' %(np.nanmean(snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]['heat_loads'])) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['H.L. S%d (std) [W]'%s] + ['%.2f' %(np.nanstd(snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]['heat_loads'])) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['H.L. exp. imped. [W]'] + ['%.2f' %(snapshots[i_snapshot]['hl_imped_sample']) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['H.L. exp. synrad [W]'] + ['%.2f' %( snapshots[i_snapshot]['hl_sr_sample']) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['T_nobeam [h]'] + [snapshots[i_snapshot]['t_offs_h_str'] for i_snapshot in xrange(N_snapshots)])


    sptable.axis('tight')
    sptable.axis('off')
    table = sptable.table(cellText=to_table,loc='center', cellLoc='center', colColours=['w']+colorleglist[:N_snapshots])
    table.scale(1,1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(myfontsz-1)
    fig_sect.suptitle('Sector %d, %d cells, %s'%(s, len(cells), {False:'recalc. values', True:'DB values'}[from_csv]))
    figlist.append(fig_sect)



# Violin plot
plt.close(1);
figviol = plt.figure(1, figsize=(12,8.5))
figviol.set_facecolor('w')
axviol = plt.subplot2grid((2,3), (0,0), colspan=3)
maxdistr = np.max(np.array(y_list)[:])
for i_snapshot, col_snsh, sign_shsh in zip([0,1], ['b', 'r'], [-1., 1.]):

    if i_snapshot >= N_snapshots:
        continue

    # normalize to intensity
    if normtointen:
        totintnorm = (snapshots[i_snapshot]['intensity_b1']+snapshots[i_snapshot]['intensity_b2'])
    else:
        totintnorm = 1.

    axviol.plot(2*[18+0.1*sign_shsh], [-50,(snapshots[i_snapshot]['hl_imped_sample']+snapshots[i_snapshot]['hl_sr_sample'])/totintnorm],
        '.-', color=col_snsh, linewidth=2, markersize=10)


    for i, s in enumerate(hl.sector_list()):
        #~ print i, i_snapshot
        axviol.fill_betweenx(y=x_hist, x1=sign_shsh*y_list[i][i_snapshot]/maxdistr*0.9+2*(i+1), x2 = 2*(i+1),
            color=col_snsh, alpha=0.5)

        axviol.plot([2*(i+1)], [np.nanmean(snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]['heat_loads'])/totintnorm],
            '.-', markersize=10, color=col_snsh)
axviol.grid('on')

axviol.set_xticks(2*(np.arange(9)+1))
axviol.set_xticklabels(['Arc %d'%s for s in hl.sector_list()]+['Impedance\n+Synch. rad.'])

if normtointen:
    axviol.set_ylabel('Norm. heat load [W/hc/p+]')
else:
    axviol.set_ylabel('Heat load [W/hc]')


axviol.set_ylim(min_hl_scale, max_hl_scale)
axviol.set_xlim(1,19)


to_table = []
to_table.append(['Fill'] + ['%d'%snapshots[i_snapshot]['filln'] for i_snapshot in xrange(N_snapshots)])
to_table.append(['Started on'] + [snapshots[i_snapshot]['tref_string_short'] for i_snapshot in xrange(N_snapshots)])
to_table.append(['T_sample [h]'] + ['%.2f'%snapshots[i_snapshot]['t_h'] for i_snapshot in xrange(N_snapshots)])
to_table.append(['Energy [GeV]'] + ['%.0f'%(snapshots[i_snapshot]['energy_GeV']) for i_snapshot in xrange(N_snapshots)])
to_table.append(['N_bunches (B1/B2)'] + ['%d/%d'%(snapshots[i_snapshot]['n_bunches_b1'],snapshots[i_snapshot]['n_bunches_b2']) for i_snapshot in xrange(N_snapshots)])
to_table.append(['Intensity (B1/B2) [p]'] + [('%.2e/%.2e'%(snapshots[i_snapshot]['intensity_b1'],snapshots[i_snapshot]['intensity_b2'])).replace('+', '') for i_snapshot in xrange(N_snapshots)])
to_table.append(['Bun.len. (B1/B2) [ns]'] + ['%.2f/%.2f'%(snapshots[i_snapshot]['bl_ave_b1']/1e-9,snapshots[i_snapshot]['bl_ave_b2']/1e-9) for i_snapshot in xrange(N_snapshots)])
to_table.append(['H.L. exp. imped. [W]'] + ['%.2f' %(snapshots[i_snapshot]['hl_imped_sample']) for i_snapshot in xrange(N_snapshots)])
to_table.append(['H.L. exp. synrad [W]'] + ['%.2f' %( snapshots[i_snapshot]['hl_sr_sample']) for i_snapshot in xrange(N_snapshots)])
to_table.append(['H.L. exp. imp.+SR [W/p+]'] + ['%.2e' %((snapshots[i_snapshot]['hl_imped_sample']+snapshots[i_snapshot]['hl_sr_sample'])/(snapshots[i_snapshot]['intensity_b1']+snapshots[i_snapshot]['intensity_b2'])) for i_snapshot in xrange(N_snapshots)])
to_table.append(['T_nobeam [h]'] + [snapshots[i_snapshot]['t_offs_h_str'] for i_snapshot in xrange(N_snapshots)])


sptable  =  plt.subplot2grid((2,3), (1,0), colspan=3)
sptable.axis('tight')
sptable.axis('off')
table = sptable.table(cellText=to_table,loc='center', cellLoc='center', colColours=['w']+colorleglist[:N_snapshots])
table.scale(1,1.5)
table.auto_set_font_size(False)
table.set_fontsize(myfontsz-1)

figviol.suptitle('%s'%({False:'recalc. values', True:'DB values'}[from_csv]))


# Polar plot
list_figpol = []
for i_sn in range(N_snapshots):
    figpol = plt.figure(2000+i_sn, figsize=(6.4*1.8, 4.8*1.8))
    figpol.set_facecolor('w')
    axpol = figpol.add_subplot(111, projection='polar')

    # I concatenate the heat loads taking into account that 
    # the polar plot starts from the first quadrant and moves counterclockwise
    all_hl = np.concatenate([snapshots[i_sn]['dict_hl_cell_by_cell'][ss]['heat_loads'][::-1]
                                for ss in [67, 56, 45, 34, 23, 12, 81, 78] ])
    all_hl[all_hl>max_hl_scale] = max_hl_scale
    all_hl[all_hl<0] = np.nan
    thetapol = np.linspace(0, 2*np.pi, len(all_hl))
    axpol.plot(thetapol, all_hl, color=colorlist[i_sn],
        lw=1.5, label='Fill %d'%snapshots[i_sn]['filln'])

    axpol.set_rmin(0.)
    if max_hl_scale is not None:
        axpol.set_rmax(max_hl_scale)
        axpol.set_rticks(np.arange(30, max_hl_scale+1, 30))
    axpol.grid(linestyle='-', color='grey', alpha=.5)
    # axpol.set_rlabel_position(-22.5)

    axpol.set_xticks(np.arange(0, 2*np.pi-0.1, np.pi/4))
    axpol.set_xticklabels(['P%d'%ip for ip in [7, 6, 5, 4, 3, 2, 1, 8, 7]])

    # axpol.plot(thetapol, all_hl*0+90/2., color='darkseagreen', linestyle='--', lw=1.5)
    # axpol.plot(thetapol, all_hl*0+160/2., color='darkgreen', linestyle='--', lw=1.5)

    axpol.legend(frameon=False)

    list_figpol.append(figpol)

if args.o:

    str_file = 'multiple_'
    for i_snapshot, snapshot in enumerate(snapshots):
        str_file += 'fill%dat%.2fh_'%(snapshot['filln'], snapshot['t_h'])

    folname = args.savein+'/cellbycell_%s_%s'%(str_file, tagfname)

    if not os.path.exists(folname):
        os.mkdir(folname)

    if normtointen:
        str_file+='hlnorm'
    else:
        str_file+='hl'

    for fig, s in zip(figlist, hl.sector_list()):
        fig.savefig(folname+'/cellbycell_%s_%s_sector%d.png'%(str_file, tagfname, s), dpi=200)

    figviol.savefig(folname+'/cellbycell_%s_%s_distrib.png'%(str_file, tagfname), dpi=200)

    for sector in hl.sector_list():
        fname = folname+'/cellbycell_%s_%s_sector%d.csv'%(str_file, tagfname, sector)
        with open(fname, 'w') as fid:
            fid.write('cell'+''.join([',snapshot%d'%isnap for isnap in xrange(len(snapshots))])+'\n')
            for i_cell, cell in enumerate(snapshots[0]['dict_hl_cell_by_cell'][sector]['cell_names']):
                fid.write(cell+''.join([',%.1e'%snapshots[isnap]['dict_hl_cell_by_cell'][sector]['heat_loads'][i_cell] for isnap in xrange(len(snapshots))])+'\n')

    fname = folname+'/cellbycell_%s_%s_generalinfo.txt'%(str_file, tagfname)
    with open(fname, 'w') as fid:
        for llll in to_table:
            fid.write('\t'.join(llll)+'\n')

    import pickle
    fnamepkl = folname+'/cellbycell_%s_%s.pkl'%(str_file, tagfname)
    with open(fnamepkl, 'wb') as fid:
        pickle.dump(snapshots, fid)


    def default(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError('Not serializable')

    import json
    fnamejson = folname+'/cellbycell_%s_%s.json'%(str_file, tagfname)
    with open(fnamejson, 'wb') as fid:
        json.dump(snapshots, fid, default=default)


plt.show()

