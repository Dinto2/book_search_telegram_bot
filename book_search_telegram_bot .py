# Import dependencies
import logging
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Each row is made up of ["Author(Year):Title", "Link"]. Just two columns: 'NAME' and 'LINK'
table = pd.read_csv('your_books_table.csv') 

def register_order(txt, name, user, date, bot, msjID):
  with open('regs.txt', 'a') as f:
    f.write(f"{name},@{user},{txt},{date},{msjID}, {bot}\n")

def explore(pattern):
  searching = pattern.split(' ')
  results = table[table.NAME.str.lower().apply(lambda sentence: all(word.lower() in sentence for word in searching))]
  return results.values.tolist()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is the presentation. What bot does")
async def TG_COMMAND(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="A response from the other commands")
async def TG_COMMAND_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="A response from the other commands")

# This is the function that interests us
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Who we will send the response
    sender_id = update.effective_chat.id 
    # Text that our sender is looking for
    looking_for = update.message.text 
    # Clean any mistake
    text = looking_for.replace('\n',' ').lstrip().rstrip() 
    message_extension = len(text)
    
    # We consider here a "valid length" between 3-36 characters.
    if message_extension in range(3,36): 
      sender_name = update.message.chat.first_name
      chat_id = update.message.chat.id
      chat_user = update.message.chat.username
      message_date = update.message.date
      if_is_bot = update.message.from_user.is_bot
      message_id = update.message.message_id
      # Records in a text file the orders made to the bot
      register_order(text, sender_name, chat_id, chat_user, message_date, if_is_bot, message_id)
      # Now we will search through the df with books
      searching = explore(text)
      # Now, it depends how many results we have. If we have one or more, or if we don't have anyone
      if len(searching) > 0:
        for i in searching[:5]:
          # Without preview image, the chat might be a little messy if you have many results and their images
          await context.bot.send_message(text=i[0]+'\n'+i[1], chat_id=sender_id, disable_web_page_preview=True)
      else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="At least write well, are you sleepy?")
        
    # A response if this is less than 3 characters    
    elif message_extension <= 3: 
      await context.bot.send_message(text="Write more! Are you sleeping?", chat_id=update.effective_chat.id)
    # A response if this is more than 36 characters
    else: 
      await context.bot.send_message(text="Why do you talk so much? So annoying!", chat_id=update.effective_chat.id)

if __name__ == '__main__':
    application = ApplicationBuilder().token('YOUR_TOKEN').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    TG_COMMAND_handler = CommandHandler('TG_COMMAND', TG_COMMAND) # Another command configurable with BotFather
    application.add_handler(TG_COMMAND_handler)

    TG_COMMAND_2_handler = CommandHandler('TG_COMMAND2', TG_COMMAND2) # Another command configurable with BotFather
    application.add_handler(TG_COMMAND_2_handler)
    
    # No-command text. Bot will use this unknown text to search books
    unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
