import sys

from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor

from untitled import Ui_MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QColorDialog


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Запускаю приложение без рамки
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.fname = ''
        # Задаю таблицу стилей

        # Задаю иконки
        self.boldButton.setIcon(QIcon(QPixmap('Sprite-0001.png')))
        self.colorButton.setIcon(QIcon(QPixmap('edit-color.png')))
        self.underButton.setIcon(QIcon(QPixmap('edit-underline.png')))
        self.italicButton.setIcon(QIcon(QPixmap('edit-italic.png')))
        self.lButton.setIcon(QIcon(QPixmap('Sprite-0001-export.png')))
        self.cButton.setIcon(QIcon(QPixmap('Sprite-0002-export-export.png')))
        self.rButton.setIcon(QIcon(QPixmap('Sprite-0003-export-export.png')))
        self.jButton.setIcon(QIcon(QPixmap('Sprite-0004-export-export.png')))

        self.boldButton.setCheckable(True)
        self.underButton.setCheckable(True)
        self.italicButton.setCheckable(True)
        self.lButton.setCheckable(True)
        self.rButton.setCheckable(True)
        self.cButton.setCheckable(True)
        self.jButton.setCheckable(True)

        # Основные функции - открыть, сохранить файл, выйти из приложения
        self.cl.clicked.connect(self.exit)
        self.action_3.triggered.connect(self.save_as)
        self.action.triggered.connect(self.open)
        self.action_2.triggered.connect(self.save)

        # Функции, влияющие на стиль текста
        self.colorButton.clicked.connect(self.change_color)
        self.boldButton.clicked.connect(lambda: self.change_font_style(bold=True))
        self.underButton.clicked.connect(lambda: self.change_font_style(underline=True))
        self.italicButton.clicked.connect(lambda: self.change_font_style(italic=True))
        self.lButton.clicked.connect(lambda: self.change_align(align='left'))
        self.rButton.clicked.connect(lambda: self.change_align(align='right'))
        self.cButton.clicked.connect(lambda: self.change_align(align='center'))
        self.jButton.clicked.connect(lambda: self.change_align(align='justify'))

        # Смена шрифта и размера шрифта
        self.fontComboBox.currentFontChanged.connect(self.change_font_family)
        self.comboBox.currentTextChanged.connect(self.change_font_size)

        # Функции, отвечающие за действия (копировать, вставить и т.д) в виде действий в меню
        self.action_6.triggered.connect(self.textEdit.copy)
        self.action_7.triggered.connect(self.textEdit.cut)
        self.action_8.triggered.connect(self.textEdit.paste)
        self.action_5.triggered.connect(self.textEdit.redo)
        self.action_9.triggered.connect(self.textEdit.undo)

        # Устанавливаю начальный размер шрифта, добавляю некоторые изменения в программе при изменении курсора
        self.textEdit.setFontPointSize(8)
        self.textEdit.selectionChanged.connect(self.update)

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_I:
                self.change_font_style(italic=True)
            elif event.key() == Qt.Key_U:
                self.change_font_style(underline=True)
            elif event.key() == Qt.Key_B:
                self.change_font_style(bold=True)
            elif event.key() == Qt.Key_S:
                self.save()

    # Функция выхода из программы
    def exit(self):
        reply = QMessageBox.question(
            self, "Message",
            "Вы действительно хотите выйти? Все несохранённые данные будут потеряны",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            app.quit()
        elif reply == QMessageBox.Save:
            self.save()
            app.quit()

    def change_font_style(self, italic=False, bold=False, underline=False):
        form = self.textEdit.textCursor().charFormat()
        form.setFontItalic(not form.fontItalic() if italic else form.fontItalic())
        form.setFontUnderline(not form.fontUnderline() if underline else form.fontUnderline())
        if bold:
            form.setFontWeight(QFont.Bold if not form.font().bold() else QFont.Normal)
        else:
            form.setFontWeight(QFont.Bold if form.font().bold() else QFont.Normal)

        self.textEdit.textCursor().setCharFormat(form)
        self.textEdit.setCurrentFont(form.font())

    def change_align(self, align='left'):
        if align == 'left':
            self.textEdit.setAlignment(Qt.AlignLeft)
        elif align == 'right':
            self.textEdit.setAlignment(Qt.AlignRight)
        elif align == 'center':
            self.textEdit.setAlignment(Qt.AlignCenter)
        else:
            self.textEdit.setAlignment(Qt.AlignJustify)

    def change_font_family(self):
        self.textEdit.setFontFamily(self.fontComboBox.currentText())

    def change_font_size(self):
        self.textEdit.setFontPointSize(int(self.comboBox.currentText()))

    def change_color(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    # Функция сохранения файла как
    def save_as(self):
        self.fname = QFileDialog.getSaveFileName(
            self, '', '', 'text document(*.txt);;html document(*.html)')[0]
        if self.fname:
            with open(self.fname, 'w', encoding='utf-8') as file:
                if self.fname.endswith('.html'):
                    file.write(self.textEdit.toHtml())
                else:
                    file.write(self.textEdit.toPlainText())

    # Функция простого сохранения
    def save(self):
        print(self.fname)
        if not self.fname:
            self.save_as()
        else:
            with open(self.fname, 'wt', encoding='utf-8') as file:
                if self.fname.endswith('.html'):
                    file.write(self.textEdit.toHtml())
                else:
                    file.write(self.textEdit.toPlainText())

    # Отвечает за изменения в программе при изменении положения курсора
    def update(self):
        self.fontComboBox.setCurrentFont(self.textEdit.currentFont())
        self.comboBox.setCurrentText(str(int(self.textEdit.fontPointSize())))

        self.italicButton.setChecked(self.textEdit.fontItalic())
        self.underButton.setChecked(self.textEdit.fontUnderline())
        self.boldButton.setChecked(self.textEdit.fontWeight() == QFont.Bold)

        self.lButton.setChecked(self.textEdit.alignment() == Qt.AlignLeft)
        self.cButton.setChecked(self.textEdit.alignment() == Qt.AlignCenter)
        self.rButton.setChecked(self.textEdit.alignment() == Qt.AlignRight)
        self.jButton.setChecked(self.textEdit.alignment() == Qt.AlignJustify)

    def open(self):
        self.fname = QFileDialog.getOpenFileName(self, '', '', 'text document(*.txt);;html document(*.html)')[0]
        if self.fname:
            with open(self.fname, 'rt', encoding='utf-8') as file:
                self.textEdit.setTextColor(QColor(0, 0, 0))
                self.textEdit.clear()
                self.textEdit.setFontPointSize(8)
                self.textEdit.setFontWeight(QFont.Normal)
                self.textEdit.setFontItalic(False)
                self.textEdit.setFontUnderline(False)
                if self.fname.endswith('.html'):
                    self.textEdit.insertHtml(file.read())
                else:
                    self.textEdit.insertPlainText(file.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
