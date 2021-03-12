#######################################################################################################################
#　control part of end-to-end framework for MAERI accelerator
#  please refer to the readme.md for more detail of this control part.
#  Jianming TONG (jianming.tong@gatech.edu)
#######################################################################################################################
import os
import math
from pathlib import Path
#######################################################################################################################
#################### user code here


#################### MAERI Configuration:
Number_Multipler_Switches = 128
Collection_Bandwidth = 16
Distribution_Bandwidth = 16

#################### Layer Configuration:
from keras.applications.vgg16 import VGG16
model = VGG16()
CONVLayerIdx = 1 # CONV 1. e.g. change to 13 if select CONV13

#################### Path configuration:
# If change mRNA & MAERI location, pls modify the following path.
# mRNA_path =  '<path to mRNA>/mRNA/'
# MAERI_Path = '<path to MAERI>/MAERI/'
mRNA_path =  os.path.dirname(os.getcwd())+"/mRNA/"
MAERI_Path = os.path.dirname(os.getcwd())+"/MAERI/"

#######################################################################################################################
#################### user code ends

#######################################################################################################################
#################### read name

def readLayerName(LayerIdx, model):
    name_suffix = model.layers[LayerIdx].name
    name = "temp"
    for i in range(len(name_suffix)):
        if name_suffix[i] == '_':
            temp = name_suffix[:i]
            if temp[:5] == "block":
                temp = name_suffix[i+1:]
                if temp[:len(temp) - 1] == "conv":
                    temp = temp[:len(temp) - 1]
            if temp != 'zero':
                name = temp
    return name


#######################################################################################################################
#################### read mRNA input model parameter
# modelParameterPath should have a '/' at the end of the line
# modelName

def write_mRNA_input_model_parameter(layerParameterPath, layerName, layerParameterFileType,
                                     layerType, layerIdx, N, C, X, Y, K, R, S, O_y, O_x, stride):
   

    outputFileName_mRNA = layerName + '_' + layerType + str(layerIdx) + '.m'

    with open(layerParameterPath + layerName + layerParameterFileType, 'w') as f:
        f.write('Model_Name = ' + layerName + '\n')
        f.write('Layer_Type = ' + layerType + '\n')
        f.write('Layer_Number = ' + str(layerIdx) + '\n\n')
        f.write('Input_parameter {' + '\n')
        f.write('  input_batch = ' + str(N) + '\n')
        f.write('  input_x = ' + str(X) + '\n')
        f.write('  input_y = ' + str(Y) + '\n')
        f.write('  input_channel = ' + str(C) + '\n')
        f.write('}' + '\n\n')
        f.write('Output_parameter {' + '\n')
        f.write('  output_batch = ' + str(N) + '\n')
        f.write('  output_x = ' + str(O_x) + '\n')
        f.write('  output_y = ' + str(O_y) + '\n')
        f.write('  output_channel = ' + str(K) + '\n')
        f.write('}' + '\n\n')
        f.write('Weight_parameter {' + '\n')
        f.write('  weight_x = ' + str(R) + '\n')
        f.write('  weight_y = ' + str(S) + '\n')
        f.write('  weight_channel = ' + str(C) + '\n')
        f.write('  weight_number = ' + str(K) + '\n')
        f.write('  weight_stride = ' + str(stride[0]) + '\n')
        f.write('}' + '\n\n')
        f.write('Hidden_parameter {' + '\n')
        f.write('  hidden_x = ' + '0' + '\n')
        f.write('  hidden_y = ' + '0' + '\n')
        f.write('  hidden_channel = ' + '0' + '\n')
        f.write('}' + '\n\n')
    f.close()
    return outputFileName_mRNA


