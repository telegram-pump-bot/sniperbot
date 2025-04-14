import logging
import os
import certifi
import logging
import asyncio
import re
import snscrape.modules.twitter as sntwitter

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import snscrape.modules.twitter as sntwitter
import re
import asyncio

# Zorg dat SSL correct werkt op Render
# Configureren van SSL-certificaat voor Render
os.environ["SSL_CERT_FILE"] = certifi.where()

# Logging activeren
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Configureren van logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API Token
TELEGRAM_API_TOKEN = "8005544914:AAHY45Fc3cP6eCKSRrTmlaPOCxSYTLqyT2A"

# /start commando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is actief! Gebruik /check om tokens te checken.")

# /check commando
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = []
    for tweet in sntwitter.TwitterUserScraper("cryptolaixe").get_items():
        # Zoek naar token adressen (40 alfanumerieke tekens)
        matches = re.findall(r'\b[A-Za-z0-9]{40}\b', tweet.content)
        if matches:
            tokens.extend(matches)
        if len(tokens) >= 5:
            break

    if not tokens:
        await update.message.reply_text("Geen token adressen gevonden in recente tweets.")
    else:
        for token in tokens:
            await update.message.reply_text(f"Gevonden token adres: `{token}`", parse_mode="Markdown")

# Functie om tweets periodiek te controleren
async def check_for_new_tweets(context: ContextTypes.DEFAULT_TYPE):
    tokens = []
    for tweet in sntwitter.TwitterUserScraper("cryptolaixe").get_items():
        # Zoek naar token adressen (40 alfanumerieke tekens)
        matches = re.findall(r'\b[A-Za-z0-9]{40}\b', tweet.content)
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

# Main functie
# Functie voor het opstarten van de bot
async def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Voeg commandhandlers toe
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check))

    # Start de periodieke taak
    job_queue = application.job_queue
    job_queue.run_repeating(check_for_new_tweets, interval=60 * 5, first=0)  # Controleert elke 5 minuten

    # Start de bot
    logger.info("Bot is gestart!")
    await app.run_polling()
    await application.run_polling()

# Voor Render — vermijd asyncio.run()
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        logger.error(f"Event loop error: {e}")

