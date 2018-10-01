# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
from emoji import emojize

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

client1=os.environ['database']
client=MongoClient(client1)
db=client.dotachat
users=db.users

symbollist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']

lvl1works={
           'concertready':0,
           'sortmedicaments':0,
           'checkpionerssleeping':0
          }
lvl2works={
           'pickberrys':0,
           'bringfoodtokitchen':0,
           'helpinmedpunkt':0,
           'helpinkitchen':0
          }

lvl3works={
           'cleanterritory':0,
           'washgenda':0
          }

def lvlsort(x):
   finallist=[]
   if x==1:
      work=lvl1works
   elif x==2:
      work=lvl2works
   elif x==3:
      work=lvl3works
   for ids in work:
      if ids==0:
         finallist.append(ids)
   return finallist
           

@bot.message_handler(commands=['start'])
def start(m):
 if m.chat.id==m.from_user.id:
  if users.find_one({'id':m.from_user.id})==None:
    users.insert_one(createuser(m.from_user.id, m.from_user.first_name, m.from_user.username))
    bot.send_message(m.chat.id,'Здраствуй, пионер! Меня зовут Ольга Дмитриевна, я буду твоей вожатой. Впереди тебя ждёт интересная жизнь в лагере "Совёнок"! '+
                     'А сейчас скажи нам, как тебя зовут (следующим сообщением).')
  else:
    x=users.find_one({'id':m.from_user.id})
    if x['working']==1:
       bot.send_message(m.chat.id, 'Здраствуй, пионер! Вижу, ты занят. Молодец! Не буду отвлекать.')
    else:
       bot.send_message(m.chat.id, 'Здраствуй, пионер! Отдыхаешь? Могу найти для тебя найти занятие!')
  


@bot.message_handler(commands=['work'])
def work(m):
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
        if x['working']==0:
            bot.send_message(m.chat.id, random.choice(worktexts), reply_to_message_id=m.message_id)
            t=threading.Timer(random.randint(60,120),givework, args=[m.from_user.id])
            t.start()
           
          
def givework(id):
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
       text=''
       if x['OlgaDmitrievna_respect']>=75:
           text+='Так как ты у нас ответственный пионер, для тебя есть важное задание!\n'
           lvl1quests=lvlsort(1)
           quest=random.choice(lvl1quests)
           if quest=='concertready':
              text+='Тебе нужно подготовить сцену для сегодняшнего выступления: '+
           'принести декорации и аппаратуру, которые нужны выступающим пионерам, выровнять стулья. Приступай!'
       elif x['OlgaDmitrievna_respect']>=40:
           text+='Нашла для тебя занятие, ['+x['pionername']+'](tg://user?id='+id+')!\n'
           lvl2quests=lvlsort(2)
           quest=random.choice(lvl2quests)
           if quest=='pickberrys':
              text+='Собери-ка ягоды для вечернего торта! Можешь взять себе в помощь еще кого-нибудь, если хочешь. Одному грести до острова тяжеловато.'
       else:
           text+='Ответственные задания я тебе пока что доверить не могу, ['+x['pionername']+'](tg://user?id='+id+'). Чтобы '+
           'вырастить из тебя образцового пионера,  начнем с малого. Сделай вот что:\n'
       
           
           



worktexts=['Ну что, пионер, скучаешь? Ничего, сейчас найду для тебя подходящее занятие! Подожди немного.',
           'Бездельничаешь? Сейчас я это исправлю! Подожди пару минут, найду тебе занятие.']
  
@bot.message_handler()
def messag(m):
  if m.from_user.id==m.chat.id:
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
        if x['setname']==1:
            not=0
            for ids in m.text:
                if ids not in symbollist:
                    not=1
            if not==0:
                users.update_one({'id':m.from_user.id},{'$set':{'pionername':m.text}})
                users.update_one({'id':m.from_user.id},{'$set':{'setname':0}})
                bot.send_message(m.chat.id, 'Привет, '+m.text+'! Заходи в '+
                                 '@everlastingsummerchat, и знакомься с остальными пионерами!')
            else:
                bot.send_message(m.chat.id, 'Доступны только символы русского и английского алфавита!')
  else:
   if m.reply_to_message!=None:
     x=users.find_one({'id':m.from_user.id})
     if x!=None:
        if x['answering']==1:
            users.update_one({'id':m.from_user.id},{'$set':{'answering':0}})
            if m.text=='Хорошо, Ольга Дмитриевна!':
                 sendm('Молодец, пионер!')
def createuser(id, name, username):
    return{'id':id,
           'name':name,
           'username':username,
           'pionername':None,
           'strenght':3,
           'agility':3,
           'intelligence':3,
           'setname':1,
           'respect':50,
           'working':0,
           'answering':0,
           'OlgaDmitrievna_respect':50,
           'Slavya_respect':50,
           'Uliana_respect':50,
           'Alisa_respect':50,
           'Lena_respect':50,
           'Electronic_respect':50,
           'Miku_respect':50,
           'Zhenya_respect':35
           
          }
    
    
    
if True:
   print('7777')
   bot.polling(none_stop=True,timeout=600)

