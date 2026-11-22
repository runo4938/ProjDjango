import telebot
import andro_cfw

# 1-Line Auto-Patcher: Routes 100% of Telegram API calls through Cloudflare Worker
session = andro_cfw.patch()

bot = telebot.TeleBot("9255717121:AAFWTJgx4MYW686FbeWnwf8rj26Ih-Xjw8Q")

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "🤖 **Hello from behind the filter!**\n\n"
        f"🌐 **Worker URL**: `{session.worker_url}`\n"
        "🔒 **Status**: Unfiltered & Running Smoothly!"
    )

if __name__ == "__main__":
    print(f"🚀 Bot starting behind Cloudflare Worker ({session.worker_url})...")
    bot.infinity_polling(timeout=20, long_polling_timeout=20)