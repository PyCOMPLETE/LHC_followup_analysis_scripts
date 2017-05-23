
import numpy as np
import LHCMeasurementTools.mystyle as ms
import pylab as pl
from hl_dicts.dict_utils import load_dict, mask_dict, merge_dicts
import LHCMeasurementTools.LHC_Heatloads as HL


folder_figs = 'figures_analysis_for_HSC'
regenerate_figures = False

moment = 'sb+2_hrs'

file_list = ['hl_dict_3_fills_2016.pkl', 'hl_dict_4_fills_2015.pkl']

main_dict = merge_dicts(load_dict(file_list[0]), load_dict(file_list[1]))
 


fills_to_analyze = [
(4511, '100 ns'),
(4246, '50 ns'),
(4525, '8b4e'),
(5386, '25 ns, 48b/tr'),
(5393, '25 ns, 48b/tr'),
(5219, '25 ns, 72b/tr'),
# (4565, '25 ns - 36b/train')
]



list_n_bunches = []
list_bunch_intensity_avg = []
list_bunch_length_avg = []
list_filln = []
list_tags = []
list_imped = []
list_sr = []

dict_hl = {}
for sector in HL.sector_list():
    dict_hl[sector] = []

for filln, tag in fills_to_analyze:
    i_fill = np.argmin(np.abs(filln-main_dict['filln']))

    n_bunches = main_dict[moment]['n_bunches']['b1'][i_fill]
    total_intensity_2beams = main_dict[moment]['intensity']['b1'][i_fill]+main_dict[moment]['intensity']['b2'][i_fill]
    bunch_intensity_avg = total_intensity_2beams/2/n_bunches
    bunch_length_avg = 0.5*(main_dict[moment]['blength']['b1']['avg'][i_fill]+main_dict[moment]['blength']['b2']['avg'][i_fill])

    list_n_bunches.append(n_bunches)
    list_bunch_intensity_avg.append(bunch_intensity_avg)
    list_bunch_length_avg.append(bunch_length_avg)
    list_filln.append(filln)
    list_tags.append(tag)
    list_imped.append((main_dict[moment]['heat_load']['imp']['b1'][i_fill]+ main_dict[moment]['heat_load']['imp']['b2'][i_fill])*53.4)
    list_sr.append((main_dict[moment]['heat_load']['sr']['b1'][i_fill]+ main_dict[moment]['heat_load']['sr']['b2'][i_fill])*53.4)

    for sector in HL.sector_list():
        dict_hl[sector].append(main_dict[moment]['heat_load']['arc_averages']['S'+str(sector)][i_fill])


pl.close('all')

