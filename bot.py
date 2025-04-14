import logging

import snscrape.modules.twitter as sntwitter

import telegram

from telegram.ext import Updater, CommandHandler, CallbackContext, Update

import re



# Setup logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)



# Je Telegram bot token

TELEGRAM_API_TOKEN = '8005544914:AAHY45Fc3cP6eCKSRrTmlaPOCxSYTLqyT2A'



# Functie om te beginnen met de bot

def start(update: Update, context: CallbackContext) -> None:

    update.message.reply_text("Bot is gestart! Stuur /check om te controleren op nieuwe pump.fun links.")



# Functie om te controleren op nieuwe pump.fun links

def check(update: Update, context: CallbackContext) -> None:

    tweets = get_latest_tweets()



    if not tweets:

        update.message.reply_text("Geen nieuwe pump.fun links gevonden.")

    else:

        for tweet in tweets:

            update.message.reply_text(f"Nieuwe tweet gevonden: {tweet['url']}")



# Functie om de laatste tweets op te halen van het specifieke account

def get_latest_tweets():

    # Account waarvan je tweets wil scrapen

    account = "cryptolaixe"

    

    # Een lijst om de gevonden tweets op te slaan

    tweet_list = []



    # Scrape de laatste 5 tweets van het account

    for tweet in sntwitter.TwitterUserScraper(account).get_items():

        if 'pump.fun' in tweet.content:

            tweet_list.append({'url': f'https://twitter.com/{account}/status/{tweet.id}'})

        if len(tweet_list) >= 5:  # Stop na 5 tweets

            break

    return tweet_list



# Foutmelding loggen

def error(update: Update, context: CallbackContext) -> None:

    logger.warning(f"Update {update} caused error {context.error}")



def main() -> None:

    # Maak de Updater aan en geef je token

    updater = Updater(TELEGRAM_API_TOKEN)



    # Haal de dispatcher op om handlers toe te voegen

    dispatcher = updater.dispatcher



    # Voeg commando handlers toe

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("check", check))



    # Log errors

    dispatcher.add_error_handler(error)



    # Start de bot

    updater.start_polling()



    # Draai de bot totdat deze wordt gestopt

    updater.idle()



if __name__ == '__main__':

    main()
