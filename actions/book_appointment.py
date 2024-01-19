from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from utils.constants import *
from utils.utils import *
from pathlib import Path
import logging
from utils.database_utils import *
logger = logging.getLogger(__name__)


class ActionAskWhichDoctor(Action):
    def name(self) -> Text:
        return "action_ask_which_doctor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        values = get_values("doctor_details",
                            column_names=['name'])
        logger.debug(values)
        doctors_name = values
        buttons = [
            {
                "title": doc[0],
                "payload": f'/appointment_intent{{"which_doctor":"{doc[0]}"}}',
            } for doc in doctors_name
        ]
        dispatcher.utter_message(response="utter_which_doctor", buttons=buttons)
        return []


class ActionAskAppointmentDate(Action):
    def name(self) -> Text:
        return "action_ask_appointment_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_appointment_date")
        return []


class ActionAskAppointmentTime(Action):
    def name(self) -> Text:
        return "action_ask_appointment_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        which_doctor = tracker.get_slot("which_doctor")
        appointment_date = tracker.get_slot("appointment_date")
        doctor_free_slots = get_values("doctor_details",
                                       column_names=["slots", "start_time", "end_time"],
                                       where_condition={'name': which_doctor}
                                       )[0]
        booked_appointment_slots = get_values("appointment_details",
                                              column_names=['start_time', 'end_time', 'doctor_name', 'user_id', 'date'],
                                              where_condition={"date": appointment_date, "doctor_name": which_doctor},
                                              group_by=['doctor_name']
                            )
        free_slots = get_time_interval(doctor_free_slots, booked_appointment_slots)
        buttons = [
            {
                "title": f"{slot[0]}-{slot[1]}",
                "payload": f'/appointment_intent{{"appointment_time":f"{slot[0]}-{slot[1]}"}}',
            } for slot in free_slots
        ]
        dispatcher.utter_message(response="utter_appointment_time", buttons=buttons)
        return []
