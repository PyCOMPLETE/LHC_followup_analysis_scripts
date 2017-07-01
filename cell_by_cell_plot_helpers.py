
def swap_even_odd(vect):
    temp_list = []
    for ii in xrange(len(vect)//2):
        temp_list.append(vect[2*ii+1])
        temp_list.append(vect[2*ii])
    return np.array(temp_list)








dict_hl_cellbycell = {}
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

        #~ if cellname=='11L1_3': print cell, cellname
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
    
    dict_hl_cellbycell[s] = {'cell_names':cells, 'heat_loads':val1}
    


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
