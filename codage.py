import os

import pyfiglet
import base64
import re
import pyinputplus as plput
from termcolor import colored
class Codage:
    '''
        In the menu()
            1/ Coder un message
            2/ Décoder un message
    '''



    @classmethod
    def customizedCoding(cls, msg):
        resultat = ''
        if len(msg) <= 50:
            crypt = 1
            for i in range(len(msg)-1):
                if msg[i] == msg[i+1]:
                    crypt += 1
                else:
                    resultat += str(crypt)+msg[i]
                    crypt = 1
            resultat += str(crypt)+msg[-1]
        return resultat

    @classmethod
    def customizedDecoding(cls, cryp):
        resultat = ''
        arr = re.split('(\d+)', cryp)
        arr.pop(0)
        for i in range(0, len(arr) - 1, 2):
            resultat += int(arr[i]) * arr[i + 1]
        return resultat

    @classmethod
    def encode(cls, msg, methode):
        if methode in ['utf8', 'ascii']:
            message_code = str.encode(msg, encoding=methode)
            print(colored('Votre message codé est : ' + str(message_code), 'green'))
            return message_code

        elif methode == 'base64':
            message_binaire = msg.encode('ascii')
            base64_binaire = base64.b64encode(message_binaire)
            message_final = base64_binaire.decode('ascii')
            print(colored('Votre message codé est:  ' + message_final, 'green'))
            return message_final

        elif methode == 'base32':
            message_binaire = msg.encode('ascii')
            base32_binaire = base64.b32encode(message_binaire)
            message_final = base32_binaire.decode('ascii')
            print(colored('Votre message codé est:  ' + message_final, 'green'))
            return message_final

        elif methode == 'base16':
            message_binaire = msg.encode('ascii')
            base16_binaire = base64.b16encode(message_binaire)
            message_final = base16_binaire.decode('ascii')
            print(colored('Votre message codé est:  ' + message_final, 'green'))
            return message_final
        elif methode == 'personalise':
            message_code = Codage.customizedCoding(msg)
            print(colored('Votre message codé : ' + message_code, 'green'))
            return message_code

    @classmethod
    def decode(cls, codage_final, methode):
        if methode in ['utf8', 'ascii']:
            message_decode = codage_final.decode(encoding=methode)
            print(colored('Votre message decode : ' + message_decode, 'green'))
            return (message_decode)

        elif methode == 'base64':
            message_binaire = codage_final.encode('ascii')
            base64_binaire = base64.b64decode(message_binaire)
            base64_message = base64_binaire.decode('ascii')
            print(colored('Votre message decode est:  ' + base64_message, 'green'))
            return base64_message

        elif methode == 'base32':
            message_binaire = codage_final.encode('ascii')
            base32_binaire = base64.b32decode(message_binaire)
            base32_message = base32_binaire.decode('ascii')
            print(colored('Votre message decode est:  ' + base32_message, 'green'))
            return base32_message

        elif methode == 'base16':
            message_binaire = codage_final.encode('ascii')
            base16_binaire = base64.b16decode(message_binaire)
            base16_message = base16_binaire.decode('ascii')
            print(colored('Votre message decode est:  ' + base16_message, 'green'))
            return base16_message

        elif methode == 'personalise':
            message_decode = Codage.customizedDecoding(codage_final)
            return message_decode

    @classmethod
    def menu(cls):
        os.system('color')
        ascii_banner = pyfiglet.figlet_format("ENCODING")
        print(colored(ascii_banner, 'red'))
        while(True):
            print('\n')
            choix = plput.inputMenu(['coder', 'quitter'])
            if choix == 'coder':
                msg = input(colored("Le message a ecoder: ", 'blue'))
                methode = plput.inputMenu(['utf8', 'ascii', 'base16', 'base32', 'base64', 'personalise'])
                codage_final = Codage.encode(msg, methode)

                print(colored('\n Maintenant le decodage: ', 'blue'))
                decoder = plput.inputMenu(['oui', 'non'])
                if decoder == 'non':
                    continueq
                else:
                    Codage.decode(codage_final, methode)
            else:
                return
#
# if __name__ == '__main__':
#     Codage.menu()
