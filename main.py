import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        self.updateButton.clicked.connect(self.updateTable)
        self.addButton.clicked.connect(self.addCoffee)
        self.editButton.clicked.connect(self.editCoffee)
        self.updateTable()

    def updateTable(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute('SELECT * FROM Coffee').fetchall()
        self.tableWidget.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()

    def addCoffee(self):
        second_form = addEditCoffeeForm()
        second_form.exec()
        self.updateTable()

    def editCoffee(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            id = self.tableWidget.item(row, 0).text()
            second_form = addEditCoffeeForm(id)
            second_form.exec()
            self.updateTable()


class addEditCoffeeForm(QDialog):
    def __init__(self, id=None):
        self.id = id
        super(addEditCoffeeForm, self).__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()

        data = (
            self.variety.text(),
            self.roastLevel.text(),
            self.groundWhole.text(),
            self.tasteDescription.text(),
            self.price.value(),
            self.packageVolume.value(),
            self.id
        )

        if self.id:
            cur.execute('''UPDATE Coffee 
            SET Variety = ?,
            RoastLevel = ?,
            GroundWhole = ?,
            TasteDescription = ?,
            Price = ?,
            PackageVolume = ?
            WHERE id = ?''', data)
        else:
            cur.execute('''
            INSERT INTO Coffee(Variety, RoastLevel, GroundWhole, TasteDescription, Price, PackageVolume) 
            VALUES (?, ?, ?, ?, ?, ?)''', data[:-1])
        con.commit()
        con.close()
        super().accept()

    def reject(self):
        super().reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())
