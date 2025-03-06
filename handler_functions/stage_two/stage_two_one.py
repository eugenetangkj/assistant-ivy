from prompts import STAGE_2_1_PROMPT, STAGE_2_2_PROMPT, STAGE_2_2_PROMPT_TWO, STAGE_2_2_PROMPT_THREE, STAGE_2_2_PROMPT_FOUR
from services.openai_manager import generate_text_gpt
from services.database_manager import updateUserStageAndSubstage, saveMessageToConversationHistory, determine_is_audio_enabled
from services.message_manager import prepare_messages_array, produce_voice_message
from telegram import Update
from definitions.role import Role
from definitions.magic_words import MagicWords


'''
Stage properties
'''
current_stage = 2
current_substage = 1


'''
Determines how the chatbot should reply to the user's free text for Stage 2-1, which is to
respond to the user's reply as to whether he has heard of what is a deepfake before.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_two_one_freetext(user_id: int, update: Update):
    # Prepare messages array
    messages = prepare_messages_array(
        prompt=STAGE_2_1_PROMPT,
        user_id=user_id,
        lower_bound_stage=2,
        lower_bound_substage=1,
        upper_bound_stage=2,
        upper_bound_substage=1
    )

    # Perform chat completion
    response = generate_text_gpt("gpt-4o", messages)

    # Determine if audio is enabled
    is_audio_enabled = determine_is_audio_enabled(user_id)


    # Output the corresponding message depending on where the user is with regards to discussing what a deepfake is
    if response.endswith(MagicWords.COMPLETE.value) or response.endswith(MagicWords.COMPLETE.value + "."):
        # CASE 1: The user has finished talking about what a deepfake is. Send transition messages.
        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_2_2_PROMPT)
            await produce_voice_message(update, STAGE_2_2_PROMPT_TWO)
        else:
            await update.message.reply_text(STAGE_2_2_PROMPT)
            await update.message.reply_text(STAGE_2_2_PROMPT_TWO)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_2_2_PROMPT, current_stage, current_substage + 1)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_2_2_PROMPT_TWO, current_stage, current_substage + 1)

        # Send links
        await update.message.reply_text(STAGE_2_2_PROMPT_FOUR, parse_mode="markdown")
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_2_2_PROMPT_FOUR, current_stage, current_substage + 1)

        # Update the user's stage
        updateUserStageAndSubstage(user_id, current_stage + 1, 1)

    elif response.endswith(MagicWords.BEYOND.value) or response.endswith(MagicWords.BEYOND.value + "."):
        # CASE 2: The user tried to ask something beyond what a deepfake is. Send transition messages.
        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_2_2_PROMPT_THREE)
        else:
            await update.message.reply_text(STAGE_2_2_PROMPT_THREE) 
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_2_2_PROMPT_THREE, current_stage, current_substage + 1)

        # Send links
        await update.message.reply_text(STAGE_2_2_PROMPT_FOUR, parse_mode="markdown")
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_2_2_PROMPT_FOUR, current_stage, current_substage + 1)

        # Update the user's stage
        updateUserStageAndSubstage(user_id, current_stage + 1, 1)

    else:
        # CASE 3: The user has not finished discussing about it
        if (is_audio_enabled):
            await produce_voice_message(update, response)
        else:
            await update.message.reply_text(response)

        saveMessageToConversationHistory(user_id, Role.SYSTEM, response, current_stage, current_substage)

