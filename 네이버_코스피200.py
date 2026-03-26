import sys
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QTextEdit, QProgressBar, QLabel, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal

iframe_base = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class DataFetcher(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list, list)
    error = pyqtSignal(str)

    def run(self):
        try:
            all_data = []
            header = None
            total_pages = 20
            for page in range(1, total_pages + 1):
                page_rows = self.fetch_page(page)
                if not page_rows:
                    continue
                filtered = [row for row in page_rows if any(cell.strip() for cell in row)]
                if not filtered:
                    continue
                if header is None:
                    header = filtered[0]
                for row in filtered:
                    if row[0].strip() in ("종목별", "순위"):
                        continue
                    all_data.append(row)
                self.progress.emit(int((page / total_pages) * 100))

            if not header:
                raise RuntimeError("편입종목상위 헤더를 찾을 수 없습니다.")
            if not all_data:
                raise RuntimeError("편입종목상위 데이터를 파싱했지만 결과가 없습니다.")

            self.finished.emit(header, all_data)
        except Exception as e:
            self.error.emit(str(e))

    def fetch_page(self, page):
        url = f"{iframe_base}&page={page}"
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.select_one("table")
        if table is None:
            raise RuntimeError(f"페이지 {page}의 편입종목상위 테이블을 찾을 수 없습니다.")
        all_rows = []
        for tr in table.select("tr"):
            cols = [cell.get_text(strip=True) for cell in tr.find_all(["th", "td"])]
            if cols:
                all_rows.append(cols)
        return all_rows

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("네이버 코스피200 데이터 수집기")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.fetch_button = QPushButton("데이터 가져오기")
        self.fetch_button.clicked.connect(self.start_fetch)
        self.layout.addWidget(self.fetch_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.save_button = QPushButton("엑셀 저장")
        self.save_button.clicked.connect(self.save_to_excel)
        self.save_button.setEnabled(False)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.header = None
        self.all_data = None

    def start_fetch(self):
        self.fetch_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.table.clear()
        self.save_button.setEnabled(False)

        self.fetcher = DataFetcher()
        self.fetcher.progress.connect(self.progress_bar.setValue)
        self.fetcher.finished.connect(self.on_fetch_finished)
        self.fetcher.error.connect(self.on_fetch_error)
        self.fetcher.start()

    def on_fetch_finished(self, header, all_data):
        self.header = header
        self.all_data = all_data
        self.fetch_button.setEnabled(True)
        self.save_button.setEnabled(True)

        self.table.setRowCount(len(all_data))
        self.table.setColumnCount(len(header) + 1)
        self.table.setHorizontalHeaderLabels(["순번"] + header)

        for idx, row in enumerate(all_data, start=1):
            self.table.setItem(idx - 1, 0, QTableWidgetItem(str(idx)))
            for col_idx, cell in enumerate(row):
                self.table.setItem(idx - 1, col_idx + 1, QTableWidgetItem(cell))

    def on_fetch_error(self, error_msg):
        self.fetch_button.setEnabled(True)
        QMessageBox.critical(self, "오류", f"데이터 가져오기 실패: {error_msg}")

    def save_to_excel(self):
        if not self.header or not self.all_data:
            QMessageBox.warning(self, "경고", "저장할 데이터가 없습니다.")
            return

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "KPI200 편입종목상위"

            ws.append(["순번"] + self.header)
            for idx, row in enumerate(self.all_data, start=1):
                ws.append([idx] + row)

            wb.save("naver_코스피200_result.xlsx")
            QMessageBox.information(self, "성공", "저장 완료: naver_코스피200_result.xlsx")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"엑셀 저장 실패: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

