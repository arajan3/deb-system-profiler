import subprocess
import os


res_in_o=open("/proc/refsinfo_o")
res_in_c=open("/proc/refsinfo_c")
res_in_r=open("/proc/refsinfo_r")
# res_in_w=open("/proc/refsinfo_w")
ps_in=open("/tmp/pstmpfs/psinfo")

kmap={}   ##Map<filename,<open,close,read>>
smap={}   ##Map<filename,<score1,score2,score>>




#Count number of Opens
key=res_in_o.readline()
kmap[key]=[0,0,0,0]
while(key):
	kmap[key][0]+=1
	key=res_in_o.readline()
#Count number of Close
key=res_in_c.readline()
kmap[key]=[0,0,0,0]
while(key):
	kmap[key][1]+=1
	key=res_in_c.readline()
#Count number of reads
key=res_in_r.readline()
kmap[key]=[0,0,0,0]
while(key):
	kmap[key][2]+=1
	key=res_in_r.readline()
#Count number of writes
# key=res_in_w.readline()
# kmap[key]=[0,0,0,0]
# while(key):
# 	kmap[key][3]+=1
# 	key=res_in_w.readline()
smap[kmap.keys()[0]]=[0,0,0]
for k,value in kmap:
	smap[k][0]=score1(value[0],value[1],value[2])

key=ps_in.readline()
while(key):
	key,te,tc=key.split(",")
	smap[key][1]=score2(te,tc)
	st ="ldd "+key+" | grep -v 'linux-vdso.so.1'  | awk -F \" => \" {'print $2'} | awk -F \" (\" {'print $1'} | grep -v -e '^$'"
	cmd = subprocess.Popen(st, shell=True, stdout=subprocess.PIPE)
	lddlist=[]
	for line in cmd.stdout:
		line=line.decode("utf-8")
		line = os.linesep.join([s for s in line.splitlines() if s])
		lddlist.append(line)
	for libpath in lddlist:
		smap[libpath][1]+=smap[key][1]	
	key=ps.readline()	
