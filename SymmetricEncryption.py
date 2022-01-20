import os

import pyinputplus as plput
import pyfiglet
import stdiomask
from des import DesKey
from Crypto.Cipher import AES
import os
from termcolor import colored


class SymetricEncryption:
    '''
        1/ chiffrer un message
        2/ déchiffrer un message
    '''

    @classmethod
    def _generate_DES_Key(cls):
        key = stdiomask.getpass()
        key = str.encode(key)
        if len(key) < 8:
            key = key + str.encode((8 - len(key)) * 'a')
        elif (len(key) > 8):
            key = key[:8]
        return key


    @classmethod
    def encrypt(cls, method='AES'):
        plaintext = input(colored("Entrer le message a chiffré : ", 'blue'))

        if method == 'AES':
            plaintext = str.encode(plaintext)
            key = stdiomask.getpass()
            key = str.encode(key)
            if len(key) < 16:
                key = key + str.encode((16 - len(key)) * 'a')
            elif (len(key) > 16):
                key = key[:16]
            cipher = AES.new(key, AES.MODE_EAX)

            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)

            print(colored("nonce: \n" + str(nonce), 'yellow'),colored( "\nciphertext: \n" + str(ciphertext), 'green'), colored("\ntag: \n" + str(tag), 'red'))
            return (nonce, ciphertext, tag)

        elif method == 'DES':

            def _des_encrypt(key, message):
                #encoded key
                key0 = DesKey(key)
                return key0.encrypt(message.encode(), padding=True)

            key = cls._generate_DES_Key()
            print (colored('Votre message chiffré est:  ', 'blue'))
            print(colored (_des_encrypt(key, plaintext), 'green'))
            encrypted = _des_encrypt(key, plaintext)
            return encrypted, key

    @classmethod
    def decrypt(cls, nonce=None, ciphertext=None, tag=None, method='AES'):

        if method == 'AES':
            key = stdiomask.getpass()
            key = str.encode(key)
            if len(key) < 16:
                key = key + str.encode((16 - len(key)) * 'a')
            elif len(key) > 16:
                key = key[:16]
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            try:
                cipher.verify(tag)
                print(colored("\n Le message est authentique: ", 'green'), colored(plaintext, 'green'))
            except ValueError:
                print(colored("cle incorrecte ou valeur courrompu", 'red'))

        elif method == 'DES':
            def _des_decrypt(key1, message):
                #encoded key
                key0 = DesKey(key1)
                return key0.decrypt(message, padding=True)

            print(colored('Votre message déchiffré est:  ', 'green'))
            print(colored(_des_decrypt(nonce, ciphertext), 'green'))

    @classmethod
    def menu(cls):
        os.system('color')
        ascii_banner = pyfiglet.figlet_format("CHIFFREMENT SYMETRIQUE")
        print(colored(ascii_banner, 'red'))
        while (True):
            print('\n')
            choix = plput.inputMenu(['chiffrement', 'quitter'])
            if (choix == 'chiffrement'):
                methode = plput.inputMenu(['AES', 'DES'])
                print(colored(methode, 'yellow'))
                if methode == 'AES':
                    nonce, ciphertext, tag = SymetricEncryption.encrypt(method=methode)
                else:
                    encrypted, key = SymetricEncryption.encrypt(method=methode)

                print(colored('\n Déchiffrement? : ', 'blue'))
                dechiff = plput.inputMenu(['oui', 'non'])
                if dechiff == 'non':
                    continue
                elif methode == 'AES':
                    SymetricEncryption.decrypt(nonce, ciphertext, tag, methode)
                elif methode == 'DES':
                    SymetricEncryption.decrypt(nonce=key, ciphertext=encrypted, tag=None, method=methode)
            else:
                return


if __name__ == '__main__':
    SymetricEncryption.menu()
