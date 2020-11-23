import pickle
import numpy as np
import LHCMeasurementTools.mystyle as ms

from data_folders import data_folder_list
import GasFlowHLCalculator.qbs_fill as qf
import matplotlib.pyplot as pl; plt=pl
import cell_by_cell_plot_helpers as cch
import LHCMeasurementTools.cell_naming as cn

import LHCMeasurementTools.LHC_Heatloads as hl

# filln = 5979
# t_sample_h = 3.3 
# t_offset_h = 2

filln = 5143
t_sample_h = 2.5
t_offset_h = .7

filln = 4535
t_sample_h = 2.7
t_offset_h = .5

window_corrector_avg_s = 180
window_timber_avg = 100.

# To have English weekdays
#~ try:
    #~ import locale
    #~ locale.setlocale(locale.LC_TIME, 'en_US')
#~ except Exception as err:
    #~ print '\nDid not manage to set locale. Got:'
    #~ print err



import sys, time, os
# merge pickles and add info on location
dict_fill_bmodes={}
for df in data_folder_list:
    with open(df+'/fills_and_bmodes.pkl', 'rb') as fid:
        this_dict_fill_bmodes = pickle.load(fid)
        for kk in this_dict_fill_bmodes:
            this_dict_fill_bmodes[kk]['data_folder'] = df
        dict_fill_bmodes.update(this_dict_fill_bmodes)


# Extract some timing info 
data_folder_fill = dict_fill_bmodes[filln]['data_folder']
t_fill_st = dict_fill_bmodes[filln]['t_startfill']
t_fill_end = dict_fill_bmodes[filln]['t_endfill']
t_ref=t_fill_st
tref_string=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))
tref_string_short=time.strftime("%d %b %Y %H:%M", time.localtime(t_ref))


# load heat load dictionary from recalculated
fill_dict = qf.get_fill_dict(filln)

# sort cells
dict_hl_cell_by_cell = cch.sample_and_sort_cell_by_cell(fill_dict, t_ref=t_ref, t_sample_h=t_sample_h, t_offset_h=t_offset_h)


# get all correctors
t_sample = t_ref + t_sample_h*3600

import pytimber
ldb = pytimber.LoggingDB()
dict_correctors = {}
print('Start download H correctors')
namesh = ldb.search('%RCBH%I_MEAS')
dict_correctors.update(ldb.getScaled(namesh, t_sample, t_sample+window_corrector_avg_s, scaleAlgorithm='AVG', 
                        scaleInterval='SECOND',scaleSize='%d'%window_corrector_avg_s))
print('Downloaded H correctors')
print('Start download V correctors')
namesv = ldb.search('%RCBV%I_MEAS')
dict_correctors.update(ldb.getScaled(namesv, t_sample, t_sample+window_corrector_avg_s, scaleAlgorithm='AVG',
                scaleInterval='SECOND',scaleSize='%d'%window_corrector_avg_s))
print('Downloaded V correctors')

#evaluate avg and simplify naming
dict_avg = {}
dict_plane = {}
for kk in list(dict_correctors.keys()):
    beam_name = kk.split(':')[-2][-2:]
    loc = kk.split('.')[2][-2:]+kk.split('.')[1][-2:]
    plane = kk.split('RCB')[-1][0]

    simplified_name = loc+'_'+beam_name
    if '16L2' in kk:
        print(kk, simplified_name, plane)

    dict_avg[simplified_name] = np.mean(dict_correctors[kk][1])
    dict_plane[simplified_name] = plane
    
    
# get cell quad association
dict_cell_to_quad = cn.cell_to_quad_dict()

