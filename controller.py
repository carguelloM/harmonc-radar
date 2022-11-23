## All imports
import os
import sys
import bb_api
import vsg_api
import pandas as pd
import numpy as np
import traceback
import csv, re
from matplotlib import pyplot as plt
import math
import time



print("**Imports Completed\n")
#############################
# Globals
#############################
dir = 'C:\\Users\\Cesar\\Dropbox (Dartmouth College)\\harmonic-radar\\raw-data\\'

#############################
# Functions
#############################
def determine_frequencies(dev_handle, reading):
    
    query = bb_api.bb_query_trace_info(dev_handle)
    data = reading['max']
    
    to_return = list()
    
    for idx in range (len(data)):
        
        bin_start = query['start_freq'] +  query['bin_size']*idx
        bin_stop = bin_start + query['bin_size']
        
        to_return.append({'capture_frequency':bin_start,'reading':data[idx]})
        
    return to_return   


#############################
# Get Frequency returns a frequency power/array 
## The good Val, so far
    #bandwith = 100 MHZ
    #ref = -70/depending on rwb,bwb
    #rwb = 300 khz (Beatrice had 3 Khz before)
    #bwb = 300 khz (Beatrice had 3 khz before)
    #swp_time= 14 ms --- 30ms
#############################
def get_frequency_reading_wide(handle_analyzer, read_frequency, name):
    '''
    This will not read the harmonic, it will only look at the frequency sent as parameter. The third parameter
    type of collection is more to determine whether to get the max value close to the requested frequency or the 
    frequency at exactly the value. For Single reading measurements max makes more sense whether for range measurements,
    frequency at value makes more sense. 
    '''

    # analyzer variables
    bandwidth = 100e6 # the size of the zoom window, this has to vary with the spacing between tones (10.0e6)
    ref_level = -70 # how low should the floor be zoomed to? (-50 except for frequency sweep)

    ## storage variables
    fileName = dir + name

    # re-configure 
    bb_api.bb_configure_center_span(handle_analyzer, read_frequency, bandwidth)
    bb_api.bb_configure_level(handle_analyzer, ref_level, bb_api.BB_AUTO_ATTEN)
    bb_api.bb_configure_gain(handle_analyzer, bb_api.BB_AUTO_GAIN)
    bb_api.bb_configure_sweep_coupling(handle_analyzer, 300.0e3, 300.0e3, 0.015, bb_api.BB_RBW_SHAPE_FLATTOP, bb_api.BB_NO_SPUR_REJECT)
    bb_api.bb_configure_acquisition(handle_analyzer, bb_api.BB_AVERAGE, bb_api.BB_LOG_SCALE)
    bb_api.bb_configure_proc_units(handle_analyzer, bb_api.BB_POWER) #they recommend/use BB_POWER
    
    # initiate
    msg = "Acquiring Spectrum- Centered at: " + str(read_frequency) + '\n'
    print(msg)
    bb_api.bb_initiate(handle_analyzer, bb_api.BB_SWEEPING, 0)
    query = bb_api.bb_query_trace_info(handle_analyzer)
    
    sweep_size = query["trace_len"]
    start_freq = query["bin_size"]
    bin_size = query["start"]
    
    print("Acquisition Completed...")
    tmp_reading = bb_api.bb_fetch_trace_32f(handle_analyzer, sweep_size)
    
    print("Saving Data to file..")
    np.savetxt(fileName, tmp_reading['trace_min'], delimiter=",")
   
    print("Data Saved")
    return

#############################
# start
#############################
# Open devices
#handle_gen = vsg_api.vsg_open_device()["handle"]
handle_analyzer = bb_api.bb_open_device()["handle"]

print("**Succesful Conection to Devices")

val = 0
while val == 0:
    device = input("Device:")
    if device == 'quit':
        break
    range = input("Range:")
    name = device + "_" + range + "_cm" 
    get_frequency_reading_wide(handle_analyzer,4.7e9, name)
#############################
# Close connection
#############################

# Stop waveform
##bb_api.bb_abort(handle_analyzer)
#print("**Waveform Aborted")

# Done with device
#vsg_api.vsg_close_device(handle_gen)
bb_api.bb_close_device(handle_analyzer)
print("Devices closed")
