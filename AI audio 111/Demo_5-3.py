# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, AudioMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage
)

# create flask server
app = Flask(__name__)
line_bot_api = LineBotApi('9HqM/jIpNLv+VQAeCWyXxaqhT/gzdiaPu14aFsuGAARgIMSAC13wDDf/rKHul4kVKBAElQyyzYVs29k19UyXM3rbygCmjBi0mYUymhcTtfiaKY+FnuuRa7ONNCozyc3BcwGWwnP12fnSImm96U/t0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fa9f05788c50681c6bd6740cc6cc97c4')



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# handle msg
import os
import speech_recognition as sr

def transcribe(wav_path):
    '''
    Speech to Text by Google free API
    language: en-US, zh-TW
    '''
    
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None
    
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):

    name_mp3 = 'recording.mp3'
    name_wav = 'recording.wav'
    message_content = line_bot_api.get_message_content(event.message.id)
    
    with open(name_mp3, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    
    os.system('ffmpeg -y -i ' + name_mp3 + ' ' + name_wav + ' -loglevel quiet')
    result = transcribe(name_wav)
    print('Transcribe:', result)
    text1="".join(result)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = result))
    #開始翻譯,上面是從linebot讀取音檔轉成文字
    # text1是字串 result是串列
    import requests, uuid, json
    from urllib.parse import parse_qsl, parse_qs
    from flask import url_for
    from linebot.models import messages
   


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
        'text': result
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)

    # print(request.json()[0]['translations'][0]['text'])
    print("b")
    message = TextSendMessage(
        text = request.json()[0]['translations'][0]['text']
        )
    print(request.json()[0]['translations'][0]['text'])
    line_bot_api.reply_message(event.reply_token, message)
    # run app

if __name__ == "__main__":
        app.run(host='127.0.0.1', port=5566)
