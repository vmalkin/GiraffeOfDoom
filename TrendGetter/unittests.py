import unittest
from trendgetter_5 import medianfilter

class Functionstest(unittest.TestCase):
    def test_medianfilter1(self):
        testarray = ["a,2", "b,7", "c,2", "d,2", "e,2"]
        resultarray = ["b,2", "c,2", "d,2", ]
        self.assertEqual(resultarray, medianfilter(testarray))

    def test_medianfilter2(self):
        testarray = ["a,2", "b,7", "c,2", "d,2", "e,2", "f,7", "g,7", "h,2"]
        resultarray = ["b,2", "c,2", "d,2", "e,2", "f,7", "g,7"]
        self.assertEqual(resultarray, medianfilter(testarray))

if __name__ == "__main__":
    unittest.main()

