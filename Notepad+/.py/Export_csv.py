from export import Ui_Form
from PyQt5.QtWidgets import QWidget, QFileDialog
import csv


class ExportCSV(Ui_Form, QWidget):
    def __init__(self, parent):
        super(ExportCSV, self).__init__()
        self.text = parent.textEdit.toPlainText()
        self.setupUi(self)
        self.setFixedSize(600, 550)
        self.curr_sep = ','
        self.separators()
        self.separator.activated.connect(self.combo_text)
        self.initUI()

    def initUI(self):
        self.open_directory_btn.clicked.connect(self.browse)
        self.export_btn.clicked.connect(self.convert_to_csv)

    def browse(self):
        file_directory = QFileDialog.getSaveFileName(
            self, 'Выберите файл для экспорта', '',
            'CSV (*.csv);;Все файлы (*)')[0]
        self.file_name.setText(file_directory)

    def separators(self):
        self.separator.addItems([', (запятая)', '; (точка с запятой)', '\\t (табуляция)', ' (пробел)', 'Произвольный:'])

    def combo_text(self):
        self.curr_sep = self.separator.currentText()
        if self.curr_sep == 'Произвольный:':
            self.user_separator.setEnabled(True)
        else:
            self.user_separator.setEnabled(False)

    def convert_to_csv(self):
        try:
            csv_file = self.file_name.text()
            separator = self.user_separator.text() if self.user_separator.isEnabled() else self.curr_sep[0]
            if separator == '\\':
                separator = '\t'
            with open(csv_file, mode='w', encoding='utf-8', newline='') as csv_file:
                text = self.text.split('\n')
                writer = csv.writer(csv_file, delimiter=separator)
                for el in text:
                    row = el.split()
                    writer.writerow([elem for elem in row])
        except FileNotFoundError:
            self.file_name.setPlaceholderText('Введите название файла')
        except PermissionError:
            self.file_name.setPlaceholderText('Введите название файла')
        except TypeError:
            self.user_separator.setPlaceholderText('Введите разделитель')
        else:
            self.close()

