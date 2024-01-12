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
# Action Name: action_ask_det_doctor
# Description: Gives list of doctors to users to choose from.
######################################################################################

class ActionAskDetDoctor(Action):
    def name(self) -> Text:
        return "action_ask_det_doctor"

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
                "payload": f'/general_intent{{"det_doctor":"{doc}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_det_doctor", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_det_appt
# Description: Gives list of appointments to users to choose from.
######################################################################################

class ActionAskDetAppt(Action):
    def name(self) -> Text:
        return "action_ask_det_appt"

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
                "payload": f'/general_intent{{"det_appt":"{appt}"}}'
            } for appt in appts
        ]
        dispatcher.utter_message(response="utter_det_appt", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_det_choice
# Description: Ask user if they want to see details or update or delete appointment.
######################################################################################

class ActionAskDetChoice(Action):
    def name(self) -> Text:
        return "action_ask_det_choice"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return []



#############################################################################################
# action: action_submit_get_details_form
# description: Submits form and routes as required.
#############################################################################################

class ActionSubmitGetDetailsForm(Action):
    def name(self) -> Text:
        return "action_submit_get_details_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        choice = tracker.get_slot(DET_CHOICE)
        date = "DB- T0D0"
        time = "DB- T0D0"
        doctor = "DB- T0D0"
        if choice == UPDATE:
            pass
        elif choice == DELETE:
            pass
        else:
            dispatcher.utter_message(response="utter_appt_details", doctor=doctor, date=date, time=time)
        return []