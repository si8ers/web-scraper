import os

import string

import requests

from hashlib import sha1

from pathlib import Path

from bs4 import BeautifulSoup


def get_url(link, path=''):
    if not path:
        path = 'get_url_cache_' + sha1(link.encode('ascii')).hexdigest()
    if not Path(path).exists():
        r = requests.get(link)
        if r.status_code == 200:
            file = open(path, 'wt')
            file.write(r.content.decode('utf-8').strip('\n'))
            file.close()
        else:
            return False
    file = open(path, 'rt')
    cont = file.read()
    file.close()
    return cont

page_count = int(input())
type_filter = input()

result = []
url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
for p in range(0, page_count):
    folder = 'Page_' + str(p + 1)
    if not os.access(folder, os.F_OK):
        os.mkdir(folder)
    ok = get_url(url + str(p + 1))
    if ok:
        soup = BeautifulSoup(ok, 'html.parser')
        articles = soup.find_all('li', {'class': 'app-article-list-row__item'})
        for article in articles:
            art_type = article.find('span', {'class': 'c-meta__type'}).text
            if art_type == type_filter:
                anchor = article.find('a')
                art_url = 'https://www.nature.com' + anchor['href']
                art_text = list(anchor.text)
                art_file = ''
                for char in art_text:
                    if char == ' ':
                        art_file += '_'
                    elif string.punctuation.find(char) == -1:
                        art_file += char
                art_file += '.txt'
                art_cont = get_url(art_url)
                if art_cont:
                    art_soup = BeautifulSoup(art_cont, 'html.parser')
                    art_body = art_soup.find('div', {'class': 'c-article-body'})
                    art_save = open(folder + '/' + art_file, 'wt')
                    art_save.write(art_body.text.strip('\n'))
                    art_save.close()
                    result.append(art_file)
# print(result)
print('Saved all articles.')
