import requests
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint       #整理打印(一次無法印很多次數)


### step 1: request
url = "https://www.twking.cc/"
r = requests.get(url)
r.encoding = 'utl-8'        #中文字，避免亂碼
# print(r.text[:3000])        #看前 3000個


### step 2: 找訊息
soup = BeautifulSoup(r.text, 'html.parser')
# soup.find_all('div', class_='booktop')
booktops = soup.find_all('div', attrs={"class": "booktop"})
for booktop in booktops:
    # print(booktop.p)          #爬到所有 top10 的主題
    
    ## 方法一(萬用，但必須嚴謹的爬)
    # tops = booktop.find_all('p')
    # top_type = tops[0].text           #哪種 top10?， text 可以只拿到字
    # print(top_type)

    # for top in tops[1:]:
    #     print('\t', top.a.text, ':', top.a.get('href'))    #拿到每個小說名，與連結網址


    ## 方法二
    top_type = booktop.p.text
    tops = booktop.css.select('p a')    #小說名
    print(top_type)

    for top in tops[1:]:
        print('\t', top.text, ':', top.get('href'))


### step 3: collection (收集)
booktop_summarize = dict()      #存在字典的變數
booktops = soup.find_all('div', attrs={"class": "booktop"})
for booktop in booktops:
    tops = booktop.find_all('p')
    for top in tops[1:]:
        top_book_name = top.a.text.strip()  #小說名稱   #strip = 清除前後的空白
        top_book_url = top.a.get('href')    #小說網址連結

        if top_book_name in booktop_summarize:
            booktop_summarize[top_book_name]['count'] += 1      #代表已'存在'在紀錄中
        else:
            booktop_summarize[top_book_name] = {
                'count' : 1,
                'href' : top_book_url
            }
# pprint(booktop_summarize)


# (' 光明壁壘', {'count': 1, 'href': 'https://www.twking.cc/162_162374/'})
pprint(sorted(booktop_summarize.items(),        # items 是一個用 dictionary 來顯示
              reverse = True,                   #降幕排序
              key= lambda x: x[1]['count']))    # lambda 是一個微型function ，拿來當排序的依據

sorted_booktop_summarize = sorted(
    booktop_summarize.items(),        
    reverse = True,                   
    key= lambda x: x[1]['count'])

"""
 格式: list of dictionary
 [
    {'novel_name': 'ABC', 'count': 1, 'novel_page_url': '.....'},
    {'novel_name': 'DEF', 'count': 2, 'novel_page_url': '.....'},
    {'novel_name': 'GHI', 'count': 3, 'novel_page_url': '.....'},
 ]
 
"""

book_rows = list()                                  #做成格式 .csv
for book in sorted_booktop_summarize:
    book_name = book[0]
    book_count = book[1]['count']
    book_page_url = book[1]['href']
    book_row = {
        'novel_name': book_name,
        'top_count': book_count,
        'novel_page_url': book_page_url
    }
    book_rows.append(book_row)

booktop_summarize_df = pd.DataFrame(book_rows)
booktop_summarize_df.to_csv('booktop.csv')      #建 .csv 名稱

