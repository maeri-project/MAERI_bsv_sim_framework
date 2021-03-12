"""
Created Time: Aug 9 9:51:56 2019
@author: Haoran Zhao

Errata:
1. fix calling parser.py
Origin:

Prefix = 'DNN-'
model = modelname + '-' + layertype + layernumber
MAERI ='_MAERI-MS-' + ms + '-DSW-' + dbw + '-RSW-' + rbw
Endfix ='_Opt-performance.txt'
mrna = Prefix + model + MAERI + Endfix

Modified:
Prefix = 'Maeri_config_'
Endfix ='.txt'
mrna = Prefix + layertype + layernumber + Endfix

@2020 May-10 by Jianming TONG

Function:
   Arguments: 
       filename: original cnn layer info
       ms: number of Multiply Switches
      dbw: Distrbution Tree Bandwidth
      rbw: ART Bandwidth
   Return:
       Layer configuration file

Usage:
   e.g. python3 wrapper.py  Model_parameter_2.txt 512 128 256
"""

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="e.g. Model_parameter_2.txt",type = str)
parser.add_argument("ms", help="The number of Multiplier Switches",type = str)
parser.add_argument("dbw", help="MAERI Distribution Tree TopBandwidth",type = str)
parser.add_argument("rbw", help="MAERI ART TopBandwidth",type = str)

args = parser.parse_args()


filename = args.filename
ms = args.ms
dbw = args.dbw
rbw = args.rbw

cmrna = '../../MAERI_Mapper -model_para={filename} -show_energy -config_file="Config_file.txt" -dn_bw={dbw} -rn_bw={rbw} -num_ms={ms} -performance -genconfig'
os.system(cmrna.format_map(vars()))

with open(filename,"r") as f:
    lines = f.readlines()
    
modelname = lines[0][13:-1]
layertype = lines[1][13:-1]
layernumber = lines[2][15:-1]

Prefix = 'Maeri_config_'
Endfix ='.txt'
mrna = Prefix + layertype + layernumber + Endfix

cchmod = 'chmod 777 {mrna}'
os.system(cchmod.format_map(vars()))

parser = 'parser.py'
cgen = 'python3 {parser} {filename} {mrna}'
os.system(cgen.format_map(vars()))

