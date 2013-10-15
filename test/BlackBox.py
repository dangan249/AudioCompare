import unittest
import os
import re
from subprocess import *


class AudioMatchBlackBox(unittest.TestCase):
    #Get current directory. We know what files are in here
    testSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/"
    testCWD = os.path.dirname(os.path.abspath(__file__)) + "/../"
    runCommand = os.path.dirname(os.path.abspath(__file__)) + "/../p4500"

    #tests: empty_args
    def test_empty_args0(self):
        self.should_produce_errors([self.runCommand], "empty_args0")

    def test_empty_args1(self):
        self.should_produce_errors([self.runCommand, " "], "empty_args1")

    def test_empty_args2(self):
        self.should_produce_errors([self.runCommand, "", " "], "empty_args2")

    def test_empty_args3(self):
        self.should_produce_errors([self.runCommand, " ", " "], "empty_args3")

    #tests: nonexistant_inputs
    def test_nonexistant_input0(self):
        self.should_produce_errors([self.runCommand, self.testSuiteDir + "nonexistant.wav"], "nonexistant_input0")

    def test_nonexistant_input1(self):
        self.should_produce_errors([self.runCommand, self.testSuiteDir + "nonexistant", "nonexistant"],
                                   "nonexistant_input1")

    def test_nonexistant_input2(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "nonexistant.wav", self.testSuiteDir + "nonexistant.wav"],
            "nonexistant_input2")

    def test_nonexistant_input3(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_deriv1.wav ", self.testSuiteDir + "nonexistant.wav"],
            "nonexistant_input3")

    def test_nonexistant_input4(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "nonexistant.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "nonexistant_input4")

    def test_nonexistant_input5(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "test_deriv1.wav.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "nonexistant_input5")

    def test_nonexistant_input6(self):
        self.should_produce_errors([self.runCommand, self.testSuiteDir + "test1_orig.wav"], "nonexistant_input6")

    def test_nonexistant_input7(self):
        self.should_produce_errors([self.runCommand, self.testSuiteDir + "test1_orig.wav"], "nonexistant_input7")

    #tests: invalidformat_input

    # why should this produce an error?
    def test_invalidformat_input0(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "test5_deriv1.wav", self.testSuiteDir + "test5_deriv1.wav"],
            "invalidformat_input0")

    # why should this produce an error?
    def test_invalidformat_input1(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "test5_deriv1.mp3", self.testSuiteDir + "test4_deriv2.wav"],
            "invalidformat_input1")

    def test_invalidformat_input2(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "test4_orig.mp3", self.testSuiteDir + "test4_deriv1.wav"],
            "invalidformat_input2")

    def test_invalidformat_input3(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "test4_orig.mp3", self.testSuiteDir + "test1_orig.wav"],
            "invalidformat_input4")

#Tests: matching_input

    def test_matching_input0(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input0", shouldMatch=True)

    def test_matching_input1(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_deriv1.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input1", shouldMatch=True)

    def test_matching_input2(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_deriv2.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "matching_input2", shouldMatch=True)

    def test_matching_input3(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_deriv2.wav"],
            "matching_input3", shouldMatch=True)

    def test_matching_input4(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_deriv3.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input4", shouldMatch=True)

    def test_matching_input5(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test2_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "matching_input5", shouldMatch=True)

    def test_matching_input6(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test3_orig.wav"],
            "matching_input6", shouldMatch=True)

    #Tests: non_matching_input
    def test_non_matching_input0(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input0", shouldMatch=False)

    def test_non_matching_input1(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_deriv1.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input1", shouldMatch=False)

    def test_non_matching_input2(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_deriv2.wav", self.testSuiteDir + "test3_orig.wav"],
            "non_matching_input2", shouldMatch=False)

    def test_non_matching_input3(self):
        self.should_not_produce_errors(
            [self.runCommand, self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input3", shouldMatch=False)

    def should_produce_errors(self, command=[], name="should_not_produce_error"):
        reString = '^ERROR(.*)$'
        errorPattern = re.compile(reString)

        call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
        callOut, callErr = call.communicate()
        returnCode = call.returncode
        currLine = 0

        self.assertNotEqual(returnCode, 0,
                            msg=name + " - should_produce_errors: Return Code Incorrect (Expected:Not 0 Actual:" + str(
                                returnCode) + ")")

        #Checking Error Message
        for line in callErr.splitlines():
            self.assertTrue(errorPattern.match(line),
                            msg=name + " - should_produce_errors: STDERR incorrect line (Output line " + str(
                                currLine) + ") (Expected:" + reString + " Actual:" + line + ")")
            currLine += 1

    def should_not_produce_errors(self, command=[], name="should_not_produce_error", shouldMatch=True):
        if (shouldMatch):
            reString = '^MATCH$'
        else:
            reString = '^NO MATCH$'
        matchPattern = re.compile(reString)

        call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
        callOut, callErr = call.communicate()
        returnCode = call.returncode
        currLine = 0

        self.assertEquals(returnCode, 0,
                          msg=name + " - should_not_produce_errors: Return Code Incorrect (Expected:0 Actual:" + str(
                              returnCode) + ")")

        #Checking Output Message
        for line in callOut.splitlines():
            self.assertTrue(matchPattern.match(line),
                            msg=name + " - should_not_produce_errors: STDOUT incorrect line (Line " + str(
                                currLine) + ") (Expected:" + reString + " Actual:" + line + ")")
            currLine += 1


if __name__ == "__main__":
    unittest.main()
