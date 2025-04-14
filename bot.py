import os
import certifi
import logging
import asyncio
import re
import snscrape.modules.twitter as sntwitter

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Zorg dat SSL correct werkt op Render
os.environ["SSL_CERT_FILE"] = certifi.where()

# Logging activeren
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram API Token
TELEGRAM_API_TOKEN = "8005544914:AAHY45Fc3cP6eCKSRrTmlaPOCxSYTLqyT2A"

# /start commando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is actief! Gebruik /check om tokens te checken.")

# /check commando
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = []

    try:
        for tweet in sntwitter.TwitterUserScraper("cryptolaixe").get_items():
            # Zoek naar links van pump.fun
            matches = re.findall(r"https://pump\.fun/([A-Za-z0-9]+)", tweet.content)
            if matches:
                tokens.extend(matches)
            if len(tokens) >= 5:
                break

        if not tokens:
            await update.message.reply_text("Geen token-adressen gevonden in recente tweets.")
        else:
            for token in tokens:
                await update.message.reply_text(f"Gevonden token adres: `{token}`", parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Fout bij het ophalen van tweets: {e}")
        await update.message.reply_text("Er is een fout opgetreden bij het ophalen van tweets.")

# Main functie
async def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    logger.info("Bot is gestart!")
    await app.run_polling()

# Voor Render — vermijd asyncio.run()
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        logger.error(f"Event loop error: {e}")
