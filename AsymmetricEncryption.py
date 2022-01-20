import pyinputplus as plput
import pyfiglet

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from hashlib import sha512
import elgamal
import os
from termcolor import colored

class AsymmetricEncryption:
    '''
        1/ chiffrer un message
            a/ RSA
            b/ ElGamal
        2/ déchiffrer un message
            a/ RSA
            b/ ElGamal
    '''

    @classmethod
    def encrypt(cls, cle_publique, cleElGamal, key, method='RSA'):
        plaintext = plput.inputStr(colored('Entrer le message à chiffrer :  ', 'blue'))
        plaintext = str.encode(plaintext)

        if (method == 'RSA'):
            choix = plput.inputMenu(['chiffrer message', 'signer message'])
            if (choix == 'chiffrer message'):
                cipher = AsymmetricEncryption.rsaEncrypt(plaintext, cle_publique, key)
                return ('encrypt', cipher)
            elif (choix == 'signer message'):
                signature = AsymmetricEncryption.rsaSign(plaintext, key)
                return ('sign', signature)
        elif (method == 'ElGamal'):
            cipher = AsymmetricEncryption.elgamalEncrypt(plaintext.decode(), cleElGamal)
            return ('encrypt', cipher)

    @classmethod
    def decrypt(cls, key, cleElGamal, method='RSA', choix='encrypt', signature=''):
        if (method == 'RSA'):
            if (choix == 'encrypt'):
                print(colored('RSA ENCRYPT'), 'yellow')
                AsymmetricEncryption.rsaDecrypt()
            elif (choix == 'sign'):
                msg = plput.inputStr(colored('Entrer le message original :  ', 'blue'))
                msg1 = AsymmetricEncryption.rsaVerifySignature(str.encode(msg), signature, key)
        elif (method == 'ElGamal'):
            AsymmetricEncryption.elgamaDecrypt(signature, cleElGamal)

    ################ RSA ######################
    @classmethod
    def rsaEncrypt(cls, ch, public_key, key):

        file_encryption = open("encrypted_data.bin", "wb")

        recipient_key = public_key
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(key.publickey())
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(ch)
        #nonce is a random number used to make sure a message is unique
        [file_encryption.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
        file_encryption.close()
        print(colored(ciphertext, 'green'))
        print(colored(tag, 'blue'))
        print(colored(cipher_aes.nonce), 'yellow')
        print(colored(enc_session_key, 'red'))
        return ciphertext

    @classmethod
    def rsaDecrypt(cls):

       # print('RSADECRYPT1')
        private_key = RSA.import_key(open("private.pem").read())

        file_decryption = open("encrypted_data.bin", "rb")

        enc_session_key, nonce, tag, ciphertext = [file_decryption.read(x) for x in
                                                   (private_key.size_in_bytes(), 16, 16, -1)]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        print(colored(data.decode("utf-8"), 'green'))
       # print('RSADECRYPT2')

    @classmethod
    def rsaSign(cls, msg, key):
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        signature = pow(hash, key.d, key.n)
        print(colored(signature, 'green'))
        return signature

    @classmethod
    def rsaVerifySignature(cls, msg, signature, key):
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        hashFromSignature = pow(signature, key.e, key.n)
        print(colored("Signature valid:", hash == hashFromSignature, 'green'))

    ################### ElGamal ####################

    @classmethod
    def elgamalEncrypt(cls, msg, elGamalKeys):
        cipher = elgamal.encrypt(elGamalKeys['publicKey'], msg)
        print(colored(cipher, 'green'))
        return cipher

    @classmethod
    def elgamaDecrypt(cls, cipher, elGamalKeys):
        plaintext = elgamal.decrypt(elGamalKeys['privateKey'], cipher)
        print(colored(plaintext, 'green'))

    ################################################

    @classmethod
    def menu(cls):
        os.system('color')
        cleElGamal = elgamal.generate_keys()

        #generate private key
        key = RSA.generate(2048)
        cle_prive = key.export_key()
        fichier = open("private.pem", "wb")
        fichier.write(cle_prive)
        fichier.close()

        #generate public key
        cle_publique = key.publickey().export_key()
        fichier = open("receiver.pem", "wb")
        fichier.write(cle_publique)
        fichier.close()

        ascii_banner = pyfiglet.figlet_format("Chiffrement Asymetrique")
        print(colored(ascii_banner, 'red'))

        while True:
            print("\n")
            choix = plput.inputMenu(['encryption', 'quitter'])
            if choix == 'encryption':
                methode = plput.inputMenu(['RSA', 'ElGamal'])
                print(colored(methode, 'yellow'))
                if methode == 'RSA':
                    choix, signature = AsymmetricEncryption.encrypt(cle_publique, cleElGamal, key, method=methode)
                else:
                    choix, cipher = AsymmetricEncryption.encrypt(cle_publique, cleElGamal, key, method=methode)

                print(colored("\n For decryption : ", 'blue'))
                decrypt = plput.inputMenu(['oui', 'non'])
                if decrypt == 'non':
                    continue
                elif decrypt == 'oui':
                    if methode == 'RSA':
                        AsymmetricEncryption.decrypt(key, cleElGamal, methode, choix, signature)
                    else:
                        AsymmetricEncryption.decrypt(key, cleElGamal, methode, choix, cipher)

            else:
                return

# if __name__ == '__main__':
#     AsymmetricEncryption.menu()
