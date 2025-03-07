from prompts.common_prompts import PERSONA_PROMPT

'''
TOPIC 1 STAGE 1:
Assistant answers the questions that the user has about how are deepfakes created.

'''
TOPIC_1_STAGE_1_CONSTRAINTS_PROMPT = (
'''
You must only discuss about the topic of how deepfakes are created. Do not discuss any other topics.
If the senior discusses about any other topics, reply that you are not able to discuss about it and inform
him to ask questions about how deepfakes are created instead.
'''
)

TOPIC_1_STAGE_1_GOAL_PROMPT = (
'''
Your goal is to explain to the senior on how deepfakes are created.
'''
)


TOPIC_1_STAGE_1_PROMPT = PERSONA_PROMPT + "\n" + TOPIC_1_STAGE_1_GOAL_PROMPT + "\n" + TOPIC_1_STAGE_1_CONSTRAINTS_PROMPT