import unittest
import os
import re
from subprocess import *
from test_common import *


class AudioMatchBlackBox(TestCommon):

    #tests: empty_args
    def test_empty_args0(self):
        self.should_produce_errors([self.runCommand], "empty_args0", raw_command=True)

    def test_empty_args1(self):
        self.should_produce_errors([self.runCommand, " "], "empty_args1", raw_command=True)

    def test_empty_args2(self):
        self.should_produce_errors([self.runCommand, "", " "], "empty_args2", raw_command=True)

    def test_empty_args3(self):
        self.should_produce_errors([self.runCommand, " ", " "], "empty_args3", raw_command=True)

    #tests: nonexistant_inputs
    def test_nonexistant_input0(self):
        self.should_produce_errors([self.testSuiteDir + "nonexistant.wav"], "nonexistant_input0")

    def test_nonexistant_input1(self):
        self.should_produce_errors([self.testSuiteDir + "nonexistant", "nonexistant"],
                                   "nonexistant_input1")

    def test_nonexistant_input2(self):
        self.should_produce_errors(
            [self.testSuiteDir + "nonexistant.wav", self.testSuiteDir + "nonexistant.wav"],
            "nonexistant_input2")

    def test_nonexistant_input3(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test1_deriv1.wav ", self.testSuiteDir + "nonexistant.wav"],
            "nonexistant_input3")

    def test_nonexistant_input4(self):
        self.should_produce_errors(
            [self.testSuiteDir + "nonexistant.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "nonexistant_input4")

    def test_nonexistant_input5(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test_deriv1.wav.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "nonexistant_input5")

    def test_nonexistant_input6(self):
        self.should_produce_errors([self.testSuiteDir + "test1_orig.wav"], "nonexistant_input6")

    def test_nonexistant_input7(self):
        self.should_produce_errors([self.testSuiteDir + "test1_orig.wav"], "nonexistant_input7")

    #tests: invalidformat_input

    def test_invalidformat_input0(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test5_deriv1.wav", self.testSuiteDir + "test5_deriv1.wav"],
            "invalidformat_input0")

    def test_invalidformat_input1(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test5_deriv1.mp3", self.testSuiteDir + "test4_deriv2.wav"],
            "invalidformat_input1")

    def test_invalidformat_input2(self):
        self.should_produce_errors(
            [self.testSuiteDir + "not_a_wav.wav", self.testSuiteDir + "not_a_wav2.wav"],
            "invalidformat_input2")

    def test_invalidformat_input3(self):
        self.should_produce_errors(
            [self.testSuiteDir + "not_a_mp3.mp3", self.testSuiteDir + "test1_orig.wav"],
            "invalidformat_input3")

    def test_invalidformat_input4(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "not_a_wav.wav"],
            "invalidformat_input4")

    def test_invalidformat_input5(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "not_a_mp3.mp3"],
            "invalidformat_input5")

    def test_invalidformat_input6(self):
        self.should_produce_errors(
            [self.testSuiteDir + "not_a_wav.wav", self.testSuiteDir + "not_a_wav.wav"],
            "invalidformat_input6")

    def test_invalidformat_input7(self):
        self.should_produce_errors(
            [self.testSuiteDir + "not_a_mp3.wav", self.testSuiteDir + "not_a_mp3.wav"],
            "invalidformat_input7")

#Tests: matching_input

    def test_matching_input0(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input0", shouldMatch=True)

    def test_matching_input1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv1.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input1", shouldMatch=True)

    def test_matching_input2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv2.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "matching_input2", shouldMatch=True)

    def test_matching_input3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_deriv2.wav"],
            "matching_input3", shouldMatch=True)

    def test_matching_input4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv3.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input4", shouldMatch=True)

    def test_matching_input5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test2_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "matching_input5", shouldMatch=True)

    def test_matching_input6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test3_orig.wav"],
            "matching_input6", shouldMatch=True)

    def test_matching_input7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "matching_input7", shouldMatch=True)

    #Tests: non_matching_input
    def test_non_matching_input0(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input0", shouldMatch=False)

    def test_non_matching_input1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv1.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input1", shouldMatch=False)

    def test_non_matching_input2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv2.wav", self.testSuiteDir + "test3_orig.wav"],
            "non_matching_input2", shouldMatch=False)

    def test_non_matching_input3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input3", shouldMatch=False)


if __name__ == "__main__":
    unittest.main()
