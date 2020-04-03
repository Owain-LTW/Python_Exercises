#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:28:45 2020

@author: owainazam

This program extracts case numbers and patient IDs from the beginning of a list of lines.
The number of patients is determined and outputted.

Each line in the input text file needs to have the format: "CaseNumber" _ "PatientID"_ followed by a decription of the data.
This is followed by the data, shown as float values, which completes the line.

The input is a single file.
"""

import sys
import numpy
#from more_itertools import unique_everseen

def main():
    script = sys.argv[0]
    fname = sys.argv[1]
    
    #file_obj = open('features.txt', 'r')
    file_obj = open(fname, 'r')
    
    data = file_obj.readlines()
    
    case_ID_desc = get_case_ID(data)
    
    print('Case numbers:', case_ID_desc[3], 'Patient IDs:', case_ID_desc[4], 'Case descriptions:', case_ID_desc[5])
    #This code below does work (using unique_everseen()). The problem is, some patient IDs are missing.
    #This returns an empty string to the list. unique_everseen then counts blank spaces as one ID, not several OW 31/3/20.
    #So below, would use case_ID[0] and case_ID[1] instead of numbers OW 31/3/20
    #print(numbers[1])
    #print(len(numbers[1]))
    #print(list(unique_everseen(numbers[1])))
    #print(len(list(unique_everseen(numbers[1]))))
    #print(numbers.counter())
    
    file_obj.close()
    
def get_case_ID(data):
    case_no = []
    pat_ID = []
    case_descriptions = []
    count_case_no = 0
    count_pat_ID = 0
    count_descriptions = 0
    
    for num in numpy.arange(len(data)):
        case_ID = data[num].split('_')[0:2]
        case_description = data[num].split('ratio')[0]
        
        case_no.append(case_ID[0])
        pat_ID.append(case_ID[1])
        case_descriptions.append(case_description)
        
        count_case_no = get_count(case_no,count_case_no)
        
        #counts number of DIFFERENT patient IDs. '' count
        count_pat_ID = get_count_gaps(pat_ID,count_pat_ID,case_descriptions) 
        count_descriptions = get_count(case_descriptions,count_descriptions)
    
    return case_no, pat_ID, case_descriptions, count_case_no, count_pat_ID, count_descriptions

def get_count(values, count):
    #print(count)
    if len(values) == 1:
        count += 1
    elif values[-1] != values[-2]:
            count += 1
    return count

def get_count_gaps(values, count, case_description):
    #print(count)
    if len(values) == 1:
        count += 1
    elif values[-1] != values[-2]:
        count += 1
    elif values[-1] == '' and values[-2] == '':
        if case_description[-1] != case_description[-2]:
            count += 1
    return count

main()
#    patient_codes_temp = []
#    patient_codes = []
    
#    for num in numpy.arange(len(data)):
#        patient_codes_temp = data[num][0:13]
#        patient_codes.append(patient_codes_temp)

        #if len(pat_codes) == 1:
        #    count_codes += 1
        #else:
        #    print(num+1, pat_codes, pat_codes[-1], pat_codes[-2])
        #    if pat_codes[-1] != pat_codes[-2]:
        #        count_codes += 1
        #print(count)


    
