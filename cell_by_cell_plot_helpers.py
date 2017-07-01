import LHCMeasurementTools.LHC_Heatloads as hl
import numpy as np



def swap_even_odd(vect):
    temp_list = []
    for ii in xrange(len(vect)//2):
        temp_list.append(vect[2*ii+1])
        temp_list.append(vect[2*ii])
    return np.array(temp_list)


def sample_and_sort_cell_by_cell(cell_by_cell_db_dictionary, t_ref, t_sample_h, t_offset_h):
    
    hid = cell_by_cell_db_dictionary

    sectors = hl.sector_list()
    dict_hl_cellbycell = {}
    for i, s in enumerate(sectors[:]):

        sect_str = str(s)
        R_part = 'R'+sect_str[0]
        L_part = 'L'+sect_str[1]

        # Find values at t_sample_h and t2 for each cell.
        val1 = []
        cells = []
        for cell in hid.keys():
            if '_D2' in cell or '_D3' in cell or '_D4' in cell or '_Q1' in cell:
                continue
            if R_part not in cell and L_part not in cell:
                continue
            try:
                ind1 = np.argmin(np.abs((np.array(hid[cell].t_stamps) - t_ref)/3600 - t_sample_h))
            except ValueError as e:
                print('Got Error %s, skipping cell %s' % (e, cell))
                continue
            cellname = cell.split('_')[1]+'_'+cell.split('.POSST')[0][-1]
            if int(cellname[:2])<11: continue # skip LSS and DS

            #~ if cellname=='11L1_3': print cell, cellname
            cells.append(cellname)


            # remove offset
            if t_offset_h is not None:
                ind_offset = np.argmin(np.abs((np.array(hid[cell].t_stamps) - t_ref)/3600 - t_offset_h))
                val_offset = float(hid[cell].values[ind_offset])
                offset_info = ', no beam at %.2fh'%t_offset_h
            else:
                val_offset = 0.
                offset_info = ''

            val1.append(float(hid[cell].float_values()[ind1]) - val_offset)

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

        cells = np.append(cells_rip, cells_lip)
        val1 = np.append(val1_rip, val1_lip)
        
        dict_hl_cellbycell[s] = {'cell_names':cells, 'heat_loads':val1}
        
    return dict_hl_cellbycell
    
def extract_and_compute_extra_fill_data(fill_dict, t_ref, t_sample_h, thresh_bint=3e10):
    
    from LHCMeasurementTools.LHC_FBCT import FBCT
    from LHCMeasurementTools.LHC_BCT import BCT
    from LHCMeasurementTools.LHC_BQM import blength
    from LHCMeasurementTools.LHC_Energy import energy

    import HeatLoadCalculators.impedance_heatload as ihl
    import HeatLoadCalculators.synchrotron_radiation_heatload as srhl
    import HeatLoadCalculators.FillCalculator as fc


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

    hl_imped_sample = hl.magnet_length['AVG_ARC'][0]*np.interp(t_sample_h, (hl_imped_fill.t_stamps-t_ref)/3600,  hl_imped_fill.heat_load_calculated_total)
    hl_sr_sample = hl.magnet_length['AVG_ARC'][0]*np.interp(t_sample_h, (hl_imped_fill.t_stamps-t_ref)/3600,  hl_sr_fill.heat_load_calculated_total)

    intensity_b1 = np.interp(t_sample_h, (bct_bx[1].t_stamps-t_ref)/3600, bct_bx[1].values)
    intensity_b2 = np.interp(t_sample_h, (bct_bx[2].t_stamps-t_ref)/3600, bct_bx[2].values)
    
    n_bunches_b1 = np.sum(fbct_bx[1].nearest_older_sample(t_sample_h*3600+t_ref)>thresh_bint)
    n_bunches_b2 = np.sum(fbct_bx[1].nearest_older_sample(t_sample_h*3600+t_ref)>thresh_bint)
    
    energy_GeV = energy(fill_dict, beam=1).nearest_older_sample(t_sample_h*3600+t_ref)
        
    return intensity_b1, intensity_b2, n_bunches_b1, n_bunches_b2, energy_GeV, hl_imped_sample, hl_sr_sample
    
    
    
