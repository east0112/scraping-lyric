import csv
import psycopg2
import psycopg2.extras

from scrapingClass import Scrp
from bs4 import BeautifulSoup
from datetime import datetime


#取得対象（検索結果一覧）のURL定義
#strUrl = 'https://www.uta-net.com/artist/18955/'
strUrl = input()
#歌詞ファイル出力先
lyricDir = r'G:\01.work\01.project\00.CloudWord\lyric' + '\\'
#Uta-Netの結合URL
lyricURL = 'https://www.uta-net.com'

#postgreSQL connect関数
def get_connection():
    strCon = " user=postgres dbname= LoveLive_music password= ll0630 port= 5432 host= localhost"
    return psycopg2.connect(strCon)

#レコード番号の最大値を取得する
def get_recordId():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT max("recordId") as "maxId" FROM "music"')
        musicRows = cur.fetchall()
        return musicRows[0]['maxId']+1

#postgreSQLのDBへ楽曲情報をINSERTする
def regist_music(recordId,musicName,lyric):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        sql = 'INSERT INTO "music" ("recordId","musicName","lyric") VALUES(%s,%s,%s)'
        cur.execute(sql,(recordId,musicName,lyric))

#メイン処理
#検索結果一覧からHTMLを取得する
soupList = Scrp.get_Html(strUrl)
classUrl = soupList.find_all(class_='td1')
urls = []

#取得したURLから楽曲URLをリストへ格納する
for tags in classUrl:
    aTag = tags.select('a')
    for a in aTag:
        url = lyricURL + a.attrs['href']
        urls.append(url)

#抽出したURLを元に歌詞を取得する
with get_connection() as conn:
    for lyricUrl in urls:
        soup = Scrp.get_lyric(lyricUrl)
        lyric = soup[0]
        musicName = soup[1]
        #レコード番号の最大値を取得する
        recordId = get_recordId()
        #取得した楽曲名、歌詞をデータベースへINSERTする
        regist_music(recordId,musicName,lyric)

    conn.commit()
