#!/bin/bash
# clone mRNA & MAERI
git clone https://github.com/georgia-tech-synergy-lab/mRNA
git clone https://github.com/georgia-tech-synergy-lab/MAERI
# add edit permit
chmod 777 simulation_framework.tar.xz
# extract
tar xvf simulation_framework.tar.xz
# setup a directory in mRNA to prepare Convolution Layer for test
mkdir ./mRNA/Input/testLayer
# copy energy configuration file into testLayer
cp ./simulation_framework/Config_file.txt ./mRNA/Input/testLayer/
# copy wrapper.py & parser.py into the mRNA/Input/xxxNet directory
cp ./simulation_framework/parser.py ./mRNA/Input/alexnet/
cp ./simulation_framework/parser.py ./mRNA/Input/googlenet/
cp ./simulation_framework/parser.py ./mRNA/Input/resnet/
cp ./simulation_framework/parser.py ./mRNA/Input/rnn/
cp ./simulation_framework/parser.py ./mRNA/Input/squeezenet/
cp ./simulation_framework/parser.py ./mRNA/Input/vggnet/
cp ./simulation_framework/parser.py ./mRNA/Input/testLayer/
cp ./simulation_framework/wrapper.py ./mRNA/Input/alexnet/
cp ./simulation_framework/wrapper.py ./mRNA/Input/googlenet/
cp ./simulation_framework/wrapper.py ./mRNA/Input/resnet/
cp ./simulation_framework/wrapper.py ./mRNA/Input/rnn/
cp ./simulation_framework/wrapper.py ./mRNA/Input/squeezenet/
cp ./simulation_framework/wrapper.py ./mRNA/Input/vggnet/
cp ./simulation_framework/wrapper.py ./mRNA/Input/testLayer/
# copy the MAERI compiler into the ./MAERI/
cp -r ./simulation_framework/compiler ./MAERI/
echo "install success"