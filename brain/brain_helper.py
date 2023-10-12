import helper


logger = helper.get_logger()


def speak(agent, sentence):
    logger.info(f"Brain Say: '{sentence}'")
    agent.publish('voice.text', sentence)
