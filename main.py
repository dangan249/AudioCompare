#!/usr/bin/env python
import sys
from WavInputFile import WavInputFile
from error import *
import wang
from optparse import OptionParser

def audio_matcher():
    """Our main control flow."""

    parser = OptionParser()
    parser.add_option("--test",
                  action="store_true", dest="test", default=False,
                  help="Run in test mode (shows stacktraces on error)")

    (options, args) = parser.parse_args()

    if len(sys.argv) < 3:
        die("Must provide two input files.")

    # Use our matching system
    try:
        matcher = wang.Wang(sys.argv[1], sys.argv[2])
        if matcher.match():
            print "MATCH"
        else:
            print "NO MATCH"
    except IOError, e:
        if options.test:
            raise
        die(e.message)
        return

if __name__ == "__main__":
    audio_matcher()
