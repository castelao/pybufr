filename = './data/wmo_sarep.bufr'
f=open(filename,'r')
#content = f.read()
#f.close()

import struct

#if (content[0:4]!='BUFR') | (content[-4:]=='7777'):
#    print "Don't looks like a BUFR file"

def safe_unpack(fmt,var):
    n=struct.calcsize(fmt)
    fullvar=var
    for i in range(n-len(var)):
        fullvar='\x00'+fullvar
    output=struct.unpack(fmt,fullvar)
    return output[0]
# ====
#
def Denary2Binary(n):
    '''convert denary integer n to binary string bStr'''
    bStr = ''
    if n < 0: raise ValueError, "must be a positive integer"
    if n == 0: return '0'
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    return bStr

def readdescriptor(filename):
    descriptors={}
    f=open(filename)
    for line in f:
        #fields = line.split('\t')
        fields=[line[1:7],line[8:72].strip(),line[73:98].strip(),int(line[98:101]),int(line[102:114]),int(line[115:118])]
        F=int(fields[0][0:1])
        X=int(fields[0][1:3])
        Y=int(fields[0][3:6])
        if F not in descriptors:
	    descriptors[F]={}
        if X not in descriptors[F]:
	    descriptors[F][X]={}
        #if Y not in descriptors[F][X]:
	#    descriptors[F][X]={}
	descriptors[F][X][Y] = {'name':fields[1],'unit':fields[2],'scale':fields[3],'reference':fields[4],'bitwidth':fields[5]}
    return descriptors

#descriptors = readdescriptor('table-B.txt')
descriptorstable = readdescriptor('/home/castelao/work/projects/BUFR/others/bufr_000340/bufrtables/B0000000000000007000.TXT')
descriptorstable[3]={}
descriptorstable[3][1]={}
descriptorstable[3][1][1] = [[0,1,1],[0,1,2]]
descriptorstable[3][1][11] = [[0,4,1],[0,4,2],[0,4,3]]
descriptorstable[3][1][12] = [[0,4,4],[0,4,5]]
descriptorstable[3][1][23] = [[0,5,2],[0,6,2]]
descriptorstable[3][1][25] = [[3,1,23],[0,4,3],[3,1,12]]
#descriptors[3][1][1] = {'name':'WMO block and station number','descriptors':[],'scale':fields[3],'reference':fields[4],'width':fields[5]}
# 3 1 1
# 3 1 11
# 3 1 12
#print descriptors
# ====


# 39 total
# ====

sectiondata={}

#sectionindex={'0':	{'BUFR':4, 
#			'totallength':3,
#			'bufredition':1}}

# Read section 0
#sec=0
sectiondata[0]={}

#sections[0]=content[:0:8]

sectiondata[0]['ident'] = f.read(4)
#size = struct.unpack('>i',content[4:7])
sectiondata[0]['size'] = safe_unpack('>i',f.read(3))
sectiondata[0]['version'] = safe_unpack('>i',f.read(1))

# Read section 1
sectiondata[1]={}

sectiondata[1]['sec1size'] = safe_unpack('>i',f.read(3))		# 1-3
sectiondata[1]['mastertablenumber'] = safe_unpack('>i',f.read(1))	# 4
sectiondata[1]['originatedcenter'] = safe_unpack('>i',f.read(2))	# 5-6
sectiondata[1]['originatedsubcenter'] = safe_unpack('>i', f.read(2))		# 7-8
sectiondata[1]['updateversion'] = safe_unpack('>i', f.read(1))	# 9
sectiondata[1]['optionalsec'] = safe_unpack('>i', f.read(1))	# 10    Atention here!!!
sectiondata[1]['datacategory'] = safe_unpack('>i', f.read(1))	# 11
sectiondata[1]['datasubcategory'] = safe_unpack('>i', f.read(1))	# 12
sectiondata[1]['localsubcategory'] = safe_unpack('>i', f.read(1))	# 13
sectiondata[1]['mastertableversion'] = safe_unpack('>i', f.read(1))	# 14
sectiondata[1]['localtableversion'] = safe_unpack('>i', f.read(1))	# 14
sectiondata[1]['year'] = safe_unpack('>i',f.read(2))			# 15
sectiondata[1]['month'] = safe_unpack('>i', f.read(1))			# 16-17
sectiondata[1]['day'] = safe_unpack('>i', f.read(1))
sectiondata[1]['hour'] = safe_unpack('>i', f.read(1))
sectiondata[1]['minute'] = safe_unpack('>i', f.read(1))
sectiondata[1]['second'] = safe_unpack('>i', f.read(1))
#reserved = safe_unpack('>i',content[26:8+sec1size])

