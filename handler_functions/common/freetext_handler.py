from prompts import REQUEST_TO_DELETE_MESSAGE
from telegram import Update
from telegram.ext import CallbackContext
from handler_functions.stage_one.stage_one_two import handle_stage_one_two_freetext
from handler_functions.stage_one.stage_one_three import handle_stage_one_three_freetext
from handler_functions.stage_two.stage_two_one import handle_stage_two_one_freetext
from handler_functions.stage_three.stage_three_one import handle_stage_three_one_freetext
from handler_functions.stage_three.stage_three_two import handle_stage_three_two_freetext
from handler_functions.stage_four.stage_four_two import handle_stage_four_two_freetext
from handler_functions.stage_four.stage_four_three import handle_stage_four_three_freetext
from handler_functions.stage_five.stage_five_one import handle_stage_five_one_freetext
from handler_functions.stage_five.stage_five_two import handle_stage_five_two_freetext
from handler_functions.stage_six.stage_six_two import handle_stage_six_two_freetext
from services.database_manager import determineUserStageAndSubstage, saveMessageToConversationHistory
from definitions.role import Role


'''
Handler function for free text messages that the user sends. It determines which stage
the user is in to determine how to respond to the user.

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_free_text(update: Update, _: CallbackContext):
    # Obtain user information from Telegram API
    user_id = update.effective_user.id
    user_message = update.message.text

    # Process user message
    await reply_to_user_message(update, user_id, user_message)


'''
Determines how the bot will reply depending on the current stage that the user is in. Common
function to be called for both voice message and free text handlers.

Parameters:
    - update: Update frame from Telegram
    - user_message: User message that the bot needs to reply to
    - user_id: ID of the user
'''
async def reply_to_user_message(update: Update, user_id: int, user_message: str):
    # Step 1: Determine the current stage and substage that the user is in
    current_stage, current_substage = determineUserStageAndSubstage(user_id)
    

    # Step 2: Handle case where user is not actually registered in the database yet
    if (current_stage is None or current_substage is None):
        #TODO: Consider if need save to conversation history
        await update.message.reply_text(REQUEST_TO_DELETE_MESSAGE)
        return
    

    # Step 3: Save the user's current message into the conversation history table
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_stage, current_substage)

    
    # Step 4: Use logic customised to the current stage and substage that the user is in
    if (current_stage == 1 and current_substage == 2):
        await handle_stage_one_two_freetext(user_id, user_message, update)
    elif (current_stage == 1 and current_substage == 3):
        await handle_stage_one_three_freetext(user_id, update)
    elif (current_stage == 2 and current_substage == 1):
        await handle_stage_two_one_freetext(user_id, update)
    elif (current_stage == 3 and current_substage == 1):
        await handle_stage_three_one_freetext(user_id, update)
    elif (current_stage == 3 and current_substage == 2):
        await handle_stage_three_two_freetext(user_id, update)
    elif (current_stage == 4 and current_substage == 2):
        await handle_stage_four_two_freetext(user_id, update)
    elif (current_stage == 4 and current_substage == 3):
        await handle_stage_four_three_freetext(user_id, update)
    elif (current_stage == 5 and current_substage == 1):
        await handle_stage_five_one_freetext(user_id, update)
    elif (current_stage == 5 and current_substage == 2):
        await handle_stage_five_two_freetext(user_id, update)
    elif (current_stage == 6 and current_substage == 2):
        await handle_stage_six_two_freetext(user_id, update)
    else:
        await update.message.reply_text("We are still constructing this part of the conversational flow.")