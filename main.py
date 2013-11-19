#!/usr/bin/env python
from error import *
import Wang
from argparse import ArgumentParser
from argparse import SUPPRESS

def audio_matcher():
    """Our main control flow."""

    parser = ArgumentParser(
        description="Compare two audio files to determine if one "
                    "was derived from the other.",
        prog="ERROR: p4500", usage=SUPPRESS)
    parser.add_argument("-f", action="append",
                        required=False, dest="files",
                        default=list(),
                        help="A file to examine. "
                        "Must provide two instance of this argument.")
    parser.add_argument("-d", action="append",
                        required=False, dest="dirs",
                        default=list(),
                        help="A directory of files to examine. "
                        "Must provide two instance of this argument.")
    parser.add_argument("--test",
                  action="store_true", dest="test", default=False,
                  help="Run in test mode (shows stacktraces on error)")

    try:
        args = parser.parse_args()
    except Exception, e:
        if "--test" in sys.argv:
            raise
        die(e.message)
        return

    search_paths = args.dirs + args.files

    if len(search_paths) != 2:
        die("Must provide exactly two input files or directories.")

    # Use our matching system
    try:
        matcher = Wang.Wang(search_paths[0], search_paths[1])
        for match in matcher.match(verbose=args.test):
            print match
    except Exception, e:
        if args.test:
            raise
        die(e)
        return

if __name__ == "__main__":
    audio_matcher()
