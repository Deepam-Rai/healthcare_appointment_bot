import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


######################################################################################
# Action Name: action_ask_del_doc
# Description: Gives list of doctors to users to choose from for deleting appointment.
######################################################################################

class ActionAskDelDoc(Action):
    def name(self) -> Text:
        return "action_ask_del_doc"

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
                "payload": f'/general_intent{{"del_doc":"{doc}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_del_doctor", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_del_appt
# Description: Gives list of appointments to users to choose from for deletion.
######################################################################################

class ActionAskDelAppt(Action):
    def name(self) -> Text:
        return "action_ask_del_appt"

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
                "payload": f'/general_intent{{"del_appt":"{appt}"}}'
            } for appt in appts
        ]
        dispatcher.utter_message(response="utter_del_appt", buttons=buttons)
        return []


#############################################################################################
# action: action_submit_delete_appt_form
# description: Verifies OTP and deletes the appointment.
#############################################################################################


class ActionSubmitDeleteApptForm(Action):
    def name(self) -> Text:
        return "action_submit_delete_appt_form"

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
            dispatcher.utter_message(response="utter_appt_deleted")
        return []
