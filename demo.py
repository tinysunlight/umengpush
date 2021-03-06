#coding=utf-8

import json

from umessage.pushclient import PushClient
from umessage.iospush import *
from umessage.androidpush import *

from umessage.errorcodes import UMPushError, APIServerErrorCode

#注意andorid和ios是不同的appkey和appMasterSecret。 在不同需求下换成各自的appkey。
appKey = 'your appkey'
appMasterSecret = 'your master secret'
deviceToken = 'your token'
PUSH_PRODUCTION = 'false'

def upush_adr_listcast(message, path, registration_list):
    list_cast = umengpush.androidpush.AndroidListcast(appKey, appMasterSecret)
    list_cast.setDeviceToken(deviceToken) 
    list_cast.setTitle('hello')
    list_cast.setText(message)
    list_cast.setCustomField({'path':path})
    list_cast.setTicker("Android unicast ticker")
    if PUSH_PRODUCTION:
        list_cast.setProductionMode()
    else:
        list_cast.setTestMode()
    list_cast.goAppAfterOpen()
    list_cast.setDisplayType(umengpush.androidnotification.AndroidNotification.DisplayType.notification)
    pushClient = umengpush.pushclient.PushClient()
    pushClient.send(list_cast)



def upush_ios_listcast(message, path, registration_list):
    list_cast = umengpush.iospush.IOSListcast(appKey, appMasterSecret)
    list_cast.setDeviceToken(deviceToken)
    list_cast.setBody(message)
    list_cast.setTitle('hello')
    list_cast.setSound('default')
    list_cast.setCustomizedField('path', path)
    if PUSH_PRODUCTION:
        list_cast.setProductionMode()
    else:
        list_cast.setTestMode()
    pushClient = umengpush.pushclient.PushClient()
    pushClient.send(list_cast)


#android
def sendAndroidUnicast():
    unicast = AndroidUnicast(appKey, appMasterSecret)
    unicast.setDeviceToken(deviceToken);
    unicast.setTicker("Android unicast ticker");
    unicast.setTitle("中文的title");
    unicast.setText("Android unicast text");
    unicast.goAppAfterOpen();
    unicast.setDisplayType(AndroidNotification.DisplayType.NOTIFICATION);
    unicast.setTestMode()
    pushClient = PushClient()
    pushClient.send(unicast)

def sendAndroidBroadcast():
    broadcast = AndroidBroadcast(appKey, appMasterSecret)
    broadcast.setTicker("Android broadcast ticker");
    broadcast.setTitle("中文的title");
    broadcast.setText("Android broadcast text");
    broadcast.goAppAfterOpen();
    broadcast.setDisplayType(AndroidNotification.DisplayType.NOTIFICATION);
    broadcast.setTestMode()
    #Set customized fields
    broadcast.setExtraField("test", "helloworld");
    pushClient = PushClient()
    pushClient.send(broadcast)

#ios
def sendIOSUnicast():
    unicast = IOSUnicast(appKey, appMasterSecret)
    unicast.setDeviceToken(deviceToken)
    unicast.setBody("这个是一个iOS单播测试")
    unicast.setBadge(1234)
    unicast.setCustomizedField("test", "helloworld");
    unicast.setProductionMode()
    pushClient = PushClient()
    ret = pushClient.send(unicast)
    unicast.statuCode = ret.status_code;
    printResult(ret)

def sendIOSBroadcast():
    broadcast = IOSBroadcast(appKey, appMasterSecret)
    broadcast.setBody("这个是一个iOS广播测试")
    broadcast.setBadge(1234)
    broadcast.setTestMode()
    pushClient = PushClient()
    pushClient.send(broadcast)

def sendIOSCustomizedcast():
    customizedcast = IOSCustomizedcast(appKey, appMasterSecret)
    customizedcast.setAlias("alias", "alias_type");
    customizedcast.setBody("这个是一个iOS个性化测试")
    customizedcast.setBadge(1234)
    customizedcast.setTestMode()
    pushClient = PushClient()
    pushClient.send(customizedcast)

def sendIOSFilecast():
    #fileId = client.uploadContents(appkey, appMasterSecret, "aa" + "\n" + "bb");
    fileId = "fileid1"
    filecast = IOSFilecast(appKey, appMasterSecret)
    filecast.setFileId(fileId);
    filecast.setBody("这个是一个iOS组播测试")
    filecast.setBadge(1234)
    filecast.setTestMode()
    pushClient = PushClient()
    pushClient.send(filecast)

def sendIOSListcast():
    listcast = IOSListcast(appKey, appMasterSecret)
    listcast.setDeviceToken("xxx,yyy,zzz")
    listcast.setBody("这个是一个iOS列播测试")
    listcast.setBadge(1234)
    listcast.setTestMode()
    pushClient = PushClient()
    pushClient.send(listcast)

def sendIOSGroupcast():
    #condition:
    #"where":
    #{
    #  	"and":
    #		[
    #			{"tag" :"iostest"}
    #		]
    #	} /

    groupcast = IOSGroupcast(appKey, appMasterSecret)

    filterJson = json.loads('{}')
    whereJson = json.loads('{}')
    testTag = json.loads('{}')
    testTag['tag'] = "iostest"
    tagArray = [testTag]
    whereJson['and'] = tagArray
    filterJson['where'] = whereJson
    groupcast.setFilter(filterJson)
    groupcast.setBody("IOS 组播测试")
    groupcast.setBadge(1);
    groupcast.setSound("default")
    groupcast.setTestMode()
    pushClient = PushClient()
    ret = pushClient.send(groupcast)
    printResult(ret)

def printResult(ret):
    print "http status code: %s" % ret.status_code

    if ret.text != "":
        ret_json = json.loads(ret.text)
        if ret_json["ret"] == IOSNotification.CONSTR_STATUS_SUCCESS:
            if 'msg_id' in ret_json['data']:
                print "msgId: %s" % ret_json['data']['msg_id']
            if 'task_id' in ret_json['data']:
                print "task_id: %s" % ret_json['data']['task_id']
        elif ret_json["ret"] == IOSNotification.CONSTR_STATUS_FAIL:
            errorcode = int(ret_json["data"]["error_code"])
            print "error Code: %s, detail: %s" % (errorcode, APIServerErrorCode.errorMessage(errorcode));

if __name__ == '__main__':
    #sendIOSUnicast()
    #sendIOSBroadcast()
    sendIOSGroupcast()
