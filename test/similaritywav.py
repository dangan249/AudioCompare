import wave
import numpy as np
import matplotlib.pyplot as plt
import sys


# open wav file and get data
def op(string):
	string = str(string)
	info = wave.open(string,'r').getparams()
	f_s = info[2] #sample rate
	nframes = info[3] #number of frame
	ch = info[0] #number of channel 
	samplewidth = info[1]
	sw = samplewidth*8
	#print sw
	# with np open it does not require struct unpack the file
	# it directly translate the entire file
	if sw == 16:
		ff = np.fromfile(open(string),np.int16)
	elif sw == 32:
		ff = np.fromfile(open(string),np.int32)
	elif sw == 8:
		ff = np.fromfile(open(string),np.int8)
	nff = ff[23:] #get data frames
	#print nff
	lff = nff[::2]	#get left channel
	#print lff
	#rff = ff[1::2] #get right channel
	return lff

	
x = op(sys.argv[1])
y = op(sys.argv[2])
#plt.plot(y,'r')
#plt.plot(x,'b')
#plt.show()

b =[]
a =[]
chunksize = 44100/50
chunks_x = len(x)/chunksize
chunks_y = len(y)/chunksize

for i in xrange((chunks_x-1)):
	a.append(np.fft.rfft(x[i*chunksize:(i+1)*chunksize]))
for i in xrange((chunks_y-1)):
	b.append(np.fft.rfft(y[i*chunksize:(i+1)*chunksize]))

a = np.array(a)
b = np.array(b)
ok = 0
diffs = {}
#print len(a)
cx = chunks_x -2
cy = chunks_y -2

# please take a look at this part
# the corrcoef is the calculation of similarity of two chunks in frequency domain
# so this loop run entire two files compare between the chunks (O(n^2)??)
# if there are over 10 matches of two chunks's similarity is over 90%, we deduce as a match

for i in xrange(cx):
	for j in xrange(cy):
		cor = np.corrcoef(a[i],b[j])
		if cor[0][1] >=0.9:
			
			diff = abs(j-i)
			if diff in diffs:
				diffs[diff] += 1
				if diffs[diff] >=10:
					ok = 1
					print 'match'
					sys.exit()

			else:
				diffs[diff] = 1

print 'no match'			
