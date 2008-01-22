import re

filename='0_01.orig'
filename_out='0_01.txt'

f=open(filename)
content=f.read()
f.close()


table = [re.split('\ \ +',r) for r in re.split('\n',content)][:-1]

f=open(filename_out,'w')
for r in table:
    row = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (r[0],r[2],r[3],r[4],r[5],r[6],r[1])
    f.write(row)

f.close()
