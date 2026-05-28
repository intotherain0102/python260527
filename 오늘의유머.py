# web2.py

from bs4 import BeautifulSoup
import urllib.request
# 정규표현식
import re

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

# 파일에 저장(write text)
f = open("todayHumor.txt", "wt", encoding="utf-8")

#url = "https://www.clien.net/service/board/sold"

# 페이지 번호를 1부터 10까지 증가시키면서 반복
for i in range(1, 11):
    url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)

    print(url)

    #웹브라우져 헤더 추가 
    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(data, "html.parser")

    # filtering
    list = soup.find_all("td", attrs={"class":"subject"})

    for tag in list:
        title = tag.find("a").text.strip()

        # 정규표현식으로 문자열 가공
        if re.search("일본", title):
            print(title)
            f.write(title + "\n")

f.close()

# 선택한 block 주석 : cntl + /
# <td class="subject">
# <a href="/board/view.php?table=bestofbest&amp;no=482962&amp;s_no=482962&amp;page=1" target="_top">"요즘 시대에서 한국인을 나누는 기준"</a>
