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
# Action Name: action_ask_update_doc
# Description: Asks user which doctor's appointment to update.
######################################################################################

class ActionAskUpdateDoc(Action):
    def name(self) -> Text:
        return "action_ask_update_doc"

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
                "payload": f'/general_intent{{"update_doc":"{doc}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_update_doc", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_update_appt
# Description: Asks user which appointment to update.
######################################################################################

class ActionAskUpdateAppt(Action):
    def name(self) -> Text:
        return "action_ask_update_appt"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        appts = ["appt-1", "appt-2"]
        buttons = [
            {
                "title": appt,
                "payload": f'/general_intent{{"update_appt":"{appt}"}}'
            } for appt in appts
        ]
        dispatcher.utter_message(response="utter_update_appt", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_update_doc_new
# Description: Asks user which new doctor for whom appointment is to be made.
######################################################################################

class ActionAskUpdateDocNew(Action):
    def name(self) -> Text:
        return "action_ask_update_doc_new"

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
                "payload": f'/general_intent{{"update_doc_new":"{doc}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_update_doc_new", buttons=buttons)
        return []



######################################################################################
# Action Name: action_ask_update_date_new
# Description: Asks user new appointment date.
######################################################################################

class ActionAskUpdateDateNew(Action):
    def name(self) -> Text:
        return "action_ask_update_date_new"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_select_update_date")
        return []



######################################################################################
# Action Name: action_ask_update_time_new
# Description: Asks user new appointment time.
######################################################################################

class ActionAskUpdateTimeNew(Action):
    def name(self) -> Text:
        return "action_ask_update_time_new"

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
                "payload": f'/general_intent{{"update_time_new":"{slot}"}}'
            } for slot in slots
        ]
        dispatcher.utter_message(response="utter_select_update_time", buttons=buttons)
        return []


#############################################################################################
# action: action_submit_update_form
# description: Verifies OTP and updates the appointment.
#############################################################################################


class ActionSubmitUpdateForm(Action):
    def name(self) -> Text:
        return "action_submit_update_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        user_otp = str(tracker.get_slot(USER_OTP))
        generated_otp = str(tracker.get_slot(GENERATED_OTP))
        if user_otp != generated_otp:
            dispatcher.utter_message(response="utter_wrong_otp")
        else:
            dispatcher.utter_message(response="utter_appt_updated")
        return []
