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


class ActionAskShowDoctor(Action):
    def name(self) -> Text:
        return "action_ask_show_doctor"

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


class ActionAskSelectMenu(Action):
    def name(self) -> Text:
        return "action_ask_appointment_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        show_doctor = tracker.get_slot("show_doctor")
        values = get_values("appointment_details",
                            column_names=['id', 'start_ts', 'end_ts', 'user_id'],
                            where_condition={'doctor_name': show_doctor}
                            )
        dispatcher.utter_message(text=values)
        dispatcher.utter_message(response="utter_select_menu")
        return []


class ActionAskAppointmentDetails(Action):
    def name(self) -> Text:
        return "action_ask_appointment_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Enter your appointment details:")
        return []