# Read section 2

if (sectiondata[1]['optionalsec'] != 0):
    print "Atention!!!! Not ready to read the section 2"
    # Nothing to read since the octet 10 of section 1 is 0
    #sec2size = safe_unpack('>i',content[30:33])
    #safe_unpack('>i',content[33:34])

# ============================================================================
# ==== Read section 3
# ============================================================================
#filename = './data/wmo_sarep.bufr'
#f=open(filename,'r')
#lixo=f.read(30)


# Looks like a good first approach, but still needs:
#    - Think about an array index. I believe is the best way to reference were to store the output data
#    - Think about a rewind system for the walk. Maybe simply save a copy, of the data when the walk is called, and when the rewind is called, it only overload the copied data.
#    - Still missing how to deal with the repetitions (class 1).

from UserList import UserList
from UserDict import UserDict
#import itertools


#class level0(UserList):
#    def __init__(self):
#        UserList.__init__(self)
#	return

class Descriptor0(UserDict):
    #def __init__(self,data):
    def __init__(self,F,X,Y):
        self.F=F
	self.X=X
	self.Y=Y
        self.data=globals()['descriptorstable'][F][X][Y]
	self.showed=False
	self.repetitions=1
	self.n=0
	return
    def walk(self):
        if self.showed==False:
	    self.showed=True
            return self.data
	else:
	    self.showed=False
	    return
    def reset(self):
        self.showed=False
	return
	
#class WalkingList(UserList):
#    #def __init__(self):
#    def __init__(self,data=None):
#        UserList.__init__(self)
#	if data!=None:
#            self.data=data
#	self.i=-1
#	print "Merda: i",self.i
#	return
#    def walk(self):
#        self.i+=1
#	if self.i<len(self):
#	    return self.data[self.i]
#	return 

class Descriptors(UserList):
    def __init__(self,F=None,X=None,Y=None):
    #def __init__(self):
        UserList.__init__(self)
        #self.data=WalkingList()
	self.i=0
	self.repetitions=1
	self.n=0
	if (F != None) & (X != None) & (Y != None):
	    self.append(F,X,Y)
        return
    def load(self,descriptorslist):
        """
	"""
	i=0
	while i<len(descriptorslist):
	   F,X,Y = descriptorslist[i] 
	   #print "Processing: %s, %s, %s" % (F,X,Y)
	   #print F,X,Y,(globals()['descriptorstable'][F][X][Y])
	   if (F==0):
	       self.data.append(Descriptor0(F,X,Y))
	   elif (F==1):
               tmp=Descriptors()
               tmp.F=F
               tmp.X=X
               tmp.Y=Y
	       if tmp.Y>0:
	           sublist=descriptorslist[i+1:i+1+X]
		   tmp.repetitions=Y
		   i+=X
               elif tmp.Y==0:
	           sublist=descriptorslist[i+2:i+2+X]
	           tmp.repfactor=Descriptor0(descriptorslist[i+1][0],descriptorslist[i+1][1],descriptorslist[i+1][2])
		   tmp.repetitions=None
		   i+=1+X
               for f,x,y in sublist:
                   if f==1:
                       print "Library not ready for hierarcheal repetitions"
                       self.data=None
                       return
               tmp.load(sublist)
	       self.data.append(tmp)
	   elif (F==3):
               tmp=Descriptors()
               tmp.F=F
               tmp.X=X
               tmp.Y=Y
	       tmp.load(globals()['descriptorstable'][F][X][Y])
	       self.data.append(tmp)
	   i+=1
	return
    def walk(self):
        #print "self.i: %s" % (self.i)
        output=self.data[self.i].walk()
	#print "output:",output
	#print "i:",i
	if (output == None):
            #print "i: %s, len(data): %s" % (self.i,len(self.data))
            if self.i<(len(self.data)-1):
	        self.i+=1
	        #self.n+=1
                if (self.data[self.i].F == 1) & (self.data[self.i].Y == 0) & ((self.data[self.i].n == 0)):
	            output = self.data[self.i].repfactor
	        else:
	            output=self.data[self.i].walk()
	    #if self.n<self.repetitions:
	    #    self.i=0
	    #if (self.i<len(self.data)):
            #    output=self.data[self.i].walk()
            else:
	        self.n+=1
                if (self.n<self.repetitions):
		    self.reset()
		    output=self.data[self.i].walk()
		else:
                    output=None
	#else:
	#    #self.i+=1
        #    #print "I'm out"
	return output
    def reset(self):
        """ Reset the counter
	"""
	self.data[self.i].reset()
	self.i=0
	return

