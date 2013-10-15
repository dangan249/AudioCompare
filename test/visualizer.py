import sys
from WavInputFile import WavInputFile
from Tkinter import *
from wang import *
from FFT import FFT
import numpy

import scipy.io.wavfile
from pylab import plot,show,subplot,specgram,detrend_none
from matplotlib.colors import LogNorm
import matplotlib.cm


CHUNK_SIZE = 1024

def visualizer():
    """Display a graph that shows which frequencies we
    will use in our hashing algorithm.
    """
    #rate,data = scipy.io.wavfile.read(sys.argv[1]) # reading
    #data = data.transpose()[0]
    #subplot(411)
    #plot(range(len(data)),data)
    #subplot(412)
    # NFFT is the number of data points used in each block for the FFT
    # and noverlap is the number of points of overlap between blocks
    #specgram(data.transpose()[0], Fs=44100, noverlap=0, detrend=detrend_none) # small window
    #specgram(data, NFFT=128, noverlap=0) # small window
    #subplot(413)
    #s = specgram(data, NFFT=512, noverlap=0)
    #subplot(414)
    #specgram(data, NFFT=1024, noverlap=0) # big window

    #show()

    #return


    try:
        input_file = WavInputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    freq_chunks = FFT(input_file, CHUNK_SIZE).series()
    print "DONE FFT"
    print numpy.amin(freq_chunks), numpy.amax(freq_chunks)
    #s = FFT(input_file, CHUNK_SIZE).series_raw()
    #print data[0:100]
    #s = specgram(data, NFFT=512, noverlap=0)
    #plot(s)
    #show()
    #return
    norm = LogNorm(0.000000001, numpy.amax(freq_chunks))

    winners = Wang._Wang__bucket_winners(freq_chunks)

    # initialize an empty window
    master = Tk()
    master.wm_title(" ".join(sys.argv[1:]))
    #first_chunk = 517
    #last_chunk = 948
    #chunks = last_chunk - first_chunk
    chunks = len(freq_chunks)
    first_chunk = 0
    lines = UPPER_LIMIT #len(freq_chunks[0])
    blockSizeX = 2
    blockSizeY = 2
    w = Canvas(master, width=chunks*blockSizeX, height=lines*blockSizeY)
    w.pack()
    # for each chunk (which will be the X axis)
    for i in range(chunks):
        print i
        # for each line (the Y axis)
        #freq = 1
        #line = 1
        for line in range(1, lines):
        #while freq < len(freq_chunks[i]):
            # compute what color this frequency should
            # appear as, based on its magnitude
            val = freq_chunks[i+first_chunk][line]
            #abs = math.sqrt((val.real * val.real) + (val.imag * val.imag)) + 1
            #mag = math.log(abs)
            mag = norm(val)

            # assign color to red if winning frequency,
            # otherwise some shade of grey
            bucket = Wang._Wang__get_bucket(line)
            if (line-LOWER_LIMIT) % BUCKET_SIZE == 0:
                color = "blue"
            elif line == winners[i][bucket]:
                color = "green"
            else:
                color_vals = matplotlib.cm.jet(mag)
                color = "#{r:02x}{g:02x}{g:02x}".format(r=int(color_vals[1]*255), g=int(color_vals[2]*255), b=int(color_vals[3]*255))
            # make a small rectangle on the screen of the appropriate color
            w.create_rectangle(i*blockSizeX, line*blockSizeY, (i+1)*blockSizeX, (line+1)*blockSizeY, fill=color, width=0)

            # the next line will represent a frequency that is logarithmically bigger than this one
            #freq += math.log10(line) * math.log10(line)
            #line += 1

    mainloop()

if __name__ == "__main__":
    visualizer()