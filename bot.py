import logging
import re
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
    await update.message.reply_text("Bot is actief! Gebruik /check om te zoeken naar pump.fun token adressen.")

# Check commando
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

# Start de bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling()

if __name__ == '__main__':
    main()
