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

dict1=[]			# dict1 is a list which stores words having absolute value of sentiment greater than 0.7
dict2=[]			# dict2 stores the sentiment value corresponding to the word in dict1
for i in t3:
	temp=i.split('\t')
	if(float(temp[2])>0.70 or float(temp[3])>0.70):
		dict1.append(temp[4])
		dict2.append(float(temp[2])-float(temp[3]))

dict3=[]
for i in dict1:
	temp=re.sub('#.*','',i)
	dict3.append(temp)

final_dict=[]			# final_dict stores the [word,sentiment] pairs
for i,j in enumerate(dict3):
	temp=[j,dict2[i]]
	final_dict.append(temp)

def score(i,final_dict):		# if a particular word is contained in final_dict, then score returns its corresponding sentiment value
	for j in final_dict:		# else if the word is not present then it returns 0
		if(j[0]==i):
			return j[1]
	return 0


p=[]
n=[]
for i in t3:
	temp=i.split('\t')
	if(float(temp[2])>float(temp[3])):
		if(float(temp[2]>0.6)):
			p.append(temp[4])

for i in t3:
	temp=i.split('\t')
	if(float(temp[2])<float(temp[3])):
		if(float(temp[3])>0.8):
			n.append(temp[4])

positive=[]
negative=[]
for i in p:
	temp=re.sub('#.*','',i)
	positive.append(temp)

for i in n:
	temp=re.sub('#.*','',i)
	negative.append(temp)

################################	ARFF Header	#############################################################

header='@RELATION quart_score'
f2.write(header + '\n')
for i in range(0,(len(dict3)+3)):
	f2.write('@ATTRIBUTE ' + 'count_' + str(i) + ' NUMERIC' + '\n')

f2.write('@ATTRIBUTE class {1,2,3,4}\n')

f2.write('@DATA\n')
###################################################################################################################

for i,j in enumerate(t1):
	l1=[]
	
	star=re.search('(?<=<star>)\d',j)
	#star1=star.group()

	for k in dict3:			# This builds features of the number of times a particular word in the dictionary is present in the review 
		l1.append(str(j.count(k)))

	temp=nltk.word_tokenize(j)
	value=0
	pcount=0			# pcount = number of positive words in a review
	ncount=0			# ncount = number of negative words in a review
	for j in temp:
		if(positive.count(j)>0):
			pcount=pcount+1
		if(negative.count(j)>0):
			ncount=ncount +1
		value=value + score(j,final_dict)
	l1.append(str(value))		# value = total positivity or negativity value for a review, calculated by taking the sum of the 
	l1.append(str(pcount))		#	  positivity of negativity scores in the whole review document
	l1.append(str(ncount))

	l1.append('?')			# append '?' to last column, this is the column which will be predicted by the model
	f2.write(','.join(l1) + '\n')
	print 'Writing from review ',i,' to ARFF file'


f1.close()
f2.close()
f3.close()

