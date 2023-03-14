from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import sqlite3

# Function for handling messages
def count_messages(update, context):
    # Connect to the database
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    message = update.message
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Add the message to the database
    if message.text is not None:
        cursor.execute('INSERT INTO messages (user_id, chat_id, message) VALUES (?, ?, ?)', (user_id, chat_id, message.text))
    elif message.photo:
        cursor.execute('INSERT INTO messages (user_id, chat_id, message) VALUES (?, ?, ?)', (user_id, chat_id, 'Photo'))
    elif message.sticker:
        cursor.execute('INSERT INTO messages (user_id, chat_id, message) VALUES (?, ?, ?)', (user_id, chat_id, 'Sticker'))
    else:
        cursor.execute('INSERT INTO messages (user_id, chat_id, message) VALUES (?, ?, ?)', (user_id, chat_id, 'Other'))
    conn.commit()

    # Close the database connection
    conn.close()

def send_stats(update, context):
    # Connect to the database
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    chat_id = update.message.chat_id

    # Count the number of messages for each participant
    cursor.execute('SELECT COUNT(*) FROM messages WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()

    # Output statistics
    count = result[0]
    context.bot.send_message(chat_id=chat_id, text=f'This chat has sent {count} messages.')

    # Close the database connection
    conn.close()


# Create a table for storing messages
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, chat_id INTEGER, message TEXT)')
conn.close()

# Create a bot and register the message handler
updater = Updater('TOKEN')

# Register the text message handler
text_handler = MessageHandler(Filters.text, count_messages)
updater.dispatcher.add_handler(text_handler)

# Register the photo and sticker message handler
media_handler = MessageHandler(Filters.photo | Filters.sticker, count_messages)
updater.dispatcher.add_handler(media_handler)

# Register the /stats command handler
updater.dispatcher.add_handler(CommandHandler('stats', send_stats))

# Start the bot
updater.start_polling()
updater.idle()
