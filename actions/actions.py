# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import re

class ActionLookUpWordDictionary(Action):
    def name(self) -> Text:
        return "actionen"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        word = None
        for x in range(len(tracker.latest_message['entities'])):
            words = tracker.latest_message['entities'][x]['value']
            if words:
                word = words
        print(word)
        
        
        
        if not word:
            dispatcher.utter_message("Mình tìm hổng ra bạn ơi")
            return []
        url = 'https://api.tracau.vn/WBBcwnwQpV89/s/{}/en'.format(word)
        response = requests.get(url).text
        #print(response, end ='\n')
        json_data = json.loads(response)['tratu'][0]['fields']['fulltext']
        #print(json_data, end ='\n')
        try:
            pro = re.search(r"<\s*tr\s+id\s*=\s*\"pa\"[^>]*>.+?<\s*\/\s*tr>", json_data).group()
            tl = re.search(r"<\s*tr\s+id\s*=\s*\"tl\"[^>]*>.+?<\s*\/\s*tr>", json_data).group()
        except e1:
            print(e1)

        try:
            meanings = re.findall(r"<\s*tr\s+id\s*=\s*\"mn\"[^>]*>.+?<\s*\/\s*tr>", json_data)
        except Exception:
            dispatcher.utter_message("Mình hơi dở pha này rồi hehe!")
            return []

        pro = re.sub(r"<\s*[^>]+>", "", pro)
        tl = re.sub(r"<\s*[^>]+>", "", tl)
        for i in range(len(meanings)):
            meanings[i] = re.sub(r"<\s*[^>]+>", "", meanings[i])
        text_respond = "=> " + word.title()
        if pro is not None:
            text_respond +=  pro.replace("◘", " ")
        if tl is not None:
            text_respond += "\n" + tl.replace("*", "* ")
        if meanings:
            for mean in meanings:
                if mean is not None:
                    text_respond += "\n" + mean.replace("■", "  -  ")

            dispatcher.utter_message("Vắt óc suy nghĩ ra thì câu trả lời bạn cần nè:\n \n" + text_respond)
        else:
            dispatcher.utter_message("Mình hơi dở pha này rồi hehe!")
            return []

        return []
