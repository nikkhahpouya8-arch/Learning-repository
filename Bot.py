from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
from Test_Database import add_user_info, add_user_age, add_user_city, get_user_info
import logging
from decouple import config
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = config("BOT_TOKEN")


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
        ],
        [
            KeyboardButton(
                "دریافت اطلاعات"
            )
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    username = update.effective_user.username
    id = update.effective_user.id

    add_user_info(id, username)
    print("User info added to the database!")

    await update.message.reply_html(text=f"سلام {user.mention_html(name=user.username)}! خوش اومدی.")

    await update.message.reply_text("با کلیک کردن گزینه های زیر میتونید به پشتیبان پیام بدید و یا اطلاعات خودتون رو تکمیل کنید.", reply_markup=start_menu())


async def show_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    id = update.effective_user.id

    user_info = get_user_info(id)

    message = (
        "پروفایل شما حاوی اطلاعات زیر است:\n"
        f"نام کاربری: {user_info['username']}\n"
        f"آیدی عددی: {user_info['telegram_id']}\n"
        f"سن شما: {user_info['age']}\n"
        f"شهر شما: {user_info['city']}\n"
    )

    await update.message.reply_text(message)


async def get_user_city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print(4)
    await update.callback_query.message.reply_text("لطفا اسم شهر خود را به فارسی تایپ کنید:")
    print(5)


async def user_city_helper(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = update.message.text
    id = update.effective_user.id

    add_user_city(id, city)

    print("User city added!")

    await update.message.reply_text(f"شهر شما ({city}) با موفقیت ثبت شد!")


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


async def get_age_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    ages = [(10, 20), (20, 30), (30, 40)]

    keyboard = []

    for start, end in ages:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=str(f'{start},{end}'),
                    callback_data=f"age_range:{start}:{end}"
                )
            ]
        )

    print(1)
    print(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(rf"بازه سن خود را انتخاب کنید", reply_markup=reply_markup)


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = update.callback_query.data

    print(data)

    age_range = data.split(":")

    start = int(age_range[1])

    end = int(age_range[2]) + 1

    keyboard = []

    for age in range(start, end):

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=str(f'{age}'),
                    callback_data=f'exact_age:{age}'
                )
            ]
        )

        if age != end:
            age += 1
            continue
        elif age == end:
            break

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(rf"سن دقیق خود را انتخاب کنید:", reply_markup=reply_markup)


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
        await get_age_range(update, context)

    elif Data.startswith("age_range"):
        await get_age(update, context)

    elif Data.startswith("exact_age"):
        id = update.effective_user.id
        Data_split = Data.split(":")
        age = Data_split[1]

        add_user_age(id, age)
        print("User age added!")
        await update.callback_query.message.reply_text(f"سن شما {age} سال میباشد")


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

    application.add_handler(
        MessageHandler(filters.Text("دریافت اطلاعات"), show_user_info)
    )

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, user_city_helper))

    application.add_handler(
        CallbackQueryHandler(handler_helper)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
