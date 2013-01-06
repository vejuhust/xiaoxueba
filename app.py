#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, Response, make_response, request, render_template, url_for
from hashlib import sha1
from xml.etree import ElementTree
from xiaoxueba5 import SimSimi
from auth import *
import datetime
import MySQLdb
from MySQLdb import escape_string


token = "weixin_python_sim"

app = Flask(__name__)


#保存到数据库
def save_to_database(name, question, answer):
    conn = MySQLdb.connect (host = db_host,
                            user = db_user,
                            passwd = db_passwd,
                            db = db_name,
                            unix_socket = db_sock,
                            charset = db_charset)
    cursor = conn.cursor()
    try:
        cursor.execute("insert into simisim_wx.dialogue set name = '%s', question = '%s', answer = '%s';" % (escape_string(name), escape_string(question.encode('utf-8')), escape_string(answer.encode('utf-8'))))
    except Exception as e:
        pass
    finally:
        cursor.close()
    conn.commit()
    conn.close()


#响应对话
def reply_message(question):
    simi = SimSimi()
    answer = simi.affected_chat(question)
    return answer


#验证接口配置信息
@app.route('/', methods = ['GET'])
def weixin_verify():
    echostr = request.args['echostr']
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    temp_array = [token, timestamp, nonce]
    temp_array.sort()
    temp_string = ''.join(temp_array)
    sha1hash = sha1(temp_string).hexdigest()
    if signature == sha1hash:
        return echostr
    else:
        return "error"


#作为接口被微信调用并返回结果
@app.route('/', methods = ['POST'])
def weixin_reply():
    #读取并解析消息
    data = request.data
    root = ElementTree.fromstring(data)
    receiver = root.find('ToUserName').text
    sender = root.find('FromUserName').text
    create_time = root.find('CreateTime').text
    message_type = root.find('MsgType').text
    if message_type == 'text':
        content = root.find('Content').text
    else:
        location = (root.find('Location_X').text, root.find('Location_Y').text)
        scale = root.find('Scale').text
        label = root.find('Label').text
    #响应对话
    reply = reply_message(content)
    #保存对话
    save_to_database(sender, content, reply)
    #回复消息
    response_text_format = """
        <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag>
        </xml>
    """
    response_text = response_text_format % (sender, receiver, create_time, reply)
    return response_text


if __name__ == '__main__':
    app.run(host='0.0.0.0')

