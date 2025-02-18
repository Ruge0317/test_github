import requests
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint       #整理打印(一次無法印很多次數)


## Step 1: 讀取主頁排行榜名單
book_tops = pd.read_csv('booktop.csv')
# print(book_tops.head(10))
book_top10s = book_tops.head(10)    #取前 10

last_chapter_titles = list()        #各本小說的最後章節標題
last_chapter_urls = list()          #各本小說的最後章節原文連結
nums_of_chapters = list()           #總共有幾個章節

for book_top10 in book_top10s.iterrows():
    print(book_top10[1]['novel_name'], book_top10[1]['novel_page_url'])   #找到所有的小說名稱


    ## step 2: 取得章節術與最後一章的連結與標題
    page_url = book_top10[1]['novel_page_url']
    r = requests.get(page_url)
    r.encoding = 'utl-8'         #中文字，避免亂碼
    page_soup = BeautifulSoup(r.text, 'html.parser')    # BeautifulSoup 做解析

    ## step 2.1: 取得包含所有章節的版面 DOM Tree節點
    chapter_wrapper = page_soup.find(
        'div',
        attrs={'class':'info-chapters flex flex-wrap'})

    ## step 2.2: 取得所有章節
    chapters = chapter_wrapper.find_all('a')
    print(f"{book_top10[1]['novel_name']}, # of chapters: {len(chapters)}")
    last_chapter = chapters[-1]
    last_chapter_title = last_chapter.get('title')
    last_chapter_url = last_chapter.get('href')
    print(f"last chapter: {last_chapter}")     #最新章節的名稱
    print(f"which at {last_chapter}")           #最新章節的網址
    print()


    ## step 3: 蒐集資訊
    last_chapter_titles.append(last_chapter_title)
    last_chapter_urls.append(last_chapter_url)
    nums_of_chapters.append(len(chapters))


book_top10s.loc[:,'chapter_numbers'] = nums_of_chapters
book_top10s.loc[:, 'last_chapter_url'] = last_chapter_urls
book_top10s.loc[:, 'last_chapter_title'] = last_chapter_titles


book_top10s.to_csv('book.top10s.csv')       #建 .csv 名稱