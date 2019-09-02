from flask import Flask, session
from flask import request
from flask_session import Session
import requests
from bs4 import BeautifulSoup
from flask import jsonify
from flask import render_template
from flask_bootstrap import Bootstrap
import json
import wmmksCKIP
from Intent import getResponse
from jieba_seg import jieba_seg
from session_init import initsession 
import sys

app = Flask(__name__)


app.config['SESSION_TYPE'] = 'filesystem'  # session類型為redis
app.config['SESSION_FILE_DIR'] = './/SessionFileSystem'  # session類型為redis
app.config['SECRET_KEY'] = 'wmmks'

app.config['SESSION_FILE_THRESHOLD'] = 500  # 存儲session的個數如果大於這個值時，就要開始進行刪除了
app.config['SESSION_FILE_MODE'] = 384  # 文檔權限類型

app.config['SESSION_PERMANENT'] = False  # 如果設置為False，則關閉瀏覽器session就失效。
app.config['SESSION_USE_SIGNER'] = False  # 是否對發送到瀏覽器上session的cookie值進行加密
app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前綴



@app.route('/')

def hello():

    global session
    
    session = initsession(session)

    return render_template('index.html')


@app.route('/inputparser',methods=['POST'])

def parse():

    global session

    data = request.form.get('inputtext')

    segdata = jieba_seg(data)

    print("------------------------------",session,"-----------------------------", file=sys.stderr)
    
    response = getResponse( {'segdata':segdata , 'originData': data} , session)  #Intent.AjaxResponse

    session = response['session']

    print(response, file=sys.stderr)
    
    return jsonify(response['botresponse'])


# -----------------------------------------------------------------------------------------------

app.run(host='0.0.0.0' , port=5000, debug=True)