if regenerate_figures:
    share_y_0 = None
    share_y_1 = None
    share_y_2 = None
    share_y_3 = None

    for i_sec, sector in enumerate(HL.sector_list()):

        print 'Sector %d'%sector

        ind = np.arange(len(list_n_bunches))  
        width = 0.35  

        norm_to = np.array(list_n_bunches)
        # norm_to = 1.


        na = np.array

        figsize = (8*1.7,6*1.1)


        ms.mystyle_arial(fontsz=18, dist_tick_lab=5)
        fig0 = pl.figure((i_sec+1)*1000+0, figsize=figsize)
        sp0 = pl.subplot(1,1,1, sharey=share_y_0); share_y_0 = sp0
        fig1 = pl.figure((i_sec+1)*1000+1, figsize=figsize)
        sp1 = pl.subplot(1,1,1, sharey=share_y_1); share_y_1 = sp1
        fig2 = pl.figure((i_sec+1)*1000+2, figsize=figsize)
        sp2 = pl.subplot(1,1,1, sharey=share_y_2); share_y_2 = sp2
        fig3 = pl.figure((i_sec+1)*1000+3, figsize=figsize)
        sp3 = pl.subplot(1,1,1, sharey=share_y_3); share_y_3 = sp3

        for ff in [fig0, fig1, fig2, fig3]:
            ff.set_facecolor('w')
            ff.subplots_adjust(top=.85, bottom=.14)

        for ff in [fig0, fig1]:
            ff.suptitle('Average Arc %d'%sector)

        for ff in [fig2, fig3]:
            ff.suptitle('Average Arc %d\n(synch. radiation is subtracted)'%sector)



        sp0.bar(ind+width/2, na(dict_hl[sector]), width, color='blue', alpha=.5,
                     bottom=None, zorder=3)
        sp0.bar(ind-width/2, na(list_imped), width, color='grey', alpha=.5,
                     bottom=None, zorder=3)
        sp0.bar(ind-width/2, na(list_sr), width, color='green', alpha=.5,
                     bottom=na(list_imped), zorder=3)

        sp1.bar(ind+width/2, na(dict_hl[sector])/norm_to*1e3, width, color='blue', alpha=.5,
                     bottom=None, zorder=3)
        sp1.bar(ind-width/2, na(list_imped)/norm_to*1e3, width, color='grey', alpha=.5,
                     bottom=None, zorder=3)
        sp1.bar(ind-width/2, na(list_sr)/norm_to*1e3, width, color='green', alpha=.5,
                     bottom=na(list_imped)/norm_to*1e3, zorder=3)

        list_imped_ec = na(dict_hl[sector]) - na(list_sr)

        sp2.bar(ind+width/2, list_imped_ec/norm_to*1e3, width, color='blue', alpha=.5,
                     bottom=None, zorder=3)
        sp2.bar(ind-width/2, na(list_imped)/norm_to*1e3, width, color='grey', alpha=.5,
                     bottom=None, zorder=3)

        sp3.bar(ind, list_imped_ec/norm_to/(list_imped_ec[0]/norm_to[0]), width, color='blue', alpha=.5,
                     bottom=None, zorder=3)


        for sp in [sp0, sp1, sp2, sp3]:
            sp.set_xticks(ind + width/2.)
            sp.set_xticklabels(['%s\nFill %d\n%db'%(tag, filln, n_bunches) for tag, n_bunches, filln in zip(list_tags, list_n_bunches, list_filln)])
            sp.set_xlim(np.min(ind)-0.2, np.max(ind)+width+0.2)
            sp.grid('on')

        sp0.set_ylabel('Heat load [W/hcell]')
        sp1.set_ylabel('Heat load [mW/hcell/bunch]', labelpad=10)
        sp2.set_ylabel('Heat load [mW/hcell/bunch]', labelpad=10)
        sp3.set_ylabel('(Heat load per bunch) / (100 ns case)', labelpad=10)
        

        fig0.savefig(folder_figs+'/sector_%s_total_heat_load.png'%sector, dpi=200)
        fig1.savefig(folder_figs+'/sector_%s_heat_load_per_bunch.png'%sector, dpi=200)
        fig2.savefig(folder_figs+'/sector_%s_heat_load_per_bunch_no_sr.png'%sector, dpi=200)
        fig3.savefig(folder_figs+'/sector_%s_heat_load_per_bunch_norm_100ns.png'%sector, dpi=200)

        # pl.show()
        # wurstel


#Latex document:
import pytolatex_chamber_tables as texchamtab
latex_folder = '.'

latex_filename = 'heat_load_info.tex'