#a=Descriptors()
#a.load(descriptorslist)

#    def append(self,F,X,Y):
#	#self.i=0
#	if (F==0):
#	    #self.data.append(WalkingList(globals()['descriptorstable'][F][X][Y]))
#	    #self.data.append(Descriptor0(globals()['descriptorstable'][F][X][Y]))
#	    #self.data.append(Descriptor0(F,X,Y))
#	    tmp=(Descriptor0(F,X,Y))
#	    #self.data.append((globals()['descriptorstable'][F][X][Y]))
#        elif (F==1):
#	    # Replicator class
#	    # X is the number of the following fields that should be replicated
#	    # Y if > 0 is the number of repetitions
#	    #   if = 0 means a delayed replicaton, and a class 0 31 should be the following field.
#	    print "Hey!!! F=1!!!"
#	    #self.nfields=X
#	    tmp=Descriptors()
#	    tmp.F=F
#	    tmp.X=X
#	    tmp.Y=Y
#	    self.insiderepetition=True
#	    #if Y==0:
#	    #    # Need to read n on the next field
#	    #    pass
#	    #else:
#	    #    self.n=Y
#	elif (F==3):
#	    tmp=Descriptors()
#	    tmp.F=F
#	    tmp.X=X
#	    tmp.Y=Y
#	    for f,x,y in globals()['descriptorstable'][F][X][Y]:
#	        print f,x,y
#	        #tmp.append(Descriptors(f,x,y))
#	        tmp.append(f,x,y)
#	    #self.data.append(tmp)
#	if self.insiderepetition==True
#	    #self.tmp.append(tmp)
#	    #if len(self.tmp)==self.tmp.X:
#	    #    self.insiderepetition==False
#	    #	self.data.append(self.tmp)
#	    self.data[-1].append(tmp)
#	else:
#            self.data.append(tmp)
#	return
#    def parser(self,descriptorlist):
#        for i,[F,X,Y] in enumerate(descriptorlist):
#	    print "i: %i" % i
#	    if F==0:
#	        #self.data.append(Descriptor0(globals()['descriptorstable'][F][X][Y]))
#		self.append(F,X,Y)
#            elif F==1:
#	        if Y>0:
#		    start=i+1
#		    end=i+1+X
#                elif Y==0:
#		    start=i+2
#		    end=i+2+X
#                tmp=Descriptors()
#                tmp.parser(descriptorlist[start:end])
#                print "tmp",tmp
#	    elif F==3:
#	        ##tmp=[]
#	        #tmp=Descriptors()
#	        #for f,x,y in globals()['descriptorstable'][F][X][Y]:
#	        #    #tmp.append(Descriptors(f,x,y))
#	        #    tmp.append(f,x,y)
#		#self.data.append(tmp)
#		self.append(F,X,Y)
#        return
#    def walk(self):
#        output=self.data[self.i].walk()
#	#print "output:",output
#	#print "i:",i
#	if (output == None):
#	    self.i+=1
#	    if (self.i<len(self.data)):
#                output=self.data[self.i].walk()
#            else:
#	        output=None
#	return output
	
# To test:
filename = '/home/castelao/work/projects/BUFR/others/bufr_000340/data/wmo_sarep.bufr'
f=open(filename,'r')
lixo=f.read(30)

# x=Descriptor(3,1,1)
# x.walk()
# x.walk()
	    

#class Descriptors:
#    def __init__(self,descriptors):
#        self.descriptors=descriptors
#        self.i=-1
#        return
#    def walk(self):
#        self.i+=1
#        return self.descriptors[self.i]


