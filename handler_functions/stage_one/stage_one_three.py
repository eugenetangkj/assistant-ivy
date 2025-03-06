from prompts import STAGE_1_3_PROMPT, STAGE_1_4_PROMPT, POPE_FRANCIS_AI_IMAGE_SIGNS_PATH, STAGE_1_4_PROMPT_TWO
from services.openai_manager import generate_text_gpt
from services.database_manager import updateUserStageAndSubstage, saveMessageToConversationHistory, determine_is_audio_enabled
from services.message_manager import prepare_messages_array, produce_voice_message
from telegram import Update
from definitions.role import Role
from definitions.magic_words import MagicWords


'''
Stage properties
'''
current_stage = 1
current_substage = 3


'''
Determines how the chatbot should reply to the user's free text for Stage 1-3, which is to
respond to the user's reply as to why he thinks the AI-generated image is real or fake.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_one_three_freetext(user_id: int, update: Update):
    # Prepare messages array
    messages = prepare_messages_array(
        prompt=STAGE_1_3_PROMPT,
        user_id=user_id,
        lower_bound_stage=1,
        lower_bound_substage=1,
        upper_bound_stage=1,
        upper_bound_substage=3
    )

    # Perform chat completion
    response = generate_text_gpt("gpt-4o", messages)

    # Determine if audio is enabled
    is_audio_enabled = determine_is_audio_enabled(user_id)

    # Output the corresponding message depending on whether the bot has gone through all the clues
    if response.endswith(MagicWords.COMPLETE.value) or response.endswith(MagicWords.COMPLETE.value + "."):
        # CASE 1: The user has went through all the clues that indicate the image is AI-generated
        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_1_4_PROMPT)
        else:
            await update.message.reply_text(STAGE_1_4_PROMPT)

        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_1_4_PROMPT, current_stage, current_substage + 1)
        await update.message.reply_photo(photo=POPE_FRANCIS_AI_IMAGE_SIGNS_PATH)
        updateUserStageAndSubstage(user_id, 2, 1)


        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_1_4_PROMPT_TWO)
        else:
            await update.message.reply_text(STAGE_1_4_PROMPT_TWO)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_1_4_PROMPT_TWO, 2, 1)
    
    
    else:
        # CASE 2: The user has not went through all the clues
        if (is_audio_enabled):
            # Audio is enabled
            await produce_voice_message(update, response)
        else:
            # Audio is disabled
            await update.message.reply_text(response)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, response, current_stage, current_substage)
