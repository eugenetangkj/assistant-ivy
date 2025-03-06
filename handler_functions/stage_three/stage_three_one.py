from prompts import STAGE_3_1_PROMPT, STAGE_3_2_PROMPT_TWO, STAGE_3_2_PROMPT_THREE
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
current_substage = 1


'''
Determines how the chatbot should reply to the user's free text for Stage 3-1, which is the
user's reponse to the articles that the bot shared. The chatbot should lead up to talk about
benefits and harms of deepfakes.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_three_one_freetext(user_id: int, update: Update):
    # Prepare the messages array
    messages = prepare_messages_array(
        prompt=STAGE_3_1_PROMPT,
        user_id=user_id,
        lower_bound_stage=2,
        lower_bound_substage=2,
        upper_bound_stage=3,
        upper_bound_substage=1
    )

    # Perform chat completion
    response = generate_text_gpt("gpt-4o", messages)

    # Determine if audio is enabled
    is_audio_enabled = determine_is_audio_enabled(user_id)


    if response.endswith(MagicWords.COMPLETE.value) or response.endswith(MagicWords.COMPLETE.value + "."):
        # CASE 1: User has finished talking about articles
        if (is_audio_enabled):
            # Audio is enabled
            await produce_voice_message(update, STAGE_3_2_PROMPT_TWO)
        else:
            # Audio is disabled
            await update.message.reply_text(STAGE_3_2_PROMPT_TWO)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_3_2_PROMPT_TWO, current_stage, current_substage + 1)
        updateUserStageAndSubstage(user_id, current_stage, current_substage + 1)

    elif response.endswith(MagicWords.BEYOND.value) or response.endswith(MagicWords.BEYOND.value + "."):
        # CASE 2: User tries to go onto another topic
        if (is_audio_enabled):
            # Audio is enabled
            await produce_voice_message(update, STAGE_3_2_PROMPT_THREE)
        else:
            # Audio is disabled
            await update.message.reply_text(STAGE_3_2_PROMPT_THREE)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, STAGE_3_2_PROMPT_THREE, current_stage, current_substage + 1)
        updateUserStageAndSubstage(user_id, current_stage, current_substage + 1)
    
    else:
        # CASE 3: User is still talking about the articles that are shared regarding deepfakes in Singapore
        if (is_audio_enabled):
            await produce_voice_message(update, response)
        else:
            await update.message.reply_text(response)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, response, current_stage, current_substage)

