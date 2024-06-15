# linebot
import time, threading
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import TextSendMessage
import config

line_bot_api = LineBotApi(config.ChannelAccessToken)
handler      = WebhookHandler(config.ChannelSecret)      
user_id_set  = set()                                   
app          = Flask(__name__)
userId       = 'U75e318413dbd47da280cee2c9ef1d407'

def loadUserId():
    try:
        idFile = open(config.idfilePath, 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None

def saveUserId(userId):
    idFile = open(config.idfilePath, 'a')
    idFile.write(userId+';')
    idFile.close()


def pushLineMsg(Msg):
    for userId in user_id_set:
        try:
            line_bot_api.push_message(userId, TextSendMessage(text=Msg))
        except Exception as e:
            print(e)
        print('PushMsg: {}'.format(Msg))

idList = loadUserId()
if idList: user_id_set = set(idList) 

###

import time, random, requests
import DAN

ServerURL = 'https://2.iottalk.tw'
Reg_addr  = None

DAN.profile['dm_name'] = 'Dummy_Device'
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name']  = "pw."+ str(random.randint(100,999)) +"_"+ DAN.profile['dm_name']
DAN.device_registration_with_retry(ServerURL, Reg_addr)

i = 1

while True:
    try:
        ODF_data = DAN.pull('Dummy_Control')
        if ODF_data != None:
            if i:
                line_bot_api.push_message(userId, TextSendMessage(text = 'linebot is ready for you'))
                i = 0
            print (ODF_data)
            if ODF_data[0] > 90:
                line_bot_api.push_message(userId, TextSendMessage(text = '我要抱抱'))

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)