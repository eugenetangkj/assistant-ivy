'''
PERSONA PROMPTS
'''
# Persona that is repeated across prompts
PERSONA_PROMPT =  (
'''
Your name is Ivy. You are an informational assistant that answers questions about deepfakes to a senior. Your
goal is to provide correct explanations that answer the questions that are being asked by the senior. You should
aim to give clear answers that directly answer the questions.
'''
)


'''
START command messages
'''
# Start message for topic 1
START_COMMAND_MESSAGE_TOPIC_1 = (
    "Hi {}. I am Assistant Ivy. I am here to answer your questions about how deepfakes are created. Please feel free to ask me any questions. 😊"
)

# Start message for topic 2
START_COMMAND_MESSAGE_TOPIC_2 = (
    "Hi {}. I am Assistant Ivy. I am here to answer your questions about how to spot deepfakes. Please feel free to ask me any questions. 😊"
)

# Start message for topic 3
START_COMMAND_MESSAGE_TOPIC_3 = (
    "Hi {}. I am Assistant Ivy. I am here to answer your questions about the benefits and harms of deepfakes. Please feel free to ask me any questions. 😊"
)


'''
DELETE command messages
'''
# Delete command message that informs the user that the user data has been deleted from the database
DELETE_COMMAND_MESSAGE = (
    "User data and all associated conversation history have been successfully deleted."
)



'''
AUDIO AND MULTIMEDIA PROMPTS
'''
# Audio production error
AUDIO_PRODUCTION_ERROR = "Sorry, I am not able to produce voice messages at this moment."

# Voice message too large error, occurs when user tries to submit a voice message input that is too large
VOICE_MESSAGE_TOO_LARGE_ERROR = "Sorry, the voice message file is too large. Can you try with a smaller voice message file?"

# Cannot convert voice message from OGG to MP3 format
VOICE_MESSAGE_FORMAT_CONVERSION_ERROR = "Sorry, the voice message cannot be converted. Can you try again?"
VOICE_MESSAGE_TRANSCRIPTION_ERROR = "Sorry, I could not understand what you have said. Can you try again?"

# Multimedia not supported message
MULTIMEDIA_NOT_SUPPORTED_MESSAGE = "Sorry, I can only accept text and voice messages at the moment."

# Messages for toggling audio mode
AUDIO_MODE_ENABLED_MESSAGE = "Audio mode is enabled. I will now reply using voice messages."
AUDIO_MODE_DISABLED_MESSAGE = "Audio mode is disabled. I will now reply with text messages."
CREATE_USER_FOR_AUDIO_MODE = "Please run `/start` before toggling the audio mode."


'''
OTHER MESSAGES
'''
# Prompt if user enters free text but cannot find the user's data in the database
REQUEST_TO_DELETE_MESSAGE = (
    "Sorry, something went wrong. Please type /start to begin again."
)
