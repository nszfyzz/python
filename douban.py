#!/usr/bin/env python
# coding = 'utf-8'
import bs4
from bs4 import BeautifulSoup
import re
import requests

def getHtmlText(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }
        r = requests.get(url,headers=headers,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def douban(url,lst):
    html = getHtmlText(url)
    soup = BeautifulSoup(html,"html.parser")

    movies = soup.find('ol',attrs={'class':'grid_view'})
    for movie_li in movies.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()

        lst.append(movie_name)

    # string_page = '?start=50&filter='
    for i in range(1,10):
        string_page = url+'?start='+str(i*25)+'&filter='
        # print(string_page)
        html = getHtmlText(string_page)
        soup = BeautifulSoup(html, "html.parser")
        movies = soup.find('ol', attrs={'class': 'grid_view'})
        for movie_li in movies.find_all('li'):
            detail = movie_li.find('div', attrs={'class': 'hd'})
            movie_name = detail.find('span', attrs={'class': 'title'}).getText()

            lst.append(movie_name)

    return lst
    # print(movies)
    # movies_info = movies.find('li')
    # print(movies_info)
    # for movie in movies_info:
    #     movie_name = movie.find('span',attrs={'class':'title'})
    #     lst.append(movie_name)
    # for movie in movies:
    #     try:
    #         if movie:
    #             movie_name = (re.findall(r'\w+', movie.string)[0])
    #             lst.append(movie_name)
    #     except:
    #         return ""

def main():
    url = 'https://movie.douban.com/top250'
    movie_list = []
    final_list = douban(url,movie_list)
    with open('movies.txt','w',encoding='utf-8') as file:
        for list in final_list:
            file.write(list+'\n')

main()

# import codecs
#
# import requests
# from bs4 import BeautifulSoup
#
# DOWNLOAD_URL = 'http://movie.douban.com/top250/'
#
#
# def download_page(url):
#     return requests.get(url, headers={
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
#     }).content
#
#
# def parse_html(html):
#     soup = BeautifulSoup(html,"html.parser")
#     movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
#
#     movie_name_list = []
#
#     for movie_li in movie_list_soup.find_all('li'):
#         detail = movie_li.find('div', attrs={'class': 'hd'})
#         movie_name = detail.find('span', attrs={'class': 'title'}).getText()
#
#         movie_name_list.append(movie_name)
#
#     next_page = soup.find('span', attrs={'class': 'next'}).find('a')
#     if next_page:
#         return movie_name_list, DOWNLOAD_URL + next_page['href']
#     return movie_name_list, None
#
#
# def main():
#     url = DOWNLOAD_URL
#
#     with codecs.open('movies', 'wb', encoding='utf-8') as fp:
#         while url:
#             html = download_page(url)
#             movies, url = parse_html(html)
#             fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))
#
#
# if __name__ == '__main__':
#     main()