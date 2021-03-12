"""
Created Time: Aug 8 17:11:56 2019

@author: Haoran Zhao


Errata:
1. Correct the K,C,R,S,X,Y 
Origin:
C = lines[22][18:-1]
K = lines[21][19:-1]
R = lines[19][13:-1]
S = lines[20][13:-1]
X = lines[13][13:-1]
Y = lines[14][13:-1]

Modified:
K = lines[22][18:-1]
C = lines[8][19:-1]
R = lines[20][13:-1]
S = lines[19][13:-1]
X = lines[6][13:-1]
Y = lines[7][13:-1]

@2020 May-4 by Jianming TONG



2. Correct the configuration: read from MAERI_config_<layerType>.txt
Origin:
part 1:
parser.add_argument("mRNA_output_file", help="e.g. DNN-vgg_model-CONV2_MAERI-MS-512-DSW-128-RSW-256_Opt-performance.txt ",type = str)

part 2:
with open(args.mRNA_output_file,"r") as f:
    lines = f.readlines()
    
Model_Name_ = lines[0][12:-1]
Layer_Type_ = lines[1][12:-1]
Layer_Number_ = lines[2][14:-1]   


# make sure two input file match
assert(Model_Name == Model_Name_)
assert(Layer_Type == Layer_Type_)
assert(Layer_Number == Layer_Number_)


T = []
T_C = []
T_K = []
T_R = []
T_S = []
T_X = []
T_Y = []
Util = []
Stat = [T_K, T_C, T_R, T_S, T_X, T_Y]
Name = ['T_K',"T_C", 'T_X', 'T_Y', "T_X'", "T_Y'"]

for i in range(len(lines)):
    if(re.search('Tile',lines[i])):
        T.append((lines[i],lines[i+1]))

for tile in T:
    for i in range(len(Stat)):       
        index1 = re.search(Name[i],tile[0])
        temp = tile[0][index1.end() + 3]
        k = 1
        while(tile[0][index1.end() + 3 + k] >= '0' and tile[0][index1.end() + 3 + k] <= '9'):
            temp += tile[0][index1.end() + 3 + k]
            k += 1
        Stat[i].append(temp)
        
    index2 = re.search('rate',tile[1])
    temp = tile[1][index2.end() + 2]
    k = 1
    while(tile[1][index2.end() + 2 + k] != '\n'):
        temp += tile[1][index2.end() + 2 + k]
        k += 1
    Util.append(temp)

Util_float = [float(i) for i in Util]
maxindex = np.argmax(Util_float)



Modified:



@2020 May 10 by Jianming TONG



Function:
    Arguments: 
        original NN model parameter file 
        mRAN output file
    Return:
        Layer configuration file

Usage:
    e.g. python parser.py Model_parameter_2.txt DNN-vgg_model-CONV2_MAERI-MS-512-DSW-128-RSW-256_Op
t-performance.txt
"""


import re
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("original_file", help="e.g. Model_parameter_2.txt",type = str)
parser.add_argument("mRNA_output_file", help="e.g. Maeri_config_CONV1.txt ",type = str)
args = parser.parse_args()

# Read the original parameter file, get C, K, R,S ,X ,Y and model name, layer type, layer number.

with open(args.original_file,"r") as f:
    lines = f.readlines()
    
Model_Name = lines[0][13:-1]
Layer_Type = lines[1][13:-1]
Layer_Number = lines[2][15:-1]
K = lines[22][18:-1]
C = lines[8][18:-1]
R = lines[20][13:-1]
S = lines[19][13:-1]
X = lines[6][12:-1]
Y = lines[7][12:-1]


# Read mRNA output file, get T_K, T_C, T_R, T_S, T_X, T_Y for all mapping strategys
# Then choose the strategy with highest average utilization

with open(args.mRNA_output_file,"r") as f:
    lines = f.readlines()
    
T_K = lines[15][6:-1]
T_C = lines[14][6:-1]
T_R = lines[12][6:-1]
T_S = lines[13][6:-1]
T_X = lines[18][7:-1]
T_Y = lines[17][7:-1]


# Create output File
with open(Model_Name + '_' + Layer_Type + Layer_Number + '.m', 'w') as f:
    f.write('K ' + K + ' ' + T_K + '\n')
    f.write('C ' + C + ' ' + T_C + '\n')
    f.write('R ' + R + ' ' + T_R + '\n')
    f.write('S ' + S + ' ' + T_S + '\n')
    f.write('X ' + X + ' ' + T_X + '\n')
    f.write('Y ' + Y + ' ' + T_Y + '\n')
    

        
