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
        doctors = get_values(
            DOCTOR_DETAILS,
            column_names=[NAME],
        )
        buttons = [
            {
                "title": doc[0],
                "payload": f'/general_intent{{"det_doctor":"{doc[0]}"}}'
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
        user_mail = tracker.get_slot(EMAIL)
        doctor = tracker.get_slot(DET_DOCTOR)
        booked_slots = get_values(
            APPOINTMENT,
            column_names=[ID, TIME, DATE],
            where_condition={
                DOCTOR_NAME: doctor,
                USER_MAIL: user_mail
            }
        )
        buttons = [
            {
                "title": f'{x[2]} - {remove_seconds_str(x[1])}',
                "payload": f'/general_intent{{"det_appt":"{x[0]}"}}'
            } for x in booked_slots
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
        slot_sets = [SlotSet(x, None) for x in GET_DETAILS_FORM_SLOTS]
        choice = tracker.get_slot(DET_CHOICE)
        if choice == UPDATE:
            pass
        elif choice == DELETE:
            pass
        else:
            details = get_values(
                APPOINTMENT,
                column_names=[TIME, DATE],
                where_condition={
                    ID: tracker.get_slot(DET_APPT)
                }
            )
            date, time = details[0]
            doctor = tracker.get_slot(DET_DOCTOR)
            dispatcher.utter_message(response="utter_appt_details", doctor=doctor, date=date, time=time)
        return slot_sets
