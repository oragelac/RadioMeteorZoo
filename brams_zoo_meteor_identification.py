# -*- coding: utf-8 -*-
"""
BRAMS Zoo meteor identification algorithm
Created on 9 June 2016

@author: stijnc
"""

import glob
import os
import utils
from datetime import datetime
import pickle

PNG_DIRECTORY = "input/png/"
CSV_DIRECTORY = "input/csv/"
OUTPUT_DIRECTORY = "output/"
MASKSIZE = (595, 864)
DATE = date #20160714

spectrograms = map(os.path.basename,glob.glob(PNG_DIRECTORY+"*.png"))
csv_files = glob.glob(CSV_DIRECTORY+"*.csv")
optimal_nbr_of_counters = {1: 1, #k: optimal_nbr_of_counters
                           2: 2,
                           3: 2,
                           4: 2,
                           5: 3,
                           6: 3,
                           7: 3,
                           8: 3,
                           9: 4,
                           10: 4}
datetime, identifications, volunteers = [], [], []
for spectrogram in spectrograms:
    dt = datetime.strptime(spectrogram[11:24], "%Y%m%d_%H%M")
    #Step 1: read detection file
    detection_files = {}
    for csv_file in csv_files:
        tmp = read_detection_file_per_spectrogram(csv_file,spectrogram)
        if tmp is not None:        
            detection_files[csv_file] = tmp
    #Step 2: run meteor identification algorithm
    threshold_image = calculate_threshold_image(detection_files)
    #Step 3: select regions that are above identification threshold
    nbr_volunteers = len(detection_files)
    if nbr_volunteers > 0 and nbr_volunteers <= 10:
        alpha = optimal_nbr_of_counters[len(detection_files)]
        binary_image = threshold_image[threshold_image.keys()[0]].copy() 
        binary_image[binary_image < alpha] = 0
        binary_image[binary_image >= alpha] = 1
        border_threshold = detect_border(binary_image)
        nbr_identifications = len(border_threshold)
        datetime.append(dt) #datetime
        identifications.append(nbr_identifications) #nbr of identifications
        volunteers.append(nbr_volunteers) #nbr of volunteers checking the file
    else:
        print "[warning] spectrogram %s has %d volunteers" % (spectrogram,nbr_volunteers)

pickle.dump( (datetime,identifications,volunteers), open( "output/pickles/brams_zoo_meteor_identification-"+DATE+".p", "wb" ) ) 