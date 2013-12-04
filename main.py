#!/usr/bin/env python
from error import *
from Matcher import Matcher
from argparse import ArgumentParser

def audio_matcher():
    """Our main control flow."""

    parser = ArgumentParser(
        description="Compare two audio files to determine if one "
                    "was derived from the other. Supports WAVE and MP3.",
        prog="audiomatch")
    parser.add_argument("-f", action="append",
                        required=False, dest="files",
                        default=list(),
                        help="A file to examine.")
    parser.add_argument("-d", action="append",
                        required=False, dest="dirs",
                        default=list(),
                        help="A directory of files to examine. "
                             "Directory must contain only audio files.")

    args = parser.parse_args()

    search_paths = args.dirs + args.files

    if len(search_paths) != 2:
        die("Must provide exactly two input files or directories.")

    code = 0
    # Use our matching system
    matcher = Matcher(search_paths[0], search_paths[1])
    results = matcher.match()

    for match in results:
        if not match.success:
            code = 1
            warn(match.message)
        else:
            print match

    return code

if __name__ == "__main__":
    exit(audio_matcher())