with open(latex_folder+'/'+ latex_filename, 'w') as fid_tex_complete:


    fid_tex_complete.write(texchamtab.start_latex_file)

    fid_tex_complete.write(r'''   
        \begin{table}[p]
        \centering
        \textbf{\LARGE Main beam parameters (after 2h in Stable Beams)}\\
        \vspace*{1 cm}
        \begin{tabular}
        {lcccc}
        \hline%\endfirsthead\hline\endhead
        ''')

    fid_tex_complete.write(r'''\textbf{Beam type} & \textbf{Fill n.} & \textbf{N. bunches} & \textbf{Avg. bun. intensity} & \textbf{Avg. bun. length}\\
        \hline
        ''')
    for i_fill, filln in enumerate(list_filln):
            fid_tex_complete.write(r'''%s & %d & %d & %.2fe11 p/b & %.2f ns\\
        '''%(list_tags[i_fill], filln, list_n_bunches[i_fill], 
            list_bunch_intensity_avg[i_fill]/1e11, list_bunch_length_avg[i_fill]*1e9))

    fid_tex_complete.write(r'''\hline
            \end{tabular}
            \end{table}
            \newpage''') 


    
    # figures average heat loads
    for sector in HL.sector_list():
        listfigs = [folder_figs+'/sector_%s_total_heat_load.png'%sector,
                folder_figs+'/sector_%s_heat_load_per_bunch.png'%sector,
                folder_figs+'/sector_%s_heat_load_per_bunch_no_sr.png'%sector,
                folder_figs+'/sector_%s_heat_load_per_bunch_norm_100ns.png'%sector]

        
        fid_tex_complete.write(r'''
            \begin{figure}[p]
            \centering''')
        for fig in listfigs:
            fid_tex_complete.write(r'''\includegraphics[width=.49\textwidth,trim={2cm -1cm 2.5cm 0cm},clip]{'''+\
            fig+\
            '''}
            ''')

        fid_tex_complete.write(r'''
            \includegraphics[width=.51\textwidth,trim={0cm 0cm 0cm 0cm},clip]{legend.pdf}
            \end{figure}
            ''')

    fid_tex_complete.write(r'''
        \FloatBarrier
        ''')

    # comparisons cell by cell
    folder_compar_plots = 'cell_by_cell_plots'
    comparison_list = [('25 ns vs 100 ns (similar number of bunches)',
                    '{cellbycell_fill5386_t2.00h_high_energy_sector%d}.png',
                    '{cellbycell_fill4511_t6.50h_100ns_high_energy_sector%d}.png' ),
                    ('25 ns vs 50 ns (600 vs 300 bunches)',
                     '{cellbycell_fill5386_t2.00h_high_energy_sector%d}.png',
                     '{cellbycell_fill4246_t4.00h_50ns_high_energy_sector%d}.png'),
                    ('25 ns vs 8b4e (similar number of bunches)',
                     '{cellbycell_fill5386_t2.00h_high_energy_sector%d}.png',
                     '{cellbycell_fill4525_t5.00h_8b4e_high_energy_sector%d}.png'),
                    ('25 ns - 600b vs 2200b (2x48bpi)',
                     '{cellbycell_fill5386_t2.00h_high_energy_sector%d}.png',
                     '{cellbycell_fill5393_t2.20h_25ns2200b_high_energy_sector%d}.png'),
                    ('25 ns - 2040b 72bpi vs 2200 2x48bpi',
                     '{cellbycell_fill5219_t1.80h_25ns2040b_high_energy_sector%d}.png',
                     '{cellbycell_fill5393_t2.20h_25ns2200b_high_energy_sector%d}.png')]

    for comparison in comparison_list:
        for sector in HL.sector_list():
            title = comparison[0]
            top_plot = folder_compar_plots + '/'+ comparison[1]%sector
            bottom_plot = folder_compar_plots + '/'+ comparison[2]%sector

            fid_tex_complete.write(r'''
                    \begin{figure}[p]
                    \centering
                    \textbf{\Large %s\\}\par\medskip
                    \includegraphics[height=.47\textheight,trim={0cm .4cm 0cm 0cm},clip]{%s}
                    \includegraphics[height=.47\textheight,trim={0cm .4cm 0cm 0cm},clip]{%s}
                    \includegraphics[width=.51\textwidth,trim={0cm 0cm 0cm 0cm},clip]{legend.pdf}
                    \end{figure}
                    '''%('Cell by cell: %s'%title, top_plot, bottom_plot))

    fid_tex_complete.write(r'''
    \FloatBarrier
    ''')

    # figures compare fill
    folder_compar_fills = 'avg_vs_time'
    comparison_fill_list = [('25 ns vs 100 ns (similar number of bunches)', 5386, 4511),
                    ('25 ns vs 50 ns (600 vs 300 bunches)', 5386, 4246),
                    ('25 ns vs 8b4e (similar number of bunches)', 5386, 4525),
                    ('25 ns - 600b vs 2200b (2x48bpi)', 5386, 5393),
                    ('25 ns - 2040b 72bpi vs 2200 2x48bpi', 5219, 5393)]
    for comparison in comparison_fill_list:
        title = comparison[0]
        top_plot = folder_compar_fills + '/'+ 'arc_avg_vs_mod_fill%d'%comparison[1]
        bottom_plot = folder_compar_fills + '/'+ 'arc_avg_vs_mod_fill%d'%comparison[2]

        fid_tex_complete.write(r'''
                \begin{figure}[p]
                \centering
                \textbf{\Large %s\\}\par\medskip
                \vspace*{1cm}
                \includegraphics[height=.7\textheight,trim={1.5cm 0cm 7.5cm 0cm},clip]{%s}
                \includegraphics[height=.7\textheight,trim={1.5cm 0cm 1.5cm 0cm},clip]{%s}
                \end{figure}
                '''%(title, top_plot, bottom_plot))



    #close tex file
    fid_tex_complete.write(texchamtab.end_latex_file)




import subprocess as sp
sp.call(('pdflatex -output-directory=%s %s'%(latex_folder, latex_folder+'/'+ latex_filename)).split())
# sp.call(('bibtex  %s'%(latex_filename.replace('.tex', '.aux'))).split())
# sp.call(('pdflatex -output-directory=%s %s'%(latex_folder, latex_folder+'/'+ latex_filename)).split())
# sp.call(('pdflatex -output-directory=%s %s'%(latex_folder, latex_folder+'/'+ latex_filename)).split())



    # hl_string = '' 
    # hl_string_offset = ''
    # for sector in HL.sector_list():
    #     hl_string+=", %.1f"%(main_dict[moment]['heat_load']['arc_averages']['S'+str(sector)][i_fill])
    #     hl_string_offset +=", %.1f"%(main_dict[moment]['hl_subtracted_offset']['arc_averages']['S'+str(sector)][i_fill])
    

    #print 'Fill %d, %s, %db, %.2fe11p/b'%(filln, tag, n_bunches, bunch_intensity_avg/1e11)+hl_string
    #print 'offset Fill %d, %db, %.2fe11p/b'%(filln, n_bunches, bunch_intensity_avg/1e11)+hl_string_offset

