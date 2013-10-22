#!/usr/bin/env python
import sys
from WavInputFile import WavInputFile
from error import *
import wang

def audio_matcher():
    """Our main control flow."""
    if len(sys.argv) < 3:
        die("Must provide two input files.")

    # Open the two input files
    try:
        file1 = WavInputFile(sys.argv[1])
        file2 = WavInputFile(sys.argv[2])
    except IOError, e:
        die(e.message)
        return

    # Use our matching system
    matcher = wang.Wang(file1, file2)
    if matcher.match():
        print "MATCH"
    else:
        print "NO MATCH"

if __name__ == "__main__":
   # try:
    audio_matcher()
    #except Exception, e:
    #    die(e.message)
