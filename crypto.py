from Crypto.Cipher import DES
from secrets import token_bytes

class KeyManager:  # contains methods for creating/storing/retrieving keys

    def generate_key(self) -> bytes:
        # create a random byte string of 8 bytes
        key = token_bytes(8)

        return key

    def key_to_file(self, key: bytes):
        # open/create file to write key to
        text_file = open("key.txt", "wb")
        text_file.write(key)
        text_file.close()

    def load_key(self) -> bytes:
        # load the key from the file
        f = open("key.txt", 'rb')
        key = f.read()
        return key

    def nonce_to_file(self, nonce):
        text_file = open("nonce.txt", "wb")
        text_file.write(nonce)
        text_file.close()

    'The rest of this class' \
    'contains methods to store/retrieve' \
    'the nonce and tag needed for DES encryption'
    def load_nonce(self):
        # load the key from the file
        f = open("nonce.txt", 'rb')
        nonce = f.read()
        print(nonce)

        return nonce

    def tag_to_file(self, tag):
        text_file = open("tag.txt", "wb")
        text_file.write(tag)
        text_file.close()

    def load_tag(self):
        # load the key from the file
        f = open("tag.txt", 'rb')
        tag = f.read()

        return tag


class Des: #this class contains methods for DES encryption/decryption

    def __init__(self):
        # generate the key
        self.nonce = None
        self.tag = None
        self.keyManager = KeyManager()
        self.key = self.keyManager.generate_key()

        # export the key to text file
        self.keyManager.key_to_file(self.key)

    def encrypt(self, msg):
        #build cipher with generated key in Encrypt->authenticate->translate mode
        cipher = DES.new(self.keyManager.load_key(), DES.MODE_EAX)

        #generate nonce, tag, ciphertext
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
        return nonce, ciphertext, tag

    def decrypt(self, nonce, ciphertext, tag):
        #build cipher for decryption
        cipher = DES.new(self.keyManager.load_key(), DES.MODE_EAX, nonce=nonce)

        #generate plaintext
        plaintext = cipher.decrypt(ciphertext)

        #error checking to ensure the tag is correct
        try:
            cipher.verify(tag)
            return plaintext.decode('ascii')
        except: #no tag -> no decryption
            return False