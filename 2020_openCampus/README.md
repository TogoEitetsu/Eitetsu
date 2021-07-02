# 2020年度オープンキャンパス

## Structure
```
.
├── app.py
├── data
│   └── reply_dict.csv
└── requirements.txt
```

## how to use
- Start App
``` 
$ heroku ps:scale web=1 
```

- Finish App
``` 
$ heroku ps:scale web=0
```

## Reference url
- https://blog.katsubemakito.net/macos/setup_heroku-cli
- https://developers.line.biz/ja/docs/messaging-api/building-sample-bot-with-heroku/#heroku-cli%E3%81%A6%E3%82%99%E3%83%AD%E3%82%AF%E3%82%99%E3%82%92%E7%A2%BA%E8%AA%8D%E3%81%99%E3%82%8B
- https://developers.line.biz/ja/docs/messaging-api/getting-started/#using-console
- https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2Fchannel%2F1655103404%2Fmessaging-api
- https://developers.line.biz/ja/reference/messaging-api/#response
- https://www.virtual-surfer.com/entry/2018/07/22/190000
- https://developers.line.biz/ja/news/
- https://qiita.com/redpanda/items/a056daea48b545250ce7


## 2020オープンキャンパス
### 概要
使用言語：　Python \
フォーマット：　LINE

### 環境
```
Click==7.0
Flask==1.1.1
pandas==1.1.0
gunicorn==20.0.4
itsdangerous==1.1.0
Jinja2==2.10.3
MarkupSafe==1.1.1
Werkzeug==0.16.0
line-bot-sdk==1.17.0
neologdn==0.4
```

### 順序
1. app.pyのサーバーたてる
2. ngrok/herokuでサーバー公開する
3. 割り振られたurlをmessaging apiのwebhook urlに登録する (今回の場合、/callback に送っている)