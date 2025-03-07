from prompts.topic_2_prompts import TOPIC_2_STAGE_1_PROMPT
from services.openai_manager import generate_text_gpt
from telegram import Update
from services.message_manager import prepare_messages_array, produce_text_or_voice_message


'''
Properties
'''
current_topic = 2
current_stage = 1


'''
Determines how the chatbot should reply to the user in topic 2 stage 1, which is about replying to
the user's questions on how to spot a deepfake.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_topic_two_stage_one(user_id: int, update: Update):
    # Fetch only messages in the current topic and stage
    messages = prepare_messages_array(
        prompt=TOPIC_2_STAGE_1_PROMPT,
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )


    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response
   

    # Output text or voice message
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)
