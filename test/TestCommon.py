import unittest
import os
import re
import time
from subprocess import *

class TestCommon(unittest.TestCase):
    OUTPUT_ERROR = 0
    OUTPUT_NO_MATCH = 1
    OUTPUT_MATCH = 2

    testSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/"
    testCWD = os.path.dirname(os.path.abspath(__file__)) + "/../"
    runCommand = os.path.dirname(os.path.abspath(__file__)) + "/../audiomatch"

    def create_command(self, files, whichAreDirectories=[False, False]):
        command = [self.runCommand]
        currFile = 0

        for f in files:
            if(whichAreDirectories[currFile] == False):
                command.append("-f")
            else:
                command.append("-d")

            command.append(f)
            currFile = currFile + 1

        return command

    def get_regex_string(self, operation, files = [], shorter = '', longer = ''):
        if(operation == self.OUTPUT_ERROR):
            return '^ERROR(.*)$'
        elif(operation == self.OUTPUT_NO_MATCH):
            return '^NO MATCH$'
        elif(operation == self.OUTPUT_MATCH):
            return '^MATCH {0} {1}((?=\s) \((([\x00-\x28]|[\x30-\x7F]){{0,25}})\)$|$)'.format(shorter, longer)
        else:
            return '';

    def get_regex(self, operation, files = [], shorter = '', longer = ''):
        return re.compile(self.get_regex_string(operation, files, shorter, longer))

    def should_finish_in_interval(self, intervalSeconds, name, otherFunc, otherFuncArgs = {}):
        intervalMilliseconds = intervalSeconds*1000;

        t1 = int(round(time.time() * 1000))
        otherFunc(**otherFuncArgs);
        t2 = int(round(time.time() * 1000))

        actualTime = (t2 - t1)

        self.assertTrue(actualTime < intervalMilliseconds, 
            msg=name + " - should_finish_in_interval: Expected Time: < "+str(intervalMilliseconds)+"ms Actual:"+str(actualTime)+"ms");

    def should_produce_set(self, files=[], name="should_produce_set", whichAreDirectories=[], *returnSet):
        command = self.create_command([self.testSuiteDir + files[0], self.testSuiteDir + files[1]], whichAreDirectories)

        errRegexes = []
        outRegexes = []

        #Parse all output regex for use when comparing output
        for outputTuple in returnSet:
            if(len(outputTuple) > 2):
                currRegex = self.get_regex_string(*outputTuple)
            else:
                currRegex = [self.get_regex_string(outputTuple[0], outputTuple[1], outputTuple[1][0], outputTuple[1][1]), self.get_regex_string(outputTuple[0], outputTuple[1], outputTuple[1][1], outputTuple[1][0])]

            if(outputTuple[0] == self.OUTPUT_ERROR):
                errRegexes.append(currRegex)
            else:
                outRegexes.append(currRegex)

        #Make the call
        call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
        callOut, callErr = call.communicate()
        returnCode = call.returncode

        #Check return code
        if(len(errRegexes) > 0):
            self.assertNotEqual(returnCode, 0,
                                msg=name + " - should_produce_errors_set: Return Code Incorrect (Expected:Not 0 Actual:" + str(
                                    returnCode) + ")")
        else:
            self.assertEqual(returnCode, 0,
                                msg=name + " - should_not_produce_errors_set: Return Code Incorrect (Expected:0 Actual:" + str(
                                    returnCode) + ")")

        #Checking Error Message
        errCount = 0
        for line in callErr.splitlines():

            foundRegex = -1
            currRegex = 0
            for errRegex in errRegexes:
                if(not isinstance(errRegex, basestring)):
                    compiledErrRegexes = [re.compile(errRegex[0]), re.compile(errRegex[1])]
                else:
                    compiledErrRegexes = [re.compile(errRegex)]

                
                for compiledErrRegex in compiledErrRegexes:
                    if(compiledErrRegex.match(line)):
                        foundRegex = currRegex
                        break
                    
                currRegex = currRegex + 1
                if(foundRegex > -1):
                    break

            self.assertTrue(foundRegex > -1,
                            msg=name + " - should_produce_errors_set: STDERR incorrect line (Output line " + str(
                                errCount) + ") (TotalErrorsNeeded: " + str(len(errRegexes) + errCount) + " MoreErrorsNeeded:" + str(len(errRegexes)) + " Error:" + line + ")")

            errRegexes.pop(foundRegex)
            errCount += 1

        #Checking Output Message
        outCount = 0
        for line in callOut.splitlines():

            foundRegex = -1
            currRegex = 0
            for outRegex in outRegexes:
                if(isinstance(outRegex, basestring)):
                    outRegex = [outRegex]

                compiledOutRegexes = []
                for currOutRegex in outRegex:
                    compiledOutRegexes.append(re.compile(currOutRegex))

                for compiledOutRegex in compiledOutRegexes:
                    if(compiledOutRegex.match(line)):
                        foundRegex = currRegex
                        break

                currRegex = currRegex + 1
                if(foundRegex > -1):
                    break


            self.assertTrue(foundRegex > -1,
                            msg=name + " - should_not_produce_errors_set: STDOUT incorrect line (Output line " + str(
                                outCount) + ") (TotalOutputsNeeded: " + str(len(outRegexes) + outCount) + " MoreOutputsNeeded:" + str(len(outRegexes)) + " Out:" + line + ")")
            outRegexes.pop(foundRegex)
            outCount += 1

        self.assertTrue(len(errRegexes) == 0, msg=name + " - set_expected_errors: Incorrect # of errros. Expected STDERR count:" + str(len(errRegexes) + errCount) + " Actual: " + str(errCount))
        self.assertTrue(len(outRegexes) == 0, msg=name + " - set_expected_output: Incorrect # of output. Expected STDOUT count:" + str(len(outRegexes) + outCount) + " Actual: " + str(outCount))



    def should_produce_errors(self, files=[], name="should_produce_error", raw_command=False):
        if raw_command:
            command = files
        else:
            command = self.create_command(files)

        call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
        callOut, callErr = call.communicate()
        returnCode = call.returncode
        currLine = 0

        errorRegexString = self.get_regex_string(self.OUTPUT_ERROR, files)
        errorPattern = self.get_regex(self.OUTPUT_ERROR, files)

        #Checking Error Message
        for line in callErr.splitlines():
            self.assertTrue(errorPattern.match(line),
                            msg=name + " - should_produce_errors: STDERR incorrect line (Output line " + str(
                                currLine) + ") (Expected:" + errorRegexString + " Actual:" + line + ")")
            currLine += 1

        #Check for extraneous output
        self.assertEquals(len(callOut), 0, 
                            msg=name + " - should_produce_errors: STDOUT nonempty (Output line 0) (Expected: Actual:" + callOut + ")");

        #Check return code
        self.assertNotEqual(returnCode, 0,
                            msg=name + " - should_produce_errors: Return Code Incorrect (Expected:Not 0 Actual:" + str(
                                returnCode) + ")")

    def should_not_produce_errors(self, files=[], name="should_not_produce_error", shouldMatch=True, shorter='', longer=''):
        if (shouldMatch):
            #MATCH shorter_file longer_file (optional: (UP TO 25 ascii characters that ARE NOT ")"))
            if(shorter != '' or longer != ''):
                reString = self.get_regex_string(self.OUTPUT_MATCH, files, shorter, longer)
                patterns = [self.get_regex(self.OUTPUT_MATCH, files, shorter, longer)]
            else:
                reString = self.get_regex_string(self.OUTPUT_MATCH, files, os.path.basename(files[0]), os.path.basename(files[1])) + " || " + self.get_regex_string(self.OUTPUT_MATCH, files, os.path.basename(files[1]), os.path.basename(files[0]))
                patterns = [self.get_regex(self.OUTPUT_MATCH, files, os.path.basename(files[0]), os.path.basename(files[1])), self.get_regex(self.OUTPUT_MATCH, files, os.path.basename(files[1]), os.path.basename(files[0]))]
        else:
            reString = self.get_regex_string(self.OUTPUT_NO_MATCH, files, shorter, longer)
            patterns = [self.get_regex(self.OUTPUT_NO_MATCH, files, shorter, longer)]

        command = self.create_command(files)

        call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
        callOut, callErr = call.communicate()
        returnCode = call.returncode
        currLine = 0

        #Checking Output Message
        for line in callOut.splitlines():
            didMatch = False

            for pattern in patterns:
                didMatch = pattern.match(line)
                if(didMatch):
                    break

            self.assertTrue(didMatch,
                            msg=name + " - should_not_produce_errors: STDOUT incorrect line (Line " + str(
                                currLine) + ") (Expected:" + reString + " Actual:" + line + ")")
            currLine += 1

        #Check for extraneous output
        self.assertEquals(len(callErr), 0, 
                            msg=name + " - should_not_produce_errors: STDERR nonempty (Output line 0) (Expected: Actual:" + callErr + ")");

        #Check return code
        self.assertEquals(returnCode, 0,
                          msg=name + " - should_not_produce_errors: Return Code Incorrect (Expected:0 Actual:" + str(
                              returnCode) + ")")
