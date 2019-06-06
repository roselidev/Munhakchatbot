import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kakao.settings")
import django
django.setup()

from bot.models import Sentence
from konlpy.tag import Kkma, Okt

def keyword(text):
    #extract keyword from user input & amplify with fasttext synonyms
    nlpy = Okt()
    kwords = nlpy.morphs(text)#extract noun from sentence
    print("keywords : " , kwords)
    return kwords

def fetchS(kw):  # Fetch sentence that is most similar
    import random
    #search keyword in DB sentences
    slist = []
    #first, get all the strings that matches any one of keywords
    for k in kw:
        slist += Sentence.objects.filter(sentence__contains=k)
        slist = [s for s in slist if len(s.sentence)>5 and len(s.sentence)<100]
        if len(slist)==0:
            return randoms()
    #return the first string
        return slist[random.randint(0,len(slist)-1)].sentence

def randoms():
    import random
    #pop any string from DB
    limit = Sentence.objects.all().count() -1
    searchindex = random.randint(0,limit)
    ret = Sentence.objects.get(pk=searchindex)
    print(ret.sentence)
    return ret.sentence

def answer(sentence):
    kw = keyword(sentence)
    return fetchS(kw)
