import subprocess
import os
import scoring
import shutil

'''
shutil.copy("/proc/refsinfo", "/tmp/pstmpfs/refsinfo.now")
refs = open("/tmp/pstmpfs/refsinfo.now")

kmap = {}  ##Map<filename,<open,close,read>>

# Count number of O,R,C from refsinfo into kmap
key = refs.readline()
while (key):
    key, no, nr, nc = os.linesep.join([s for s in key.splitlines() if s]).split(",")
    kmap[key] = [no, nr, nc]
    key = refs.readline()
'''

smap = {}  ##Map<filename,<score1,score2,score>>
'''
smap["null"] = [0, 0, 0]
for k, value in kmap.items():
    if (k not in smap):
        smap[k] = [0, 0, 0]
    smap[k][0] = scoring.score1(value[0], value[1], value[2])
# print(str(k)+" "+str(smap[k][0])+"\n")
'''

shutil.copy("/tmp/pstmpfs/psinfo", "/tmp/pstmpfs/psinfo.now")
ps_in = open("/tmp/pstmpfs/psinfo.now")
key = ps_in.readline()
while (key):
    #print(str(key))
    if (key.count(",") != 2):
        key = ps_in.readline()
        continue
    key = os.linesep.join([s for s in key.splitlines() if s])
    key, te, tc = key.split(",")
    if (key not in smap):
        smap[key] = [0, 0, 0]
    smap[key][1] = scoring.score2(te, tc)
    # FIXME: Always add /lib64/ld-linux-x86-64.so.2 or /lib64/ld-linux.so.2 to list
    cmdstr = "ldd " + key + " | grep -v 'linux-vdso.so.1'  | awk -F \" => \" {'print $2'} | awk {'print $1'} | grep -v -e '^$'"
    #print(cmdstr)
    cmd = subprocess.Popen(cmdstr, shell=True, stdout=subprocess.PIPE)
    lddlist = []
    for line in cmd.stdout:
        line = line.decode("utf-8")
        line = os.linesep.join([s for s in line.splitlines() if s])
        lddlist.append(line)
    for libpath in lddlist:
        if (libpath not in smap):
            smap[libpath] = [0, 0, 0]
        smap[libpath][1] += int(smap[key][1])
    key = ps_in.readline()

for key in smap.keys():
    smap[key][2] = smap[key][0] + smap[key][1]

print(smap)