import sys, time, os
sys.path.append("../")

import LHCMeasurementTools.TimberManager as tm
import LHCMeasurementTools.SetOfHomogeneousVariables as shv
import LHCMeasurementTools.LHC_Heatloads as hl
import LHCMeasurementTools.mystyle as ms
import scipy.stats as stats

from data_folders import data_folder_list

import GasFlowHLCalculator.qbs_fill as qf

import cell_by_cell_plot_helpers as cch

import argparse
import pickle
import numpy as np
import pylab as plt



# defaults
t_offset = None
min_hl_scale = None
max_hl_scale = None
tagfname = ''


# parse arguments
parser = argparse.ArgumentParser(epilog='Example: 002b_bar_plot_per_sector_multiple_fills.py --at filln:5108!t_h:2.5!t_offs_h:0.05 filln:5108!t_h:3.5!t_offs_h:0.05')
parser.add_argument('-o', help='Save plots on disk.', action='store_true')
parser.add_argument('--fromcsv', help='Load heatloads from csvs. By default, use recalculated.', action='store_true')

parser.add_argument('--min-hl-scale', help='Minimum of plot.', type=float)
parser.add_argument('--max-hl-scale', help='Maximum of plot.', type=float)
parser.add_argument('--no-plot-model', help='Plot imp. SR contribution to heat loads.', action='store_true')
parser.add_argument('--tag', help='Tag of plot windows.', default='')
parser.add_argument('-v', help='Verbose.', action='store_true')
parser.add_argument('--legend', help='Plot a legend for Imp/SR', action='store_true')
parser.add_argument('--normtointensity', help='Normalize to beam intensity', action='store_true')

parser.add_argument('--at', help="Snapshots in the form: filln:5108!t_h:2.5!t_offs_h:0.05 filln:5108!t_h:3.5!t_offs_h:0.05", nargs='+')


#~ parser.add_argument('--t', help='Time at which you plot the heat loads in hours.', type=float)
#~ parser.add_argument('--t-offset', help='Time within the fill which sets heat loads to 0 in hours.', type=float)
#~ parser.add_argument('--filln',type=int, default=None)

args = parser.parse_args()

#~ if args.filln:
    #~ filln = args.filln
#~ if args.t:
    #~ t_sample_h = args.t
if args.min_hl_scale:
    min_hl_scale = args.min_hl_scale
if args.max_hl_scale:
    max_hl_scale = args.max_hl_scale
#~ if args.t_offset:
    #~ t_offset = args.t_offset
if args.tag:
    tagfname = args.tag

plot_model = not args.no_plot_model

from_csv = args.fromcsv
normtointen = args.normtointensity


#histogram parameters
if not normtointen:
    minhist = -5
    maxhist = 230
    nbinhist = 20
    distr_bw = 7
else:
    minhist = -.5e-13
    maxhist = 5e-13
    nbinhist = 20
    distr_bw = 7/2e14



# beuild snaphosts dicts
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
        hid = qf.get_fill_dict(filln)

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
    intensity_b1, intensity_b2, n_bunches_b1, n_bunches_b2, energy_GeV, hl_imped_sample, hl_sr_sample = cch.extract_and_compute_extra_fill_data(fill_dict, t_ref, t_sample_h, thresh_bint=3e10)

    # extract heat load data
    dict_hl_cell_by_cell = cch.sample_and_sort_cell_by_cell(hid, t_ref=t_ref, t_sample_h=t_sample_h, t_offset_h=t_offset)
    
    snapshots[i_snapshot]['intensity_b1'] = intensity_b1
    snapshots[i_snapshot]['intensity_b2'] = intensity_b2
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
    

