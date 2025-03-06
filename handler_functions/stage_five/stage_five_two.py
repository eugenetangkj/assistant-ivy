from prompts import STAGE_5_2_PROMPT, STAGE_6_1_PROMPT_ONE, STAGE_6_1_PROMPT_TWO, STAGE_6_1_PROMPT_THREE
from services.openai_manager import generate_text_gpt
from services.database_manager import updateUserStageAndSubstage, saveMessageToConversationHistory, determine_is_audio_enabled
from services.message_manager import prepare_messages_array, produce_voice_message
from telegram import Update
from definitions.role import Role
from definitions.magic_words import MagicWords

'''
Stage properties
'''
current_stage = 5
current_substage = 2


'''
Determines how the chatbot should reply to the user's free text for Stage 5-2, which is about
discussing the Online Criminal Harms Act.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_five_two_freetext(user_id: int, update: Update):
    # Prepare messages array
    messages = prepare_messages_array(
        prompt=STAGE_5_2_PROMPT,
        user_id=user_id,
        lower_bound_stage=5,
        lower_bound_substage=2,
        upper_bound_stage=5,
        upper_bound_substage=2
    )

    # Perform chat completion
    response = generate_text_gpt("gpt-4o", messages)

    # Determine if audio is enabled
    is_audio_enabled = determine_is_audio_enabled(user_id)

 
    # Reply according to where the user is with regards to the discussion on how to spot deepfakes
    if response.endswith(MagicWords.COMPLETE.value) or response.endswith(MagicWords.COMPLETE.value + "."):
        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_6_1_PROMPT_ONE)
        else:
            await update.message.reply_text(STAGE_6_1_PROMPT_ONE)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_6_1_PROMPT_ONE, current_stage + 1, 1)

        await update.message.reply_text(STAGE_6_1_PROMPT_TWO, parse_mode="markdown")
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_6_1_PROMPT_TWO, current_stage + 1, 1)


        if (is_audio_enabled):
            await produce_voice_message(update, STAGE_6_1_PROMPT_THREE)
        else:
            await update.message.reply_text(STAGE_6_1_PROMPT_THREE)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_6_1_PROMPT_THREE, current_stage + 1, 1)

        updateUserStageAndSubstage(user_id, current_stage + 1, 2)
    else:
        if (is_audio_enabled):
            await produce_voice_message(update, response)
        else:
            await update.message.reply_text(response)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, response, current_stage, current_substage)
