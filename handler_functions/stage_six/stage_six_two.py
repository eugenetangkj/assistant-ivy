from prompts import STAGE_6_2_PROMPT
from services.openai_manager import generate_text_gpt
from services.database_manager import saveMessageToConversationHistory, determine_is_audio_enabled
from services.message_manager import prepare_messages_array, produce_voice_message
from telegram import Update
from definitions.role import Role

'''
Stage properties
'''
current_stage = 6
current_substage = 2


'''
Determines how the chatbot should reply to the user's free text for Stage 6-2, which is about
free discussion and replying to the user's questions about deepfakes.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_six_two_freetext(user_id: int, update: Update):
    # Prepare messages array
    messages = prepare_messages_array(
        prompt=STAGE_6_2_PROMPT,
        user_id=user_id,
        lower_bound_stage=6,
        lower_bound_substage=1,
        upper_bound_stage=6,
        upper_bound_substage=2
    )

    # Perform chat completion
    response = generate_text_gpt("gpt-4o", messages)

    # Determine if audio is enabled
    is_audio_enabled = determine_is_audio_enabled(user_id)

    # Reply according to where the user is with regards to the discussion on how to spot deepfakes
    if (is_audio_enabled):
        await produce_voice_message(update, response)
    else:
        await update.message.reply_text(response)
    saveMessageToConversationHistory(user_id, Role.SYSTEM, response, current_stage, current_substage)
