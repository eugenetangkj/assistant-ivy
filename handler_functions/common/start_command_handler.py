from prompts import START_COMMAND_MESSAGE, POPE_FRANCIS_AI_IMAGE_PATH, START_COMMAND_ALTERNATIVE_MESSAGE
from telegram import Update
from telegram.ext import CallbackContext
from services.database_manager import check_if_user_exist, add_user, saveMessageToConversationHistory
from definitions.role import Role


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

    if check_if_user_exist(user_id):
        # Case 1: User already exist
        await update.message.reply_text(START_COMMAND_ALTERNATIVE_MESSAGE.format(user_name))
    else:
        # Case 2: User does not exist

        # Add the user to the database
        add_user(user_id)

        # Send introduction message
        introduction_message = START_COMMAND_MESSAGE.format(user_name)
        await update.message.reply_text(introduction_message)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, introduction_message, 1, 1)

        # Send the Pope Francis AI-generated image
        await update.message.reply_photo(photo=POPE_FRANCIS_AI_IMAGE_PATH)