#-*-utf-8-*-
from flask import Flask,request
from xml.etree import ElementTree
import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def read_xml(text,target): 
    root = ElementTree.fromstring(text) 
    node_find = root.find(target) 
    print 'node is:',node_find.text
    return node_find.text 

def get_resp(text):
    requrl=u'http://www.tuling123.com/openapi/api?key=47cc18410bf4423aaef992b56401835b&userid=bearliejj&info='+text
    req = urllib2.Request(url=requrl)
    res_data = urllib2.urlopen(req)
    data = json.load(res_data)
    seid=data.get('text')
    print 'resp is:',seid
    return str(seid)

app = Flask(__name__)
print 'start-------'
@app.route('/',methods=['GET'])
def index():
    msg = request.args.get('echostr','empty')
    return msg
@app.route('/',methods=['POST'])
def chatPost():
    print 'start chat======'
    body = request.data
    print 'body:',body
    content = read_xml(body,'Content')
    tou = read_xml(body,'FromUserName')
    print 'tou====>>>>>',tou
    fromu = read_xml(body,'ToUserName')
    resp = get_resp(content)
    if content.find('http')>=0:
        file_abs='/home/longhua/otherhttp.log'
        if tou=='o5CEAwvMjQqWuDLPphZnyXZcee48':
            file_abs='/home/longhua/http.log'
        f=open(file_abs,'a')
        rip = request.remote_addr
        f.write('['+rip+'] ')
        f.write(content)
        f.write('\n')
    result = u'<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>12345678</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>'%(str(tou),str(fromu),str(resp))
    return result
@app.route('/he')
def hello():
    return u'hello word'
@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    return msg

if __name__ == '__main__':
    app.run()
