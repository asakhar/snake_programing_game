import unittest
from os import path
from guinterface import create_from_template

class CreatefromtemplateTest(unittest.TestCase):
    def test_Tes1(self):
        create_from_template('#ff00ff')
        if not path.exists('images/#ff00ff.png'):
            assert False

    def test_Test2(self):
        color = '#ff0080'
        create_from_template(color)
        if not path.exists(f'images/{color}.png'):
            assert False
        
        

    def test_Test3(self):
        color = '#f0854f'
        create_from_template(color)
        if not path.exists(f'images/{color}.png'):
            assert False

    def test_multiple_grayscale_run(self):
        for i in range(256):
            color = '#'+hex(i)[2:].zfill(2)*3
            create_from_template(color)
            if not path.exists(f'images/{color}.png'):
                assert False


if __name__ == "__main__":
    unittest.main()