print 'REMINDER: Please write consistency check!!!!'
    
    

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
            
            
    for i_snapshot in xrange(N_snapshots):
        
        this_hld = snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]
        cells = this_hld['cell_names']
        hl_cells = this_hld['heat_loads'].copy()

        # normalize to intensity
        if normtointen:
            totintnorm = (snapshots[i_snapshot]['intensity_b1']+snapshots[i_snapshot]['intensity_b2'])
        else:
            totintnorm = 1.

        if normtointen:
            hl_cells/= totintnorm

        ind = np.arange(len(cells)) 
        #alternating grey background
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
    
        import statsmodels.api as sm
        obstat = sm.nonparametric.KDEUnivariate(hl_cells)
        obstat.fit()
        obstat.fit(bw=distr_bw)
        density = obstat.evaluate
        tempy = density(x_hist)
        axhist.plot(x_hist, tempy, linewidth=3, color=colorlist[i_snapshot], alpha=0.8)
        axhist.grid('on')
        axhist.set_xlim(minhist, maxhist)
        
        y_list.append(tempy)
        
    to_table = []
    to_table.append(['Fill'] + ['%d'%snapshots[i_snapshot]['filln'] for i_snapshot in xrange(N_snapshots)])
    to_table.append(['Started on'] + [snapshots[i_snapshot]['tref_string_short'] for i_snapshot in xrange(N_snapshots)])
    to_table.append(['T_sample [h]'] + ['%.2f'%snapshots[i_snapshot]['t_h'] for i_snapshot in xrange(N_snapshots)])
    to_table.append(['N_bunches (B1/B2)'] + ['%d/%d'%(snapshots[i_snapshot]['n_bunches_b1'],snapshots[i_snapshot]['n_bunches_b2']) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['Intensity [p] (B1/B2)'] + ['%.2e/%.2e'%(snapshots[i_snapshot]['intensity_b1'],snapshots[i_snapshot]['intensity_b2']) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['Energy [GeV]'] + ['%.0f'%(snapshots[i_snapshot]['energy_GeV']) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['H.L. S%d (avg) [W]'%s] + ['%.2f' %(np.mean(snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]['heat_loads'])) for i_snapshot in xrange(N_snapshots)])
    to_table.append(['H.L. S%d (std) [W]'%s] + ['%.2f' %(np.std(snapshots[i_snapshot]['dict_hl_cell_by_cell'][s]['heat_loads'])) for i_snapshot in xrange(N_snapshots)])
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
    
    
if args.o:
    
    str_file = 'multiple_'
    for i_snapshot, snapshot in enumerate(snapshots):
        str_file += 'fill%dat%.2fh_'%(snapshot['filln'], snapshot['t_h'])
    
    if normtointen:
        str_file+='hlnorm'
    else:
        str_file+='hl'
    
    for fig, s in zip(figlist, hl.sector_list()):
        fig.savefig('cell_by_cell_plots/cellbycell_%s_%s_sector%d.png'%(str_file, tagfname, s), dpi=200)
    

plt.show()


'''

    #single sector plot
    fig_sect = plt.figure(1000+i, figsize=(12,8.5), tight_layout=False)
    fig_sect.patch.set_facecolor('w')
    #~ ax1_sect = fig_sect.add_subplot(221, sharey=spshare, rowspan=2)
    ax1_sect = plt.subplot2grid((2,2), (0,0), colspan=2, sharey=spshare)
    
    spshare = ax1_sect

    if plot_model:
        if args.legend:
            label1, label2 = 'Imp', 'SR'
        else:
            label1, label2 = None, None
        ax1_sect.axhspan(ymin=0, ymax=hl_imped_t1/totintnorm, color='grey', alpha=0.5, label=label1)
        ax1_sect.axhspan(ymin=hl_imped_t1/totintnorm, ymax=(hl_imped_t1+hl_sr_t1)/totintnorm, color='green', alpha=0.5, label=label2)
        if args.legend:
            ax1_sect.legend(bbox_to_anchor=(1,1), loc='upper left')


    ind = np.arange(len(cells))
    if normtointen:
        val1/=totintnorm
        
    for igrey in ind[1::2]:
        ax1_sect.axvspan(igrey-0.5, igrey+0.5, color='k', alpha=.1)
    ax1_sect.bar(ind-width/2, val1, width, color='b', label='%.1f h after start of fill'%t1, alpha=0.5)



    if normtointen:
        ax1_sect.set_ylabel('Norm. heat load [W/hc/p+]')
    else:
        ax1_sect.set_ylabel('Heat load [W/hc]')
    ax1_sect.set_ylim(min_hl_scale, max_hl_scale)
    #ax1_sect.legend(loc='upper right')
    ax1_sect.set_xticks(ind)
    #~ ax1_sect.xaxis.set_major_formatter(plt.NullFormatter())
    if show_labels:
        ax1_sect.set_xticklabels(cells, rotation=90)
    #~ plt.setp(ax1_sect.get_xticklabels(), visible=False)
    ax1_sect.set_xlim(ind[0]-2*width, ind[-1]+2*width)



    fig_sect.subplots_adjust(left=.06, right=.96, top=0.9, hspace=0.35, bottom=0.07)
        
    fig_sect.suptitle('Fill. %d started on %s\n(t=%.2fh, %s%s)\nSector %d, %d cells, %s'%(filln, tref_string,
                        t1, tagfname, offset_info, s, len(cells), {False:'recalc. values', True:'DB values'}[from_csv]))
    #plt.subplots_adjust(top=.83, left=.05)
    #~ ax1_sect.xaxis.grid('off')
    ax1_sect.yaxis.grid(True)
    
    
    # histogram
    histval, binedges = np.histogram(val1, bins=nbinhist, range=(minhist, maxhist))
    
    axhist = plt.subplot2grid((2,2), (1,0), colspan=1, sharey=spsharehist, sharex=spsharehist)
    spsharehist = axhist
    normhist = histval/(len(val1)*np.mean(np.diff(binedges)))
    axhist.bar(left=binedges[:-1], width=np.diff(binedges), height=normhist, alpha=0.5)
    
    
    #~ density = stats.gaussian_kde(val1)
    
    
    import statsmodels.api as sm
    obstat = sm.nonparametric.KDEUnivariate(val1)
    obstat.fit()
    obstat.fit(bw=5.)
    density = obstat.evaluate
    tempy = density(x_hist)
    axhist.plot(x_hist, tempy, linewidth=3, color='blue', alpha=0.8)
    axhist.grid('on')
    axhist.set_xlim(minhist, maxhist)
    
    y_list.append(tempy)
    
    figlist.append(fig_sect)
    
plt.figure(2000)
bad_sectors = [12, 23, 81,  78]
good_sectors = [34, 45, 56, 67]
bad_distr = 0*x_hist
good_distr = 0*x_hist

for ii, s in enumerate(sectors[:]):
    colorcurr = ms.colorprog(ii, 8)
    plt.plot(x_hist, y_list[ii], color=colorcurr, linewidth=3)
    if s in bad_sectors:
        bad_distr+=y_list[ii]
    else:
        good_distr+=y_list[ii]
    
    
plt.figure(3000)
plt.plot(x_hist, bad_distr/np.sum(bad_distr))
plt.plot(x_hist, good_distr/np.sum(good_distr))

if args.o:
    for fig, s in zip(figlist, sectors[:]):
        fig.savefig('cell_by_cell_plots/cellbycell_fill%d_t%.2fh_%s_sector%d.png'%(filln, t1, tagfname, s), dpi=200)

plt.show()
'''