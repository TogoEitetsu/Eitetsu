from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import pandas as pd
import neologdn

REPLY_PATH = './data/reply_dict.csv'
reply_dict = pd.read_csv(REPLY_PATH)

def generate_reply(input):
    try: 
        for row in reply_dict.itertuples():
            if row.key in input:
                reply = row.reply
        return reply
    except UnboundLocalError:
        reply = "それについてはわかりません"
        return reply


app = Flask(__name__)


line_bot_api = LineBotApi('###############################')
handler = WebhookHandler('###############################')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == '00000000000000000000000000000000':
        pass
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=generate_reply(neologdn.normalize(event.message.text))))

@app.route('/')
def index():
    return 'Hello World!'

'''
if __name__ == "__main__":
    #app.run()
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True) 
'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
