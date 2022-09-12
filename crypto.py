from Crypto.Cipher import DES
from secrets import token_bytes
import base64

#from Crypto.SelfTest.Cipher.test_DES3 import key
from bitstring import BitArray

from typing import Iterable

class KeyManager:
    def bitize(self, byts: bytes) -> 'list[int]':
        """
        bitize bytes
        """
        bits = []
        # TODO: your code here
        c = BitArray(byts)

        for x in c:
            bits.append(int(x))

        print(bits)
        return bits


    def debitize(bits: Iterable[int]) -> bytes:
        """
        debbitize a list of bits
        """
        if len(bits) % 8 != 0:
            raise ValueError('bits length is not a multiple of 8')

        # TODO: your code here
        byts = bytes()
        binary_string = ""
        for x in bits:
            binary_string += str(x)
        print("binary string: " + binary_string)

        b = bytearray()
        b = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')

        byts = b
        return byts


    def generate_key(self) -> bytes:
        # create a random byte string of 8 bytes
        key = token_bytes(8)

        return key

    def key_to_file(self, key: bytes):
        #open/create file to write key to
        text_file = open("key.txt", "wb")
        text_file.write(key)
        text_file.close()

    def load_key(self) -> bytes:
        # load the key from the file
        f = open("key.txt", 'rb')
        key = f.read()

        #convert string to bytes
        #key = bytearray(, 'utf-8')
        #key = bytes(key)
        print(key)

        return key

class Des:

    def __init__(self):
        #generate the key
        self.nonce = None
        self.tag = None
        self.keyManager = KeyManager()
        self.key = self.keyManager.generate_key()

        #export the key to text file
        self.keyManager.key_to_file(self.key)

    def encrypt(self, msg):
        cipher = DES.new(self.keyManager.load_key(), DES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
        print(f'encrypt nonce: {nonce}, ciphertext:{ciphertext}, tag {tag}')
        return nonce, ciphertext, tag

    def decrypt(self, nonce, ciphertext, tag):
        cipher = DES.new(self.keyManager.load_key(), DES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        print(f'decrypt nonce: {nonce}, ciphertext:{ciphertext}, tag {tag}')
        print(f'plaintext in decrypt: {plaintext}')

        try:
            cipher.verify(tag)
            return plaintext.decode('ascii')
        except:
            return False

'''''
    nonce, ciphertext, tag = encrypt(input('Enter a message: '))
    plaintext = decrypt(nonce, ciphertext, tag)

    print(f'Cipher text: {ciphertext}')

    if not plaintext:
        print('Message is corrupted!')
    else:
        print(f'Plain text: {plaintext}')
'''