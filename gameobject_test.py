from gameobject import contra
import unittest


class ObjectsTest(unittest.TestCase):
    def testZeros(self):
        self.assertEqual(contra([0, 0],[0, 0]),True)
    def testOne1(self):
        self.assertEqual(contra([1, 0],[0, 0]),False)

    def testTwo2(self):
        self.assertEqual(contra([1, 1],[0, 1]),False)

    def test3(self):
        self.assertEqual(contra([1, 1],[1, 0]),False)
    
    def test4(self):
        self.assertEqual(contra([1, 1],[1, 1]),False)

    def test5(self):
        self.assertEqual(contra([1,0],[1,-1]),False)

    def test6(self):
        self.assertEqual(contra([1,0],[-1,0]),True)

    def test7(self):
        self.assertEqual(contra([1,2],[0,2]),False)
