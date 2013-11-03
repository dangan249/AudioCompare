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
            [self.testSuiteDir + "not_a_wav.wav", self.testSuiteDir + "not_a_wav2.wav"],
            "invalidformat_input0")

    def test_invalidformat_input1(self):
        self.should_produce_errors(
            [self.testSuiteDir + "not_a_mp3.mp3", self.testSuiteDir + "test1_orig.wav"],
            "invalidformat_input1")

    def test_invalidformat_input2(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "not_a_wav.wav"],
            "invalidformat_input2")

    def test_invalidformat_input3(self):
        self.should_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "not_a_mp3.mp3"],
            "invalidformat_input3")

    def test_invalidformat_input4(self):
        self.should_produce_errors(
            [self.testSuiteDir + "not_a_wav.wav", self.testSuiteDir + "not_a_wav.wav"],
            "invalidformat_input4")

    def test_invalidformat_input5(self):
        self.should_produce_errors(
            [self.testSuiteDir + "not_a_mp3.wav", self.testSuiteDir + "not_a_mp3.wav"],
            "invalidformat_input5")


    #tests: invalidcommand_input
    #Note: If "Valid Command Line Input changes, we need to change these"

    def test_invalidcommand_input0(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "not_a_wav.wav", self.testSuiteDir + "not_a_wav2.wav"],
            "invalidformat_input0", raw_command=True)

    def test_invalidcommand_input01(self):
        self.should_produce_errors(
            [self.runCommand, self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_orig.wav"],
            "invalidcommand_input0", raw_command=True)

    def test_invalidcommand_input01(self):
        self.should_produce_errors(
            [self.runCommand, "-f", self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_orig.wav"],
            "invalidcommand_input01", raw_command=True)

    def test_invalidcommand_input02(self):
        self.should_produce_errors(
            [self.runCommand, "-f", self.testSuiteDir + "test1_orig.wav", "-g", self.testSuiteDir + "test1_orig.wav"],
            "invalidcommand_input02", raw_command=True)

    def test_invalidcommand_input03(self):
        self.should_produce_errors(
            [self.runCommand, "-f", self.testSuiteDir + "test1_orig.wav", "-f", self.testSuiteDir + "test1_orig.wav", "-t", "afsdfsdfgzgsdagsdg"],
            "invalidcommand_input03", raw_command=True)

    def test_invalidcommand_input04(self):
        self.should_produce_errors(
            [self.runCommand, "-f", self.testSuiteDir + "test1_orig.wav", "-f", self.testSuiteDir + "test1_orig.wav", "-qdqwddsvFET54TGREGEGVFDVV", "afsdfsdfgzgsdagsdg"],
            "invalidcommand_input04", raw_command=True)

    def test_invalidcommand_input05(self):
        self.should_produce_errors(
            [self.runCommand, "-f", self.testSuiteDir + "test1_orig.wav", "-f", self.testSuiteDir + "test1_orig.wav", "FDSAGDFGADFGDVADFBADB", "afsdfsdfgzgsdagsdg"],
            "invalidcommand_input05", raw_command=True)

    def test_invalidcommand_input06(self):
        self.should_produce_errors(
            [self.runCommand, "-f", self.testSuiteDir + "test1_orig.wav"],
            "invalidcommand_input06", raw_command=True)

    def test_invalidcommand_input07(self):
        self.should_produce_errors(
            [self.runCommand, "-f", "-f"],
            "invalidcommand_input07", raw_command=True)

    def test_invalidcommand_input08(self):
        self.should_produce_errors(
            [self.runCommand, "-f", self.testSuiteDir + "test1_orig.wav", "-f", self.testSuiteDir + "test1_orig.wav", "-qdqwddsvFET54TGREGEGVFDVV"],
            "invalidcommand_input08", raw_command=True)

    def test_invalidcommand_input09(self):
        self.should_produce_errors(
            [self.runCommand, "-qdqwddsvFET54TGREGEGVFDVV"],
            "invalidcommand_input09", raw_command=True)

    #Tests: matching_input
    #Note: Not prepended with "test_" due to later efficiency testing

    def matching_input0(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input0", shouldMatch=True)

    def matching_input1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv1.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input1", shouldMatch=True)

    def matching_input2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv2.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "matching_input2", shouldMatch=True)

    def matching_input3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_deriv2.wav"],
            "matching_input3", shouldMatch=True)

    def matching_input4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv3.wav", self.testSuiteDir + "test1_orig.wav"],
            "matching_input4", shouldMatch=True)

    def matching_input5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test2_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "matching_input5", shouldMatch=True)

    def matching_input6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test3_orig.wav"],
            "matching_input6", shouldMatch=True)

    def matching_input7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test1_deriv1.wav"],
            "matching_input7", shouldMatch=True)

    def matching_input8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test4_deriv2.wav", self.testSuiteDir + "test4_orig.mp3"],
            "matching_input8", shouldMatch=True)

    def matching_input9(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test4_orig.mp3", self.testSuiteDir + "test4_deriv2.wav"],
            "matching_input9", shouldMatch=True)

    def matching_input10(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test4_orig.mp3", self.testSuiteDir + "test4_deriv1.wav"],
            "matching_input10", shouldMatch=True)

    def matching_input11(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test4_deriv1.wav", self.testSuiteDir + "test4_orig.mp3"],
            "matching_input11", shouldMatch=True)

    #Tests: non_matching_input
    #Note: Not prepended with "test_" due to later efficiency testing

    def non_matching_input0(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input0", shouldMatch=False)

    def non_matching_input1(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv1.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input1", shouldMatch=False)

    def non_matching_input2(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test1_deriv2.wav", self.testSuiteDir + "test3_orig.wav"],
            "non_matching_input2", shouldMatch=False)

    def non_matching_input3(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test2_orig.wav"],
            "non_matching_input3", shouldMatch=False)

    def non_matching_input4(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test4_orig.mp3", self.testSuiteDir + "test3_orig.wav"],
            "non_matching_input4", shouldMatch=False)

    def non_matching_input5(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test4_orig.mp3"],
            "non_matching_input5", shouldMatch=False)

    def non_matching_input6(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test5_orig.mp3", self.testSuiteDir + "test4_orig.mp3"],
            "non_matching_input6", shouldMatch=False)

    def non_matching_input7(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test4_orig.mp3", self.testSuiteDir + "test5_orig.mp3"],
            "non_matching_input7", shouldMatch=False)

    def non_matching_input8(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "test3_orig.wav", self.testSuiteDir + "test5_orig.mp3"],
            "non_matching_input8", shouldMatch=False)


    #Tests: efficiency_expectations

    def test_efficiency_expectations00(self):
        self.should_finish_in_interval(10, "efficiency_expectations00", self.matching_input0)

    def test_efficiency_expectations01(self):
        self.should_finish_in_interval(10, "efficiency_expectations01", self.matching_input1)

    def test_efficiency_expectations02(self):
        self.should_finish_in_interval(10, "efficiency_expectations02", self.matching_input2)

    def test_efficiency_expectations03(self):
        self.should_finish_in_interval(10, "efficiency_expectations03", self.matching_input3)

    def test_efficiency_expectations04(self):
        self.should_finish_in_interval(10, "efficiency_expectations04", self.matching_input4)

    def test_efficiency_expectations05(self):
        self.should_finish_in_interval(10, "efficiency_expectations05", self.matching_input5)

    def test_efficiency_expectations06(self):
        self.should_finish_in_interval(10, "efficiency_expectations06", self.matching_input6)

    def test_efficiency_expectations07(self):
        self.should_finish_in_interval(10, "efficiency_expectations07", self.matching_input7)

    def test_efficiency_expectations08(self):
        self.should_finish_in_interval(10, "efficiency_expectations08", self.matching_input8)

    def test_efficiency_expectations09(self):
        self.should_finish_in_interval(10, "efficiency_expectations09", self.matching_input9)

    def test_efficiency_expectations10(self):
        self.should_finish_in_interval(10, "efficiency_expectations10", self.matching_input10)

    def test_efficiency_expectations11(self):
        self.should_finish_in_interval(10, "efficiency_expectations11", self.matching_input11)

    def test_efficiency_expectations12(self):
        self.should_finish_in_interval(10, "efficiency_expectations12", self.non_matching_input0)

    def test_efficiency_expectations13(self):
        self.should_finish_in_interval(10, "efficiency_expectations13", self.non_matching_input1)

    def test_efficiency_expectations14(self):
        self.should_finish_in_interval(10, "efficiency_expectations14", self.non_matching_input2)

    def test_efficiency_expectations15(self):
        self.should_finish_in_interval(10, "efficiency_expectations15", self.non_matching_input3)

    def test_efficiency_expectations16(self):
        self.should_finish_in_interval(10, "efficiency_expectations16", self.non_matching_input4)

    def test_efficiency_expectations17(self):
        self.should_finish_in_interval(10, "efficiency_expectations17", self.non_matching_input5)

    def test_efficiency_expectations18(self):
        self.should_finish_in_interval(10, "efficiency_expectations18", self.non_matching_input6)

    def test_efficiency_expectations19(self):
        self.should_finish_in_interval(10, "efficiency_expectations19", self.non_matching_input7)


if __name__ == "__main__":
    unittest.main()
