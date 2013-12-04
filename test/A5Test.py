import unittest
import os
import re
from subprocess import *
from TestCommon import TestCommon


class AudioMatchBlackBox(TestCommon):
    #Get current directory. We know what files are in here
    testSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/A5new/"
    testCWD = os.path.dirname(os.path.abspath(__file__)) + "/../"
    runCommand = os.path.dirname(os.path.abspath(__file__)) + "/../audiomatch"

    # Files to SHOULD match
    def test_z00_z00(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "D9/z00.mp3", self.testSuiteDir + "D9/z00.mp3"],
            "z00_z00", shouldMatch=True)

    def test_z111_z11(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "D9/z111", self.testSuiteDir + "D9/z11.mp3"],
            "z111_x11", shouldMatch=True)

    def test_z116_z16(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "D9/z116.wav", self.testSuiteDir + "D9/z16.mp3"],
            "z116_x16", shouldMatch=True)


if __name__ == "__main__":
    unittest.main()
