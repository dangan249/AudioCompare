import os
from Matcher import Wang


def print_results(tests, should_match):
    for test in tests:
        matcher = Wang(test)
        (score, length) = matcher.match(debug=True)
        if not should_match:
            msg = "SHOULD NOT MATCH:"
        else:
            msg = "SHOULD MATCH:    "
        print "{m} score:{s}\tlength:{l}\tratio:{r} \t{f}".format(m=msg, s=score, l=length, r=score/length, f=map(os.path.basename, test))

def scores():
    testSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/"
    profTestSuiteDir = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/A6/"

    matching_tests = [
         (testSuiteDir + "eminem5-10.wav", testSuiteDir + "eminem5-10_22k.wav"),
         (testSuiteDir + "eminem5-10.wav", testSuiteDir + "eminem5-10.wav"),
         (testSuiteDir + "eminem5-10.wav", testSuiteDir + "eminem5-10_22k.mp3"),
         (testSuiteDir + "eminem.mp3", testSuiteDir + "eminem5-10_22k.mp3"),
         (testSuiteDir + "eminem.mp3", testSuiteDir + "eminem5-10_22k.wav"),
         (testSuiteDir + "test1_orig.wav", testSuiteDir + "test1_orig.wav"),
         (testSuiteDir + "test1_deriv2.wav", testSuiteDir + "test1_deriv1.wav"),
         (testSuiteDir + "test1_orig.wav", testSuiteDir + "test1_deriv2.wav"),
         (testSuiteDir + "test1_deriv3.wav", testSuiteDir + "test1_orig.wav"),
         (testSuiteDir + "test2_orig.wav", testSuiteDir + "test2_orig.wav"),
         (testSuiteDir + "test3_orig.wav", testSuiteDir + "test3_orig.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "hewlett.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x10.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x11.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x12.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "trouble.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x1.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x2.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x3.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x4.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x5.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x6.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "wayfaring.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "x8.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "x9.wav"),
         (profTestSuiteDir + "x10.wav", profTestSuiteDir + "x10.wav"),
         (profTestSuiteDir + "x11.wav", profTestSuiteDir + "x10.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "x11.wav", profTestSuiteDir + "x11.wav"),
         (profTestSuiteDir + "x12.wav", profTestSuiteDir + "x12.wav"),
         (profTestSuiteDir + "x1.wav", profTestSuiteDir + "x1.wav"),
         (profTestSuiteDir + "x1.wav", profTestSuiteDir + "x2.wav"),
         (profTestSuiteDir + "x1.wav", profTestSuiteDir + "x3.wav"),
         (profTestSuiteDir + "x2.wav", profTestSuiteDir + "x1.wav"),
         (profTestSuiteDir + "x2.wav", profTestSuiteDir + "x2.wav"),
         (profTestSuiteDir + "x2.wav", profTestSuiteDir + "x3.wav"),
         (profTestSuiteDir + "x3.wav", profTestSuiteDir + "x1.wav"),
         (profTestSuiteDir + "x3.wav", profTestSuiteDir + "x2.wav"),
         (profTestSuiteDir + "x3.wav", profTestSuiteDir + "x3.wav"),
         (profTestSuiteDir + "x4.wav", profTestSuiteDir + "x4.wav"),
         (profTestSuiteDir + "x4.wav", profTestSuiteDir + "x5.wav"),
         (profTestSuiteDir + "x4.wav", profTestSuiteDir + "x6.wav"),
         (profTestSuiteDir + "x5.wav", profTestSuiteDir + "x4.wav"),
         (profTestSuiteDir + "x5.wav", profTestSuiteDir + "x5.wav"),
         (profTestSuiteDir + "x5.wav", profTestSuiteDir + "x6.wav"),
         (profTestSuiteDir + "x6.wav", profTestSuiteDir + "x4.wav"),
         (profTestSuiteDir + "x6.wav", profTestSuiteDir + "x5.wav"),
         (profTestSuiteDir + "x6.wav", profTestSuiteDir + "x6.wav"),
         (profTestSuiteDir + "x7.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "x7.wav", profTestSuiteDir + "x8.wav"),
         (profTestSuiteDir + "x7.wav", profTestSuiteDir + "x9.wav"),
         (profTestSuiteDir + "x8.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "x8.wav", profTestSuiteDir + "x8.wav"),
         (profTestSuiteDir + "x8.wav", profTestSuiteDir + "x9.wav"),
         (profTestSuiteDir + "x9.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "x9.wav", profTestSuiteDir + "x8.wav"),
         (profTestSuiteDir + "x9.wav", profTestSuiteDir + "x9.wav"),
    ]

    nonmatching_tests = [
         (testSuiteDir + "test1_orig.wav", testSuiteDir + "test2_orig.wav"),
         (testSuiteDir + "test1_deriv1.wav", testSuiteDir + "test2_orig.wav"),
         (testSuiteDir + "test1_deriv2.wav", testSuiteDir + "test3_orig.wav"),
         (testSuiteDir + "test3_orig.wav", testSuiteDir + "test2_orig.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "trouble.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x1.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x2.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x3.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "hewlett.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x8.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x9.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x10.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x11.wav"),
         (profTestSuiteDir + "trouble.wav", profTestSuiteDir + "x12.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "trouble.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "x1.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "x2.wav"),
         (profTestSuiteDir + "wayfaring.wav", profTestSuiteDir + "x3.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "x10.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "x11.wav", profTestSuiteDir + "x7.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x8.wav"),
         (profTestSuiteDir + "x11.wav", profTestSuiteDir + "x8.wav"),
         (profTestSuiteDir + "hewlett.wav", profTestSuiteDir + "x9.wav"),
         (profTestSuiteDir + "x12.wav", profTestSuiteDir + "x9.wav"),
         (profTestSuiteDir + "x1.wav", profTestSuiteDir + "x10.wav"),
         (profTestSuiteDir + "x1.wav", profTestSuiteDir + "x11.wav"),
         (profTestSuiteDir + "x1.wav", profTestSuiteDir + "x12.wav")
    ]

    print_results(matching_tests, True)
    print_results(nonmatching_tests, False)

if __name__ == "__main__":
    scores()
