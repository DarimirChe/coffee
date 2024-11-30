import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        self.updateButton.clicked.connect(self.updateTable)

    def updateTable(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute('SELECT * FROM Coffee').fetchall()
        self.tableWidget.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())