sectiondata[3]={}
sectiondata[3]['sec3size'] = safe_unpack('>i',f.read(3))
sectiondata[3]['reserved'] = safe_unpack('>i', f.read(1))
sectiondata[3]['nsubsets'] = safe_unpack('>i', f.read(2))
sectiondata[3]['xxxx'] = safe_unpack('>i', f.read(1))

n_descriptors = (sectiondata[3]['sec3size']-7)/2
sectiondata[3]['descriptors']=Descriptors()
tmp=[]
for i in range(n_descriptors):
    FX = safe_unpack('>i', f.read(1))
    F = FX/64
    X = FX%64
    Y = safe_unpack('>i', f.read(1))
    #sectiondata[3]['descriptors'].append([FX,F,X,Y])
    #sectiondata[3]['descriptors'].append(F,X,Y)
    tmp.append([F,X,Y])
    print F,X,Y
    #if F == 0:
    #    print descriptorstable[F][X][Y]
sectiondata[3]['descriptors'].load(tmp)
# ============================================================================
# ==== Read section 4
# ============================================================================
sectiondata[4]={}

sectiondata[4]['size'] = safe_unpack('>i',f.read(3))
sectiondata[4]['reserved'] = safe_unpack('>i', f.read(1))


def int2bin(n, count=8):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

class BinaryData:
    def __init__(self,f,size):
        self.f=f
	dir(self.f)
	self.size=size
	self.n=0
	self.bitline=''
	return
    def read(self,nbits):
        while (nbits>len(self.bitline)):
	    #self.bitline+=int2bin(safe_unpack('>i', self.f.read(1)))
	    #print dir(self.f)
	    self.n+=1
	    if (self.n>=self.size):
	        print "Trying to read more then was supposed"
		return
	    x=self.f.read(1)
	    #print "x: %s" % x
	    self.bitline+=int2bin(safe_unpack('>i', x))
	output=self.bitline[:nbits]
	self.bitline=self.bitline[nbits:]
	return output


# Need to change it. Should read variable by variable.
#rownbits=8
bitline=''
#for i in range(sectiondata[4]['size']-4):
#    bitline+=f.read(1)
#    bitline+=int2bin(safe_unpack('>i', f.read(1)))
binarydata=BinaryData(f,sectiondata[4]['size'])

def datatype(unit):
    """
    """
    datatypes={'NUMERIC':'int',
     'YEAR':'int',
     'MONTH':'int',
     'DAY':'int',
     'HOUR':'int',
     'MINUTE':'int',
     'SECOND':'int',
     'DEGREE':'int',
     'CCITTIA5':'str',
     }
    if unit in datatypes.keys():
        return datatypes[unit]
    else:
        return unit

sectiondata[4]['data']=[]
fin=0
#sizes=[7,10,12,4,6,5,6,10,8]
#for s in sizes:
sectiondata[3]['descriptors'].reset()
d=sectiondata[3]['descriptors'].walk()
#for i in range(40):
while d:
    s=d['bitwidth']
    #ini=fin
    #fin+=s
    b=binarydata.read(s)
    if datatype(d['unit'])=='int':
        #output = int(bitline[ini:fin],2)
        output = int(b,2)
	output = (output+d['reference'])
	if d['scale'] != 0:
	    output = output/10.**(d['scale'])
    elif(datatype(d['unit'])=='str'):
        output="".join([struct.pack('>i',int(b[j*8:j*8+8],2))[-1] for j in range(len(b)/8)])
    else:
        output = b
    sectiondata[4]['data'].append(output)
    #print s,ini,fin,d['name'],bitline[ini:fin],sectiondata[4]['data'][-1]
    print s,d['name'],b,sectiondata[4]['data'][-1]
    d=sectiondata[3]['descriptors'].walk()

#for i in range(sectiondata[4]['size']-4-8):
#    sectiondata[4]['data'].append(safe_unpack('>i', f.read(1)))

# Read section 5
sectiondata[5]={'closer':f.read(4)}


for k in sectiondata:
    print "%s" % k
    for kk in sectiondata[k]:
        print "   %s: %s" % (kk,sectiondata[k][kk])

