import unittest
from InputFile import InputFile


class InputFileTest(unittest.TestCase):

    def setUp(self):
        self.inputFile1 = InputFile("../test_data/sine1.wav")

    def testFormat1(self):
        self.assertEqual(self.inputFile1.get_channels(), 2)
        self.assertEqual(self.inputFile1.get_block_align(), 4)

    def testRead1(self):
        data1 = self.inputFile1.get_audio_samples(1024)
        self.assertEqual(len(data1[0]), 1024)
        self.assertEqual(len(data1[1]), 1024)
        self.assertEqual(len(data1), 2)

    def testBadFile(self):
        self.assertRaises(IOError, InputFile, "../test_data/boston.txt")

    def tearDown(self):
        self.inputFile1.close()

if __name__ == "__main__":
    unittest.main()