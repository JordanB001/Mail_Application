import sys

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableView, \
    QGroupBox, QDialog, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class MainWindow(QDialog):

    def __init__(self, user_Name, mailBoxList, mailList, mailBox):
        super().__init__()

        self.mailBox = mailBox
        self.mailBox_Change = mailBox
        self.emails = mailList
        self.setWindowTitle('Boite Mail')

        self.create_MailBox(user_Name, mailBoxList)
        self.create_MailList(mailList)
        self.create_MailView()

        main_Layout = QHBoxLayout()

        main_Layout.addWidget(self.mailBox)
        main_Layout.addWidget(self.mail_List_Box)
        main_Layout.addWidget(self.mail_View)

        self.mailBox_List.clicked.connect(self.on_cell_clicked_MailBox)
        self.mail_List.clicked.connect(self.on_cell_clicked)

        self.setLayout(main_Layout)

        self.widgetWebEngine.setHtml("Aucun Mail")

    def create_MailBox(self, USER_NAME=None, mailListBox=None):
        if mailListBox is None:
            mailListBox = ["Nothing"]

        self.mailBox = QGroupBox(USER_NAME)

        self.mailBox_List = QTableView()

        self.modelMailBoxList = QStandardItemModel(0, 0)
        self.mailBox_List.setModel(self.modelMailBoxList)

        for row in range(len(mailListBox)):
            self.modelMailBoxList.insertRow(row)
            self.modelMailBoxList.setItem(row, 0, QStandardItem(mailListBox[row]))

        layout = QHBoxLayout()
        layout.addWidget(self.mailBox_List)

        self.mailBox.setLayout(layout)

    def create_MailList(self, listeMail=None):
        if listeMail is None:
            listeMail = [[]]

        self.mail_List_Box = QGroupBox("Liste des Mails")
        layout = QVBoxLayout()

        self.mail_List = QTableView()
        self.modelMailList = QStandardItemModel(0, 0)
        self.mail_List.setModel(self.modelMailList)

        self.mailList_Change(listeMail)

        layout.addWidget(self.mail_List)

        self.mail_List_Box.setLayout(layout)

    def create_MailView(self):
        self.mail_View = QGroupBox("MailView")
        layout = QVBoxLayout()

        self.mail_Header = QLabel("Nothing")
        self.widgetWebEngine = QWebEngineView()
        layout.addWidget(self.mail_Header)
        layout.addWidget(self.widgetWebEngine)

        self.mail_View.setLayout(layout)

    def mailView_Change(self, email_Header, email_Body):
        textLabel = str("Objet:   " + email_Header[0]) + "\nDe:         " + str(email_Header[1])
        self.mail_Header.setText(textLabel)
        self.widgetWebEngine.setHtml(email_Body)

    def on_cell_clicked(self, index: QModelIndex):
        row = index.row()
        email = self.emails[row]
        self.mailView_Change(email[0], email[1])

    def mailList_Change(self, listeMail=None):
        if listeMail is None:
            listeMail = [[]]

        for row in range(len(listeMail)):
            headSubject = str(listeMail[row][0][1])
            headFrom = str(listeMail[row][0][0])
            text = headSubject.split("<")[0] + ": " + headFrom

            self.modelMailList.insertRow(row)
            self.modelMailList.setItem(row, 0, QStandardItem(text))

    def on_cell_clicked_MailBox(self, index: QModelIndex):
        nameList = index.data()

