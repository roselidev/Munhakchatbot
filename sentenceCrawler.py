import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kakao.settings")
import django
django.setup()
from bot.models import Sentence
from konlpy.tag import Kkma
from sentenceMod import sentenceModifierSTR


def crawler(base, root):
    # return dictionary of {sentence:tag} 
    import requests
    from bs4 import BeautifulSoup
    
    # get into each link in the index page
    page = requests.get(root)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.select('body .mw-category-group a')
    linkurls = [link for link in links]

    # get information of the book & get text
    ret={}
    txt=''

    for linkurl in linkurls:
        try:
            print('getting into ' + linkurl.text)
            linkurl = linkurl['href']
            page = requests.get(base + linkurl)
            soup = BeautifulSoup(page.text, 'html.parser')
            title = soup.find('span', {'id': 'header_title_text'}).text
            author = soup.find('span', {'class': 'fn'}).text
            tag = title.replace(" ", '') + author.replace(" ", '')
            txt = soup.select(' .mw-parser-output p')[:-1]
        except Exception as e:
            print(e, title, author)
            continue
        for string in txt:
            string = string.text.replace("\n", '')
            sentencer = Kkma()
            sentence = sentencer.sentences(string)
                #refine string
            for s in sentence:
                s = sentenceModifierSTR(s)
                ret[s] = tag
                #print(s + 'appended')
            print('Store Done for' + tag)
    return ret


base = 'https://ko.wikisource.org'
root = 'https://ko.wikisource.org/wiki/%EB%B6%84%EB%A5%98:%EB%8B%A8%ED%8E%B8%EC%86%8C%EC%84%A4'
sentence_dict = crawler(base, root)
for s, t in sentence_dict.items():
    if(len(s)>300) :  # When parsed data is too long, skip it
        continue
    else:
        Sentence(sentence=s, tag=t).save()  # Store in DB

