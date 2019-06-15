import requests
from bs4 import BeautifulSoup

class Scrp:
    #URLからHTMLを取得する
    #Parameters
    #url：HTMLを取得するURL
    #Returns
    #soup：html
    def get_Html(url):
        #requestsを用いてWebページのHTMLを取得する
        responceList = requests.get(url)
        responceList.status_code
        #BeautifulSoupを用いてURL要素を抽出する
        soup = BeautifulSoup(responceList.content,"lxml")
        return soup

    #HTMLから楽曲情報を抽出する
    #Parameters
    #url：HTMLを取得するURL
    #Returns
    #lyric：歌詞情報
    #music：曲名
    def get_lyric(url):
        responceList = requests.get(url)
        responceList.status_code
        #BeautifulSoupを用いてURL要素を抽出する
        soup = BeautifulSoup(responceList.content,"lxml")
        #歌詞を抽出する
        lyric = soup.find_all(id='kashi_area')
        #曲名を抽出する
        music = soup.find_all(id='ttl_name_box')

        return lyric[0].text,music[0].find('span').text.replace('曲名：','')
