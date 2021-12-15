# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 17:25:25 2021

@author: Gianluca


READ ME :
    
    This code is dedicated to show nice images that describe the experiments
    perfomed in November & December on the CNC machine

"""

# import csv files for the different experiments.
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np



directory = "D:\Vibrations-mems-data"

file_a1_0 = directory + "\\" + "resume-ap1-0.csv"
file_a1_5 = directory + "\\" + "resume-ap1-5.csv"
file_a2_0 = directory + "\\" + "resume-ap2-0.csv"
file_a3_0 = directory + "\\" + "resume-ap3-0.csv"
file_a4_0 = directory + "\\" + "resume-ap4-0.csv"
file_a5_0 = directory + "\\" + "resume-ap5-0.csv"
file_a9_0 = directory + "\\" + "resume-ap9-0.csv"


a1_0 = pd.read_csv(file_a1_0)
a1_5 = pd.read_csv(file_a1_5)
a2_0 = pd.read_csv(file_a2_0)
a3_0 = pd.read_csv(file_a3_0)
a4_0 = pd.read_csv(file_a4_0)
a5_0 = pd.read_csv(file_a5_0)
a9_0 = pd.read_csv(file_a9_0)     

a_list = [a1_0,a1_5,a2_0,a3_0,a4_0,a5_0,a9_0]
size_a = len(a_list)
"""
Files that contain chattering :
    
- ap_2 -> 5750 & 6000 RPM
- ap 2.5 -> 5750 & 7000 RPM (où est le fichier 2.5 mm ?)
- ap 4 ->  5750 ( sticking at 6000 RPM)
- ap 5 -> 7500 (sticking ?)
- ap 9 -> 4250, 4500, 5000 RPM

    
"""

chatter_list = [ [2,5750],[2,6000], [4,5750], [4,6000], [5,7500],[6,4250], [6,4500], [6,5000]]
size_chatter = len(chatter_list)

for chatter_num in range(size_chatter):
    chatter = chatter_list[chatter_num]
    chatter_a_val = chatter[0] # Value 'a' when chatter
    chatter_a_RPM = chatter[1] # Value 'RPM' when chatter
    for a_num in range(size_a):
        
        #a_temp = a_list[a_num] # files 'a' to be checked
        
        if a_list[a_num]['A_depth'][0] == chatter_a_val:
            
            # Get to the right line and changes the chatter value
            
            #a_temp.loc[a_temp['RPM'] == chatter_a_RPM, 'Chatter'] = 1
            
            #a_temp['Chatter'] = a_temp['RPM'].apply(lambda x : 1 if x == chatter_a_RPM else 0)
            
        #a_list[a_num] = a_temp # save the change
            
            a_list[a_num]['Chatter'].where(~(a_list[a_num].RPM == chatter_a_RPM), other=1, inplace=True)
        a_list[a_num]['color'] = a_list[a_num]['Chatter'].apply(lambda chatter: 'red' if chatter == 1 else 'blue' )


# Add a color for the points or size
for a_num in range(size_a):
    plt.scatter(a_list[a_num]['RPM'].tolist(), a_list[a_num]['A_depth'].tolist(), color = a_list[a_num]['color'].tolist())
    
    
# Define the ticks that will be shown on the plot    

x_ticks = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000]
x_labels = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000]

plt.xticks(ticks=x_ticks, labels=x_labels)

y_ticks = [0,1,2,3,4,5,6,7]
y_labels = [0,1,2,3,4,5,6,7]

plt.yticks(ticks=y_ticks,labels=y_labels)


# Define the legend 

red_patch = mpatches.Patch(color='red', label = 'Chatter')
blue_patch = mpatches.Patch(color='blue', label = 'No Chatter')
plt.legend(handles=[red_patch,blue_patch],loc='upper left')

# Define the axis labels
plt.title('Discrete SLD')
plt.ylabel('Axial depth of cut [mm]')
plt.xlabel('Spindle speed [RPM]')


fig_name = 'Discrete_SLD.jpeg'

# To save the figure
#plt.savefig(fig_name, dpi='figure')

plt.show()


