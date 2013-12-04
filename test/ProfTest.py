import unittest
import os
import re
from subprocess import *
from TestCommon import TestCommon


class AudioMatchBlackBox(TestCommon):
    #Get current directory. We know what files are in here
    testSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/A6/"
    testCWD = os.path.dirname(os.path.abspath(__file__)) + "/../"
    runCommand = os.path.dirname(os.path.abspath(__file__)) + "/../audiomatch"

    # Files to SHOULD match
    def test_hewlett_hewlett(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "hewlett.wav"],
            "hewlett_hewlett", shouldMatch=True)

    def test_hewlett_x10(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x10.wav"],
            "hewlett_x10", shouldMatch=True)

    def test_hewlett_x11(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x11.wav"],
            "hewlett_x11", shouldMatch=True)

    def test_hewlett_x12(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x12.wav"],
            "hewlett_x12", shouldMatch=True)

    def test_trouble_trouble(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "trouble.wav"],
            "trouble_trouble", shouldMatch=True)

    def test_trouble_x1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x1.wav"],
            "trouble_x1", shouldMatch=True)

    def test_trouble_x2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x2.wav"],
            "trouble_x2", shouldMatch=True)

    def test_trouble_x3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x3.wav"],
            "trouble_x3", shouldMatch=True)

    def test_trouble_x4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x4.wav"],
            "trouble_x4", shouldMatch=True)

    def test_trouble_x5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x5.wav"],
            "trouble_x5", shouldMatch=True)

    def test_trouble_x6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x6.wav"],
            "trouble_x6", shouldMatch=True)

    def test_wayfaring_wayfaring(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "wayfaring.wav"],
            "wayfaring_wayfaring", shouldMatch=True)

    def test_wayfaring_x7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x7.wav"],
            "wayfaring_x7", shouldMatch=True)

    def test_wayfaring_x8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x8.wav"],
            "wayfaring_x8", shouldMatch=True)

    def test_wayfaring_x9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x9.wav"],
            "wayfaring_x9", shouldMatch=True)

    def test_x10_x10(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x10.wav", self.testSuiteDir + "x10.wav"],
            "x10_x10", shouldMatch=True)

    def test_x11_x10(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x11.wav", self.testSuiteDir + "x10.wav"],
            "x11_x10", shouldMatch=True)

    def test_x11_x11(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x11.wav", self.testSuiteDir + "x11.wav"],
            "x11_x11", shouldMatch=True)

    def test_x12_x12(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x12.wav", self.testSuiteDir + "x12.wav"],
            "x12_x12", shouldMatch=True)

    def test_x1_x1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x1.wav", self.testSuiteDir + "x1.wav"],
            "x1_x1", shouldMatch=True)

    def test_x1_x2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x1.wav", self.testSuiteDir + "x2.wav"],
            "x1_x2", shouldMatch=True)

    def test_x1_x3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x1.wav", self.testSuiteDir + "x3.wav"],
            "x1_x3", shouldMatch=True)

    def test_x2_x1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x2.wav", self.testSuiteDir + "x1.wav"],
            "x2_x1", shouldMatch=True)

    def test_x2_x2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x2.wav", self.testSuiteDir + "x2.wav"],
            "x2_x2", shouldMatch=True)

    def test_x2_x3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x2.wav", self.testSuiteDir + "x3.wav"],
            "x2_x3", shouldMatch=True)

    def test_x3_x1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x3.wav", self.testSuiteDir + "x1.wav"],
            "x3_x1", shouldMatch=True)

    def test_x3_x2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x3.wav", self.testSuiteDir + "x2.wav"],
            "x3_x2", shouldMatch=True)

    def test_x3_x3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x3.wav", self.testSuiteDir + "x3.wav"],
            "x3_x3", shouldMatch=True)

    def test_x4_x4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x4.wav", self.testSuiteDir + "x4.wav"],
            "x4_x4", shouldMatch=True)

    def test_x4_x5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x4.wav", self.testSuiteDir + "x5.wav"],
            "x4_x5", shouldMatch=True)

    def test_x4_x6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x4.wav", self.testSuiteDir + "x6.wav"],
            "x4_x6", shouldMatch=True)

    def test_x5_x4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x5.wav", self.testSuiteDir + "x4.wav"],
            "x5_x4", shouldMatch=True)

    def test_x5_x5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x5.wav", self.testSuiteDir + "x5.wav"],
            "x5_x5", shouldMatch=True)

    def test_x5_x6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x5.wav", self.testSuiteDir + "x6.wav"],
            "x5_x6", shouldMatch=True)

    def test_x6_x4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x6.wav", self.testSuiteDir + "x4.wav"],
            "x6_x4", shouldMatch=True)

    def test_x6_x5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x6.wav", self.testSuiteDir + "x5.wav"],
            "x6_x5", shouldMatch=True)

    def test_x6_x6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x6.wav", self.testSuiteDir + "x6.wav"],
            "x6_x6", shouldMatch=True)

    def test_x7_x7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x7.wav", self.testSuiteDir + "x7.wav"],
            "x7_x7", shouldMatch=True)

    def test_x7_x8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x7.wav", self.testSuiteDir + "x8.wav"],
            "x7_x8", shouldMatch=True)

    def test_x7_x9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x7.wav", self.testSuiteDir + "x9.wav"],
            "x7_x9", shouldMatch=True)

    def test_x8_x7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x8.wav", self.testSuiteDir + "x7.wav"],
            "x8_x7", shouldMatch=True)

    def test_x8_x8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x8.wav", self.testSuiteDir + "x8.wav"],
            "x8_x8", shouldMatch=True)

    def test_x8_x9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x8.wav", self.testSuiteDir + "x9.wav"],
            "x8_x9", shouldMatch=True)

    def test_x9_x7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x9.wav", self.testSuiteDir + "x7.wav"],
            "x9_x7", shouldMatch=True)

    def test_x9_x8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x9.wav", self.testSuiteDir + "x8.wav"],
            "x9_x8", shouldMatch=True)

    def test_x9_x9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x9.wav", self.testSuiteDir + "x9.wav"],
            "x9_x9", shouldMatch=True)

    # Files that SHOULD NOT match
    def test_hewlett_trouble(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "trouble.wav"],
            "hewlett_trouble", shouldMatch=False)

    def test_hewlett_x1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x1.wav"],
            "hewlett_x1", shouldMatch=False)

    def test_hewlett_x2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x2.wav"],
            "hewlett_x2", shouldMatch=False)

    def test_hewlett_x3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x3.wav"],
            "hewlett_x3", shouldMatch=False)

    def test_trouble_hewlett(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "hewlett.wav"],
            "trouble_hewlett", shouldMatch=False)

    def test_trouble_x7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x7.wav"],
            "trouble_x7", shouldMatch=False)

    def test_trouble_x8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x8.wav"],
            "trouble_x8", shouldMatch=False)

    def test_trouble_x9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x9.wav"],
            "trouble_x9", shouldMatch=False)

    def test_trouble_x10(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x10.wav"],
            "trouble_x10", shouldMatch=False)

    def test_trouble_x11(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x11.wav"],
            "trouble_x11", shouldMatch=False)

    def test_trouble_x12(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "trouble.wav", self.testSuiteDir + "x12.wav"],
            "trouble_x12", shouldMatch=False)

    def test_wayfaring_trouble(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "trouble.wav"],
            "wayfaring_trouble", shouldMatch=False)

    def test_wayfaring_x1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x1.wav"],
            "wayfaring_x1", shouldMatch=False)

    def test_wayfaring_x2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x2.wav"],
            "wayfaring_x2", shouldMatch=False)

    def test_wayfaring_x3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x3.wav"],
            "wayfaring_x3", shouldMatch=False)

    def test_wayfaring_x4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x4.wav"],
            "wayfaring_x4", shouldMatch=False)

    def test_wayfaring_x5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x5.wav"],
            "wayfaring_x5", shouldMatch=False)

    def test_wayfaring_x6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x6.wav"],
            "wayfaring_x6", shouldMatch=False)

    def test_wayfaring_x10(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x10.wav"],
            "wayfaring_x10", shouldMatch=False)

    def test_wayfaring_x11(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x11.wav"],
            "wayfaring_x11", shouldMatch=False)

    def test_wayfaring_x12(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "wayfaring.wav", self.testSuiteDir + "x12.wav"],
            "wayfaring_x12", shouldMatch=False)

    def test_x10_x7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x10.wav", self.testSuiteDir + "x7.wav"],
            "x10_x7", shouldMatch=False)

    def test_x11_x7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x11.wav", self.testSuiteDir + "x7.wav"],
            "x11_x7", shouldMatch=False)

    def test_hewlett_x8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x8.wav"],
            "x10_x8", shouldMatch=False)

    def test_x11_x8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x11.wav", self.testSuiteDir + "x8.wav"],
            "x11_x8", shouldMatch=False)

    def test_hewlett_x9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "hewlett.wav", self.testSuiteDir + "x9.wav"],
            "hewlett_x9", shouldMatch=False)

    def test_x12_x9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x12.wav", self.testSuiteDir + "x9.wav"],
            "x12_x9", shouldMatch=False)

    def test_x1_x10(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x1.wav", self.testSuiteDir + "x10.wav"],
            "x1_x10", shouldMatch=False)

    def test_x1_x11(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x1.wav", self.testSuiteDir + "x11.wav"],
            "x1_x11", shouldMatch=False)

    def test_x1_x12(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "x1.wav", self.testSuiteDir + "x12.wav"],
            "x1_x12", shouldMatch=False)


if __name__ == "__main__":
    unittest.main()
