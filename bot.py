import logging
import snscrape.modules.twitter as sntwitter
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Telegram Bot Token
TELEGRAM_API_TOKEN = '8005544914:AAHY45Fc3cP6eCKSRrTmlaPOCxSYTLqyT2A'

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Start commando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is actief! Gebruik /check om te zoeken naar pump.fun links.")

# Check commando
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweets = get_latest_tweets()
    if not tweets:
        await update.message.reply_text("Geen pump.fun links gevonden.")
    else:
        for tweet in tweets:
            await update.message.reply_text(f"Gevonden: {tweet['url']}")

# Scraper
def get_latest_tweets():
    account = "cryptolaixe"
    tweet_list = []

    for tweet in sntwitter.TwitterUserScraper(account).get_items():
        if 'pump.fun' in tweet.content:
            tweet_list.append({'url': f'https://twitter.com/{account}/status/{tweet.id}'})
        if len(tweet_list) >= 5:
            break
    return tweet_list

# Start de bot (zonder async main)
def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling()

if __name__ == '__main__':
    main()
