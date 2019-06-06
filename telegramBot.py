import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kakao.settings")
import django
django.setup()

from bot.models import Sentence
from konlpy.tag import Okt
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format('wiki.ko.vec')

def keyword(text):
    #extract keyword from user input
    nlpy = Okt()
    kwords = nlpy.morphs(text)#extract noun from sentence
    result = kwords
    for k in kwords:
        tmp = model.most_similar(k)
        tmp = [w[0] for w in tmp]
        result += tmp
    return kwords

def fetchS(kw):  # Fetch sentence that is most similar
    import random
    #search keyword in DB sentences
    slist = []
    #first, get all the strings that matches any one of keywords
    for k in kw:
        slist += Sentence.objects.filter(sentence__contains=k)
    #second, eliminate strings that are too short or too long
    slist = [s for s in slist if len(s.sentence)>5 and len(s.sentence)<100]    
    if len(slist)==0:
        return random(kw)
    #return the first string
        return slist[random.randint(0,len(slist)-1)].sentence

def random(kw):
    import random
    #pop any string from DB
    limit = Sentence.objects.all().count() -1
    searchindex = random.randint(0,limit)
    ret = Sentence.objects.get(pk=searchindex)
    print(ret.sentence)
    return ret.sentence

def get_message(bot, update):
    update.message.reply_text(chatbot(update.message.text))

def chatbot(u):
    kw = keyword(u)
    return fetchS(kw)

from telegram.ext import Updater, MessageHandler, Filters
import telegram

myToken = '735083403:AAGuOa2ebHktP8hvGPqY-KFjOknHx3R-Ar8'

bot = telegram.Bot(token = myToken)
updater = Updater(myToken)
updates = bot.getUpdates()
for u in updates:
    print(u.message)
    bot.sendMessage(chat_id=u.message.chat_id, text=chatbot(u.message.text))
message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)
updater.start_polling(timeout=3, clean=True)
updater.idle()
