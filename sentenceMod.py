import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kakao.settings")
import django
django.setup()
from konlpy.tag import Okt

from bot.models import Sentence

def changeTone(str):
    PoliteDict={
        "하어요.":"해요.",
        "한어요.":"해요.",
        "는어요.":"않아요",
        "랍어요.":"라워요.",
        "웁어요.":"워요.",
        "갑어요.":"가워요.",
        "렵어요.":"려워요.",
        "랍어요.":"리워요.",
        "겹어요.":"겨워요.",
        "습어요.":"스워요.",
        "니어요.":"니다."
    }
    str = str.replace("다.", "어요.")
    for before, after in PoliteDict.items():
        if before in str:
            str = str.replace(before, after)
    return str

def noSpecialChar(str):
    import re
    return re.sub("[^a-zA-z0-9?!~.,…ㄱ-ㅣ가-힣 ]","",str)

def PolishSentence(str):
    str = noSpecialChar(str)
    str = changeTone(str)
    return str;

def sentenceModifierDB():  # Modify all string stored in DB
    sentence_set = Sentence.objects.all()
    for s in sentence_set.iterator():
        if "다." in s.sentence:
            s.sentence = PolishSentence(s.sentence)
            s.save()
def sentenceModifierSTR(str):  # Modify input string and return modified string
    return PolishSentence(str)
