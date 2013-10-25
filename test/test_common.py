import unittest
import os
import re
from subprocess import *

class TestCommon(unittest.TestCase):
    testSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/"
    testCWD = os.path.dirname(os.path.abspath(__file__)) + "/../"
    runCommand = os.path.dirname(os.path.abspath(__file__)) + "/../p4500"

    errorRegexString = '^ERROR(.*)$'
    errorPattern = re.compile(errorRegexString)

    matchRegexString = '^MATCH$'
    matchPattern = re.compile(matchRegexString)

    noMatchRegexString = '^NO MATCH$'
    noMatchPattern = re.compile(noMatchRegexString)

    def create_command(self, files):
        command = [self.runCommand]
        for f in files:
            command.append("-f")
            command.append(f)

        return command

    def should_produce_errors(self, files=[], name="should_not_produce_error", raw_command=False):
        if raw_command:
            command = files
        else:
            command = self.create_command(files)

        call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
        callOut, callErr = call.communicate()
        returnCode = call.returncode
        currLine = 0

        self.assertNotEqual(returnCode, 0,
                            msg=name + " - should_produce_errors: Return Code Incorrect (Expected:Not 0 Actual:" + str(
                                returnCode) + ")")

        #Checking Error Message
        for line in callErr.splitlines():
            self.assertTrue(self.errorPattern.match(line),
                            msg=name + " - should_produce_errors: STDERR incorrect line (Output line " + str(
                                currLine) + ") (Expected:" + self.errorRegexString + " Actual:" + line + ")")
            currLine += 1

    def should_not_produce_errors(self, files=[], name="should_not_produce_error", shouldMatch=True):
        if (shouldMatch):
            pattern = self.matchPattern
            reString = self.matchRegexString
        else:
            pattern = self.noMatchPattern
            reString = self.noMatchRegexString

        command = self.create_command(files)

        call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
        callOut, callErr = call.communicate()
        returnCode = call.returncode
        currLine = 0

        self.assertEquals(returnCode, 0,
                          msg=name + " - should_not_produce_errors: Return Code Incorrect (Expected:0 Actual:" + str(
                              returnCode) + ")")

        #Checking Output Message
        for line in callOut.splitlines():
            self.assertTrue(pattern.match(line),
                            msg=name + " - should_not_produce_errors: STDOUT incorrect line (Line " + str(
                                currLine) + ") (Expected:" + reString + " Actual:" + line + ")")
            currLine += 1