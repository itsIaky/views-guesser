
import telebot
from keys import *
import Service
from datetime import datetime
import json

bot = telebot.TeleBot(token=chiave)


film_data = {}
Number_of_data = 0
needed_data = ['IMDb Rating','Age Rating','Industry','Release date','Director','Writer','Language','Duration']
ageRating = {'TV-PG': 0, 'R': 1, 'Unrated': 2, 'PG-13': 3, 'TV-MA': 4, 'TV-G': 5, 'TV-14': 6, 'PG': 7, 'TV-Y7': 8, 'G': 9, 'NC-17': 10, 'TV-Y': 11, 'Approved': 12, 'TV-Y7-FV': 13, 'MA-17': 14, 'TV-13': 15, 'Drama': 16, 'Drama, Romance': 17, 'Passed': 18, '18+': 19}
industry = {'Hollywood / English': 0, 'Tollywood': 1, 'Wrestling': 2, 'Bollywood / Indian': 3, 'Punjabi': 4, 'Anime / Kids': 5, 'Dub / Dual Audio': 6, 'Pakistani': 7, 'Stage shows': 8, '3D Movies': 9}



@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    global Number_of_data
    print(message.text)
    msg = message.text
    if ( 'start' in message.text ):
        bot.reply_to(message, "Welcome! \nPlease, Enter the data relating to the film whose views you want to know\nStart by entering the IMDb Rating")
    elif ( 'help' in message.text ):
        response = 'The informations that you should enter are:\n'
        for i in needed_data:
            response += i + '\n'
        bot.reply_to(message, response)
    else:
        errors = False
        #Tutti i vari controlli
        if Number_of_data == 0:
            # controllo IMDb Rating
            try:
                rating = float(msg)
                rating = int(rating)
                if rating < 0 or rating > 10:
                    bot.reply_to(message, "The IMDb Rating should be between 0 and 10.\nPlease retry")
                    errors = True
                else:
                    film_data["imdb"] = msg
                    print(film_data)
                    Number_of_data+=1
            except:
                bot.reply_to(message, "The IMDb Rating should be a number. Not a string or else.\nPlease retry")
                errors = True
        elif Number_of_data == 1:
            # controllo sull'age Rating
            print(msg)
            if msg not in ageRating.keys():
                bot.reply_to(message, "You've inserted an age Rating that does not exist.\nPlease retry")
                errors = True
            else:
                film_data["age"] = Service.Predicter().ageRating[msg]


                Number_of_data+=1
        elif Number_of_data == 2:
            # controllo sull'idustria
            if msg not in industry.keys():
                bot.reply_to(message, "You've inserted an industry that does not exist.\nPlease retry")
                errors = True
            else:
                film_data["ind"] = Service.Predicter().industry[msg]
                Number_of_data+=1
        elif Number_of_data == 3:
            # controllo sulla data d'uscita
            try:
                date = datetime.strptime(msg, '%Y-%m-%d').date().year
                film_data["date"] = msg
                Number_of_data+=1
            except:
                bot.reply_to(message, "You've mistanken the date.\nPlease retry")
                errors = True
        elif Number_of_data == 4:
            # controllo sul director
            if msg not in Service.Predicter().director:
                bot.reply_to(message, "You've inserted a director that does not exist.\nPlease retry")
                errors = True
            else:
                film_data["dir"] = msg
                Number_of_data+=1
        elif Number_of_data == 5:
            # controllo sul writer
            if msg not in Service.Predicter().director:
                bot.reply_to(message, "You've inserted a writer that does not exist.\nPlease retry")
                errors = True
            else:
                film_data["wri"] = msg
                Number_of_data+=1
        elif Number_of_data == 6:
            # controllo sulla ligua
            if msg not in Service.Predicter().language:
                bot.reply_to(message, "You've inserted a language that does not exist.\nPlease retry")
                errors = True
            else:
                film_data["lan"] = msg
                Number_of_data+=1
        elif Number_of_data == 7:
            # controllo sulla durata
            try:
                rating = int(msg)
                if rating <= 0:
                    bot.reply_to(message, "The duration should be greater than 0.\nPlease retry")
                    errors = True
                else:
                    film_data["dur"] = msg
                    Number_of_data+=1
            except:
                bot.reply_to(message, "The duration should be a number. Not a string or else.\nPlease retry")
                errors = True


        if Number_of_data == len(needed_data):
            bot.reply_to(message, "Whait. I'm calculating the views that it is going to get if it was pirated by someone in the internet")
            responce = Service.Predicter().predict(film_data)
            print("stocco")
            print(responce[0])
            views = int(responce[0])
            bot.reply_to(message, "Based on my calculations your title is going to get " + str(views) + " veiws")
            Number_of_data = 0
            film_data.clear()
        else:
            if errors == False:
                res = "Good. Now enter " + needed_data[Number_of_data]
                if Number_of_data == 3:
                    res+="\nReamember that the date should be written by using this format (YYYY-mm-dd)"
                bot.reply_to(message,res)
        errors = False
            

    
bot.infinity_polling()

        
        

