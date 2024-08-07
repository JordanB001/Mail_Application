import os
import sys

from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv

from mail_recuperation import *
from user_Interface import MainWindow

load_dotenv()
CLIENT_USER = os.getenv("CLIENT_USER")
CLIENT_MDP = os.getenv("CLIENT_MDP")
SERVEUR_NAME = "outlook.office365.com"
SERVEUR_PORT = 993

email = []


def mail_Recup_Et_Parsage(mail, boxName="inbox", nombre_De_Mail_A_Affiche=25):
    emails = []

    email_Ids = recuperation_Email_Boite(mail, box_Name=boxName)

    if len(email_Ids) > nombre_De_Mail_A_Affiche:
        start_Taille_Liste_Email_Ids = - nombre_De_Mail_A_Affiche
        end_Taille_Liste_Email_Ids = -1
    else:
        start_Taille_Liste_Email_Ids = 0
        end_Taille_Liste_Email_Ids = len(email_Ids)

    for email_Id in range(start_Taille_Liste_Email_Ids, end_Taille_Liste_Email_Ids):
        status, msg_Data = mail.fetch(email_Ids[email_Id], "(RFC822)")
        print(msg_Data)
        emails.append(email_Parse(msg_Data[0]))
    emails.reverse()

    return emails


def mail_Parsage_Par_BoxName(mail):
    email_Parse_BoxName = []
    liste_BoxName = recuperer_Liste_Box_Name(mail)
    print(liste_BoxName)
    liste_BoxName.remove("Inbox")
    liste_BoxName.remove("Cours")
    liste_BoxName.remove("Sent")

    for boxName in liste_BoxName:
        email_Ids_BoxName = recuperation_Email_Boite(mail, box_Name=boxName, criteria="ALL")
        for email_Id in email_Ids_BoxName:
            status, msg_Data = mail.fetch(email_Id, "(RFC822)")
            email_Parse_BoxName.append(email_Parse(msg_Data[0]))
    return email_Parse_BoxName


if __name__ == "__main__":
    mail_outlook = connexion_Email(CLIENT_USER, CLIENT_MDP, SERVEUR_NAME, SERVEUR_PORT)

    emails = mail_Recup_Et_Parsage(mail_outlook)
    #emails = mail_Parsage_Par_BoxName(mail_outlook)
    mail_List_MailBoxName = recuperer_Liste_Box_Name(mail_outlook)

    #PARTIE UI
    app = QApplication(sys.argv)

    email = emails[-2]

    mainWindow = MainWindow(CLIENT_USER, mail_List_MailBoxName, emails, mailBox=mail_outlook)
    mainWindow.mailView_Change(email[0], email[1])

    mainWindow.show()
    mail_outlook.close()
    mail_outlook.logout()
    sys.exit(app.exec())
