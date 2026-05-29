import os
import random
import sqlite3
import sys

from openpyxl import Workbook
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

DB_FILE = os.path.join(os.path.dirname(__file__), "bycle.db")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Bycle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            qty INTEGER NOT NULL
        )
        """
    )
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM Bycle")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_data = []
        for i in range(1, 101):
            sample_data.append(
                (
                    f"Bicycle {i:03d}",
                    100000 + (i * 1250),
                    1 + (i % 20),
                )
            )
        cursor.executemany(
            "INSERT INTO Bycle (name, price, qty) VALUES (?, ?, ?)", sample_data
        )
        conn.commit()

    return conn


class BycleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bycle 관리 앱")
        self.resize(760, 520)

        self.conn = init_db()
        self.cursor = self.conn.cursor()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()
        self.qty_input = QLineEdit()
        self.search_input = QLineEdit()

        self.title_label = QLabel("Bycle Bike Manager")
        self.subtitle_label = QLabel("SQLite + PyQt6로 자전거 재고를 쉽고 빠르게 관리")
        self.title_label.setObjectName("titleLabel")
        self.subtitle_label.setObjectName("subtitleLabel")

        self.price_input.setValidator(QIntValidator(0, 100000000, self))
        self.qty_input.setValidator(QIntValidator(0, 100000000, self))
        self.id_input.setReadOnly(True)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "가격", "수량"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.doubleClicked.connect(self.on_table_double_clicked)
        self.table.setAlternatingRowColors(True)

        self.add_button = QPushButton("추가")
        self.update_button = QPushButton("수정")
        self.delete_button = QPushButton("삭제")
        self.search_button = QPushButton("검색")
        self.refresh_button = QPushButton("전체목록")
        self.clear_button = QPushButton("입력 초기화")
        self.export_button = QPushButton("excel로 출력")

        self.add_button.clicked.connect(self.add_item)
        self.update_button.clicked.connect(self.update_item)
        self.delete_button.clicked.connect(self.delete_item)
        self.search_button.clicked.connect(self.search_items)
        self.refresh_button.clicked.connect(self.load_data)
        self.clear_button.clicked.connect(self.clear_inputs)
        self.export_button.clicked.connect(self.export_to_excel)

        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        search_layout = QHBoxLayout()

        header_layout = QVBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        header_layout.setSpacing(6)

        form_layout.addWidget(QLabel("ID"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("이름"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("가격"))
        form_layout.addWidget(self.price_input)
        form_layout.addWidget(QLabel("수량"))
        form_layout.addWidget(self.qty_input)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)

        search_layout.addWidget(QLabel("검색 (ID 또는 이름)"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.refresh_button)

        input_card = QWidget()
        input_card.setObjectName("inputCard")
        input_card_layout = QVBoxLayout(input_card)
        input_card_layout.setContentsMargins(20, 20, 20, 20)
        input_card_layout.setSpacing(15)
        input_card_layout.addLayout(form_layout)
        input_card_layout.addLayout(button_layout)
        input_card_layout.addLayout(search_layout)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(input_card)
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #f5f7fb, stop:1 #e2ebf7);
            }
            QWidget {
                font-family: "Malgun Gothic", "Segoe UI", Arial, sans-serif;
                font-size: 11pt;
                color: #334e68;
            }
            QLabel {
                color: #334e68;
            }
            QLabel#titleLabel {
                font-size: 22pt;
                font-weight: 700;
                color: #102a43;
            }
            QLabel#subtitleLabel {
                font-size: 11pt;
                color: #627d98;
            }
            QWidget#inputCard {
                background: #ffffff;
                border: 1px solid #d9e2ec;
                border-radius: 18px;
            }
            QLineEdit {
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                padding: 10px;
                background: #f9fbff;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 1px solid #7b9acc;
                background: #ffffff;
            }
            QPushButton {
                border: none;
                border-radius: 12px;
                padding: 10px 18px;
                font-weight: 600;
                background-color: #3b82f6;
                color: #ffffff;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QTableWidget {
                background: transparent;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #1e3a8a;
                color: white;
                padding: 10px;
                border: none;
                font-weight: 600;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e3a8a;
            }
            """
        )

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.verticalHeader().setVisible(False)

        self.load_data()

    def show_message(self, title: str, message: str):
        QMessageBox.information(self, title, message)

    def execute_query(self, query: str, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def load_data(self):
        self.table.setRowCount(0)
        self.cursor.execute("SELECT id, name, price, qty FROM Bycle ORDER BY id")
        rows = self.cursor.fetchall()
        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col_index in (0, 2, 3):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_inputs(self):
        self.id_input.clear()
        self.name_input.clear()
        self.price_input.clear()
        self.qty_input.clear()
        self.search_input.clear()
        self.table.clearSelection()

    def add_item(self):
        name = self.name_input.text().strip()
        price = self.price_input.text().strip()
        qty = self.qty_input.text().strip()

        if not name:
            self.show_message("입력 오류", "자전거 이름을 입력해주세요.")
            return

        if not price or not qty:
            self.show_message("입력 오류", "가격과 수량을 모두 입력해주세요.")
            return

        self.cursor.execute(
            "INSERT INTO Bycle (name, price, qty) VALUES (?, ?, ?)",
            (name, int(price), int(qty)),
        )
        self.conn.commit()
        self.load_data()
        self.clear_inputs()

    def update_item(self):
        item_id = self.id_input.text().strip()
        if not item_id:
            self.show_message("수정 오류", "수정할 항목을 먼저 선택해주세요.")
            return

        name = self.name_input.text().strip()
        price = self.price_input.text().strip()
        qty = self.qty_input.text().strip()

        if not name or not price or not qty:
            self.show_message("수정 오류", "이름, 가격, 수량을 모두 입력해주세요.")
            return

        self.cursor.execute(
            "UPDATE Bycle SET name = ?, price = ?, qty = ? WHERE id = ?",
            (name, int(price), int(qty), int(item_id)),
        )
        self.conn.commit()
        self.load_data()
        self.clear_inputs()

    def delete_item(self):
        item_id = self.id_input.text().strip()
        if not item_id:
            self.show_message("삭제 오류", "삭제할 항목을 먼저 선택해주세요.")
            return

        confirm = QMessageBox.question(
            self,
            "삭제 확인",
            f"ID {item_id} 항목을 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.cursor.execute("DELETE FROM Bycle WHERE id = ?", (int(item_id),))
        self.conn.commit()
        self.load_data()
        self.clear_inputs()

    def export_to_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Excel 파일로 저장",
            os.path.join(os.path.dirname(__file__), "bycle.xlsx"),
            "Excel 파일 (*.xlsx)",
        )
        if not path:
            return

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Bycle"
        worksheet.append(["ID", "이름", "가격", "수량"])

        self.cursor.execute("SELECT id, name, price, qty FROM Bycle ORDER BY id")
        for row_data in self.cursor.fetchall():
            worksheet.append(list(row_data))

        workbook.save(path)
        self.show_message("엑셀 저장 완료", f"{os.path.basename(path)} 파일로 저장되었습니다.")

    def search_items(self):
        query = self.search_input.text().strip()
        if not query:
            self.load_data()
            return

        if query.isdigit():
            self.cursor.execute(
                "SELECT id, name, price, qty FROM Bycle WHERE id = ? OR name LIKE ? ORDER BY id",
                (int(query), f"%{query}%"),
            )
        else:
            self.cursor.execute(
                "SELECT id, name, price, qty FROM Bycle WHERE name LIKE ? ORDER BY id",
                (f"%{query}%",),
            )

        rows = self.cursor.fetchall()
        self.table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col_index in (0, 2, 3):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def on_table_double_clicked(self):
        row = self.table.currentRow()
        if row < 0:
            return

        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.price_input.setText(self.table.item(row, 2).text())
        self.qty_input.setText(self.table.item(row, 3).text())

    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BycleApp()
    window.show()
    sys.exit(app.exec())