# cell corrector association
dict_correctors_sector = {}
for i_s, s in enumerate(hl.sector_list()):
    cells = dict_hl_cell_by_cell[s]['cell_names']
    list_corr_B1_B2 = []
    list_current_B1 = []
    list_current_B2 = []
    for cell in cells:
        extname = cell.replace('_', '_CV94')
        name_quad = dict_cell_to_quad[extname]
        place = name_quad.replace('Q', '')
        
        if place.startswith('10') or place.startswith('34'):
            print('Skipped %s!'%place)
            list_corr_B1_B2.append('')
            list_current_B1.append(np.nan)
            list_current_B2.append(np.nan)
        else:
            corr_config = place+'_'+dict_plane[place+'_B1']+dict_plane[place+'_B2']
            list_corr_B1_B2.append(corr_config)
            list_current_B1.append(dict_avg[place+'_B1'])
            list_current_B2.append(dict_avg[place+'_B2'])
    
    dict_correctors_sector[s] = {'list_corr_B1_B2':list_corr_B1_B2,
                                 'list_current_B1':list_current_B1,
                                 'list_current_B2':list_current_B2,   }
        
        
    



# plots
width = 0.8

pl.close('all')
ms.mystyle_arial(fontsz=13,dist_tick_lab=3)

pl.figure(100)
axcorr = pl.subplot(111)
pl.figure(101)
axcorrlog = pl.subplot(111)

spshare = None
spsharecorr = None
figsect_list = []
for i_s, s in enumerate(hl.sector_list()):

    fig_sect = plt.figure(1000+i_s, figsize=(12,8.5), tight_layout=False)
    fig_sect.patch.set_facecolor('w')
    ax1_sect = plt.subplot2grid((2,2), (0,0), colspan=2, sharey=spshare)
    spshare = ax1_sect
    
    cells = dict_hl_cell_by_cell[s]['cell_names']
    hl_cells = dict_hl_cell_by_cell[s]['heat_loads'].copy()
    
    ind = np.arange(len(cells)) 

    ax1_sect.bar(ind-width/2, hl_cells, width*0.7, 
            color='b', alpha=.5)
            
    ax1_sect.set_xticks(ind)
    ax1_sect.set_xticklabels(cells, rotation=90)
    
    ax1_sect.set_xlim(ind[0]-2*width, ind[-1]+2*width)
    ax1_sect.yaxis.grid(True)
    ax1_sect.yaxis.axes.get_xaxis().set_visible(False)
    ax1_sect.set_ylabel('Heat load [W/hc]')

    ax2_sect = plt.subplot2grid((2,2), (1,0), colspan=2, sharey=spsharecorr, sharex=ax1_sect)
    spsharecorr = ax2_sect
    ax2_sect.bar(ind-width/2, np.abs(dict_correctors_sector[s]['list_current_B1']), width/2., 
            color='b', alpha=.5)
    ax2_sect.bar(ind, np.abs(dict_correctors_sector[s]['list_current_B2']), width/2., 
            color='r', alpha=.5)
    ax2_sect.set_xticks(ind)
    ax2_sect.set_xticklabels(dict_correctors_sector[s]['list_corr_B1_B2'], rotation=90)
    ax2_sect.yaxis.grid(True)
    ax2_sect.set_ylabel('Corrector current (abs.) [A]')
    
    for ax in [ax1_sect, ax2_sect]:
        for igrey in ind[1::2]:
            ax.axvspan(igrey-0.5, igrey+0.5, color='k', alpha=.1)
    
    colorcurr = ms.colorprog(i_s, 8, v1=0.9, v2=1.0, cm='hsv')       
    axcorr.plot(np.abs(dict_correctors_sector[s]['list_current_B1']), dict_hl_cell_by_cell[s]['heat_loads'], '.', markersize=10, color=colorcurr)
    axcorrlog.semilogx(np.abs(dict_correctors_sector[s]['list_current_B1']), dict_hl_cell_by_cell[s]['heat_loads'], '.', markersize=10, color=colorcurr)
            
    fig_sect.subplots_adjust(left=.06, right=.96, top=0.9, hspace=0.12, bottom=0.11)
    
# plots
width = 0.8

pl.close('all')
ms.mystyle_arial(fontsz=13,dist_tick_lab=3)

figcorr = pl.figure(100)
figcorr.patch.set_facecolor('w')
axcorr = pl.subplot(111)

figcorrlog = pl.figure(101)
figcorrlog.patch.set_facecolor('w')
axcorrlog = pl.subplot(111)


