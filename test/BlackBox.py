import unittest
import os
import re
from subprocess import *
from array import *

class AudioMatchBlackBox(unittest.TestCase):
	#Get current directory. We know what files are in here
	testSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/"
	testCWD = "../"
	runCommand = os.path.dirname(os.path.abspath(__file__))+"/../main.py"

	def setUp(self):
		pass

	def test_input_invalid(self):
		#tests: empty_args
		self.should_produce_errors([self.runCommand], "empty_args0")
		self.should_produce_errors([self.runCommand, " "], "empty_args1")
		self.should_produce_errors([self.runCommand, "", " "], "empty_args2")
		self.should_produce_errors([self.runCommand, " ", " "], "empty_args3")

		#tests: nonexistant_input
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"nonexistant.wav"], "nonexistant_input0")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"nonexistant", "nonexistant"], "nonexistant_input1")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"nonexistant.wav", self.testSuiteDir+"nonexistant.wav"], "nonexistant_input2")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test1_deriv1.wav ", self.testSuiteDir+"nonexistant.wav"], "nonexistant_input3")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"nonexistant.wav", self.testSuiteDir+"test1_deriv1.wav"], "nonexistant_input4")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test_deriv1.wav.wav", self.testSuiteDir+"test1_deriv1.wav"], "nonexistant_input5")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test1_orig.wav"], "nonexistant_input6")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test1_orig.wav"], "nonexistant_input7")

        #tests: invalidformat_input
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test4_deriv1.wav", self.testSuiteDir+"test4_deriv1.wav"], "invalidformat_input0")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test4_deriv1.wav", self.testSuiteDir+"test4_deriv2.wav"], "invalidformat_input1")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test4_orig.mp3", self.testSuiteDir+"test4_deriv1.wav"], "invalidformat_input2")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test1_deriv1.wav", self.testSuiteDir+"test4_deriv1.wav"], "invalidformat_input3")
		self.should_produce_errors([self.runCommand, self.testSuiteDir+"test4_orig.mp3", self.testSuiteDir+"test1_orig.wav"], "invalidformat_input4")

	def test_input_valid(self):
		#Tests: matching_input
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_orig.wav", self.testSuiteDir+"test1_orig.wav"], "matching_input0", shouldMatch=True)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_deriv1.wav", self.testSuiteDir+"test1_orig.wav"], "matching_input1", shouldMatch=True)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_deriv2.wav", self.testSuiteDir+"test1_deriv1.wav"], "matching_input2", shouldMatch=True)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_orig.wav", self.testSuiteDir+"test1_deriv2.wav"], "matching_input3", shouldMatch=True)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_deriv3.wav", self.testSuiteDir+"test1_orig.wav"], "matching_input4", shouldMatch=True)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test2_orig.wav", self.testSuiteDir+"test2_orig.wav"], "matching_input5", shouldMatch=True)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test3_orig.wav", self.testSuiteDir+"test3_orig.wav"], "matching_input6", shouldMatch=True)

		#Tests: non_matching_input
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_orig.wav", self.testSuiteDir+"test2_orig.wav"], "non_matching_input0", shouldMatch=False)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_deriv1.wav", self.testSuiteDir+"test2_orig.wav"], "non_matching_input1", shouldMatch=False)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test1_deriv2.wav", self.testSuiteDir+"test3_orig.wav"], "non_matching_input2", shouldMatch=False)
		self.should_not_produce_errors([self.runCommand, self.testSuiteDir+"test3_orig.wav", self.testSuiteDir+"test2_orig.wav"], "non_matching_input3", shouldMatch=False)

	def should_produce_errors(self, command = [], name = "should_not_produce_error"):
		reString = '^ERROR(.*)$'
		errorPattern = re.compile(reString)

		call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
		callOut, callErr = call.communicate()
		returnCode = call.returncode
		currLine = 0

		self.assertNotEqual(returnCode, 0, msg=name + " - should_produce_errors: Return Code Incorrect (Expected:Not 0 Actual:"+str(returnCode)+")")
		
		#Checking Error Message
		for line in callErr.splitlines():
			assertTrue(errorPattern.match(line), msg=name + " - should_produce_errors: STDERR incorrect line (Output line "+str(currLine)+") (Expected:"+reString+" Actual:"+line+")")
			currLine += 1

	def should_not_produce_errors(self, command = [], name = "should_not_produce_error", shouldMatch = True):
		if(shouldMatch): reString = '^MATCH$'
		else: reString = '^NO MATCH$'
		matchPattern = re.compile(reString)

		call = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testCWD)
		callOut, callErr = call.communicate()
		returnCode = call.returncode
		currLine = 0

		self.assertEquals(returnCode, 0, msg=name + " - should_not_produce_errors: Return Code Incorrect (Expected:0 Actual:"+str(returnCode)+")")

		#Checking Output Message
		for line in callOut.splitlines():
			self.assertTrue(matchPattern.match(line), msg=name + " - should_not_produce_errors: STDOUT incorrect line (Line "+str(currLine)+") (Expected:"+reString+" Actual:"+line+")")
			currLine += 1

unittest.main()