#######################################################################################################################
#################### Input Network Model
if __name__=='__main__':
    print(model.summary())  # display the size & number of parameters of each layer of VGG16

    # extract the parameters of all conv layers of neural network
    conv_layer_index = []
    conv_weights = []
    for LayerIdx in range(len(model.layers)):
        temp = readLayerName(LayerIdx, model)
        if temp == "conv" or temp == 'conv2d':
            conv_weights.append(model.layers[LayerIdx].get_weights())
            conv_layer_index.append(LayerIdx)

    layerType = 'conv'
    ######## generate configuration for the first convolution layer of vgg16

    index = CONVLayerIdx
    [batch, height_in, width_in, channel] = model.layers[index].input_shape
    [unused, height_out, width_out, num_kernel] = model.layers[index].output_shape
    [filter_height, filter_width] = model.layers[index].kernel_size
    [stride_x, stride_y] = model.layers[index].strides
    layerIdx = index
    if batch == None:
        batch = 1

    num_ms = Number_Multipler_Switches
    dbw = Distribution_Bandwidth
    cbw = Collection_Bandwidth
    mRNAPath = mRNA_path
    MAERI_Path = MAERI_Path
    layerType = layerType
    layerIdx = layerIdx
    N = batch
    C = channel
    X = width_in
    Y = height_in
    K = num_kernel
    S = filter_width
    R = filter_height
    O_x = width_out
    O_y = height_out
    stride_x = stride_x
    stride_y = stride_y

    layerParameterPath = mRNAPath + 'Input/testLayer/'
    layerName = 'testLayer_parameter' + str(layerIdx)
    layerParameterFileType = '.txt'

    # transform layerType into the format that mRNA can understand
    if layerType == 'conv2d' or layerType == 'conv':
        layerType = 'CONV'
    elif layerType == 'dense':
        layerType = 'FC'
    elif layerType == 'max_pooling2d':
        layerType = 'MAXPOOL'
    elif layerType == 'flatten':
        print('flatten layer should be implemented off-chip')
        quit('flatten')
    else:
        print("please check layerType: available options are 'conv2d','dense','max_pooling2d','flatten' ")

    outputFileName_mRNA = write_mRNA_input_model_parameter(layerParameterPath, layerName,
                                                           layerParameterFileType, layerType, layerIdx,
                                                           N, C, X, Y, K, R, S, O_y, O_x, (stride_y, stride_x))
     
    ###################################################################################################################
    #################### run the mRNA

    os.chdir(layerParameterPath)
    if os.path.exists(outputFileName_mRNA):
        os.system('rm ' + outputFileName_mRNA)
    os.system('python3 ' + 'wrapper.py ' + layerName + layerParameterFileType + ' ' + str(num_ms) + ' ' + str(dbw)
              + ' ' + str(cbw))

    os.chdir(MAERI_Path)
    os.system('cp ' + layerParameterPath + outputFileName_mRNA + ' ' + MAERI_Path + 'compiler/data/')

    # read from output file of mRNA and verify the result
    with open('./compiler/data/' + outputFileName_mRNA, "r") as f1:
        lines = f1.readlines()

    LayerInfo = []
    for lineIdx in lines:
        temp = lineIdx.split()
        temp.pop()
        LayerInfo.append(int(temp.pop()))

    K_verified = LayerInfo[0]
    C_verified = LayerInfo[1]
    R_verified = LayerInfo[2]
    S_verified = LayerInfo[3]
    X_verified = LayerInfo[4]
    Y_verified = LayerInfo[5]

    if K != K_verified or C != C_verified or R != R_verified or S != S_verified or X != X_verified or Y != Y_verified:
        print('Please check the mRNA output file, file type: .m')
        quit('mRNA_output')
    del K_verified, C_verified, R_verified, S_verified, X_verified, Y_verified

    ###################################################################################################################
    #################### get configuration NumVN & VNsize from mRNA configuration.
   
    with open(layerParameterPath + 'Maeri_config_' + layerType + str(layerIdx) + '.txt', "r") as f1:
        lines = f1.readlines()

    VNSz  = lines[20][10:-1]
    NumVN = lines[21][9:-1]

    ###################################################################################################################
    #################### run the MAERI compiler to generate the RN_Config.vmh & Layer_Info.vmh

    os.chdir(MAERI_Path + 'compiler')
    os.system('scons')

    os.chdir(MAERI_Path)
    os.system('rm ' + MAERI_Path + 'RN_Config.vmh')
    os.system('rm ' + MAERI_Path + 'Layer_Info.vmh')
    os.system('./compiler/maeri_compiler ' + str(num_ms) + ' ' + str(VNSz) +
              ' ' + './compiler/data/' + outputFileName_mRNA)

    f = open("AcceleratorConfig.bsv", "w")
    f.write("typedef " + str(dbw) + " DistributionBandwidth;" + "\n")
    f.write("typedef " + str(cbw) + " CollectionBandwidth;" + "\n")
    f.write("typedef " + str(num_ms) + " NumMultSwitches;" + "\n")
    f.close()

