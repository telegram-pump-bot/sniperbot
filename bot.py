import logging
import re
import asyncio
import snscrape.modules.twitter as sntwitter
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Zet logging aan
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Zet hier je eigen Telegram bot token
TOKEN = "8005544914:AAHY45Fc3cP6eCKSRrTmlaPOCxSYTLqyT2A"

# /start commando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welkom bij DiamondSniperBot 💎\nGebruik /check om de laatste token adressen te bekijken.")

# /check commando met logging
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = []
    try:
        logging.info("Scraping tweets van @cryptolaixe...")
        async for tweet in sntwitter.TwitterUserScraper("cryptolaixe").get_items():
            logging.info(f"Tweet gevonden: {tweet.content}")
            matches = re.findall(r'https://pump\.fun/([A-Za-z0-9]+)', tweet.content)
            if matches:
                tokens.extend(matches)
            if len(tokens) >= 5:
                break
        logging.info(f"Gevonden tokens: {tokens}")

    except Exception as e:
        logging.error(f"Fout bij het scrapen: {str(e)}")
        await update.message.reply_text(f"❌ Fout bij het ophalen van tweets: {str(e)}")
        return

    if not tokens:
        await update.message.reply_text("⚠️ Geen token adressen gevonden in recente tweets.")
    else:
        for token in tokens:
            await update.message.reply_text(f"Gevonden token adres: `{token}`", parse_mode="Markdown")

# Main functie om bot te starten
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    logging.info("Bot is gestart!")
    await app.run_polling()

# Start bot
if __name__ == "__main__":
    asyncio.run(main())

