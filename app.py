# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('j4ojDrQEpVFoyneQCtMGVklNikygsApOwuWr3ptnldW3breG2wLH7GFIQkiTCYnFB8vuKE3+yBCShr3JYTXR/Gpo+RF1pU1HYJoMhCiPWYf9EpIBAOJGcngR1l7qkw716U4xMJm4ChehGyVT27cpEAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('eef28b727ccbf95cbee6f6ddd819a113')

line_bot_api.push_message('U51565d28aa7d4e4e717bb1d3f8b32307', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        audio_message = AudioSendMessage(
            original_content_url='https://campus-studio.com/download/twsong.mp3',
            duration=81000
        )
        line_bot_api.reply_message(event.reply_token, audio_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
