from prompts import STAGE_4_2_PROMPT, STAGE_4_3_PROMPT_TWO, STAGE_4_3_PROMPT_THREE, STAGE_4_3_PROMPT_FOUR, STAGE_4_3_PROMPT_FIVE, SCAMSHIELD_POSTER_PATH
from services.openai_manager import generate_text_gpt
from services.database_manager import updateUserStageAndSubstage, saveMessageToConversationHistory, determine_is_audio_enabled
from services.message_manager import prepare_messages_array, produce_voice_message
from telegram import Update
from definitions.role import Role
from definitions.magic_words import MagicWords

'''
Stage properties
'''
current_stage = 4
current_substage = 2


'''
Determines how the chatbot should reply to the user's free text for Stage 4-2, which is about
discussing how to spot deepfakes.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_four_two_freetext(user_id: int, update: Update):
    # Prepare messages array
    messages = prepare_messages_array(
        prompt=STAGE_4_2_PROMPT,
        user_id=user_id,
        lower_bound_stage=4,
        lower_bound_substage=1,
        upper_bound_stage=4,
        upper_bound_substage=2
    )

    # Perform chat completion
    response = generate_text_gpt("gpt-4o", messages)

    # Determine if audio is enabled
    is_audio_enabled = determine_is_audio_enabled(user_id)


    # Reply according to where the user is with regards to the discussion on how to spot deepfakes
    if response.endswith(MagicWords.COMPLETE.value) or response.endswith(MagicWords.COMPLETE.value + "."):
        await update.message.reply_text(STAGE_4_3_PROMPT_TWO, parse_mode="markdown")
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_3_PROMPT_TWO, current_stage, current_substage + 1)

        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_4_3_PROMPT_THREE) 
            await produce_voice_message(update, STAGE_4_3_PROMPT_FOUR) 
        else:
            await update.message.reply_text(STAGE_4_3_PROMPT_THREE, parse_mode="markdown")
            await update.message.reply_text(STAGE_4_3_PROMPT_FOUR)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_3_PROMPT_THREE, current_stage, current_substage + 1)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_3_PROMPT_FOUR, current_stage, current_substage + 1)

        await update.message.reply_photo(photo=SCAMSHIELD_POSTER_PATH)
        updateUserStageAndSubstage(user_id, current_stage, current_substage + 1)

    elif response.endswith(MagicWords.BEYOND.value) or response.endswith(MagicWords.BEYOND.value + "."):
        await update.message.reply_text(STAGE_4_3_PROMPT_FIVE, parse_mode="markdown")
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_3_PROMPT_FIVE, current_stage, current_substage + 1)

        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_4_3_PROMPT_THREE) 
            await produce_voice_message(update, STAGE_4_3_PROMPT_FOUR) 
        else:
            await update.message.reply_text(STAGE_4_3_PROMPT_THREE, parse_mode="markdown")
            await update.message.reply_text(STAGE_4_3_PROMPT_FOUR)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_3_PROMPT_THREE, current_stage, current_substage + 1)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_3_PROMPT_FOUR, current_stage, current_substage + 1)

        await update.message.reply_photo(photo=SCAMSHIELD_POSTER_PATH)
        updateUserStageAndSubstage(user_id, current_stage, current_substage + 1)

    else:
        if (is_audio_enabled):
            await produce_voice_message(update, response)
        else:
            await update.message.reply_text(response)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, response, current_stage, current_substage)
