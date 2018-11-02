'''
Implementation of CYK Algorithm
''''

import numpy
import itertools
import sys,time

def make_grammar(filname):
	f=open(filname)
	t=' '
	cfg=[]
	for i in f.read():
		if i!='\n':
			t+=i
		else:
			#print t
			temp=t.split()
			temp.remove('->')
			cfg.append(temp)
			#print temp
			t=' '
	#print cfg
	return cfg


def print_chart(l1,l2,X):
	for i in range(l2):
		for j in range(l1-i):
			k=j+i
			#print i,j,k,
			#print X[j][k]
			print "{",
			for m in range(len(X[j][k])):
				print X[j][k][m],
			print "}",
		print "\n"
	return


def print_delay(string,d,nt):
	for i in range(nt):
		print string,
		time.sleep(d)

'''
grammar="""
A -> B C .
B -> B B .
B -> b .
C -> c .
"""
inp='b b c ' #input string
'''

if len(sys.argv) < 3 or len(sys.argv)>3:
	print "Require more arguments to run"
	print "usage:python cyk2.py grammar_file input_sring"
	exit()
else:
	fil=sys.argv[1]
	inp=sys.argv[2]
	
print "------------------------------------------------------------------------"
print "\n\n\t\t#################____ CYK PARSING _____##############"
print "\nInput CFG grammar in CNF.\nConvention: enter grammar in the form 'A -> B C '"
print "------------------------------------------------------------------------"

'''
grammar="""
S -> NP VP .
NP -> ART N .
VP -> V N .
N -> boy .
N -> mango .
V -> eats .
ART -> the .
"""
inp='the boy eats mango'
'''
w=inp.split()
n=len(w) #length of input string

'''
temp= grammar.split()
cfg=[[]]

pno=temp.count('.') # Number of productions

#Preparing production list A->BC is represented as [A, B, C] in a list cfg[pno][3]
for i in range(pno):
	cfg.append([])
i=0
for sym in temp:
	if sym=='->':
		continue
	elif sym=='.':
		i=i+1
	else:
		cfg[i].append(sym)
if [] in cfg:
	cfg.remove([])
#print cfg
'''
print "\nProcessing the parameters.",
print_delay('.',0.2,10)

print "\nReading the grammar file...",
print_delay('.',0.2,10)

print "\n Reading input string....",
print_delay('.',0.2,10)


time.sleep(1)

cfg=make_grammar(fil) #A->BC is represented as [A, B, C]

pno=len(cfg) # Number of productions

V=[]
for i in range(len(cfg)):
	V.append(cfg[i][0])
V=list(set(V)) #Set of non-terminals
Vno=len(V) #Number of non-terminals

T=[]
for i in range(len(cfg)):
	if cfg[i][1] not in V:
		T.append(cfg[i][1])
T=list(set(T)) #Set of terminals
Tno=len(T) #Number of terminals

S=cfg[0][0] #Start symbol

#r=Vno+Tno #Total number of symbols

print "\nNumber of Non-terminals,|V|=",Vno,V
print "Number of Terminals,    |T|=",Tno,T
print "Length of string,       |W|=",n
print "Number of productions,  |P|=",pno
#print "Total number of symbols |V U T|=",r
time.sleep(1)
#Create Chart
B=[[]]
for i in range(n):
	B.append([])
	for j in range(n):
		B[i].append(0)
B.remove([])
#print B

print "\n"
#For Uniproductions	
for i in range(n):
	#print i
	for r in cfg:
		#print r
		if r[0] in V and r[1] in T:
			#print r[1],w[i]
			if r[1]==w[i]:
				print "* Replace '"+w[i]+"' by '"+r[0]+"' using "+r[0]+" -> "+r[1]
				time.sleep(0.4)
				if B[i][i]==0:
					B[i][i]=[r[0]]	
				else:
					B[i][i].append(r[0])
				#print_chart(n,1,B)

print "\nChart After parsing Uniproductions\n",print_chart(n,1,B)
time.sleep(1)
#For A->BC
print "\nFor productions of the form A->BC"
for i in range(1,n):
	f3=False
	print "\n-------------------Length of Span=",i," ----------------------"
	for j in range(n-i):
		k=j+i
		l=j
		print "\n\tTo Find B_",j,k,"....."
		t=[]
		while l <= k-1:

			temp=[[]]
			for x in range(2):	
				temp.append([])
			print "\t\tCompiring B_",j,l,"and B_",l+1,k,"....."
			print "\t\tB[",j,"][",l,"]=",B[j][l],"B[",l+1,"][",k,"]=",B[l+1][k]
			
			for x in range(len(B[j][l])):
				temp[0].append(B[j][l][x])
			for x in range(len(B[l+1][k])):
				temp[1].append(B[l+1][k][x])
			l=l+1
			print "*",temp
			#print "Temp_b4=",temp
			temp=temp[:-1]
			#if [] in temp:
				#temp.remove([])
			#print "Temp_afr=",temp
			temp1=list(itertools.product(*temp))
			print "Temp1=",temp1
			if temp1!=[]:
				for ind in range(len(temp1)):
					t.append(temp1[ind])
			t=list(set(t))
		print "***",t

		t2=[]
		for r in cfg:
			if len(r)==3:
				if r[0] in V and r[1] in V and r[2] in V:
					t1=(r[1],r[2])
					print "if ",t1," in ",t
					if t1 in t:
						f3=True
						print "\n* Replace "+r[1]+" "+r[2]+" by "+r[0]+" Using rule "+r[0]+" -> "+r[1]+" "+r[2]+"\n"
						time.sleep(0.4)
						t2.append(r[0])
					#else:
						#print "No replacement ocuured."
		print t2
		B[j][k]=list(set(t2))
	
	if f3==False:
		print "\nNo replacement at span",i,".\n"
	
	print "Current Chart after Span=",i
	print_chart(n,i+1,B)
	time.sleep(0.4)
		#print "Changed\n",B
print "-------"*10
print "final Chart:"
print_chart(n,n,B)

time.sleep(0.4)
if S in B[0][n-1]:
	print "Language Accepted "
else:
	print "Not accepted"

