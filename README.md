# telegramstatbot
This Python code uses the telegram.ext library to create a Telegram bot that can count and report the number of messages sent in a chat.

The code connects to a SQLite database called "messages.db" using the sqlite3 module. The count_messages() function is a message handler that adds the message content, user ID, and chat ID to the database. If the message contains text, the message text is stored in the database. If the message contains a photo, the string "Photo" is stored. If the message contains a sticker, the string "Sticker" is stored. Otherwise, the string "Other" is stored.

The send_stats() function is a command handler that retrieves the number of messages sent in the chat from the database and sends the count as a message to the chat.

The code creates a table in the SQLite database to store the messages. Then it creates a Telegram bot using the Updater() class and passes a Telegram API token to it. It registers the count_messages() function to handle text messages, photos, and stickers. It registers the send_stats() function to handle the "/stats" command. Finally, it starts the bot and enters a loop to continuously listen for incoming messages.

Unfortunately this code only processes messages sent personally to the bot if you have ideas how to fix it I would be happy to see them.
