import socket
from crypto import KeyManager, Des

my_des = Des() #global DES instance used in client and server modules

class Client: #contains methods related to the client
    def __init__(self, addr, port, buffer_size=1024): #initialize the socket connection
        self.addr = addr
        self.port = port
        self.buffer_size = buffer_size

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.addr, self.port))

    def send(self, msg_bytes: bytes): #send message to the server
        self.s.send(msg_bytes)

    def recv(self, buffer_size=None) -> bytes: #receive message from server
        if buffer_size is None:
            buffer_size = self.buffer_size
        msg_bytes = self.s.recv(self.buffer_size)

        return msg_bytes

    def close(self): #close the socket
        self.s.close()


if __name__ == '__main__':
    client = Client('localhost', 9999)
    client_keyman = KeyManager()
    client_keyman.load_key()

    while True:
        msg = input('> ')
        if msg == 'exit':
            break

        # set up DES algorithm
        # nonce: unique id for call to API || tag: authentication tag
        clientNonce, ciphertext, clientTag = my_des.encrypt(msg)  # encode message in cipher text

        client_keyman.nonce_to_file(clientNonce)
        client_keyman.tag_to_file(clientTag)

        # send message in cipher text
        client.send(ciphertext)

        # receive cipher text
        rec_ciphertext = client.recv(1024)

        # decrypt cipher text and print plain text
        plaintext = my_des.decrypt(client_keyman.load_nonce(), rec_ciphertext, client_keyman.load_tag())
        print("pt: ", str(plaintext), " || ct: ", rec_ciphertext)

    client.close()
