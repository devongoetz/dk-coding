#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:06:54 2018

@author: devongoetz
"""
# DK Coding Challenge
# Devon Goetz
# 18 Jan 2018

def load_data(filename):
    """
    Reads file.
    
    Parameters:
        filename: name of file (string)
        
    Returns:
        datafile: a list of lists (for this data, of the form
                                   [[timestamp], [ax], [ay], [az], [wx], [wy], [wz]])
    """
    timestamp = []
    ax = []
    ay = []
    az = []
    wx = []
    wy = []
    wz = []
    
    file = open(filename)
    line = file.readlines()
    
    for i in line:
        splitline = i.split(',')
        timestamp.append(int(splitline[0]))
        ax.append(float(splitline[1]))
        ay.append(float(splitline[2]))
        az.append(float(splitline[3]))
        wx.append(float(splitline[4]))
        wy.append(float(splitline[5]))
        bad_wz = splitline[6]
        good_wz = bad_wz.replace('\n','')
        wz.append(float(good_wz))
        
    datafile = [timestamp, ax, ay, az, wx, wy, wz]
    return datafile
    


def searchContinuityAboveValue(data, indexBegin, indexEnd, threshold, winLength):
    """
    from indexBegin to indexEnd, search data for values that are higher than threshold.
    Return the first index where data has values that meet this criteria
    for at least winLength samples.
    
    Parameters:
        data: a list of data values (one of the columns from our large swing file)
        indexBegin/indexEnd: indices for a desired range of numbers (ints)
        threshold: number above which the data must be (float)
        winLength: number of samples for which data must be above threshold (int)
        
    Returns:
        firstindex: the first index at which the data has been above treshold for winLength (int)
    """
    above = []
    while len(above) < winLength:
        for i in range(indexBegin, indexEnd+1): #add one in order to examine data at indexEnd
            if data[i] > threshold:
                above.append(i) #creates list of indices
                if len(above) >= winLength:               
                    firstindex = above[0]
                    return firstindex
            else:
                above = [] #resets above to empty if the next index is too small, so we only have a list of consective indices



def backSearchContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """
    from indexBegin to indexEnd (where indexBegin is larger than indexEnd),
    search data for values that are higher than thresholdLo and lower than thresholdHi.
    Return the first index where data has values that meet this criteria
    for at least winLength samples.
        
    Parameters:
        data: a list of data values (one of the columns from our large swing file)
        indexBegin/indexEnd: indices for a desired range of numbers (ints)
        thresholdLo/thresholdHi: numbers between which the data must be (floats)
        winLength: number of samples for which data must be above threshold (int)
        
    Returns:
        firstindex: the first index at which the data has been between tresholds for winLength (int)
    """
    between = []
    while len(between) < winLength:
        for i in range(indexBegin, indexEnd-1, -1): #subtract one to examine data at indexEnd
            if thresholdHi > data[i] > thresholdLo:
                between.append(i) #creates list of indices
                if len(between) >= winLength:               
                    firstindex = between[0]
                    return firstindex
            else:
                between = [] #resets between to empty so we only have a list of consective indices


def searchContinuityAboveValueTwoSignals(data1, data2, indexBegin, indexEnd, threshold1, threshold2, winLength):
    """
    from indexBegin to indexEnd, search data1 for values that are
    higher than threshold1 and also search data2 for values that are
    higher than threshold2. Return the first index where both data1 and data2
    have values that meet these criteria for at least winLength samples.
    
    Parameters:
        data1/data2: lists of data values (two of the columns from our large swing file)
        indexBegin/indexEnd: indices for a desired range of numbers (ints)
        threshold1/threshold2: numbers above which the data must be (floats)
        winLength: number of samples for which data must be above threshold (int)
        
    Returns:
        firstindex: the first index at which the data has been between tresholds for winLength (int)
    """
    above = []
    while len(above) < winLength:
        for i in range(indexBegin, indexEnd+1):
            if (data1[i] > threshold1) and (data2[i] > threshold2):
                above.append(i) #list of indices
                if len(above) >= winLength:               
                    firstindex = above[0]
                    return firstindex
            else:
                above = [] #resets above for continuity


def searchMultiContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """
    from indexBegin to indexEnd, search data for values that are
    higher than thresholdLo and lower than thresholdHi.
    Return the the starting index and ending index of all continuous
    samples that meet this criteria for at least winLength data points.
    
    Parameters:
        data: a list of data values (one of the columns from our large swing file)
        indexBegin/indexEnd: indices for a desired range of numbers (ints)
        thresholdLo/thresholdHi: numbers between which the data must be (floats)
        winLength: number of samples for which data must be above threshold (int)
        
    Returns:
        indices: the first and last indices at which the data has been between tresholds for winLength
                 (a list of tuples)
    """
    between = []
    indices = []
    for i in range(indexBegin, indexEnd+1):
        if thresholdHi > data[i] > thresholdLo:
            between.append(i) #creates list of indices
            if len(between) >= winLength:
                firstindex = between[0]
                lastindex = between[-1]
        else:
            if len(between) >= winLength: #if there is a section of data that fits our parameters
                  indexpair = (firstindex, lastindex)
                  indices.append(indexpair)
            between = [] #resets between to empty so we only have a list of consective indices
    return indices



### Challenge Question: When is impact?
#datafile = load_data('latestSwing.csv')
##I think that the a columns are acceleration in each direction and
##the w columns are angular speed in each direction,
##meaning that when impact occurs, angular speed in the x direction 
##(assuming a mostly planar swing) is at a zero
#wx = datafile[3]
#our_index = backSearchContinuityWithinRange(wx, len(wx)-1, 1, -0.02, 0.02, 10)
##I've made some assumptions based upon my lack of familiarity with the dataset,
##including that the winLength of 10 is enough to eliminate any momentary pauses in the swing
##and that the 0.02 range around 0 is enough to capture the actual time at which
##angluar speed is 0
#print(our_index)
##The answer I got is 194.







