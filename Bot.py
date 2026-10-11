from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
from Test_Database import add_user_info
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = "8936754159:AAGw7kGHjxLH4oSi0ui29CPBTLgqrtzsPLM"


def start_menu():
    keyboard = [
        [
            KeyboardButton(
                "تکمیل اطلاعات"
            )
        ],
        [
            KeyboardButton(
                "پشتیبانی"
            )
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def start(Update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = Update.effective_user

    await Update.message.reply_html(text=f"سلام {user.mention_html(name=user.username)}! خوش اومدی.")

    await Update.message.reply_text("با کلیک کردن گزینه های زیر میتونید به پشتیبان پیام بدید و یا اطلاعات خودتون رو تکمیل کنید.", reply_markup=start_menu())


async def get_user_city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print(4)
    # city = Update.message.text
    await update.callback_query.message.reply_text("لطفا اسم شهر خود را به فارسی تایپ کنید:")
    print(5)


async def fill_info(Update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(1)
    Keyboard = [

        [InlineKeyboardButton(
            text="سن",
            callback_data="سن"
        ),


            InlineKeyboardButton(
            text="شهر",
            callback_data="شهر"
        )]

    ]
    print(2)
    reply_markup = InlineKeyboardMarkup(Keyboard)
    print(3)
    await Update.message.reply_text(rf"کدام بخش رو میخوای پر کنی؟", reply_markup=reply_markup)


async def get_user_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Keyboard = [

        [InlineKeyboardButton(
            text="10-19",
            callback_data="10-19"
        ),

            InlineKeyboardButton(
            text="20-29",
            callback_data="20-29"
        ),

            InlineKeyboardButton(
            text="30-39",
            callback_data="30-39"
        )]

    ]
    reply_markup = InlineKeyboardMarkup(Keyboard)

    await update.callback_query.message.reply_text(rf"لطفا رده سنی خودتون رو انتخاب کنید:", reply_markup=reply_markup)


async def user_age_handler_helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    print(data)

    if data == "10-19":
        await age10_19(update, context)

    elif data == "20-29":
        await age20_29(update, context)

    elif data == "30-39":
        await age30_39(update, context)


async def age10_19(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(1)
    keyboard = [
        [
            InlineKeyboardButton(
                text=str(age),
                callback_data=str(age)
            )
            for age in range(10, 15)
        ],
        [
            InlineKeyboardButton(
                text=str(age),
                callback_data=str(age)
            )
            for age in range(15, 20)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سن دقیق خودتون رو انتخاب کنید:",
        reply_markup=reply_markup
    )

    return ConversationHandler.END


async def age20_29(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                text=str(age),
                callback_data=str(age)
            )
            for age in range(20, 25)
        ],
        [
            InlineKeyboardButton(
                text=str(age),
                callback_data=str(age)
            )
            for age in range(25, 30)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سن دقیق خودتون رو انتخاب کنید:",
        reply_markup=reply_markup
    )

    return ConversationHandler.END


async def age30_39(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                text=str(age),
                callback_data=str(age)
            )
            for age in range(30, 35)
        ],
        [
            InlineKeyboardButton(
                text=str(age),
                callback_data=str(age)
            )
            for age in range(35, 40)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سن دقیق خودتون رو انتخاب کنید:",
        reply_markup=reply_markup
    )

    return ConversationHandler.END


async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    age = int(query.data)

    await query.edit_message_text(
        f"سن انتخاب‌شده: {age}"
    )


async def support(Update: Update, context: ContextTypes.DEFAULT_TYPE):

    Keyboard = [
        [InlineKeyboardButton(text="پیام به پشتیبان",
                              url='https://t.me/Protector_of_the_rlm?text=درود%20بر%20تو%20ای%20پشتیبان',
                              style="danger"
                              )
         ]
    ]

    reply_markup = InlineKeyboardMarkup(Keyboard)

    await Update.message.reply_text(rf"کاربر عزیز‍ ممنون از اینکه ربات ما رو انتخاب کردید! برای ارتباط با پشتیبان ربات روی دکمه ی زیر کلیک کنید.",
                                    reply_markup=reply_markup)


async def message_support(Update: Update, Context: ContextTypes.DEFAULT_TYPE):

    query = Update.callback_query

    await query.answer

    await query.edit_message_text(text="درحال انتقال به پیوی پشتیبان...")


async def handler_helper(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logging.info(f"logging callbackquery: {update.callback_query.data}")\

    Data = update.callback_query.data
    print(Data)

    if Data == "شهر":
        await get_user_city(update, context)

    elif Data == "سن":
        await get_user_age(update, context)


def main():
    application = (
        Application.builder().token(BOT_TOKEN).build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(filters.Regex("پشتیبانی"), support)
    )

    application.add_handler(
        MessageHandler(filters.Text("تکمیل اطلاعات"), fill_info)
    )

    # application.add_handler(
    #     CallbackQueryHandler(get_user_city)
    # )

    # application.add_handler(
    #     CallbackQueryHandler(get_user_age)
    # )

    application.add_handler(
        MessageHandler(filters.Regex("10-19"), age10_19)
    )

    application.add_handler(
        MessageHandler(filters.Regex("20-29"), age20_29)
    )

    application.add_handler(
        CallbackQueryHandler(handler_helper)
    )

    application.add_handler(
        MessageHandler(filters.Regex("30-39"), age30_39)
    )

    # application.add_handler(
    #     CallbackQueryHandler(message_support)
    # )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
