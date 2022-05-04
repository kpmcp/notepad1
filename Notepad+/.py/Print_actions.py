from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog


class Printer:
    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

    def print_preview_dialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(self.print_preview)
        preview_dialog.exec_()

    def print_preview(self, printer):
        self.textEdit.print_(printer)
