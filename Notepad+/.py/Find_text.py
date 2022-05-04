# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find_text_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QTextDocument, QSyntaxHighlighter, QTextCharFormat, QTextCursor
from PyQt5.QtCore import QRegularExpression, Qt


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(362, 142)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/notepad_img.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.direction_groupbox = QtWidgets.QGroupBox(Form)
        self.direction_groupbox.setGeometry(QtCore.QRect(150, 60, 131, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.direction_groupbox.sizePolicy().hasHeightForWidth())
        self.direction_groupbox.setSizePolicy(sizePolicy)
        self.direction_groupbox.setObjectName("direction_groupbox")
        self.up_radio_btn = QtWidgets.QRadioButton(self.direction_groupbox)
        self.up_radio_btn.setGeometry(QtCore.QRect(0, 20, 51, 17))
        self.up_radio_btn.setChecked(True)
        self.up_radio_btn.setObjectName("up_radio_btn")
        self.down_radio_btn = QtWidgets.QRadioButton(self.direction_groupbox)
        self.down_radio_btn.setGeometry(QtCore.QRect(70, 20, 51, 17))
        self.down_radio_btn.setObjectName("down_radio_btn")
        self.searched_text = QtWidgets.QLineEdit(Form)
        self.searched_text.setGeometry(QtCore.QRect(70, 40, 211, 20))
        self.searched_text.setObjectName("searched_text")
        self.find_btn = QtWidgets.QPushButton(Form)
        self.find_btn.setEnabled(False)
        self.find_btn.setGeometry(QtCore.QRect(290, 40, 61, 23))
        self.find_btn.setCheckable(False)
        self.find_btn.setChecked(False)
        self.find_btn.setAutoRepeat(False)
        self.find_btn.setAutoExclusive(False)
        self.find_btn.setObjectName("find_btn")
        self.case_sensitive_checkbox = QtWidgets.QCheckBox(Form)
        self.case_sensitive_checkbox.setGeometry(QtCore.QRect(10, 80, 121, 17))
        self.case_sensitive_checkbox.setObjectName("case_sensitive_checkbox")
        self.what_to_search_lbl = QtWidgets.QLabel(Form)
        self.what_to_search_lbl.setGeometry(QtCore.QRect(10, 40, 41, 21))
        self.what_to_search_lbl.setObjectName("what_to_search_lbl")
        self.find_all_btn = QtWidgets.QPushButton(Form)
        self.find_all_btn.setEnabled(False)
        self.find_all_btn.setGeometry(QtCore.QRect(290, 70, 61, 23))
        self.find_all_btn.setObjectName("find_all_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Поиск"))
        self.direction_groupbox.setTitle(_translate("Form", "Направление"))
        self.up_radio_btn.setText(_translate("Form", "Вверх"))
        self.down_radio_btn.setText(_translate("Form", "Вниз"))
        self.find_btn.setText(_translate("Form", "Найти"))
        self.case_sensitive_checkbox.setText(_translate("Form", "С учётом регистра"))
        self.what_to_search_lbl.setText(_translate("Form", "Что:"))
        self.find_all_btn.setText(_translate("Form", "Найти всё"))


class SearchHighLighter(QSyntaxHighlighter):
    def __init__(self, parent, case_sensitive=False):
        super().__init__(parent)
        self.case_sensitive = case_sensitive
        self.pattern = QRegularExpression()
        self.format = QTextCharFormat()
        self.format.setBackground(Qt.cyan)

    def highlightBlock(self, text):
        match_iterator = None
        if self.case_sensitive:
            match_iterator = self.pattern.globalMatch(text)
        else:
            match_iterator = self.pattern.globalMatch(text.lower())
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.format)

    def searchText(self, text):
        self.pattern = QRegularExpression(text)
        self.rehighlight()


class FindText(QWidget, Ui_Form):
    def __init__(self, parent):
        super(FindText, self).__init__()
        self.setFixedSize(400, 150)
        self.document = parent.textEdit.document()
        self.editor = parent.textEdit
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.case_sensitive_checkbox.clicked.connect(self.can_find)
        self.find_btn.clicked.connect(self.searchText)
        self.find_all_btn.clicked.connect(self.searchAllText)
        self.searched_text.textChanged.connect(self.textEdited)
        self.searched_text.setText(self.editor.textCursor().selectedText())

    def can_find(self):
        if self.case_sensitive_checkbox.isChecked():
            self.find_btn.setEnabled(False)
        else:
            self.find_btn.setEnabled(True)

    def textEdited(self):
        if self.searched_text.text() != '':
            self.find_btn.setEnabled(True)
            self.find_all_btn.setEnabled(True)
        else:
            self.find_btn.setEnabled(False)
            self.find_all_btn.setEnabled(False)

    def searchText(self):
        flag = QTextDocument.FindBackward if self.up_radio_btn.isChecked() else QTextDocument.FindWholeWords
        if self.editor.find(self.searched_text.text(), flag) is False:
            dialog = QMessageBox(self)
            dialog.setWindowTitle('Notepad+')
            dialog.setText('Не удалось найти "{}".'.format(self.searched_text.text()))
            dialog.setIcon(QMessageBox.Information)
            dialog.show()

    def searchAllText(self):
        is_checked = self.case_sensitive_checkbox.isChecked()
        searchHighLighter = SearchHighLighter(self.editor.document(), is_checked)
        searchHighLighter.searchText(self.searched_text.text())
