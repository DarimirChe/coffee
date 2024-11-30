import sys
import sqlite3

from UI import main
from UI import addEditCoffeeForm
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.updateButton.clicked.connect(self.updateTable)
        self.ui.addButton.clicked.connect(self.addCoffee)
        self.ui.editButton.clicked.connect(self.editCoffee)
        self.updateTable()

    def updateTable(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        result = cur.execute('SELECT * FROM Coffee').fetchall()
        self.ui.tableWidget.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()

    def addCoffee(self):
        second_form = addEditCoffee()
        second_form.exec()
        self.updateTable()

    def editCoffee(self):
        row = self.ui.tableWidget.currentRow()
        if row != -1:
            id = self.ui.tableWidget.item(row, 0).text()
            second_form = addEditCoffee(id)
            second_form.exec()
            self.updateTable()


class addEditCoffee(QDialog):
    def __init__(self, id=None):
        self.id = id
        super(addEditCoffee, self).__init__()
        self.ui = addEditCoffeeForm.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def accept(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()

        data = (
            self.ui.variety.text(),
            self.ui.roastLevel.text(),
            self.ui.groundWhole.text(),
            self.ui.tasteDescription.text(),
            self.ui.price.value(),
            self.ui.packageVolume.value(),
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
