import codecs
import unittest
from crypto import KeyManager


class MyTestCase(unittest.TestCase):

    # test key generation is different in 2 different instances
    def test_key_generation(self):
        myDes = KeyManager()
        k1 = myDes.generate_key()
        k2 = myDes.generate_key()

        self.assertNotEqual(k1, k2)  # add assertion here

    def test_key_to_file(self):
        myDes = KeyManager()
        k1 = myDes.generate_key()

        myDes.key_to_file(k1)
        print(k1)
        
    def test_load_key(self):
        myDes = KeyManager()
        k1 = myDes.generate_key()
        myDes.key_to_file(k1)

        k2 = myDes.load_key()
        k3 = myDes.load_key()
        self.assertEqual(k3, k2)

    def test_client_server(self):



if __name__ == '__main__':
    unittest.main()
