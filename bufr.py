filename = '/home/castelao/work/projects/BUFR/others/bufr_000340/data/wmo_sarep.bufr'
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

def int2bin(n, count=8):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

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

# Read section 3
sectiondata[3]={}
sectiondata[3]['sec3size'] = safe_unpack('>i',f.read(3))
sectiondata[3]['reserved'] = safe_unpack('>i', f.read(1))
sectiondata[3]['nsubsets'] = safe_unpack('>i', f.read(2))
sectiondata[3]['xxxx'] = safe_unpack('>i', f.read(1))

n_descriptors = (sectiondata[3]['sec3size']-7)/2
sectiondata[3]['descriptors']=[]
for i in range(n_descriptors):
    FX = safe_unpack('>i', f.read(1))
    F = FX/64
    X = FX%64
    Y = safe_unpack('>i', f.read(1))
    #sectiondata[3]['descriptors'].append([FX,F,X,Y])
    sectiondata[3]['descriptors'].append([F,X,Y])
    print F,X,Y
    if F == 0:
        print descriptors[F][X][Y]

from UserList import UserList
#import itertools


class WalkingList(UserList):
    #def __init__(self,data=None):
    def __init__(self):
        UserList.__init__(self)
	#if data!=None:
        #    self.data=data
	self.i=-1
	return
    def walk(self):
        self.i+=1
	if self.i<len(self):
	    return self.data[self.i]
	return 


class Descriptor(UserList):
    def __init__(self,F,X,Y):
        #UserList.__init__(self)
        self.data=WalkingList()
	self.i=0
        self.F=F
	self.X=X
	self.Y=Y
	if (F==0):
	    self.data.append(globals()['descriptorstable'][F][X][Y])
	if (F==3):
	    for f,x,y in globals()['descriptorstable'][F][X][Y]:
	        print f,x,y
	        self.data.append(Descriptor(f,x,y))
	return
    def walk(self):
        output=self.data[self.i].walk()
	if (output == None):
	    self.i+=1
	    if (x.i<len(self.data)):
                output=self.data[self.i].walk()
            else:
	        output=None
	return None
	

	    

class Descriptors:
    def __init__(self,descriptors):
        self.descriptors=descriptors
        self.i=-1
        return
    def walk(self):
        self.i+=1
        return self.descriptors[self.i]

# Read section 4
sectiondata[4]={}

sectiondata[4]['size'] = safe_unpack('>i',f.read(3))
sectiondata[4]['reserved'] = safe_unpack('>i', f.read(1))

#rownbits=8
bitline=''
for i in range(sectiondata[4]['size']-4):
    bitline+=int2bin(safe_unpack('>i', f.read(1)))

sectiondata[4]['data']=[]
fin=0
sizes=[7,10,12,4,6,5,6,10,8]
for s in sizes:
    ini=fin
    fin+=s
    print s,ini,fin,bitline[ini:fin]
    sectiondata[4]['data'].append(int(bitline[ini:fin],2))

#for i in range(sectiondata[4]['size']-4-8):
#    sectiondata[4]['data'].append(safe_unpack('>i', f.read(1)))

# Read section 5
sectiondata[5]={'closer':f.read(4)}


for k in sectiondata:
    print "%s" % k
    for kk in sectiondata[k]:
        print "   %s: %s" % (kk,sectiondata[k][kk])

