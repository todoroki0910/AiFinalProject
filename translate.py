import requests, uuid, json
from urllib.parse import parse_qsl, parse_qs
from flask import url_for
from linebot.models import messages
from line_chatbot_api import *

def translate(event,text):
    key = "941a7833406b4b4d9ccb668e7ddcd48a"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    location = "uksouth"
    print("a")
    path = '/translate'
    constructed_url = endpoint + path
    params = {
        'api-version': '3.0',
        'from':"zh-Hans",
        'to': ['en']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)

    # print(request.json()[0]['translations'][0]['text'])
    print("b")
    message = TextSendMessage(
        text = request.json()[0]['translations'][0]['text']
        )
    print(request.json()[0]['translations'][0]['text'])
    line_bot_api.reply_message(event.reply_token, message)