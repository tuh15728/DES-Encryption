import socket
from crypto import KeyManager, Des
from sys import getsizeof
import server

clientNonce = None
clientTag = None
my_des = Des()


class Client:
    def __init__(self, addr, port, buffer_size=1024):
        self.addr = addr
        self.port = port
        self.buffer_size = buffer_size

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.addr, self.port))

    def send(self, msg_bytes: bytes):
        self.s.send(msg_bytes)

    def recv(self, buffer_size=None) -> bytes:
        if buffer_size is None:
            buffer_size = self.buffer_size
        msg_bytes = self.s.recv(self.buffer_size)

        return msg_bytes

    def close(self):
        self.s.close()


if __name__ == '__main__':
    client = Client('localhost', 9999)
    client_keyman = KeyManager()
    client_keyman.load_key()

    while True:
        msg = input('> ')
        if msg == 'exit':
            break

        # TODO: your code here
        # set up DES algorithm
        # nonce: unique id for call to API || tag: authentication tag
        client.clientNonce, ciphertext, client.clientTag = my_des.encrypt(msg)  # encode message in cipher text
        print(f'client nonce: {client.clientNonce}, ciphertext:{ciphertext}, tag {client.clientTag}')

        # send message in cipher text
        client.send(ciphertext)

        # receive cipher text
        rec_ciphertext = client.recv(1024)

        # decrypt cipher text and print plain text
        plaintext = my_des.decrypt(server.serverNonce, rec_ciphertext, server.serverTag)
        print("pt: ", str(plaintext), " || ct: ", rec_ciphertext)

    client.close()
