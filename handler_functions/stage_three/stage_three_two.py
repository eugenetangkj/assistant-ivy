from prompts import STAGE_3_2_PROMPT, STAGE_4_1_PROMPT, STAGE_4_1_PROMPT_TWO, STAGE_4_1_PROMPT_THREE, STAGE_4_1_PROMPT_FOUR
from services.openai_manager import generate_text_gpt
from services.database_manager import updateUserStageAndSubstage, saveMessageToConversationHistory, determine_is_audio_enabled
from services.message_manager import prepare_messages_array, produce_voice_message
from telegram import Update
from definitions.role import Role
from definitions.magic_words import MagicWords

'''
Stage properties
'''
current_stage = 3
current_substage = 2


'''
Determines how the chatbot should reply to the user's free text for Stage 3-2, which is about
discussing the benefits of deepfakes.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_three_two_freetext(user_id: int, update: Update):
    # Prepare messages array
    messages = prepare_messages_array(
        prompt=STAGE_3_2_PROMPT,
        user_id=user_id,
        lower_bound_stage=3,
        lower_bound_substage=1,
        upper_bound_stage=3,
        upper_bound_substage=2
    )

    # Perform chat completion
    response = generate_text_gpt("gpt-4o", messages)

    # Determine if audio is enabled
    is_audio_enabled = determine_is_audio_enabled(user_id)


    # Reply according to where the user is with regards to the discussion on the benefits of deepfakes
    if response.endswith(MagicWords.COMPLETE.value) or response.endswith(MagicWords.COMPLETE.value + "."):
        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_4_1_PROMPT)
            await produce_voice_message(update, STAGE_4_1_PROMPT_TWO)
        else:
            await update.message.reply_text(STAGE_4_1_PROMPT)
            await update.message.reply_text(STAGE_4_1_PROMPT_TWO)

        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_1_PROMPT, current_stage + 1, 1)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_1_PROMPT_TWO, current_stage + 1, 1)

        await update.message.reply_text(STAGE_4_1_PROMPT_THREE)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_1_PROMPT_THREE, current_stage + 1, 1)

        updateUserStageAndSubstage(user_id, current_stage + 1, 2)

    elif response.endswith(MagicWords.BEYOND.value) or response.endswith(MagicWords.BEYOND.value + "."):
        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_4_1_PROMPT_FOUR)
            await produce_voice_message(update, STAGE_4_1_PROMPT_TWO)
        else:
            await update.message.reply_text(STAGE_4_1_PROMPT_FOUR)
            await update.message.reply_text(STAGE_4_1_PROMPT_TWO)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_1_PROMPT_FOUR, current_stage + 1, 1)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_1_PROMPT_TWO, current_stage + 1, 1)

        await update.message.reply_text(STAGE_4_1_PROMPT_THREE)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_4_1_PROMPT_THREE, current_stage + 1, 1)

        updateUserStageAndSubstage(user_id, current_stage + 1, 2)

    else:
        if (is_audio_enabled):
            await produce_voice_message(update, response)
        else:
            await update.message.reply_text(response)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, response, current_stage, current_substage)

