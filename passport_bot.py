from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8684584686:AAFmAgU3TJ2nV2q8lVY4z-s0QM8yOQBFdos"

async def process_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo = update.message.photo[-1]
    file = await photo.get_file()

    await file.download_to_drive("photo.jpg")

    img = Image.open("photo.jpg")

    passport = img.resize((413,531))

    # A4 sheet
    a4 = Image.new("RGB",(2480,3508),"white")

    for r in range(6):
        for c in range(5):
            a4.paste(passport,(c*450+50,r*550+50))

    a4.save("a4_passport.jpg")

    # 4x6 sheet
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

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, process_photo))

app.run_polling()
