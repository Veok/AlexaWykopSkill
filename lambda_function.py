from __future__ import print_function

import json
import urllib2
import random
import re
import string
from microsofttranslator import Translator


def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def read_last_entry(intent, session):
    data = json.load(urllib2.urlopen('http://a.wykop.pl/stream/hot/appkey,NPeaINJAQH'))
    return read_entry(data[0])


def read_random_entry(intent, session):
    data = json.load(urllib2.urlopen('http://a.wykop.pl/stream/hot/appkey,NPeaINJAQH'))
    return read_entry(random.choice(data))


def read_entry(entry):
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = ''

    translator = Translator('wykopalexa', 'Y3ThYcaJRUm0Y2zfF0oTlz92c3UDIaDKup+KD7Ror3k=')
    entryText = re.sub('<[^<]+?>', '', entry['body'])
    speech_output = translator.translate(entryText, 'en-us', 'pl')

    return build_response(session_attributes,
                          build_speechlet_response('wykop', speech_output, reprompt_text, should_end_session))


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "LastEntry":
        return read_last_entry(intent, session)
    elif intent_name == "RandomEntry":
        return read_random_entry(intent, session)
    elif intent_name == "Pasta":
        return pasta()
    elif intent_name == 'UsunKonto':
        return usun_konto()
    elif intent_name == "Rock":
        return rock_paper_scissors()
    elif intent_name == "Scissors":
        return rock_paper_scissors()
    elif intent_name == "Paper":
        return rock_paper_scissors()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def pasta():
    speech_output = 'Mehal Byalek coonchyk nocno varte v servrovni wykopu. Za oaknem zadluzoney villy poznyanskie kozyolki ocyeraly sye cyescyami, kturyh Byalek wolal byy nyigdy nye myec.'

    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    return build_response(session_attributes,
                          build_speechlet_response('wykop', speech_output, reprompt_text, should_end_session))


def usun_konto():
    speech_output = 'Sam yousoon konto styulyeyashu'

    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    return build_response(session_attributes,
                          build_speechlet_response('wykop', speech_output, reprompt_text, should_end_session))


def rock_paper_scissors():
    tab = ['rock', 'paper', 'scissors']

    speech_output = random.choice(tab)

    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    return build_response(session_attributes,
                          build_speechlet_response('wykop', speech_output, reprompt_text, should_end_session))


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Wykop mirkoblog. "
    reprompt_text = "I can read random or last entries for you. All of them are translated from polish to english."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Wykop skill. " \
                    "Yousoon konto! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
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
