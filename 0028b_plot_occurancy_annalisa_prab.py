import numpy as np 
import myfilemanager as mfm
import pylab as pl
import mystyle as ms


pl.close('all')

filln_list = [4947, 4958, 4961, 4964, 4979, 4980] 
beam_list = [1,2]
beam_color=['b', 'r']
max_bunches_per_train = 72
delta_sigma_th = 0.25 # we consider 15% of emittance growth
slot_to_be_removed = 100


for ic, beam in enumerate(beam_list):
    
    occurrence_list = max_bunches_per_train*[0] # beams injected in trains of 72 b.
    times_each_bunch_passage = max_bunches_per_train*[0]
    b = np.arange(1, max_bunches_per_train+1, 1)
    
    for filln in filln_list:
        ob = mfm.myloadmat_to_obj('bbb_emi_dict%dB%d.mat'%(filln, beam))
    
        # Check if the bucket vector is sorted
        indexes_sorted = np.argsort(ob.bunch_n)
        if all(np.diff(indexes_sorted)>0):
            bunch_n_sorted = ob.bunch_n
            sigma_v_before_blowup_sorted = ob.sigma_v_before_blowup
            sigma_v_after_blowup_sorted = ob.sigma_v_after_blowup

        else:
            bunch_n_sorted = np.take(ob.bunch_n, indexes_sorted)
            sigma_v_before_blowup_sorted = np.take(ob.sigma_v_before_blowup, indexes_sorted)
            sigma_v_after_blowup_sorted = np.take(ob.sigma_v_after_blowup, indexes_sorted)
        
        bunch_n_sorted = bunch_n_sorted[slot_to_be_removed::]
        sigma_v_before_blowup_sorted = sigma_v_before_blowup_sorted[slot_to_be_removed::]
        sigma_v_after_blowup_sorted = sigma_v_after_blowup_sorted[slot_to_be_removed::]
        
        delta_sigma_v_sorted = sigma_v_after_blowup_sorted-sigma_v_before_blowup_sorted
        delta_sigma_v_sorted = delta_sigma_v_sorted/sigma_v_before_blowup_sorted # percent
        
        pl.figure(beam)
        pl.plot(bunch_n_sorted, delta_sigma_v_sorted, '.')
        pl.title('Beam %d'%beam)
            
        # Identify bunch number    
        bunch_number_along_train = []
        i_count_bunches = 1
        try:
            for i in range(len(bunch_n_sorted)):
                if np.diff(bunch_n_sorted)[i]==1: 
                    bunch_number_along_train.append(i_count_bunches)
                    i_count_bunches+=1
                else: bunch_number_along_train.append(i_count_bunches);i_count_bunches=1
        except: 
             bunch_number_along_train.append(i_count_bunches)
         
        
        # Check blownup bunches
        for ii, delta_sigma in enumerate(delta_sigma_v_sorted):
            if delta_sigma > delta_sigma_th:
                bunch_number = bunch_number_along_train[ii]
                i_occ_list = bunch_number - 1
                occurrence_list[i_occ_list]+=1.
        print 'sono qui'
    
        for ib in b:
            n_same_bunch = bunch_number_along_train.count(ib)
            i_times = ib-1
            times_each_bunch_passage[i_times]  = times_each_bunch_passage[i_times]+n_same_bunch
                
    occurrence_percent = (np.array(occurrence_list)/np.array(times_each_bunch_passage))*100
    
    fig_vlines=pl.figure(beam+10, figsize=(7,6))
    fig_vlines.patch.set_facecolor('w')
    pl.vlines(b, [0], occurrence_percent, linewidth=2.0)
    pl.title(r'%d%% vertical emittance growth B%d'%(delta_sigma_th*100,beam), fontsize=16)
    pl.ylim(0,100)
    pl.xlim(0,75)
    pl.xlabel('Bunches #')
    pl.ylabel('Occurrence [%]')
    pl.grid('on')
    fig_vlines.savefig('plot_Annalisa_PRAB/occurrence_B%d'%(beam), dpi=300)
    
    fig_h=pl.figure(beam+20, figsize=(7,6))
    fig_h.patch.set_facecolor('w')
    

    width = 1.0
    pl.bar(b, occurrence_percent, width, facecolor=beam_color[ic], alpha=0.5, 
             align='center',edgecolor=beam_color[ic])
    pl.xlabel('Bunches #')
    pl.ylabel('Occurrence [%]')
    pl.title(r'%d%% vertical emittance growth B%d'%(delta_sigma_th*100,beam), fontsize=16)
    pl.ylim(0,100)
    pl.xlim(0,75)
    pl.grid('on')
    ms.mystyle_arial(18)
    fig_h.savefig('plot_Annalisa_PRAB/BARPLOT_occurrence_B%d'%(beam), dpi=300)
    
    
        
    


pl.show()
