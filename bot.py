#!/bin/env python

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler
        , Filters,ConversationHandler)

MOOD, CONSENT, DURATION, = range(3)

## Set API KEY
apiKey=""

def start(update, context):
    reply_keyboard = [['Bored' , 'Horny', 'Find mommy','/cancel']]
    user = update.message.from_user
    info = "The author created this bot to give my friends a hard time('hard time', pun unintended) and not to cause harm to anyone. It's all good fun!"
    greeter = info + "\n\nNow tell us " + user.first_name + " what's it going to be today?\n Enter /cancel to exit"
    update.message.reply_text(
            greeter,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                
    return  MOOD


def mood_setter(update, context):
    user = update.message.from_user
    reply_keyboard = [['yay','nay','/cancel']]
    print(update.message.text)    
    if update.message.text == 'Find mommy':
        update.message.reply_text("You have to book an appointment first. Shall I book one for you?",
            reply_markup = (
                ReplyKeyboardMarkup(
                    reply_keyboard,
                    one_time_keyboard=True)
            )
    )
    else:
        update.message.reply_text("An appointment with my client should fix that", reply_markup = (
                ReplyKeyboardMarkup(
                    reply_keyboard,
                    one_time_keyboard=True)
                )
        )
   
    return CONSENT
                       
def consent_getter(update, context):
    user = update.message.from_user
    if update.message.text == 'yay':
        reply_keyboard = [['30 minutes','60 minutes', 'Full night','/cancel']]
        update.message.reply_text("Wise choice, enter duration",
            reply_markup = (
                ReplyKeyboardMarkup(reply_keyboard, 
                one_time_keyboard=True)
            )
        )
        return DURATION
    if update.message.text == 'nay':
        update.message.reply_text("Okay, come back if you change your mind!")
        return ConversationHandler.END

def duration_getter(update, context):
    user = update.message.from_user
    print(update.message.text)
    if update.message.text == "Full night":
        duration = "night"
    else:
        duration = "next " + update.message.text
    message = "Very well, Randi is yours for the " + duration
    update.message.reply_text(message)
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text("Okay, come back if you change your mind!",
             reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    updater = Updater(
            apiKey,
             use_context=True
             )
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states = {
                
                MOOD : [MessageHandler(Filters.regex('^(Bored|Horny|Find mommy)$'), mood_setter)],
                CONSENT: [
                    MessageHandler(Filters.regex(
                        '^(yay|nay)$'
                        ),
                    consent_getter)
                ],

                DURATION:[MessageHandler(Filters.regex('^(30 minutes|60 minutes|Full night)$'), duration_getter)],
            },
     
            fallbacks=[CommandHandler('cancel', cancel)]
        )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
