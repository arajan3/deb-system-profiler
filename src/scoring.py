wht=500  #weight for open-close
wo=100	 #weight for open	
wr=50	#weight for read
we=1	#weight for exec
wc=10	#weight for cpu time

def get_sec(time_str):
	num=time_str.count(":")
	# print(str(num)+"here")
	if(num == 2):
		h, m, s = time_str.split(':')
		if '-' in str(h):
			d, h = str(h).split('-')
			h = 24*int(d) + int(h)
		else:
			h = int(h)

		return h * 3600 + int(m) * 60 + int(s)
	if(num == 1):
		m, s = time_str.split(':')
		return int(m)*60+int(s)	

def score1(o,c,r):   #o=open,c=close,r=read
	bonus=wht*(o-c)
	sops=wo*o+wr*r
	return bonus+sops

def score2(te,tc):    #te=execution time,tc=cpu time
	# print(str(te)+" "+str(tc)+"\n")
	se=we*get_sec(te)
	sc=wc*get_sec(tc)
	return se+sc	
