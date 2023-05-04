import telebot
from keys import *
import Service
from datetime import datetime
import json
import difflib

bot = telebot.TeleBot(token=chiave)

def greenSquare():
    return u'\U00002705'
def redSquare():
    return u'\U0000274C'

startedChats = []
chatsInformation = []
needed_data = ['IMDb Rating','Age Rating','Industry','Release date','Director','Writer','Language','Duration']
ageRating = {'tv-pg': 0, 'r': 1, 'unrated': 2, 'pg-13': 3, 'tv-ma': 4, 'tv-g': 5, 'tv-14': 6, 'pg': 7, 'tv-y7': 8, 'g': 9, 'nc-17': 10, 'tv-y': 11, 'approved': 12, 'tv-y7-fv': 13, 'ma-17': 14, 'tv-13': 15, 'drama': 16, 'drama, romance': 17, 'passed': 18, '18+': 19}
industry = {'hollywood / english': 0, 'tollywood': 1, 'wrestling': 2, 'bollywood / indian': 3, 'punjabi': 4, 'anime / kids': 5, 'dub / dual audio': 6, 'pakistani': 7, 'stage shows': 8, '3d movies': 9}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! \nPlease, Enter the data relating the film whose views you want to predict")
    bot.send_message(message.chat.id, "Start by entering the IMDb Rating")

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.id not in startedChats:
        startedChats.append(message.chat.id)
        chatsInformation.append({"chatid":message.chat.id, "N":0, "data":{}})
    situationIndex = startedChats.index(message.chat.id)
    chat_talking_with_me = chatsInformation[situationIndex]
    keys = list(chat_talking_with_me["data"].keys())
    res = "Data you have submitted:"
    i = 0
    while i < len(needed_data):
        if i < len(chat_talking_with_me["data"].keys()) : res += "\n " + greenSquare() + " " + needed_data[i] + ": " + str(chat_talking_with_me["data"][keys[i]])
        else: res += "\n " + redSquare() + " " + needed_data[i] + ": -"
        i+=1
    bot.reply_to(message, res)
    
@bot.message_handler(commands=['clear'])
def clear(message):
    if message.chat.id not in startedChats:
        startedChats.append(message.chat.id)
        chatsInformation.append({"chatid":message.chat.id, "N":0, "data":{}})
    else:
        situationIndex = startedChats.index(message.chat.id)
        chatsInformation[situationIndex] = {"chatid":message.chat.id, "N":0, "data":{}}
    bot.reply_to(message, "Your submitted data has been deleted")

@bot.message_handler(commands=['help','?'])
def start(message):
    global startedChats
    global chatsInformation
    if message.chat.id not in startedChats:
        startedChats.append(message.chat.id)
        chatsInformation.append({"chatid":message.chat.id, "N":0, "data":{}})
    situationIndex = startedChats.index(message.chat.id)
    chat_talking_with_me = chatsInformation[situationIndex]
    if chat_talking_with_me["N"] == 0:
        response = 'The informations that you should enter are:\n'
        for i in needed_data:
            response += i + '\n'
        bot.reply_to(message, response)
        bot.send_message(message.chat.id,"You can start by entering the IMDb Rating\nIt should be a number between 0 and 10.")
    elif chat_talking_with_me["N"] == 1:
        possibleRating = ""
        for code in ageRating.keys():
            possibleRating+=code + '\n'
        bot.reply_to(message,"Possible examples of age rating are:\n" + possibleRating)
    elif chat_talking_with_me["N"] == 2:
        possibleIndustries = ""
        for code in Service.Predicter().industry.keys():
            possibleIndustries+=code + '\n'
        bot.reply_to(message,"Possible examples of industries are:\n" + possibleIndustries)
    elif chat_talking_with_me["N"] == 3:
        bot.reply_to(message,"You should enter the release date of your film\nReamember that the date should be written by using this format (YYYY-mm-dd)")
    elif chat_talking_with_me["N"] == 4:
        bot.reply_to(message,"Now you should enter the names of the directors of your film\nIf you have to insert more than one director just reameber to devide them by using a ,")
    elif chat_talking_with_me["N"] == 5:
        bot.reply_to(message,"Now you should enter the names of the writers of your film\nIf you have to insert more than one writer just reameber to devide them by using a ,")
    elif chat_talking_with_me["N"] == 6:
        bot.reply_to(message,"Now you should enter the languages of your film\nIf you have to insert more than one language just reameber to devide them by using a ,")
    elif chat_talking_with_me["N"] == 7:
        bot.reply_to(message,"Now you should enter the durations of your film")




