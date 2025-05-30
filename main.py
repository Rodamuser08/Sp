import time
from telebot import TeleBot, types
from reg import reg
from hit_sender import send  
from sp import sh
import asyncio

# Load the bot token
with open('token.txt', 'r') as token_file:
    token = token_file.read().strip()

bot = TeleBot(token, parse_mode="HTML") 

s1p = ["Status: Charged",] 
s2p = ["Status: Approved"] 
s3p = ["Status: Declined"] 

@bot.message_handler(commands=['sp'])
def check_card(message):
    try:
        cc = message.text.split('/sp', 1)[1].strip()
        user_id = message.from_user.id
        username = message.from_user.username or "NoUsername"

        msg = bot.reply_to(message, "Checking your card...")
        msg_id = msg.message_id  
        start_time = time.time()

        # Validate card format
        cc = reg(cc)
        if not cc:
            bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text="Invalid card format. Please use the correct format: `cc|mm|yy|cvv`",
                parse_mode="Markdown"
            )
            return


        result = asyncio.run(sh(cc))
        print(f"SP Response: {result}")  # Debugging Log

        if any(k in result for k in s1p):
            key = "Shopify Hit £1.00 🔥"
        elif any(k in result for k in s2p):
            key = "Shopify Approved ✅"
        elif any(k in result for k in s3p):
            key = "Shopify Declined. 🚫"
        else:
            key = f"Unknown Response"

        time_taken = round(time.time() - start_time, 2)

        send_response = send(cc, key, username, time_taken)

        print(send_response)

        
        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_id,
                text=send_response,
                parse_mode="HTML" 
            )
        except Exception as e:
            print(f"Error editing message: {e}")
            print(f"Problematic Response: {send_response}")
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_id,
                text="An error occurred while processing your request. Please try again later."
            )

    except Exception as e:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text="An error occurred while processing your request."
        )
        print(f"Error: {e}")

# Start the bot
print("Started")
bot.infinity_polling(timeout=25, long_polling_timeout=5)
