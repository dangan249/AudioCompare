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

    def matching_input12(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3.mp3", self.testSuiteDir + "eminem.mp3.mp3"],
            "matching_input12", shouldMatch=True)

    def matching_input13(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3.mp3", self.testSuiteDir + "eminem.wav"],
            "matching_input13", shouldMatch=True)

    def matching_input14(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3.mp3", self.testSuiteDir + "eminem.wav.mp3"],
            "matching_input14", shouldMatch=True)

    def matching_input15(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem5-10_22k.mp3", self.testSuiteDir + "eminem.wav.mp3"],
            "matching_input15", shouldMatch=True)

    def matching_input16(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.wav.mp3", self.testSuiteDir + "eminem5-10_22k.mp3"],
            "matching_input16", shouldMatch=True)

    def matching_input17(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.wav.mp3", self.testSuiteDir + "eminem5-10_22k.wav"],
            "matching_input17", shouldMatch=True)

    def matching_input18(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem5-10_22k.mp3", self.testSuiteDir + "eminem5-10_22k.wav"],
            "matching_input18", shouldMatch=True)

    def matching_input19(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem5-10_22k.mp3", self.testSuiteDir + "eminem5-10.wav"],
            "matching_input19", shouldMatch=True)

    def matching_input20(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem_22k.mp3", self.testSuiteDir + "eminem5-10.wav"],
            "matching_input20", shouldMatch=True)

    def matching_input21(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem5-10.wav", self.testSuiteDir + "eminem_22k.mp3"],
            "matching_input21", shouldMatch=True)

    def matching_input22(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem_22k.wav", self.testSuiteDir + "eminem_22k.mp3"],
            "matching_input22", shouldMatch=True)

    def matching_input23(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem_22k.mp3", self.testSuiteDir + "eminem_22k.wav"],
            "matching_input23", shouldMatch=True)

    def matching_input24(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3", self.testSuiteDir + "eminem_22k.wav"],
            "matching_input24", shouldMatch=True)

    def matching_input25(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3", self.testSuiteDir + "eminem_22k.mp3"],
            "matching_input25", shouldMatch=True)

    def matching_input26(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3", self.testSuiteDir + "eminem5-10_22k.wav"],
            "matching_input26", shouldMatch=True)

    def matching_input27(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3", self.testSuiteDir + "eminem5-10_22k.mp3"],
            "matching_input27", shouldMatch=True)

    def matching_input28(self):
        self.should_not_produce_errors(
            [self.testSuiteDir + "eminem.mp3", self.testSuiteDir + "eminem5-10.wav"],
            "matching_input28", shouldMatch=True)

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

    def test_efficiency_expectations_matching00(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching00", self.matching_input0)

    def test_efficiency_expectations_matching01(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching01", self.matching_input1)

    def test_efficiency_expectations_matching02(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching02", self.matching_input2)

    def test_efficiency_expectations_matching03(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching03", self.matching_input3)

    def test_efficiency_expectations_matching04(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching04", self.matching_input4)

    def test_efficiency_expectations_matching05(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching05", self.matching_input5)

    def test_efficiency_expectations_matching06(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching06", self.matching_input6)

    def test_efficiency_expectations_matching07(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching07", self.matching_input7)

    def test_efficiency_expectations_matching08(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching08", self.matching_input8)

    def test_efficiency_expectations_matching09(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching09", self.matching_input9)

    def test_efficiency_expectations_matching10(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching10", self.matching_input10)

    def test_efficiency_expectations_matching11(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching11", self.matching_input11)

    def test_efficiency_expectations_matching12(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching12", self.matching_input12)

    def test_efficiency_expectations_matching13(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching13", self.matching_input13)

    def test_efficiency_expectations_matching14(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching14", self.matching_input14)

    def test_efficiency_expectations_matching15(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching15", self.matching_input15)

    def test_efficiency_expectations_matching16(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching16", self.matching_input16)

    def test_efficiency_expectations_matching17(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching17", self.matching_input17)

    def test_efficiency_expectations_matching18(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching18", self.matching_input18)

    def test_efficiency_expectations_matching19(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching19", self.matching_input19)

    def test_efficiency_expectations_matching20(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching20", self.matching_input20)

    def test_efficiency_expectations_matching21(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching21", self.matching_input21)

    def test_efficiency_expectations_matching22(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching22", self.matching_input22)

    def test_efficiency_expectations_matching23(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching23", self.matching_input23)

    def test_efficiency_expectations_matching24(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching24", self.matching_input24)

    def test_efficiency_expectations_matching25(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching25", self.matching_input25)

    def test_efficiency_expectations_matching26(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching26", self.matching_input26)

    def test_efficiency_expectations_matching27(self):
        self.should_finish_in_interval(10, "efficiency_expectations_matching27", self.matching_input27)

    def test_efficiency_expectations_non_matching01(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching01", self.non_matching_input0)

    def test_efficiency_expectations_non_matching02(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching02", self.non_matching_input1)

    def test_efficiency_expectations_non_matching03(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching03", self.non_matching_input2)

    def test_efficiency_expectations_non_matching04(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching04", self.non_matching_input3)

    def test_efficiency_expectations_non_matching05(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching05", self.non_matching_input4)

    def test_efficiency_expectations_non_matching06(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching06", self.non_matching_input5)

    def test_efficiency_expectations_non_matching07(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching07", self.non_matching_input6)

    def test_efficiency_expectations_non_matching08(self):
        self.should_finish_in_interval(10, "efficiency_expectations_non_matching08", self.non_matching_input7)


if __name__ == "__main__":
    unittest.main()
