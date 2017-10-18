"""
Simple Python Lambda service for a basic "fact" skill.
Intents supported:
  Custom:
    ScienceCategory
    TechnologyCategory
    EngineeringCategory
    MathCategory
    UnhandledIntent (associated with random gibberish utterances)
  Default/ Required:
    LaunchRequest (a request that calls the launch() function)
    AMAZON.HelpIntent (intent that calls the help() function)
    AMAZON.CancelIntent or AMAZON.StopIntent (both intents call the end() function)

To add an intent: 
1) First add it to the Alexa Skill Builder. 
2) Then add a function within this lambda with the exact same name (including capitalization). 
3) Customize the return statement for that function so that Alexa will respond the way you want when
   a user invokes the intent. 
* Note: it's the same concept to update or delete intents. Just make sure that there is a function 
in this lambda for each intent in the Skill Builder.  
Skill Builder match the function names 
"""

import sys
import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# **************************** CUSTOMIZE BELOW *************************************************

# --------------- Functions that implement your custom intents ------------------

def EngineeringCategory():
    return "<speak>Hedy Lamar was a well-known actress in the 40's, but also a pioneer in the "+\
        "field of wireless communications. She helped develop a radio guidance system for torpedoes "+\
        "during World War II that used spread spectrum and frequency hopping technology with the "+\
        "goal of preventing the Nazis from jamming the signals. Her work is now a major component " +\
        "of modern Wi-Fi and Bluetooth technology. </speak>"

def MathCategory():
    return "<speak>Katherine Johnson was one of the brilliant NASA engineers depicted in the 2016 film "+\
        "Hidden Figures. She worked at Langley from 1953 to 1986, making critical technical "+\
        "contributions which included calculating the trajectory of the 1961 flight of Alan Shepard, "+\
        "the first American in space. She is also credited with verifying the calculations "+\
        "for John Glenn’s launch to orbit and the Apollo 11 trajectory to the moon. In 2015 " +\
        "she received the nation's highest civilian award - the Presidential Medal of Freedom.</speak>" 

def ScienceCategory():
    return "<speak>Gertrude Belle Elion is responsible for many lifesaving drugs, including "+\
    "the first major drug used to fight leukemia. Her career as a chemist was inspired by the "+\
    "death of her grandfather from cancer. She vowed to find its cure and in her quest "+\
    "to do so developed 45 treatments that help the immune system overcome cancer, organ transplant "+\
    "and Herpes. She won the Nobel Prize for Medicine in 1988.</speak>"

def TechnologyCategory():
    return "<speak>For the fifth consecutive year, Facebook COO Sheryl Sandberg has been named " +\
    "the most powerful woman in technology on the Forbes’ 100 Most Powerful Women list. Her book, " +\
    "Lean In, encouraged women to step up and lead in the workplace has sold more than one million " +\
    "copies and was on top of the bestseller lists since its launch.</speak>"
    
def UnhandledIntent():
    return "<speak>I do not understand. You can say any any of the following categories: " +\
        "Science, Technology, Engineering or Math. </speak>"


# --------------- Functions that implement default intents (only change between the <speak> tags)-------

def launch():
    #Called when the user launches the skill without specifying what they want
    return "<speak>Welcome to the Inspirational Women Skill, where you can learn about the " +\
        "contributions of inspirational women throughout history. To start, you can say any" +\
        "of the following categories: Science, Technology, Engineering or Math.</speak>"

def help():
    # Called when the user asks for help
    return "<speak>This skill provides information about inspirational women. You can ask about" +\
        "any of the following categories: Science, Technology, Engineering, or Math. </speak>"

def end():
    # Called when the user says Stop or Cancel 
    return "<speak> Girl Power! </speak>"


# ***************************** CUSTOMIZE ABOVE **************************************************

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):

    card_output = re.sub('<[^>]*>', '', output)
    
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': card_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    session_attributes = {} # No session attributes needed for simple fact response
    reprompt_text = None # No reprompt text set
    should_end_session = True # Can end session after fact is returned (no additional dialogue)

    if intent_name == 'launch':
        should_end_session = False # Opening a skill requires the session remain open
    elif intent_name == "AMAZON.HelpIntent":
        should_end_session = False # Asking for help requires the session remain open
        intent_name = 'help'
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        intent_name = 'end'
    else: 
        intent_name = intent_name
   
    speech_output = getattr(sys.modules[__name__],intent_name)()

    return build_response(session_attributes, build_speechlet_response
                          (intent_name,speech_output,reprompt_text,should_end_session))

# --------------- Main handler ------------------

def handler(event, context):
    logger.info("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    TODO: Uncomment the if statement below and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # Defines an intent_name of "launch" if a LaunchRequest occurs
    if event['request']['type'] == "LaunchRequest":
        event['request']['intent'] = { 'name':'launch' }
    
    return on_intent(event['request'], event['session'])
