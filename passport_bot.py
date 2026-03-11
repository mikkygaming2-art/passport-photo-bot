from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from flask import Flask
import threading

TOKEN = "8684584686:AAEOHNalOyxT5Q1aJB6vyTWeKdlJnn1hdmo"

# ---------- Web server for Render ----------
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Passport bot running"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()


# ---------- Telegram Bot ----------
async def process_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo = update.message.photo[-1]
    file = await photo.get_file()
    await file.download_to_drive("photo.jpg")

    img = Image.open("photo.jpg")

    passport = img.resize((413,531))

    # ---------- A4 layout (30 photos) ----------
    a4 = Image.new("RGB",(2480,3508),"white")

    for r in range(6):
        for c in range(5):
            x = c*450+50
            y = r*550+50
            a4.paste(passport,(x,y))

    a4.save("a4_passport.jpg")

    # ---------- 4x6 layout (8 photos) ----------
    sheet = Image.new("RGB",(1800,1200),"white")

    x_spacing = 430
    y_spacing = 560
    margin_x = 40
    margin_y = 40

    for row in range(2):
        for col in range(4):
            x = margin_x + col * x_spacing
            y = margin_y + row * y_spacing
            sheet.paste(passport,(x,y))

    sheet.save("4x6_passport.jpg")

    await update.message.reply_photo(photo=open("a4_passport.jpg","rb"))
    await update.message.reply_photo(photo=open("4x6_passport.jpg","rb"))


# ---------- Start bot ----------
bot = ApplicationBuilder().token(TOKEN).build()

bot.add_handler(MessageHandler(filters.PHOTO, process_photo))

bot.run_polling()