spshare = None
spsharecorr = None
for i_s, s in enumerate(hl.sector_list()):

    fig_sect = plt.figure(1000+i_s, figsize=(12,8.5), tight_layout=False)
    fig_sect.patch.set_facecolor('w')
    figsect_list.append(fig_sect)
    ax1_sect = plt.subplot2grid((2,2), (0,0), colspan=2, sharey=spshare)
    spshare = ax1_sect
    
    cells = dict_hl_cell_by_cell[s]['cell_names']
    hl_cells = dict_hl_cell_by_cell[s]['heat_loads'].copy()
    
    ind = np.arange(len(cells)) 

    ax1_sect.bar(ind-width/2, hl_cells, width*0.7, 
            color='b', alpha=.5)
            
    ax1_sect.set_xticks(ind)
    ax1_sect.set_xticklabels(cells, rotation=90)
    
    ax1_sect.set_xlim(ind[0]-2*width, ind[-1]+2*width)
    ax1_sect.yaxis.grid(True)
    ax1_sect.yaxis.axes.get_xaxis().set_visible(False)
    ax1_sect.set_ylabel('Heat load [W/hc]')
    ax1_sect.set_ylim(bottom=0)

    ax2_sect = plt.subplot2grid((2,2), (1,0), colspan=2, sharey=spsharecorr, sharex=ax1_sect)
    spsharecorr = ax2_sect
    ax2_sect.bar(ind-width/2, np.abs(dict_correctors_sector[s]['list_current_B1']), width/2., 
            color='b', alpha=.5)
    ax2_sect.bar(ind, np.abs(dict_correctors_sector[s]['list_current_B2']), width/2., 
            color='r', alpha=.5)
    ax2_sect.set_xticks(ind)
    ax2_sect.set_xticklabels(dict_correctors_sector[s]['list_corr_B1_B2'], rotation=90)
    ax2_sect.yaxis.grid(True)
    ax2_sect.set_ylabel('Corrector current (abs.) [A]')
    
    for ax in [ax1_sect, ax2_sect]:
        for igrey in ind[1::2]:
            ax.axvspan(igrey-0.5, igrey+0.5, color='k', alpha=.1)
            
    fig_sect.subplots_adjust(left=.06, right=.96, top=0.9, hspace=0.12, bottom=0.11)
    fig_sect.suptitle('Fill. %d started on %s(t=%.2fh)\nSector %d, %d cells, %s'%(filln, tref_string,t_sample_h, s, len(cells), {False:'recalc. values', True:'DB values'}[False]))
        
    colorcurr = ms.colorprog(i_s, 8, v1=0.9, v2=1.0, cm='hsv')       
    axcorr.plot(np.abs(dict_correctors_sector[s]['list_current_B1']), dict_hl_cell_by_cell[s]['heat_loads'], '.', markersize=10, color=colorcurr)
    axcorrlog.semilogx(np.abs(dict_correctors_sector[s]['list_current_B1']), dict_hl_cell_by_cell[s]['heat_loads'], '.', markersize=10, color=colorcurr)

for ax in [axcorr, axcorrlog]:
    ax.grid('on') 
    ax.set_ylim(bottom=0)
    ax.set_ylabel('Heat load [W/hc]')
    ax.set_xlabel('B1 corrector current (abs.) [A]')
    
figcorrlog.suptitle('Fill. %d started on %s(t=%.2fh)'%(filln, tref_string,t_sample_h))
figcorr.suptitle('Fill. %d started on %s(t=%.2fh)'%(filln, tref_string,t_sample_h))

def save_cell_by_cell(infolder='./'):
    str_file = 'fill%dat%.2fh_'%(filln, t_sample_h)
    for fig, s in zip(figsect_list, hl.sector_list()):
            fig.savefig(infolder+'/correctors_cellbycell_%s_sector%d.png'%(str_file, s), dpi=200)

def save_correlation_plot(infolder='./'):
    str_file = 'fill%dat%.2fh_'%(filln, t_sample_h)
    figcorr.savefig(infolder+'/correctors_cellbycell_%s_correlation.png'%(str_file), dpi=200)
    figcorrlog.savefig(infolder+'/correctors_cellbycell_%s_correlation_log.png'%(str_file), dpi=200)
   
pl.show()
        

