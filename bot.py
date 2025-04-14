import logging
import os
import snscrape.modules.twitter as sntwitter
import re
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# Logging activeren
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram API Token
TELEGRAM_API_TOKEN = "8005544914:AAHY45Fc3cP6eCKSRrTmlaPOCxSYTLqyT2A"
# Je chat_id (Kan je vinden via je bot als je de juiste code gebruikt)
CHAT_ID = 'JOUW_CHAT_ID_HIER'  # Vul hier je echte chat ID in

# /start commando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is actief! Ik volg de Twitter van @cryptoalxe voor token adressen.")

# Functie om de tweets van @cryptoalxe te scannen voor token adressen
async def check_for_tokens():
    tokens = []
    # Scrape de tweets van de gebruiker @cryptoalxe
    for tweet in sntwitter.TwitterUserScraper("cryptoalxe").get_items():
        # Zoek naar token adressen in de tekst van de tweet (voorbeeld: https://pump.fun/token_address)
        matches = re.findall(r'https://pump\.fun/([A-Za-z0-9]+)', tweet.content)
        if matches:
            tokens.extend(matches)

    # Als we tokens vinden, stuur ze dan naar je Telegram
    if tokens:
        for token in tokens:
            message = f"Nieuwe token adres gevonden: `{token}`"
            await send_message_to_telegram(message)
    else:
        logger.info("Geen tokens gevonden in de laatste tweets.")

# Functie om een bericht naar je Telegram te sturen
async def send_message_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        logger.info("Bericht succesvol verstuurd naar Telegram.")
    else:
        logger.error(f"Fout bij het versturen van het bericht naar Telegram: {response.status_code}")

# Functie om de bot op te starten en periodiek te laten controleren
async def main():
    # Telegram bot setup
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # Start de bot
    logger.info("Bot is gestart!")
    await app.run_polling()

    # Start het periodieke controleren van de tweets van @cryptoalxe
    while True:
        await check_for_tokens()
        await asyncio.sleep(60 * 5)  # Elke 5 minuten controleren

# Voer de bot uit
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        logger.error(f"Fout bij het starten van de bot: {e}")

