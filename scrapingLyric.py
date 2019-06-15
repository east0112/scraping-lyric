import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

#取得対象（検索結果一覧）のURL定義
#strUrl = 'http://artists.utamap.com/fasearchkasi.php?artistfid=1093633_1'
#置換対象の文字列定義
strBeforeCode = 'http://www.utamap.com/showkasi.php?surl='
#置換後の文字列定義
strAfterCode = 'http://www.utamap.com/phpflash/flashfalsephp.php?unum='
#歌詞ファイル出力先
lyricDir = r'G:\01.work\01.project\00.CloudWord\lyric' + '\\'
#HTMLから除去するタグ（１）
removeTag1 = r'<html><body><p>test1=51&amp;test2='
#HTMLから除去するタグ（２）
removeTag2 = r'</p></body></html>'

#postgreSQL connect関数
def get_connection():
    strCon = " user=postgres dbname= LoveLive_music password= ll0630 port= 5432 host= localhost"
    return psycopg2.connect(strCon)

#requestsを用いてWebページのHTMLを取得する
def get_Html(url):
    responceList = requests.get(url)
    responceList.status_code
    #BeautifulSoupを用いてURL要素を抽出する
    soup = BeautifulSoup(responceList.content,"lxml")
    return soup

#取得した歌詞情報から余計なタグを除去する
def remove_Html(html):
    print(removeTag1)
    print(removeTag2)
    print(html)
    #tmp = html.strip('body')
    #tmp = tmp.strip(removeTag2)
    return tmp

strUrl = input()

soupList = get_Html(strUrl)
classUrl = soupList.find_all(class_='ct140')

#メイン処理
urls = []
for tags in classUrl:
    aTag = tags.select('a')
    for a in aTag:
        urls.append(a.attrs['href'])

#CSV作成
f = open(lyricDir + 'lyric_{0:%Y%m%d%H%M%S}'.format(datetime.now()) + '.csv','w')
writer = csv.writer(f, lineterminator='\n')
csvlist = []
#抽出したURLを元に歌詞を取得する
for lyricUrl in urls:
    lyricUrl = lyricUrl.replace(strBeforeCode,strAfterCode)
    soup = get_Html(lyricUrl)
    csvlist.append(soup)
    #csvlist.append(remove_Html(soup))

# 出力
writer.writerow(csvlist)

# ファイルクローズ
f.close()
