#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:22:47 2020

This program reads text files with lines in this format:
(epoch: 1, iters: 100, time: 0.573) G_GAN: 1.121 G_GAN_Feat: 5.887 G_VGG: 6.070 D_real: 0.696 D_fake: 0.642
If the text file has a header, it is automatically removed

The program extracts the loss values G_GAN, G_GAN_Feat, etc. from a line, 
calculates the average for each epoch, and plots on a graph loss value against epoch.

Usage: python loss_log_plot.py <filename.txt>

@author: owainazam
"""
import sys
import numpy
import matplotlib.pyplot
#Data is of structure:
    #(epoch: 1, iters: 100, time: 0.573) G_GAN: 1.121 G_GAN_Feat: 5.887 G_VGG: 6.070 D_real: 0.696 D_fake: 0.642
#with several lines for epoch: 1, several lines for epoch: 2 etc.

#later, change so that program works in terminal OW 31/03/20
#what about using multiple files? OW 31/03/20
    
def main():
    script = sys.argv[0]
    
    fname = sys.argv[1]
    
    file_obj = open(fname, 'r')
#open file - OW done 31/03/20
    data = file_obj.readlines()
    data_check(data)
    
    data, header = remove_header(data)
    
    check_lines(data)
    
    values_array = make_array(data)
    
    epoch_index_list = []
    
    for idx,line in enumerate(values_array[0:,0]):
        if values_array[idx,0] != values_array[idx-1,0]:
            epoch_index_list.append(idx)

    all_means = [[]]
    all_stddevs = [[]]
    
    for ind,n in enumerate(epoch_index_list):
        ind -= 1 #this avoids epoch_index_list[ind+1] becoming too large.

        means = []
        std_devs = []
        for cols, loss_val in enumerate(values_array[0,0:]):
            mean = numpy.mean(values_array[epoch_index_list[ind]:epoch_index_list[ind+1],cols])
            std_dev = numpy.std(values_array[epoch_index_list[ind]:epoch_index_list[ind+1],cols])

            means.append(mean)
            std_devs.append(std_dev)
            
        all_means.append(means)
        all_stddevs.append(std_devs)
    
    for n in range(2):
        all_means.pop(0)
        all_stddevs.pop(0)
        
    all_means_arr = numpy.array(all_means)
    all_stddevs_arr = numpy.array(all_stddevs)
    
    for i in range(len(all_means_arr[:,0])):
        all_stddevs_arr[i,0] = float(i+1)
        
    #print(all_means_arr)
    #print(all_stddevs_arr)
    
    visualize(all_means_arr,all_stddevs_arr)

    #print(values_array[epoch_index_list[ind]:epoch_index_list[ind+1],1])
    #print('Mean: ', means,'Std_dev: ',std_devs)

def visualize(data1,data2):
    fig = matplotlib.pyplot.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    
    matplotlib.pyplot.plot(data1[:,0],data1[:,1])
    matplotlib.pyplot.plot(data1[:,0],data1[:,2])
    matplotlib.pyplot.plot(data1[:,0],data1[:,3])
    matplotlib.pyplot.plot(data1[:,0],data1[:,4])
    matplotlib.pyplot.plot(data1[:,0],data1[:,5])
    
    ax.errorbar(data1[:,0], data1[:,1], yerr=data2[:,1], label='G_GAN')
    ax.errorbar(data1[:,0], data1[:,2], yerr=data2[:,2], label='G_GAN_Feat')
    ax.errorbar(data1[:,0], data1[:,3], yerr=data2[:,3], label='G_VGG')
    ax.errorbar(data1[:,0], data1[:,4], yerr=data2[:,4], label='D_real')
    ax.errorbar(data1[:,0], data1[:,5], yerr=data2[:,5], label='D_fake')
    
    matplotlib.pyplot.legend()
    
    matplotlib.pyplot.title('Loss_values - averages')
    matplotlib.pyplot.xlabel('Epoch')
    matplotlib.pyplot.ylabel('Average')
    #ave_plot = matplotlib.pyplot.plot(data[:,1])

    fig.tight_layout()
    matplotlib.pyplot.show()
        
    
    
    '''   
    place into data (use readlines) - OW done 31/03/20
    
    first line is the date - remove this from data - OW done 31/03/20
    
    What if there's more than 1 line? - OW can now remove multiple lines from top of file 31/03/20
    
    check that the structure of each line matches the first - use that checking code I have
        #OW checking code checks the number of splits on each line using whitespace separator 01/04/20
    
    produce 3D array - OW done 31/03/20
    '''
    file_obj.close()

def check_lines(data):
    no_of_lines = len(data)
    incorrect_lines = []
    print('Checking lines of data are equivalent before plotting')
    if len(data) <=1: #nothing to check
        print('Only 1 line specified on input. Please add more lines. Returning.')
        return
    else:
        split_line0 = data[0].split()
        number_of_splits = len(split_line0)
        for line in numpy.arange(no_of_lines):
            current_split_line = data[line].split()
            if len(current_split_line) != number_of_splits:
                #print('Line %d does not check: ' % (line))
                incorrect_lines.append(line)
    print('Line checking complete')
    if len(incorrect_lines) > 0:
        print('These lines do not check:', incorrect_lines)
    else:
        print('All lines match')
    
    return
'''
(epoch: 1, iters: 100, time: 0.573) G_GAN: 1.121 G_GAN_Feat: 5.887 G_VGG: 6.070 D_real: 0.696 D_fake: 0.642 
'''

def make_array(data):
    no_of_lines = len(data)
    array = [[]]
    #array = numpy.empty((len(data),6),dtype = float, order='C')

    #for line in numpy.arange(15):
    for line in numpy.arange(no_of_lines):
        first_split = data[line].split(')')
        #print(first_split)
        epoch_int = first_split[0].split(',')[0]
        epoch = float(epoch_int.split()[1])
        
        loss_vals_labels = first_split[1].split()
        G_GAN = float(loss_vals_labels[1]); G_GAN_Feat = float(loss_vals_labels[3])
        G_VGG = float(loss_vals_labels[5]); D_real = float(loss_vals_labels[7])
        D_fake = float(loss_vals_labels[9])
        
        dataline = [epoch, G_GAN, G_GAN_Feat, G_VGG, D_real, D_fake]
        #print(dataline)
        
        array.append(dataline)
    array.pop(0)
    #print(array)
    
    array = numpy.array(array, dtype = float)
    print('Data shown below -', 'Epoch:', loss_vals_labels[0],loss_vals_labels[2],loss_vals_labels[4], \
          loss_vals_labels[6],loss_vals_labels[8])
    print(array)
    
    return array

    
def remove_header(data):
    header = ''
    lines = []
    if 'epoch:' in data[0]:
        return data, ''
    for line in numpy.arange(len(data)):
        if 'epoch:' not in data[line]:
            header = header + data[line]
            lines.append(line)
    data.pop(int(lines[0]))

    return data, header
    

def data_check(data):
    assert len(data) > 0, 'No data present - open a different file'
    assert len(data) > 10, 'Not much data present - open a different file?'
    assert 'epoch:' not in data[0], 'Are title and date present at top of file?'
    
    return
    
if __name__ == '__main__':
    main()
