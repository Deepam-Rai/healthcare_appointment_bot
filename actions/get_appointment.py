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

#
# class ActionAskShowDoctor(Action):
#     def name(self) -> Text:
#         return "action_ask_show_doctor"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         values = get_values("doctor_details",
#                             column_names=['name'])
#         logger.debug(values)
#         doctors_name = values
#         buttons = [
#             {
#                 "title": doc[0],
#                 "payload": f'/appointment_intent{{"which_doctor":"{doc[0]}"}}',
#             } for doc in doctors_name
#         ]
#         dispatcher.utter_message(response="utter_which_doctor", buttons=buttons)
#         return []


class ActionAskSelectAppointment(Action):
    def name(self) -> Text:
        return "action_ask_select_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        show_doctor = tracker.get_slot("show_doctor")
        email = tracker.get_slot('email')
        values = get_values("appointment_details",
                            column_names=['id', 'doctor_name','date', 'start_time', 'end_time'],
                            where_condition={'user_id': email}
                            )
        value_buttons = [l[:3] for l in values]

        buttons = [
                    {
                        "title": f'Appointment ID : {l[0]}, Doctor Name : {l[1]}, Date : {l[2]}',
                        "payload": f'/appointment_intent{{"select_menu":"{l[0]}"}}',
                    } for l in value_buttons
                ]
        dispatcher.utter_message(text="Select an appointment to add details/update/delete it:", buttons=buttons)

        return []


class ActionAskSelectMenu(Action):
    def name(self) -> Text:
        return "action_ask_select_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_select_menu")
        return []


class ActionAskAppointmentDetails(Action):
    def name(self) -> Text:
        return "action_ask_appointment_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Please enter your appointment details:")
        return []


class ActionSubmitGetAppointmentForm(Action):
    def name(self) -> Text:
        return "action_submit_get_appointment_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        app_id = tracker.get_slot('select_appointment')
        details = tracker.get_slot('details')
        if details:
            is_updated = update_row(
                "appointment_details",
                conditions={"id": app_id},
                update_fields={"details": details},
            )
            logger.error(is_updated)
        return []