@bot.message_handler(commands=['search'])
def search(message):
    if message.chat.id not in startedChats:
        startedChats.append(message.chat.id)
        chatsInformation.append({"chatid":message.chat.id, "N":0, "data":{}})
    situationIndex = startedChats.index(message.chat.id)
    chat_talking_with_me = chatsInformation[situationIndex]

    if len(message.text.split(' ')) == 3:
        search_array = message.text.split(' ')[1].lower()
        search = message.text.removeprefix("/search " + search_array).strip().lower().replace('-'," ")
        if search_array == "industry":
            possibleIndustries = ""
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
    elif len(message.text.split(' ')) == 2:
        search = message.text.removeprefix("/search ").strip().lower()
        if chat_talking_with_me["N"] == 4:
            possibleDirectors = ""
            d = message.text.lower().replace('-'," ")
            for s in difflib.get_close_matches(d.strip(), list(Service.Predicter().director.keys())):
                possibleDirectors += s + '\n'
            bot.reply_to(message,"Search results:\n" + possibleDirectors)
        elif chat_talking_with_me["N"] == 5:
            possibleWriters = ""
            w = message.text.lower().replace('-'," ")
            for s in difflib.get_close_matches(w.strip(), list(Service.Predicter().writer.keys())):
                possibleWriters += s + '\n'
            bot.reply_to(message,"Search results:\n" + possibleWriters)
        elif chat_talking_with_me["N"] == 6:
            possibleLanguages = ""
            l = message.text.lower()
            for s in difflib.get_close_matches(l.strip(), list(Service.Predicter().language.keys())):
                possibleLanguages += s + '\n'
            bot.reply_to(message,"Search results:\n" + possibleLanguages)
        elif chat_talking_with_me["N"] == 2:
            possibleIndustries = ""
            i = message.text.lower()
            for s in difflib.get_close_matches(i.strip(), list(Service.Predicter().industry.keys())):
                possibleIndustries += s + '\n'
            bot.reply_to(message,"Search results:\n" + possibleIndustries)
        elif chat_talking_with_me["N"] == 1:
            possibleRating = ""
            for code in ageRating.keys():
                possibleRating+=code + '\n'
            bot.reply_to(message,"Possible examples of age rating are:\n" + possibleRating)
        elif chat_talking_with_me["N"] == 3:
            bot.reply_to(message,"You should enter the release date of your film\nReamember that the date should be written by using this format (YYYY-mm-dd)")
        elif chat_talking_with_me["N"] == 7:
            bot.reply_to(message,"Now you should enter the durations of your film")
    else:
        if len(message.text.split(' ')) == 1:
            bot.reply_to(message,"Wrong way to make a reaserch!")
        elif chat_talking_with_me["N"] == 0:
            bot.reply_to(message,"The IMDb Rating is a number between 0 and 10")
            


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
    msg = message.text.replace('\n','').lower().strip()
    print(msg)
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
            bot.send_message(message.chat.id,"Please try with one of there:\n" + possibleRating)
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
            bot.send_message(message.chat.id,"Please try with one of there:\n" + possibleIndustries)
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
            bot.send_message(message.chat.id, "Remember the max number of directors is 3")
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
            bot.send_message(message.chat.id, "Remember the max number of writer is 6")
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
                res+="\nRemember that the date should be written by using this format (YYYY-mm-dd)"
            if chat_talking_with_me["N"] in [4, 5, 6]:
                res+="\nRemember that you can send multiple directors, writers or languages by separating each of them with a comma (',')"
            bot.reply_to(message,res)
    errors = False

bot.infinity_polling()

        
        

