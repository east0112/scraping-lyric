#歌詞の全データを元に、DBの単語データを全更新する。
import csv
import psycopg2
import psycopg2.extras
from janome.tokenizer import Tokenizer

from scrapingClass import Scrp
from bs4 import BeautifulSoup

#postgreSQL connect関数
def get_connection():
    strCon = " user=postgres dbname= LoveLive_music password= ll0630 port= 5432 host= localhost"
    return psycopg2.connect(strCon)

#単語データを削除する
def delete_words():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        sql = 'DELETE FROM "lyric_words"'
        cur.execute(sql)

#楽曲データを取得する
def get_music():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT "recordId","lyric","musicName" FROM "music"')
        musicRows = cur.fetchall()
        return musicRows

#形態素解析 関数
def analysis_regist(musicId,lyric):
    t = Tokenizer()
    for token in t.tokenize(lyric):
        if token.part_of_speech.split(',')[0] in ["名詞","動詞","形容詞","副詞"]:
            #output.append(token.surface)
            regist_music(musicId,token.surface,token.part_of_speech.split(',')[0])

#postgreSQLのDBへ楽曲情報をINSERTする
def regist_music(recordId,word,speech):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        sql = 'INSERT INTO "lyric_words" ("music_id","word","speech") VALUES(%s,%s,%s)'
        cur.execute(sql,(recordId,word,speech))

#メイン処理
with get_connection() as conn:
    #単語データを全て削除する
    delete_words()
    #楽曲データを全て取得する
    musicRows = get_music()
    #取得した楽曲数だけ単語登録処理を行う
    count = 0
    for music in musicRows:
        count+=1
        print('解析中：' + str(count) + '曲目：' + music['musicName'])
        analysis_regist(music['recordId'],music['lyric'])

    conn.commit()
