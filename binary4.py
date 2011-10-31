from __future__ import division
import re
import nltk
import sys

file1=sys.argv[1]		#movie review filename
file2=sys.argv[2]		#output arff file

f1=open(file1)
f2=open(file2,'w')
t1=f1.readlines()

f1.seek(0)
t2=f1.read()

f3=open('senti.txt')		# senti.txt contains the sentiWordnet dictionary
t3=f3.readlines()
t3=t3[24:]
del t3[-1]

dict1=[]			# dict1 is a list which stores words having absolute value of sentiment greater than 0.5
dict2=[]			# dict2 stores the sentiment value corresponding to the word in dict1
for i in t3:
	temp=i.split('\t')
	if(float(temp[2])>0.5 or float(temp[3])>0.5):
		dict1.append(temp[4])
		dict2.append(float(temp[2]) - float(temp[3]))

dict3=[]
for i in dict1:
	temp=re.sub('#.*','',i)
	dict3.append(temp)

final_dict=[]				# final_dict stores the [word,sentiment] pairs
for i,j in enumerate(dict3):
	temp=[j,dict2[i]]
	final_dict.append(temp)

def score(i,final_dict):		# if a particular word is contained in final_dict, then score returns its corresponding sentiment value
	for j in final_dict:		# else if the word is not present then it returns 0
		if(j[0]==i):
			return j[1]
	return 0


################################	ARFF Header	#############################################################
header='@RELATION binary_class'
f2.write(header + '\n')
for i in range(0,len(dict3)+1):
	f2.write('@ATTRIBUTE ' + 'count_' + str(i) + ' NUMERIC' + '\n')
f2.write('@ATTRIBUTE class {0,1}\n')

f2.write('@DATA\n')
###################################################################################################################


for i,j in enumerate(t1):
	l1=[]

	star=re.search('(?<=<star>)\d',j)
       # if(int(star.group(0))>2):
        #        star1=1
        #else: star1=0

	for k in dict3:			# This builds features of the number of times a particular word in the dictionary is present in the review 
		l1.append(str(j.count(k)))
	
	value=0				# value = total positivity or negativity value for a review, calculated by taking the sum of the 
	temp=nltk.word_tokenize(j)
	for k in temp:
		value=value + score(k,final_dict)	

	l1.append(str(value))
	l1.append('?')
	f2.write(','.join(l1) + '\n')
	print 'Writing from review ',i,' to ARFF file'

f1.close()
f2.close()
f3.close()
