import telebot
from keys import *
import Service
from datetime import datetime
import json
import difflib

bot = telebot.TeleBot(token=chiave)

startedChats = []
chatsInformation = []
needed_data = ['IMDb Rating','Age Rating','Industry','Release date','Director','Writer','Language','Duration']
ageRating = {'TV-PG': 0, 'R': 1, 'Unrated': 2, 'PG-13': 3, 'TV-MA': 4, 'TV-G': 5, 'TV-14': 6, 'PG': 7, 'TV-Y7': 8, 'G': 9, 'NC-17': 10, 'TV-Y': 11, 'Approved': 12, 'TV-Y7-FV': 13, 'MA-17': 14, 'TV-13': 15, 'Drama': 16, 'Drama, Romance': 17, 'Passed': 18, '18+': 19}
industry = {'Hollywood / English': 0, 'Tollywood': 1, 'Wrestling': 2, 'Bollywood / Indian': 3, 'Punjabi': 4, 'Anime / Kids': 5, 'Dub / Dual Audio': 6, 'Pakistani': 7, 'Stage shows': 8, '3D Movies': 9}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! \nPlease, Enter the data relating the film whose views you want to predict")
    bot.send_message(message.chat.id, "Start by entering the IMDb Rating")

@bot.message_handler(commands=['search'])
def search(message):
    search_array = message.text.split(' ')[1].lower()
    search = message.text.removeprefix("/search " + search_array).strip().lower()

    if search_array == "industry":
        possibleIndustries = ""
        print(search)
        for code in difflib.get_close_matches(search.strip().lower(), list(Service.Predicter().industry.keys())):
            possibleIndustries+=code + '\n'
        bot.reply_to(message, "Search results:\n" + possibleIndustries)
    elif search_array == "director":
        possibleDirectors = ""
        for code in difflib.get_close_matches(search.strip().lower(), list(Service.Predicter().director.keys())):
            possibleDirectors+=code + '\n'
        bot.reply_to(message, "Search results:\n" + possibleDirectors)
    elif search_array == "writer":
        possibleWriters= ""
        for code in difflib.get_close_matches(search.strip().lower(), list(Service.Predicter().writer.keys())):
            possibleWriters+=code + '\n'
        bot.reply_to(message, "Search results:\n" + possibleWriters)
    elif search_array == "language":
        possibleLanguages = ""
        for code in difflib.get_close_matches(search.strip().lower(), list(Service.Predicter().language.keys())):
            possibleLanguages+=code + '\n'
        bot.reply_to(message, "Search results:\n" + possibleLanguages)
    else:
        bot.reply_to(message, "Can't find " + search_array)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    global startedChats
    situationIndex = 0
    print(message.chat.id)
    if message.chat.id not in startedChats:
        startedChats.append(message.chat.id)
        chatsInformation.append({"chatid":message.chat.id, "N":0, "data":{}})
    situationIndex = startedChats.index(message.chat.id)
    chat_talking_with_me = chatsInformation[situationIndex]
    msg = message.text
    
    if ( 'help' in message.text ):
        response = 'The informations that you should enter are:\n'
        for i in needed_data:
            response += i + '\n'
        bot.reply_to(message, response)
    else:
        errors = False
        #Tutti i vari controlli
        if chat_talking_with_me["N"] == 0:
            # controllo IMDb Rating
            try:
                rating = float(msg)
                rating = int(rating)
                if rating < 0 or rating > 10:
                    bot.reply_to(message, "The IMDb Rating should be between 0 and 10.\nPlease retry")
                    errors = True
                else:
                    chat_talking_with_me["data"]["imdb"] = msg
                    chat_talking_with_me["N"]+=1
            except:
                bot.reply_to(message, "The IMDb Rating should be a number. Not a string or else.\nPlease retry")
                errors = True
        elif chat_talking_with_me["N"] == 1:
            # controllo sull'age Rating
            if msg not in ageRating.keys():
                possibleRating = ""
                for code in ageRating.keys():
                    possibleRating+=code + '\n'
                bot.reply_to(message, "You've inserted an age Rating that does not exist.")
                bot.reply_to(message,"Please try with one of there:\n" + possibleRating)
                errors = True
            else:
                chat_talking_with_me["data"]["age"] = Service.Predicter().ageRating[msg]
                chat_talking_with_me["N"]+=1
        elif chat_talking_with_me["N"] == 2:
            # controllo sull'idustria
            if msg not in Service.Predicter().industry.keys():
                possibleIndustries = ""
                for code in difflib.get_close_matches(msg.strip().lower(), list(Service.Predicter().industry.keys())):
                    possibleIndustries+=code + '\n'
                bot.reply_to(message, "You've inserted an industry that does not exist.")
                bot.reply_to(message,"Please try with one of there:\n" + possibleIndustries)
                errors = True
            else:
                chat_talking_with_me["data"]["ind"] = Service.Predicter().industry[msg]
                chat_talking_with_me["N"]+=1
        elif chat_talking_with_me["N"] == 3:
            # controllo sulla data d'uscita
            try:
                date = datetime.strptime(msg, '%Y-%m-%d').date().year
                chat_talking_with_me["data"]["date"] = msg
                chat_talking_with_me["N"]+=1
            except:
                bot.reply_to(message, "You've mistanken the date.\nPlease retry")
                errors = True
        elif chat_talking_with_me["N"] == 4:
            # controllo sul director
            #if msg not in Service.Predicter().director:
            if len(Service.Predicter().checkDirector(msg)) != 0:
                possibleDirectors = ""
                directors = msg.lower().split(',')
                for d in directors:
                    for s in difflib.get_close_matches(d.strip(), list(Service.Predicter().director.keys())):
                        possibleDirectors += s + '\n'
                #for code in Service.Predicter().director.keys():
                #    if msg in code:
                #        possibleDirectors+=code + '\n'
                bot.reply_to(message, "You've inserted a director that does not exist.")
                if possibleDirectors != "":
                    bot.reply_to(message,"Please try with one of there:\n" + possibleDirectors)
                errors = True
            else:
                chat_talking_with_me["data"]["dir"] = msg
                chat_talking_with_me["N"]+=1
        elif chat_talking_with_me["N"] == 5:
            # controllo sul writer
            #if msg not in Service.Predicter().writer:
            if len(Service.Predicter().checkWriter(msg)) != 0:
                possibleWriters = ""
                writers = msg.lower().split(',')
                for w in writers:
                    for code in difflib.get_close_matches(w.strip(), list(Service.Predicter().writer.keys())):
                        possibleWriters+=code + '\n'
                bot.reply_to(message, "You've inserted a writer that does not exist.")
                if possibleWriters != "":
                    bot.reply_to(message,"Please try with one of there:\n" + possibleWriters)
                errors = True
            else:
                chat_talking_with_me["data"]["wri"] = msg
                chat_talking_with_me["N"]+=1
        elif chat_talking_with_me["N"] == 6:
            # controllo sulla ligua
            #if msg not in Service.Predicter().language:
            if len(Service.Predicter().checkLanguage(msg)) != 0:
                bot.reply_to(message, "You've inserted a language that does not exist.\nPlease retry")
                errors = True
            else:
                chat_talking_with_me["data"]["lan"] = msg
                chat_talking_with_me["N"]+=1
        elif chat_talking_with_me["N"] == 7:
            # controllo sulla durata
            try:
                rating = int(msg)
                if rating <= 0:
                    bot.reply_to(message, "The duration should be greater than 0.\nPlease retry")
                    errors = True
                else:
                    chat_talking_with_me["data"]["dur"] = msg
                    chat_talking_with_me["N"]+=1
            except:
                bot.reply_to(message, "The duration should be a number. Not a string or else.\nPlease retry")
                errors = True


        if chat_talking_with_me["N"] == len(needed_data):
            bot.reply_to(message, "Whait. I'm calculating the views that it is going to get if it was pirated by someone in the internet")
            responce = Service.Predicter().predict(chat_talking_with_me["data"])
            views = int(responce[0])
            bot.send_message(message.chat.id, "Based on my calculations your title is going to get " + str(views) + " veiws")
            bot.send_message(message.chat.id,"If you what to predict the views of another film just start by entering the IMDb rating")
            chat_talking_with_me["N"] = 0
            chat_talking_with_me["data"].clear()
        else:
            if errors == False:
                res = "Good. Now enter " + needed_data[chat_talking_with_me["N"]]
                if chat_talking_with_me["N"] == 3:
                    res+="\nReamember that the date should be written by using this format (YYYY-mm-dd)"
                bot.reply_to(message,res)
        errors = False


bot.infinity_polling()

        
        

