import sys
import re

file1=sys.argv[1]	# ARFF file containing predictions
file2=sys.argv[2]	# Orinal Test(txt) file, containting movie reviews
file3=sys.argv[3]	# Output file name

f1=open(file1)
t1=f1.readlines()

f2=open(file2)
txt=f2.readlines()

f3=open(file3,'w')

k=0
for i,j in enumerate(t1):
	if(re.match('@(data|DATA|Data)',j)):
		k=i+1
		while(t1[k]=='\n'):
			k=k+1

t2=t1[k:]
t3=[]
for i,j in enumerate(t2):
	t2[i]=j.rstrip('\n')

for i in t2:
	t3.append(i.split(','))

t4=[]
for i in t3:
	t4.append(i[-1])


for i,j in enumerate(txt):
	if(t4[i]=='1'):
		value='P'
	else: 	value='N'
	temp='</id><PN>' + value + '</PN><review>'
	temp=re.sub('</id><review>',temp,j)
	f3.write(temp)

f3.close()
f2.close()
f1.close()
