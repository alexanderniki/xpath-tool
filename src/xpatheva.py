#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import lxml.etree

from hspace_filler import HSpaceFiller
from app_settings import AppSettings


class XpathEva(QMainWindow):
    
    def __init__(self):

        super().__init__()
        self.settings = AppSettings()

        self.d_print("XpathEva constructor")

        self.filename = ""
        self.xpath_query = ""

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.show_dialog)

        menu_bar = self.menuBar()
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(openFile)
        
        self.filename_label_default_text = "Filename: "
        self.filename_label = QLabel(self)
        self.filename_label.setText(self.filename_label_default_text)
        self.query_edit = QLineEdit()
        self.query_result = QTextEdit()
        self.evaluate_btn_filler = HSpaceFiller()
        self.evaluate_button = QPushButton("Evaluate")
        self.evaluate_button.clicked.connect(self.evaluate_query)
        
        self.vbox = QVBoxLayout()
        self.evaluate_button_layout = QHBoxLayout()

        self.evaluate_button_layout.addWidget(self.evaluate_btn_filler)
        self.evaluate_button_layout.addWidget(self.evaluate_button)

        self.vbox.addWidget(self.filename_label)
        self.vbox.addWidget(self.query_edit)
        self.vbox.addWidget(self.query_result)
        # self.vbox.addWidget(self.evaluate_button)
        self.vbox.addLayout(self.evaluate_button_layout)
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)
        
        self.setGeometry(
                         self.settings.x_position,
                         self.settings.y_position,
                         self.settings.window_width,
                         self.settings.window_height
        )
        self.setWindowTitle('XpathEva')
        self.statusBar().showMessage('Ready')
        self.show()

        self.xpath_query_result = XpathQueryResult

    def show_dialog(self):
        file_opened = QFileDialog.getOpenFileName(self, 'Open File', '')  # This is still not a filename, but a structure like "(" ", " ")"
        self.filename = str(file_opened[0])
        print("Filename: " + self.filename)
        self.filename_label.setText(self.filename_label_default_text + self.filename)

    def evaluate_query(self):
        print("evaluate_query()")
        if (self.filename !=""):
            tree = lxml.etree.parse(self.filename)
        entries = tree.xpath(self.query_edit.text())
        print(type(entries))
        print("Query: " + self.query_edit.text())

        result_string = ""
        try:  # Если результат - это массив объектов

            result_length = len(entries)  # test query: sum(/bookstore/book/price)

            for i in range(0, result_length, 1):  # То для каждого объекта в массиве
                    """
                    Here I have to "normalise" received result somehow
                    Тут нужно каким-то образом "нормализовать" полученный результат.
                    Дело в том, что не всегда у результата бывают аттрибуты text и tag, например.
                    Нужно это как-то проверять и показывать только то, то реально удалось получить.
                    Начал с создания класса XpathQueryResult, но непонятно, правильный ли это путь
                    Также, можно попытаться воспользоваться втроенной функцией type():
                    if (type(entries) is float), тогда делать что-то для float и т.п.
                    """
                    try:  # Пробуем получить его тэг и текст
                        print(entries[i].tag + ": " + entries[i].text)  #  test query: /bookstore/book[1]/title/@lang
                        print(entries[i].attrib)
                        result_string = result_string + entries[i].tag + " : " + entries[i].text + "\n"
                    except Exception as e:  # А если это не объект или тэга и текста нет (другими словами, если нам прилетает тип String или массив строк)
                        print(traceback.format_exc())
                        result_string = entries[i]  # То просто печатаем каждый String из массива в вывод
        except Exception as e: # Если прилетает что-то отличное от массива объектов или String (например, Float)
            print(traceback.format_exc())
            result_length = 1  # То считаем длину результата равной единице
            result_string = entries  # И печатаем то, что прилетело
        self.query_result.setText(str(result_string))

    def d_print(self, message):
        if self.settings.debug == 1:
            print(message)
        else:
            pass

    def __del__(self):
        self.d_print("XpathEva closed")


class XpathEvaApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.evaluator = XpathEva()


class XpathQueryResult:
    query = None  # Type: string
    result = None  # Actual result itself
    tag = None  # Tag attribute
    text = None  # Text attribute
    attrib = None  # Attributes for the result.  Type: dictionary


if __name__ == '__main__':
    app = XpathEvaApp()
    sys.exit(app.exec_())
