from prompts import STAGE_1_2_PROMPT, STAGE_1_2_FAKE_MESSAGE, STAGE_1_2_REAL_MESSAGE, STAGE_1_2_UNSURE_MESSAGE, STAGE_1_2_IRRELEVANT_MESSAGE, AUDIO_PRODUCTION_ERROR
from services.openai_manager import generate_text_gpt
from services.database_manager import updateUserStageAndSubstage, saveMessageToConversationHistory, determine_is_audio_enabled
from telegram import Update
from definitions.role import Role
from definitions.magic_words import MagicWords
from services.message_manager import produce_voice_message


'''
Stage properties
'''
current_stage = 1
current_substage = 2


'''
Determines how the chatbot should reply to the user's free text for Stage 1-2, which is
after the bot shows the user an AI-generated image of Pope Francis, and asks the user whether
he thinks the image is real or fake.

Parameters:
    - user_id: User id of the user
    - user_message: Free text message that the user has sent
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_stage_one_two_freetext(user_id: int, user_message: str, update: Update):
    # Generate the prompt
    prompt = STAGE_1_2_PROMPT.format(user_message)
    messages = [
        {
            "role": "developer",
            "content": prompt
        }
    ]

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
   
    # Decide on the corresponding message depending on classification
    message = ""
    if response.endswith(MagicWords.FAKE.value):
        updateUserStageAndSubstage(user_id, 1, 3)
        message = STAGE_1_2_FAKE_MESSAGE
    elif response.endswith(MagicWords.REAL.value):
        updateUserStageAndSubstage(user_id, 1, 3)
        message = STAGE_1_2_REAL_MESSAGE
    elif response.endswith(MagicWords.UNSURE.value):
        message = STAGE_1_2_UNSURE_MESSAGE
    else:
        message = STAGE_1_2_IRRELEVANT_MESSAGE

    # Output message based on whether the user has enabled audio output
    if (determine_is_audio_enabled(user_id)):
        # Case 1: Audio is enabled. We need to output audio message
        await produce_voice_message(update, message)
    else:
        # Case 2: Audio is disabled. We need to output text message.
        await update.message.reply_text(message)

    # Save the system message into the database
    saveMessageToConversationHistory(user_id, Role.SYSTEM, message, current_stage, current_substage)
