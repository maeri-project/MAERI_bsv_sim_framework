import os

print(os.path.abspath(__file__))
print(os.getcwd())
print(os.path.dirname(os.getcwd())+"/MAERI/")
MAERI_Path = os.path.dirname(os.getcwd())+"/mRNA/"
print(MAERI_Path)


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
