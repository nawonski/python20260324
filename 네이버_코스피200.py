import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

iframe_base = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_page(page):
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

all_data = []
header = None
for page in range(1, 21):
    page_rows = fetch_page(page)
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

if not header:
    raise RuntimeError("편입종목상위 헤더를 찾을 수 없습니다.")
if not all_data:
    raise RuntimeError("편입종목상위 데이터를 파싱했지만 결과가 없습니다.")

# 출력
print("순번 | " + " | ".join(header))
for idx, row in enumerate(all_data, start=1):
    print(f"{idx} | " + " | ".join(row))

# Excel 저장 (openpyxl)
wb = Workbook()
ws = wb.active
ws.title = "KPI200 편입종목상위"

ws.append(["순번"] + header)
for idx, row in enumerate(all_data, start=1):
    ws.append([idx] + row)

wb.save("naver_코스피200_result.xlsx")
print("저장 완료: naver_코스피200_result.xlsx")

