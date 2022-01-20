import hashlib
import os

import pyinputplus as plput
import pyfiglet
from termcolor import colored
class Hashage:
    '''
        Hashage(MD5, SHA1, SHA256)
        Craquage de hashage(MD5, SHA1, SHA256)
    '''

    @classmethod
    def multidigest(cls, texte):
        methode = plput.inputMenu(['MD5', 'SHA1', 'SHA256'])
        texte_encode = texte.encode()
        if methode == 'MD5':
            return hashlib.md5(texte_encode).hexdigest()

        elif methode == 'SHA1':
            return hashlib.sha1(texte_encode).hexdigest()

        elif methode == 'SHA256':
            return hashlib.sha256(texte_encode).hexdigest()

    @classmethod
    def pass_cracker(cls, hash):
        with open('pentbox-wlist.txt', 'r+') as file:
            passes = file.read().splitlines()
        for passe in passes:
            passe = passe.encode()
            if hashlib.md5(passe).hexdigest() == hash:
                return passe
            elif hashlib.sha1(passe).hexdigest() == hash:
                return passe
            elif hashlib.sha256(passe).hexdigest() == hash:
                return passe
        return colored("Nous sommes desolés \n mais on n'a pas pu trouver le mot de passe", 'red')

    @classmethod
    def menuHash(cls):
        ascii_banner = pyfiglet.figlet_format("HASHAGE")
        print(colored(ascii_banner, 'red'))
        while(True):
            print('\n')
            choix = plput.inputMenu(['hash', 'quitter'])
            if choix == 'hash':
                texte = input(colored("Entrer le texte a hashe : \n", 'blue'))
                texte_hashe = Hashage.multidigest(texte)
                print(colored(texte_hashe, 'green'))
            else:
                return

    @classmethod
    def menuCrack(cls):
        os.system('color')
        ascii_banner = pyfiglet.figlet_format("HASH CRACKER")
        print(colored(ascii_banner, 'red'))
        while(True):
            print('\n')
            choix = plput.inputMenu(['crack', 'quitter'])
            if choix == 'crack':
                hash = input(colored('Entrer le hash a cracker \n', 'blue'))
                hash_cracke = str(Hashage.pass_cracker(hash))
                print(colored('Hash cracke =====>   ' + hash_cracke, 'green'))
            else:
                return

# if __name__ == '__main__':
#     Hashage.menuCrack()
