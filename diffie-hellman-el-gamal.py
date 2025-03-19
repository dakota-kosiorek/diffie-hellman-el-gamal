# Dakota Kosiorek
import random

class User:
    def __init__(self, name:str, p: int, g: int):
        self.name = name
        self.p = p
        self.g = g
        self.encrypted_messages = {}
        self.generate_new_keys()

    def generate_new_keys(self):
        self.secret_key = random.randint(0, self.p - 2)
        self.h = (self.g ** self.secret_key) % self.p
        self.public_key = (self.h, self.g, self.p)

    def send_el_gamal_message(self, m: str, u):
        # Since new keys are generated with each new message sent, the old
        # messages must be read first because public, secret, and shared keys
        # will change
        self.read_messages() 

        target_public = u.public_key
        u_h = target_public[0]
        
        m_num = [ord(c) for c in m]
        ciphertext = []

        for c in m_num:
            s = (u_h ** self.secret_key) % self.p # shared secret

            c1 = (self.g ** self.secret_key) % self.p
            c2 = (c * s) % self.p

            ciphertext.append((c1, c2))
            self.generate_new_keys()

        if self.name not in u.encrypted_messages:
            u.encrypted_messages[self.name] = [ciphertext]
        else:
            u.encrypted_messages[self.name].append(ciphertext)

    def read_messages(self):
        for contact in self.encrypted_messages:
            print(f'From {contact}')
            for i, message in enumerate(self.encrypted_messages[contact]):
                plaintext = []
                for m in message:
                    s = (m[0]**self.secret_key) % self.p
                    plaintext.append(chr((pow(s, -1, self.p) * m[1]) % self.p))
                
                plaintext = ''.join(plaintext)
                print(f'Message #{i}: {plaintext}')

        self.encrypted_messages = {}

def main():
    p = 131 # prime number
    g = 19 # primitive root

    alice = User('alice', p, g)
    bob = User('bob', p, g)
    
    alice.send_el_gamal_message('Hello there!', bob)
    alice.send_el_gamal_message('This is message #2...', bob)
    bob.send_el_gamal_message('Does this work?', alice)
    alice.send_el_gamal_message('Yup! :3', bob)
    
    alice.read_messages()
    bob.read_messages()

if __name__ == '__main__':
    main()