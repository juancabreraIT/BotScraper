# -*- coding: utf-8 -*-
__author__ = 'JuanCabrera'

import telebot              # API library for the bot
from telebot import types   # API types for the bot
from bs4 import BeautifulSoup
import requests

TOKEN = '192274303:AAG3HldmTiYVASW6Z6u-mPiHO9NZn5zuBjc' # Token @BotFather supplied

bot = telebot.TeleBot(TOKEN) # Creating the bot

#################### URLs
greenMartaURL = 'http://restaurantegreendos.com/index.php?z=4';
magnoliaURL = 'http://www.magnoliacatering.es/menu-diario/';
terrazaLink = 'https://www.facebook.com/Restaurante-Bar-La-Terrazza-695849873878729/';
stopLink = 'https://www.facebook.com/cafestopfuencarral/';
fenixLink = 'https://www.facebook.com/fenixcaferestaurante/';
fenixTwitter = 'https://twitter.com/fenixcaferest';
lunaLink = 'https://www.facebook.com/restaurantelalunamadrid/';
####################

# listener
def listener(messages):                             
    for m in messages:                              
        if m.content_type == 'text':                
            cid = m.chat.id                         # ID of the chat
            print "[" + str(cid) + "]: " + m.text   # Print something like: -> [52033876]: /start
            print "userID: " + str(m.from_user.id)
            
bot.set_update_listener(listener)
            

#################### Commands
@bot.message_handler(commands=['green'])
def command_green(m):
    cid = m.chat.id
    bot.send_message(cid, greenMartaURL)
    html = getHTML(greenMartaURL)
    if html is None:
        bot.send_message(cid, "Algo está roto!!!!!")
        return
    
    bot.send_message(cid, greenMarta(html))
    
@bot.message_handler(commands=['terrazza'])
def command_terrazza(m):
    cid = m.chat.id
    bot.send_message(cid, terrazaLink)
    
@bot.message_handler(commands=['stop'])
def command_stop(m):
    cid = m.chat.id
    bot.send_message(cid, stopLink)
    
@bot.message_handler(commands=['fenix'])
def command_fenix(m):
    cid = m.chat.id
    bot.send_message(cid, fenixLink)
    bot.send_message(cid, fenixTwitter)

@bot.message_handler(commands=['luna'])
def command_luna(m):
    cid = m.chat.id
    bot.send_message(cid, lunaLink)
    
@bot.message_handler(commands=['magnolia'])
def command_magnolia(m):
    cid = m.chat.id
    bot.send_message(cid, magnoliaURL)
    html = getHTML(magnoliaURL)
    if html is None:
        return
    
    bot.send_message(cid, magnolia(html))

### Here is where web scraping starts ###
### WEB SCRAPING ZONE ###
#########################################

#################### Methods
def getHTML(url):

    req = requests.get(url)
            
    return BeautifulSoup(req.text, "html5lib") if req.status_code == 200 else None

def greenMarta(html):
    
    result = "RESTAURANTE GREEN MARTA II\n"
    
    mainDiv = html.find_all('div', {'id': 'main'})[0]
    result += mainDiv.select('strong > strong > h1 > font > u')[0].getText() + "\n******************************\n"
    paraLlevar = mainDiv.select('p > strong')
    
    for pEntry in paraLlevar:
        if pEntry.getText().strip() == "":
            continue
        result += pEntry.getText().strip() + "\n"

    result += greenPrimeros(html)
    result += greenSegundos(html)

    return result
    
def greenPrimeros(html):
    result = "\n***** Primeros *****\n"
    
    platos = html.select('#main > strong > strong > h1 > font > em')
    
    arrayPrimeros = str(platos[0]).replace("<em>", "").replace("</em>", "").split("<br/>")
    
    for element in arrayPrimeros:
        result += str(element.strip()).decode("utf8") + "\n"

    return result
    
def greenSegundos(html):
    
    result = "***** Segundos *****\n"
    
    headers1 = html.find_all('h1')[4]
    platos = []
 
    for h1 in headers1:
        array = str(h1).replace("<font face=\"times\" size=\"5\"><em>", "").replace("</em></font>", "").split("<br/>")[0:-1]
        for item in array:
            platos.append(item)
    
    for plato in platos:
        result += str(plato).decode("utf8") + "\n"
    
    return result
    
def magnolia(html):
    
    result = "RESTAURANTE MAGNOLIA\n"
    
    fecha = html.find_all('p', {'class': 'titulo'})[0]
    
    result += fecha.getText() + "\n******************************\n"
    
    carta = html.find_all('div', {'class': 'cajaCarta'})[0]
    
    result += carta.getText().replace(":", "").replace("Sin plato", "\n")
    
    return result
    

    
#Peticiones
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo


    
    
                