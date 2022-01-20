# Cryptography-App

C'est une petite suite de sécurité sympa et légère, comprenant quelques outils de base qui vont vous permettre de tester la fiabilité de vos serveurs et de vos machines.

Celle-ci est écrite en python et elle s’utilise en ligne de commande ( en attendant un upgrade en interface prochainement)

Parmi les fonctionnalités disponibles dans cette application, on notera la présence d’outils permettant d’effectuer divers tests sur: 

   #
* Le Chiffrement: 
  * Chiffrement symmetrique: ```SymmetricEncryption.py```
    * AES 
    * DES 
    
  * Chiffrement asymmetrique: ```AsymmetricEncryption.py```
    * RSA
    * ElGamal
  #
* Le Déchiffrement:
  * Déchiffrement symmetrique: ```SymmetricEncryption.py```
      * AES
      * DES
  * Déchiffrement asymmetrique: ```AsymmetricEncryption.py```
      * RSA 
      * ElGamal
  #
* Signature et vérification de signature: ```AsymmetricEncryption.py```
     * RSA
  #
* Codage et Décodage par:  ```codage.py```
  * utf8
  * ascii
  * base64
  * base32
  * base16
  #
* Hachage:  ```hashage.py```
  * MD5
  * SHA1
  * SHA256
  #
* Craquage de hashage: ```hashage.py```
( à l'aide du dictionnaire ```pentbox-wlist.txt```)
  * MD5
  * SHA1
  * SHA256
  #
 * Crunch  ```crun.py```
   * Génération d'un dictionnaire d'emails selon les contraintes suivantes:
      - ```nom.prenom@insat.ucar.tn```
  #
* Authentification 
  * Register  ```authentifaction.py```
      - Controle sur les données et hashage du mot de passe dans la BD 
  * Login   ```authentifaction.py```
      - Authentification pourrait être double factor (vérification avec BD, envoi du TOKEN par mail)
  * Logout  ```authentifaction.py```
      - Se déconnecter de l'application en supprimant le TOKEN enregistré dans la BD 
  #
  * Mini Chat app with encryption  ```server.py``` et ```client.py```
    * Cette application utilise le chiffrement symmetrique et asymmetrique. Le serveur permet de générer les clés pblique et privé lors de l'exécution et l'échange des clés publiques avec les clients connécté au serveur.
      Le serveur utilise la clé publique de client afin de chiffrer un nombre généré aléatoirement ```session key``` qui va étre partager avec le client aprés. 
      
      Le client déchiffre   ```encrypted session key``` en utilisant sa clé privé pour l'utiliser dans le chiffrement et le déchiffrement des messages ( en utilisant  AES dans le mode CFB)
      Le serveur peut gérer plusieurs clients connectés en même temps et il n'affiche pas les message échanger entre les clients
      
    * Utilisation:
      - Le serveur est démarré en utilisant cette commande ```python server.py```  (port par défaut 4444 et Host: localhost, ces paramètres peuvent être spécifiés comme paramètre dans le code commenté)
      - Le client peut etre démarré soit par la commande ```python client.py``` ou bien à traver l'application aprés la création de compte et l'authentification

      - Le serveur peut être arrêter en tapant ```TERMINATE``` dans le terminal du serveur
      - Le client peut être arrêter en tapant ```EXIT``` dans le terminal du serveur (le token enregistré dans la BD sera supprimé)
  #
  
Le outils disponibles sont certes limités en nombre, mais vous avez déjà une très bonne base pour effectuer quelques tests basiques.


