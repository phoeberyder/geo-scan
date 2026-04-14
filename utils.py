from skyfield.api import EarthSatellite, wgs84, load
import numpy as np
import csv

def tle_collator(filename):
    '''
    Takes csv file of tles and makes them into list of tles
    
    Input:
        filename: path to csv file
    
    Output:
        list of tles
    '''

    with load.open(filename, mode='r') as f:
        data = list(csv.DictReader(f))
    ts = load.timescale()
    sat_list = [EarthSatellite.from_omm(ts, fields) for fields in data]
    return sat_list

def range_finder_general(norad_id):
    lovell = wgs84.latlon(53.2365, -2.3087)
    ts = load.timescale()
    t = ts.utc(2025, 11, 6, 0, 3)
    sats = tle_collator('active_sats_051125.csv')
    for satellite in sats:
        if satellite.model.satnum == norad_id:
            target = satellite
    sat_pos = target.at(t).position.km

    # Transmitter and receiver locations
    mhr = wgs84.latlon(42.6, 288.5)
    lovell = wgs84.latlon(53.2365, -2.3087)

    tx_pos = mhr.at(t).position.km
    rx_pos = lovell.at(t).position.km

    # Distances
    d_tx_sat = np.linalg.norm(sat_pos - tx_pos)
    d_sat_rx = np.linalg.norm(sat_pos - rx_pos)
    d_tx_rx = np.linalg.norm(tx_pos - rx_pos)

    difference_rx = (target - lovell)
    difference_tx = (target - mhr)

    topocentric_rx = (difference_rx.at(t))
    topocentric_tx = (difference_tx.at(t))

    _, _, the_range, _, _, range_rate = topocentric_rx.frame_latlon_and_rates(lovell)
    _, _, the_range_tx, _, _, range_rate_tx = topocentric_tx.frame_latlon_and_rates(mhr)
    rr = range_rate_tx.m_per_s/2 + range_rate.m_per_s/2


    # Bistatic range
    bistatic_range = d_tx_sat + d_sat_rx - d_tx_rx
    return bistatic_range, rr

def peak_finder_general(range_sample, resample_number, data):
    slice_general = data[:, range_sample:range_sample+1]
    peak_index = np.argmax(slice_general)
    return np.linspace(-0.315, 0.315, resample_number)[peak_index]

def offset_calculator(norad_id, start_min, azimuth, catalog, scan_gap_large, central_norad_id):
    ts = load.timescale()
    # t = ts.utc(2026, 11, 6, 0, 0)
    minute = start_min
    out_arr = []
    lovell = wgs84.latlon(53.2365, -2.3087)
    sats = tle_collator(catalog)
    x = 0.0525
    pointing_az_list = []
    pointing_el_list = []
    for i in range(7):
        # print(minute)
        t = ts.utc(2025, 11, 6, 0, minute)

        for satellite in sats:
            if satellite.model.satnum == norad_id:
                target = satellite
            if satellite.model.satnum == central_norad_id:
                central = satellite

        

        tar_az, tar_el, yar_rg = az_el_and_range(target, t, lovell)
        cent_az, cent_el, fsjdshjdsbhj = az_el_and_range(central, t, lovell)
        # print(tar_az, cent_az)
        if scan_gap_large == True:
            if i==0:
                point_az = cent_az - (6*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (6*x)
                pointing_el_list.append(point_el)
            if i==1:
                point_az = cent_az - (4*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (4*x)
                pointing_el_list.append(point_el) 
            if i==2:
                point_az = cent_az - (2*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (2*x)
                pointing_el_list.append(point_el)
            if i==3:
                point_az = cent_az - (0*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (0*x)
                pointing_el_list.append(point_el) 
            if i==4:
                point_az = cent_az + (2*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el + (2*x)
                pointing_el_list.append(point_el)  
            if i==5:
                point_az = cent_az + (4*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el + (4*x)
                pointing_el_list.append(point_el) 
            if i==6:
                point_az = cent_az + (6*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el + (6*x)
                pointing_el_list.append(point_el) 
        else:
            print('small')
            if i==0:
                point_az = cent_az - (3*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (3*x)
                pointing_el_list.append(point_el)
            if i==1:
                point_az = cent_az - (2*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (2*x)
                pointing_el_list.append(point_el) 
            if i==2:
                point_az = cent_az - (1*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (1*x)
                pointing_el_list.append(point_el) 
            if i==3:
                point_az = cent_az - (0*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el - (0*x)
                pointing_el_list.append(point_el)
                print()
            if i==4:
                point_az = cent_az + (1*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el + (1*x)
                pointing_el_list.append(point_el)  
            if i==5:
                point_az = cent_az + (2*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el + (2*x)
                pointing_el_list.append(point_el) 
            if i==6:
                point_az = cent_az + (3*x)
                pointing_az_list.append(point_az) 
                point_el = cent_el + (3*x)
                pointing_el_list.append(point_el)    

        if azimuth==True:
            out_arr.append(np.round(tar_az, 4))
        else:
            out_arr.append(np.round(tar_el, 4))
        minute += 1
    if azimuth==True:
        out_arr = [out_arr[j]-pointing_az_list[j] for j in range(7)]
    else:
        out_arr = [out_arr[j]-pointing_el_list[j] for j in range(7)]
    return out_arr