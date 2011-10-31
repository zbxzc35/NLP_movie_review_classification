#!/bin/bash


# usage ./binaryRatingSameUsers.sh binaryRatingSameUsers.model (test_file.txt) (output_file.txt)
# (test_file.txt) 	- contains the input movie reviews
# (output_file.txt)	- test_file.txt with predictions inserted




wekapath=/home/cs4705/bin/weka-3-6-3

export PYTHONPATH=$PYTHONPATH:/home/cs4705/nltk-2.0b5/

python binary4.py $2 binarySameUsersTest.arff

echo -e '\Classifying Input Data using Model...\n'

#java -Xmx2560M -cp $wekapath/weka.jar weka.classifiers.bayes.NaiveBayes -T author_test.arff -l $1 -p 0

java -Xmx2560M -cp $wekapath/weka.jar weka.filters.supervised.attribute.AddClassification -remove-old-class -classification -serialized $1 -i binarySameUsersTest.arff -o binarySameUsers_predicted.arff -c last

echo -e '\nBuilding output file...\n'

python final_binary.py binarySameUsers_predicted.arff $2 $3

echo -e '\nOutput file build complete\n'
