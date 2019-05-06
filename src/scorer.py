import subprocess
import os
import scoring



res_in_o=open("refsinfo_o")
res_in_c=open("refsinfo_c")
res_in_r=open("refsinfo_r")
# res_in_w=open("/proc/refsinfo_w")
ps_in=open("/tmp/pstmpfs/psinfo")

kmap={}   ##Map<filename,<open,close,read>>
smap={}   ##Map<filename,<score1,score2,score>>




#Count number of Opens
key=res_in_o.readline()
key = os.linesep.join([s for s in key.splitlines() if s])
kmap[key]=[0,0,0]
while(key):
	key = os.linesep.join([s for s in key.splitlines() if s])
	if(key not in kmap):
		# print(str(key)+"\n")
		kmap[key]=[0,0,0]
	kmap[key][0]+=1
	key=res_in_o.readline()
#Count number of Close
key=res_in_c.readline()

while(key):
	key = os.linesep.join([s for s in key.splitlines() if s])
	if(key not in kmap):
		# print(str(key)+"\n")
		kmap[key]=[0,0,0]
	kmap[key][1]+=1
	key=res_in_c.readline()
#Count number of reads
key=res_in_r.readline()

while(key):
	key = os.linesep.join([s for s in key.splitlines() if s])
	if(key not in kmap):
		# print(str(key)+"\n")
		kmap[key]=[0,0,0]
	kmap[key][2]+=1
	key=res_in_r.readline()
#Count number of writes
# key=res_in_w.readline()
# kmap[key]=[0,0,0,0]
# while(key):
# 	kmap[key][3]+=1
# 	key=res_in_w.readline()
smap["null"]=[0,0,0]
for k,value in kmap.items():
	if(k not in smap):
		smap[k]=[0,0,0]
	smap[k][0]=scoring.score1(value[0],value[1],value[2])
	# print(str(k)+" "+str(smap[k][0])+"\n")
key=ps_in.readline()
while(key):
	print(str(key))
	if(key.count(",")!=2):
		key=ps_in.readline()
		continue
	key = os.linesep.join([s for s in key.splitlines() if s])
	key,te,tc=key.split(",")
	if(key not in smap):
		smap[key]=[0,0,0]
	smap[key][1]=scoring.score2(te,tc)
	st ="ldd "+key+" | grep -v 'linux-vdso.so.1'  | awk -F \" => \" {'print $2'} | awk -F \" \(\" {'print $1'} | grep -v -e '^$'"
	cmd = subprocess.Popen(st, shell=True, stdout=subprocess.PIPE)
	lddlist=[]
	for line in cmd.stdout:
		line=line.decode("utf-8")
		line = os.linesep.join([s for s in line.splitlines() if s])
		lddlist.append(line)
	for libpath in lddlist:
		if(libpath not in smap):
			smap[libpath]=[0,0,0]
		smap[libpath][1]=int(smap[libpath][1])+int(smap[key][1])	
	key=ps_in.readline()	


print(smap)