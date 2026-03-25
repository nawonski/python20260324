# web.py
#웹크롤링 선언
from bs4 import BeautifulSoup
#웹사이트 요청
import urllib.request

#파일로 저장
f = open("todayHumor.txt", "wt", encoding="utf-8")
#정규표현식 추가
import re


#페이지처
for i in range(1, 11):
    url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)
    print(url)
    #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
    hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
    #웹브라우져 헤더 추가 
    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()
    #검색이 용이한 스프객체
    soup = BeautifulSoup(data, "html.parser")
    lst = soup.find_all("td", attrs={"class":"subject"})
    for tag in lst:
        title = tag.find("a").text.strip()
        if re.search("한국",title):
            print(title)
            f.write(title + "\n")

f.close()

# <td class="subject"><a href="/board/view.php?table=bestofbest&amp;no=482486&amp;s_no=482486&amp;page=1" target="_top">이재명 장기집권 꼭 해야 됨</a><span class="list_memo_count_span"> [24]</span>  <img src="//www.todayhumor.co.kr/board/images/list_icon_pencil.gif?2" alt="창작글" style="margin-right:3px;top:2px;position:relative"> </td>


