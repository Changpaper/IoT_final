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
userId       = 'Uf133470b912b5defa38b6e4d63b822b7'

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
Reg_addr  = '170.1.3'

DAN.profile['dm_name'] = '039120_ODF'
DAN.profile['df_list'] = ['Volume']
DAN.profile['d_name']  = '039120_Dummy_Device'
DAN.device_registration_with_retry(ServerURL, Reg_addr)

i = 1

while True:
    try:
        ODF_data = DAN.pull('Volume')
        if ODF_data != None:
            if i:
                line_bot_api.push_message(userId, TextSendMessage(text = 'linebot is ready for you'))
                i = 0
            print (ODF_data[0])
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