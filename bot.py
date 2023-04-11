from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import random
import urllib.parse as urlparse

qr = "👨‍💻 Tạo mã QR"

domain = "https://chootc.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(qr)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    text = "<b>Vui lòng gửi thông tin theo cú pháp:</b>\nDòng 1: Số tài khoản\nDòng 2: Tên ngân hàng\nDòng 3: Số tiền chuyển\nDòng 4: Nội dung chuyển\n\n<b>Ví dụ:</b>\n38333333333888\nmbbank\n1,000,000\nChuc mung sinh nhat em"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if update.message.chat.type != "private":
        return
    
    if "/qr" in update.message.text  or qr in update.message.text:
        text = "<b>Vui lòng gửi thông tin theo cú pháp:</b>\nDòng 1: Số tài khoản\nDòng 2: Tên ngân hàng\nDòng 3: Số tiền chuyển\nDòng 4: Nội dung chuyển\n\n<b>Ví dụ:</b>\n38333333333888\nmbbank\n1,000,000\nChuc mung sinh nhat em"

        await context.bot.send_message(chat_id, text=text, parse_mode=constants.ParseMode.HTML)

    info = update.message.text.split("\n")

    try:
        qr_link = url_fix(f"https://img.vietqr.io/image/{info[1]}-{info[0]}-compact2.jpg?amount={formatMoney(info[2])}&addInfo={info[3]}&accountName=QR")
        await context.bot.send_photo(chat_id, qr_link)
    except IndexError:
        if "/qr" in update.message.text  or qr in update.message.text:
            return
        text = "Sai cú pháp rồi đồ ngok"
        await context.bot.send_message(chat_id, text=text)

    
def url_fix(s):
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urlparse.quote(path, '/%')
    qs = urlparse.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

def formatMoney(value):
    return value.replace(",", "").replace(".", "")

app = ApplicationBuilder().token(
    "5721300942:AAFLc5GA2xwQOx9bX8MXuVZIvbP9ZcNDRVU").build()

app.add_handler(CommandHandler("start", start)) 
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()