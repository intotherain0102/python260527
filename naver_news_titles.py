import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

url = (
    "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8"
    "&query=%EB%B0%98%EB%8F%84%EC%B2%B4&ackey=727xlqxb"
)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

news_titles = []
seen = set()

container = soup.select_one("div.fds-news-item-list-desk")
if container is None:
    container = soup

for a in container.select('a[data-heatmap-target=".tit"]'):
    title = a.get_text(strip=True)
    if not title:
        continue
    if title in seen:
        continue
    seen.add(title)
    news_titles.append(title)

print("크롤링된 뉴스 제목:")
for index, title in enumerate(news_titles, 1):
    print(f"{index}. {title}")

workbook = Workbook()
sheet = workbook.active
sheet.title = "Naver News"
sheet.append(["번호", "제목"])
for index, title in enumerate(news_titles, 1):
    sheet.append([index, title])

output_file = "naver_result.xlsx"
workbook.save(output_file)
print(f"결과가 '{output_file}'에 저장되었습니다.")
