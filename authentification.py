from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from termcolor import colored
import mysql.connector
import getpass
import hashlib
import os
import re
import stdiomask
import binascii

config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'securite',
  'raise_on_warnings': True
}
os.system('color')
#connecting to the database
cnx = mysql.connector.connect(**config)
db_cursor = cnx.cursor()

def register():
  try:
    prenom = input(colored("Donner votre prenom (5 caracteres):  ", 'blue'))
    if not len(prenom) == 5:
      raise print(colored('\n le prenom doit avoir un nombre de caractère de 5.', 'red'))
    nom = input(colored("Donner votre nom (6 caracteres):   ", 'blue'))
    if not len(nom) == 6:
      raise print(colored('\n le nom doit avoir un nombre de caractère de 6.', 'red'))
    email = input(colored("Donner votre email:   ", 'blue'))
    if "@" not in email:
      raise print(colored('Verifier votre mail ', 'red'))
    db_cursor.execute("SELECT * FROM login WHERE email = '" + email + "'")
    email_found = db_cursor.fetchone()
    if email_found:
      raise print(colored(" L'email donné existe déjà",'red'))
    pwd1 = stdiomask.getpass(colored("Donner votre mot de passe:   ", 'blue'))
    pwd2 = stdiomask.getpass(colored("Repeter votre mot de passe    ", 'blue'))
    if not pwd1.__eq__(pwd2):
      raise print(colored('les mots de passe ne sont pas égaux', 'red'))
    # msg = prenom +'.'+ nom + '@insat.ucar.tn'
    # if not pwd1.__eq__(msg):
    #   raise print(colored("le mot de passe n'est pas écrit sous la forme attendue", 'red'))
    salt = os.urandom(32)
    hashe = hashlib.pbkdf2_hmac('sha256', pwd1.encode('utf-8'), salt, 100000)
    password = salt + hashe
    query = "INSERT INTO login(nom,prenom,email,pwd,salt) VALUES('"+nom+"','"+prenom+"','"+email+"','"+password.hex()+"','"+salt.hex()+"')"
    db_cursor.execute(query)
    cnx.commit()
    db_cursor.close()
    cnx.close()
    return prenom
  except:
    print(colored("Un des données entrées est faux !! ", 'red'))

def generateToken():
  token = binascii.hexlify(os.urandom(20)).decode()
  return token

def send_email(mail, token):
  msg = MIMEMultipart()
  msg['From'] = 'noreply.2bandb@gmail.com'
  msg['To'] = mail
  msg['Subject'] = 'Le Token'
  message = 'Voila votre Token, copiez le :  '+token
  msg.attach(MIMEText(message))
  mailserver = smtplib.SMTP('smtp.gmail.com', 587)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.ehlo()
  mailserver.login('noreply.2bandb@gmail.com', 'Band&B1901')
  mailserver.sendmail('noreply.2bandb@gmail.com', mail, msg.as_string())
  mailserver.quit()

def login():
  try:
    print(colored("**** Vous etes dans 'Login' **** \n",'green'))
    email = input(colored("Donne votre email:   ", 'blue'))
    pwd = stdiomask.getpass(colored("Donner votre mot de passe:   ", 'blue'))
    print(colored ('Verification par Token', 'blue'))
    db_cursor.execute("SELECT * FROM login WHERE email = '"+email+"'")
    email_found = db_cursor.fetchone()
    if email_found is None:
      raise print(colored(" L'email donné n'est pas trouvé", 'red'))
    salt = email_found[5]
    salt_binary = binascii.unhexlify(salt)
    new_key = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt_binary, 100000)
    new_key = new_key.hex()
    new_key = salt + new_key
    if new_key == email_found[4]:
      token = generateToken()
      db_cursor.execute("INSERT INTO tokens(token,idd) VALUES (%s,%s)",(token, int(email_found[0])))
      token_verification = generateToken()
      send_email(email, token_verification)
      input_token = input(colored("Copier le token ICI:    ", 'blue'))
      if not token_verification.__eq__(input_token):
        db_cursor.execute("delete from tokens where idd=%s", (int(email_found[0])))
        raise print(colored('nous sommes désolés mais le Token copié est fausse!!', 'red'))
    else:
      raise print(colored('le mot de pass entré est fausse!!', 'red'))
    cnx.commit()
    db_cursor.close()
    cnx.close()
    print(colored('Verification par Token terminée', 'blue'))
    return int(email_found[0]) , (email_found[1])
  except:
    print(colored("Désolé, Votre authentification a échoué", 'red'))

def logout(id):
  cnx = mysql.connector.connect(**config)
  db_cursor = cnx.cursor()
  db_cursor.execute("delete from tokens where idd="+str(id)+";")
  cnx.commit()
  db_cursor.close()
  cnx.close()