import logging
import os
import certifi
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
import snscrape.modules.twitter as sntwitter
import re
import asyncio

# Configureren van SSL-certificaat voor Render
os.environ["SSL_CERT_FILE"] = certifi.where()

# Configureren van logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API-token
API_TOKEN = 'JOUW_API_TOKEN_HIER'  # Vul hier je Telegram bot token in.

# Functie voor de /check command
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = []
    for tweet in sntwitter.TwitterUserScraper("cryptolaixe").get_items():
        matches = re.findall(r'https://pump\.fun/([A-Za-z0-9]+)', tweet.content)
        if matches:
            tokens.extend(matches)
        if len(tokens) >= 5:
            break

    if not tokens:
        await update.message.reply_text("Geen token adressen gevonden in recente tweets.")
    else:
        for token in tokens:
            await update.message.reply_text(f"Gevonden token adres: `{token}`", parse_mode="Markdown")

# Functie voor de /start commando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo! Ik ben je pump.fun bot. Gebruik /check om de laatste token adressen te vinden.")

# Functie om tweets periodiek te controleren
async def check_for_new_tweets(context: ContextTypes.DEFAULT_TYPE):
    tokens = []
    for tweet in sntwitter.TwitterUserScraper("cryptolaixe").get_items():
        matches = re.findall(r'https://pump\.fun/([A-Za-z0-9]+)', tweet.content)
        if matches:
            tokens.extend(matches)
        if len(tokens) >= 5:
            break

    if tokens:
        for token in tokens:
            # Stuur bericht naar gebruiker (verander chat_id naar de juiste waarde)
            chat_id = 'JOUW_CHAT_ID_HIER'  # Vul hier je chat_id in
            await context.bot.send_message(chat_id=chat_id, text=f"Nieuwe token adres gevonden: `{token}`", parse_mode="Markdown")
    else:
        logger.info("Geen nieuwe token adressen gevonden.")

# Functie voor het opstarten van de bot
async def main():
    application = Application.builder().token(API_TOKEN).build()

    # Voeg commandhandlers toe
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check))

    # Start de periodieke taak
    job_queue = application.job_queue
    job_queue.run_repeating(check_for_new_tweets, interval=60 * 5, first=0)  # Controleert elke 5 minuten

    # Start de bot
    logger.info("Bot is gestart!")
    await application.run_polling()

if __name__ == '__main__':
    # Start de bot
    import asyncio
    asyncio.run(main())
