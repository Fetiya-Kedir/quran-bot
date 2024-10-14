import logging
import random
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Set up logging for debugging and monitoring
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Admin usernames
ADMINS = ["AbdurehimK55", "MisterAbboud", "Ke34m"]

# Define your FAQ responses
FAQ_RESPONSES = {
    "📝እንዴት መመዝገብ ይቻላል?": (
        "ለመመዝገብ እባክዎን ለእርዳታ አስተዳዳሪውን (Admin) ያነጋግሩ: \n"
        "Ustaz Abdurahim(https://t.me/AbdurehimK55) \n"
        "Abdurahman(https://t.me/MisterAbboud) \n"
        "Eman(https://t.me/Ke34m)"
    ),
    "📅 የክፍል መርሃ ግብር?": (
        "ትምህርቶቻችን በየሳምንቱ \nሰኞ፣\nማክሰኞ፣\nእሮብ፣\nአርብ እና\n ቅዳሜ ከምሽቱ 2:30 ይጀምራል እና ከጥዋቱ 12:30 ይጀምራል።\n"
        "የእኛ የቁርአን ትምህርት ፕሮግራማችን እነዚህን ያካትታል፣\n"
        "✨ነዘር\n"
        "✨ተጅዊድ\n"
        "✨ሒፍዝ እና\n"
        "✨ቃዒደቱ-ን-ኑራኒያ"
    ),
    "💰 ክፍያዎች?": "የእኛ የቁርዓን ትምህርት ፕሮግራማችን የክፍያ መጠን በወር 400 ብር ነው።",
    "🕒 የኮርሱ ቆይታ?": "የኮርሱ ቆይታ ለ6 ወራት ነው።",
    "📞 ለበለጠ መረጃ?": (
        "ለበለጠ መረጃ በቴሌግራም Ustaz Abdurahim: (https://t.me/AbdurehimK55) ሊያገኙን ይችላሉ።"
    )
}

# Define Hadiths
HADITHS = [
    "حديث البخاري\n: قال النبي ﷺ: خيركم من تعلم القرآن وعلمه. \nነብዩ (ሶ.ዐ.ወ) እንዲህ ብለዋል፡- 🕋ከናንተ (ሙስሊሞች) በላጩ ቁርኣንን ተምረው ያስተማሩት ናቸው።🌙(ሳሂህ አል ቡኻሪ)",
    "حديث مسلم\n: قال النبي ﷺ: اقرأوا القرآن، فإنه يأتي يوم القيامة شفيعاً لأصحابه.”\nነብዩ (ሶ.ዐ.ወ) እንዲህ አሉ፡- * 🕌ቁርኣንን አንብብ በትንሣኤ ቀን ለአነባቢዎቹ አማላጅ ሆኖ ይመጣልና*⭐ (ሶሒህ ሙስሊም)",
    " حديث الترمذي\n: قال النبي ﷺ: من قرأ حرفاً من كتاب الله فله به حسنة، والحسنة بعشر أمثالها.”\nነብዩ (ሶ.ዐ.ወ) እንዲህ ብለዋል፡- *🌃ከአላህ ኪታብ የተጻፈ ደብዳቤ ያነበበ ሰው ምንዳ ያገኛል። ምንዳውም በአስር ይጨመርለታል።*🌟 (ቲርሚዚ)"
]

last_hadith_index = -1

# Helper function to check admin status
def is_admin(username):
    return username in ADMINS

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    global last_hadith_index
    user_name = update.effective_user.first_name
    greeting = f"االسَّلامُ عَلَيْكُم ورَحْمَةُ اللهِ وَبَرَكاتُهُه\n{user_name}!"

    last_hadith_index = (last_hadith_index + 1) % len(HADITHS)
    hadith = HADITHS[last_hadith_index]

    keyboard = [
        ["📝እንዴት መመዝገብ ይቻላል?", "📅 የክፍል መርሃ ግብር?"],
        ["💰 ክፍያዎች?", "🕒 የኮርሱ ቆይታ?"],
        ["📞 ለበለጠ መረጃ?"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text(f"{greeting}\n\n{hadith}\n\nእባክዎ ከታች ካለው አማራጭ ውስጥ ጥያቄ ይምረጡ፡፡", reply_markup=reply_markup)

# FAQ handler
async def faq_handler(update: Update, context: CallbackContext) -> None:
    question = update.message.text
    logger.info(f"Received FAQ request: {question} from {update.effective_user.username}")
    response = FAQ_RESPONSES.get(question, "Sorry, I don't have an answer for that.")
    await update.message.reply_text(response)

# Feedback handler
async def feedback(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Please type your feedback, and I'll forward it to the admin.")
    context.user_data['expecting_feedback'] = True

# Handle messages (FAQs and feedback)
async def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('expecting_feedback', False):
        feedback_message = update.message.text
        for admin in ADMINS:
            await context.bot.send_message(chat_id=f"@{admin}", text=f"New feedback from {update.effective_user.username}: {feedback_message}")
        await update.message.reply_text("Thank you for your feedback!")
        context.user_data['expecting_feedback'] = False
    else:
        await faq_handler(update, context)

# Error handler
async def error(update: Update, context: CallbackContext) -> None:
    logger.error(f"Update {update} caused error {context.error}. User: {update.effective_user.username}")
    await update.message.reply_text("An error occurred. Please try again later.")

# Main function
def main() -> None:
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
