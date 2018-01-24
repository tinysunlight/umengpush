#coding=utf-8
import json
from .umengnotification import UmengNotification

class IOSNotification(UmengNotification):

    APS_KEYS = ["badge", "sound", "content-available"]
    ALERT_KEYS = ["body", "title", "subtitle"]

    def setPredefinedKeyValue(self, key, value):
        if key in self.ROOT_KEYS:
            self.rootJson[key] = value
        elif key in self.APS_KEYS:
            apsJson = json.loads('{}')
            payloadJson = json.loads('{}')
            if "payload" in self.rootJson:
                payloadJson = self.rootJson["payload"]
            else:
                self.rootJson["payload"] = payloadJson
            if "aps" in payloadJson:
                apsJson = payloadJson["aps"]
            else:
                payloadJson["aps"] = apsJson
            apsJson[key] = value
        elif key in self.ALERT_KEYS:
            apsJson = json.loads('{}')
            payloadJson = json.loads('{}')
            alertJson = json.loads('{}')
            if "payload" in self.rootJson:
                payloadJson = self.rootJson["payload"]
            else:
                self.rootJson["payload"] = payloadJson
            if "aps" in payloadJson:
                apsJson = payloadJson["aps"]
            else:
                payloadJson["aps"] = apsJson
            if "alert" in apsJson:
                alertJson = apsJson["alert"]
            else:
                apsJson["alert"] = alertJson
            alertJson[key] = value
        elif key in self.POLICY_KEYS:
            policyJson = json.loads('{}')
            if "policy" in self.rootJson:
                policyJson = self.rootJson["policy"]
            else:
                self.rootJson["policy"] = policyJson
            policyJson[key] = value
        else:
            if key in ["payload","aps","policy"]:
                print("You don't need to set value for {}, just set values for the sub keys in it.".format(key))
            else:
                print("Unknownd key: {}".format(key))

    def setBody(self, body):
        self.setPredefinedKeyValue("body", body)

    def setBadge(self, badge):
        self.setPredefinedKeyValue("badge", badge)

    def setSound(self, sound):
        self.setPredefinedKeyValue("sound", sound)

    def setTitle(self, title):
        self.setPredefinedKeyValue("title", title)

    def setContentAvailable(self, contentAvailable):
        self.setPredefinedKeyValue("content-available", contentAvailable)

    def setCustomizedField(self, key, value):
        payloadJson = json.loads('{}')
        if "payload" in self.rootJson:
            payloadJson = self.rootJson["payload"]
        else:
            self.rootJson["payload"] = payloadJson
        payloadJson[key] = value