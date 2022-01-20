import os

import pyinputplus as plput
import pyfiglet
from termcolor import colored
from SymmetricEncryption import SymetricEncryption
from AsymmetricEncryption import AsymmetricEncryption
from codage import Codage
from hashage import Hashage
import authentification
from client import Client

os.system('color')
def menu():
    print ('\n')
    print ('\n')
    print ('\n')
    print ('\n')
    ascii_banner = pyfiglet.figlet_format("Bienvenue A Notre Application")
    print(colored(ascii_banner, 'yellow'))
    while (True):
        print("")
        choix = plput.inputMenu(['Register', 'Login', 'Quitter'])
        if choix == 'Register':
            prenom = authentification.register()
            if not prenom != '':
                return
        elif choix == 'Login':
            idd, prenom = authentification.login()
            if isinstance(idd, int):
                break
        else:
            return
    while True:
        choice = plput.inputMenu(
            ['codage', 'hashage', 'crack hashage', 'chiffrement symetrique', 'chiffrement asymetrique', 'chat-room',
             'quitter'])
        if (choice == 'codage'):
            Codage.menu()
        elif (choice == 'hashage'):
            Hashage.menuHash()
        elif (choice == 'crack hashage'):
            Hashage.menuCrack()
        elif (choice == 'chiffrement symetrique'):
            SymetricEncryption.menu()
        elif (choice == 'chiffrement asymetrique'):
            AsymmetricEncryption.menu()
        elif (choice == 'chat-room'):
            client = Client("localhost", 4444, prenom, idd)
            client.create_connection()
            break
        elif (choice == 'quitter'):
            authentification.logout(idd)
            return


if __name__ == '__main__':
    menu()
