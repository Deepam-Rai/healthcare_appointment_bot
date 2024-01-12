import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


######################################################################################
# Action Name: action_ask_book_doctor
# Description: Gives list of doctors to users to choose from.
######################################################################################

class ActionAskBookDoctor(Action):
    def name(self) -> Text:
        return "action_ask_book_doctor"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        doctors = ["doc1", "doc2", "doc3"]
        buttons = [
            {
                "title": doc,
                "payload": f'/general_intent{{"book_doctor":"{doc}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_select_doc", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_book_date
# Description: Asks user to choose an appointment date.
######################################################################################

class ActionAskBookDate(Action):
    def name(self) -> Text:
        return "action_ask_book_date"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_select_book_date")
        return []


######################################################################################
# Action Name: action_ask_book_time
# Description: Asks user to choose an appointment time.
######################################################################################

class ActionAskBookTime(Action):
    def name(self) -> Text:
        return "action_ask_book_time"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        slots = ["slot1", "slot2", "slot3"]
        buttons = [
            {
                "title": slot,
                "payload": f'/general_intent{{"book_time":"{slot}"}}'
            } for slot in slots
        ]
        dispatcher.utter_message(response="utter_select_book_time", buttons=buttons)
        return []


#############################################################################################
# action: action_submit_book_form
# description: Submits book form.
#############################################################################################

class ActionSubmitBookForm(Action):
    def name(self) -> Text:
        return "action_submit_book_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        confirm = tracker.get_slot(BOOK_CONFIRM)
        if confirm == FALSE:
            dispatcher.utter_message(response="utter_booking_cancelled")
        else:
            dispatcher.utter_message(response="utter_booking_done")
        return []
