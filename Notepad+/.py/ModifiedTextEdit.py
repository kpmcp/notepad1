import os
from PyQt5.QtWidgets import QTextEdit, QMessageBox
from PyQt5.QtGui import QImage, QTextDocument

IMAGE_EXTENSIONS = ['.jpg', '.png', '.bmp', '.jpeg', '.jpe', '.jfif',
                    '.tif', '.tiff', '.ico', '.webp', '.heic', '.dib', '.gif']


#  returns file_extension
def splitext(path):
    return os.path.splitext(path)[1].lower()


class SuperTextEdit(QTextEdit):
    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(SuperTextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        document = self.document()
        if source.hasUrls():
            for url in source.urls():
                file_extension = splitext(str(url.toLocalFile()))
                if url.isLocalFile() and file_extension in IMAGE_EXTENSIONS:
                    image = QImage(url.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, url, image)
                    cursor.insertImage(url.toLocalFile())
                else:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle('Ошибка воспроизведения картинки')
                    dlg.setText('Не удалось загрузить картинку. Скачайте её на ваш компьютер и вставьте.')
                    dlg.setIcon(QMessageBox.Warning)
                    dlg.show()
            else:
                return

        super(SuperTextEdit, self).insertFromMimeData(source)
