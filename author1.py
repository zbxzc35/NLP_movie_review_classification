from __future__ import division
import re
import nltk
import sys

file1=sys.argv[1]		# movie review filename
file2=sys.argv[2]		# output arff filename

f1=open(file1)
t1=f1.readlines()

f1.seek(0)
t2=f1.read()
t2=re.sub('(?<=<reviewer>)\w','',t2)	# remove author info, t2 will now be used to build the feature list


f2=open(file2,'w')

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

final_dict=[]			# final_dict stores the [word,sentiment] pairs
for i,j in enumerate(dict3):
        temp=[j,dict2[i]]
        final_dict.append(temp)

def score(i,final_dict):	# if a particular word is contained in final_dict, then score returns its corresponding sentiment value
        for j in final_dict:	# else if the word is not present then it returns 0
                if(j[0]==i):
			return j[1]
	return 0


################################	ARFF Header	#############################################################
header='@RELATION author1'
f2.write(header + '\n')

for i in range(0,len(dict3) +6):
	f2.write('@ATTRIBUTE ' + 'feat_' + str(i) + ' NUMERIC' + '\n')
f2.write('@ATTRIBUTE class {A,B,C,D}\n')

f2.write('@DATA\n')
######################################################################################################################
for i,j in enumerate(t1):
	l1=[]

	auth=re.search('(?<=<reviewer>)\w',j)
	
	# 1: number of characters in review
	l1.append(str(len(j)))

	# 2: number of sentences
	temp=re.search('w>[\w|\W]*',j)
	temp1=temp.group()
	temp1=re.sub('\*[\w|\W]*','',temp1)
	temp2=temp1.split('.')
	l1.append(str(len(temp2)))

	# 3: avg sentence length
	k=0
	for p in temp2:
		k=k+ len(p)
	l1.append(str(k/len(temp2)))	

	# 4: number of words
	temp3=temp1.split(' ')
	l1.append(str(len(temp3)))

	# 5: avg word length
	k=0
	for p in temp3:
		k=k+len(p)
	l1.append(str(k/len(temp3)))

	# 6: lexical diversity as defined in NLTK book.
	temp4=set(temp3)
	l1.append(str(len(temp3)/len(temp4)))

	# feature vectors corresponding to count of dictionary words in a review.
	for k in dict3:
		l1.append(str(j.count(k)))

############################################################
	l1.append('?')
	#l1.append(auth.group())
	f2.write(','.join(l1) + '\n')
	print 'Writing from review ',i,' to ARFF file'
############################################################

f1.close()
f2.close()


