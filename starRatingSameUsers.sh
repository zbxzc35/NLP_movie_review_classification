#!/bin/bash



# usage ./binaryRatingSameUsers.sh binaryRatingSameUsers.model (test_file.txt) (output_file.txt)
# (test_file.txt) 	- contains the input movie reviews
# (output_file.txt)	- test_file.txt with predictions inserted




wekapath=/home/cs4705/bin/weka-3-6-3

export PYTHONPATH=$PYTHONPATH:/home/cs4705/nltk-2.0b5

python quart_score.py $2 starRatingSameUsersTest.arff

echo -e '\Classifying Input Data using Model...\n'

java -Xmx2560M -cp $wekapath/weka.jar weka.classifiers.functions.SMO -T starRatingSameUsersTest.arff -l $1 -p 0

java -Xmx2560M -cp $wekapath/weka.jar weka.filters.supervised.attribute.AddClassification -remove-old-class -classification -serialized $1 -i starRatingSameUsersTest.arff -o starRatingSameUsers_predicted.arff -c last

echo -e '\nBuilding output file...\n'

python final_star.py starRatingSameUsers_predicted.arff $2 $3

echo -e '\nOutput file build complete\n'
