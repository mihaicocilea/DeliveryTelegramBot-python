from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler
import logging
import asyncio

# BOT_TOKEN
TOKEN = '#'
DESTINATION_GROUP_ID = -709787337 

# Add the source group IDs to this dictionary
# The key is the source group ID, and the value is the destination chat_id where the confirmation message should be sent
SOURCE_GROUP_IDS = [-1002008044260, -1002108602197, -1002068674092, -1001961189618, -1002040809442, -1002023712455, -1001994427922, -1002039407309, -1002099617559, -1001999113266, -1001991247714, -1002068405465]

# # - TOKEN BOT ORIGINAL

# -1002008044260 - pizzaDe10
# -1002108602197 - shaorma spot
# -1002068674092 - maniax
# - -1001961189618 - WOK & NOODLES

# -1002040809442 - All Time
# -1002023712455 - Daily
# -1001994427922 - Gurmand
# -1002039407309 - Holo's
# -1002099617559 - Angels
# -1001999113266 - Captain Jack
# -1001991247714 - Passage
# -1002068405465 - Rossa

# -709787337 - grup COMENZI

# -1002010136456 - grup comenzi TEST
# -1002129567820 - grup restaurant TEST


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    update.message.reply_text('Nu mai spama comanda, nu face nimic! 🙃')

async def forward_message(update, context):

    try:
        if update.message.chat_id in SOURCE_GROUP_IDS:
            special_chars = r"./!;:-,'"
            translator = str.maketrans('', '', special_chars)
            
            # Obține informații despre chat-ul sursă
            source_chat_info = await context.bot.get_chat(update.message.chat_id)

           # Construiește textul mesajului cu numele grupului
            source_chat_name = source_chat_info.title.translate(translator)

            # Textul pentru noul caption
            new_caption = f"*{source_chat_name}* a trimis o comandă"

            # Obține caption-ul original al mesajului
            original_caption = update.message.caption
            
             # Combinația dintre noul și vechiul caption (dacă există)
            if original_caption:
                clean_caption = original_caption.translate(translator)
                new_caption += f"\n\n*TIMP PRELUARE*: {clean_caption} minute"

            forwarded_message = await context.bot.copy_message(
                chat_id=DESTINATION_GROUP_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                caption=new_caption,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("OK 👌🏻", callback_data='ok')]]),
                parse_mode='MarkdownV2'
            )
            

    except Exception as e:
        logging.error(f"An error occurred while forwarding the message: {e}")

async def confirm_message(update, context):
    query = update.callback_query
    user = query.from_user

    try:
        await query.answer()
        
        # Textul pentru caption-ul original
        original_caption = query.message.caption

        edit_text = f"\n\n*COMANDA A FOST PRELUATA* de {user.mention_markdown()}"
        new_caption = f"{original_caption}{edit_text}"

        await context.bot.edit_message_caption(
            caption=new_caption,
            parse_mode='MarkdownV2',
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )

    except Exception as e:
        logging.error(f"An error occurred while confirming the message: {e}")

def main():
    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, forward_message))
    application.add_handler(CallbackQueryHandler(confirm_message))

    # Run bot
    application.run_polling()

if __name__ == '__main__':
    main()
