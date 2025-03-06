from prompts import START_COMMAND_MESSAGE_TOPIC_1, START_COMMAND_MESSAGE_TOPIC_2, START_COMMAND_MESSAGE_TOPIC_3
from telegram import Update
from telegram.ext import CallbackContext
from services.database_manager import check_if_user_exist, add_user, determineUserTopic, updateUserTopic

'''
Handler function for /start command where it initiates the conversation. It sends
the introduction message and an AI-generated image of Pope Francis if the user does not
exist in the database, else it generates a basic message asking the user if he has any
questions about deepfakes.

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_start(update: Update, _: CallbackContext):
    # Obtain user information from Telegram API
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id


    # Check if the user exists in the database.
    if not check_if_user_exist(user_id):
        # User does not exist. Add the user to the database.
        add_user(user_id)
    
    # Send the introduction message depending on the current topic of the bot
    topic, = determineUserTopic(user_id)
    if topic is None or topic >= 4:
        # For reason, topic cannot be found or it is an invalid topic. Reset the topic to default topic 1.
        updateUserTopic(user_id, 1)
        topic = 1
    
    # Send the corresponding introduction messages depending on the current topic
    start_message = START_COMMAND_MESSAGE_TOPIC_1
    if topic == 2:
        start_message = START_COMMAND_MESSAGE_TOPIC_2
    elif topic == 3:
        start_message = START_COMMAND_MESSAGE_TOPIC_3    
    await update.message.reply_text(start_message.format(user_name))
