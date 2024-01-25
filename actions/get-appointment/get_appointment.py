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
        value_buttons = [value[:3] for value in values]

        buttons = [
                    {
                        "title": f'Appointment ID : {value_button[0]}, Doctor Name : {value_button[1]}, Date : {value_button[2]}',
                        "payload": f'/appointment_intent{{"select_appointment":"{value_button[0]}"}}',
                    } for value_button in value_buttons
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
        select_menu = tracker.get_slot("select_menu")
        return_values = []
        if select_menu == "add_details":
            app_id = tracker.get_slot('select_appointment')
            details = tracker.get_slot('appointment_details')
            if details:
                is_updated = update_row(
                    "appointment_details",
                    conditions={"id": app_id},
                    update_fields={"details": details},
                )
                logger.error(is_updated)
                dispatcher.utter_message(text="Your details have been saved successfully!")
            dispatcher.utter_message(text="Please choose an option to proceed:")
            dispatcher.utter_message(response="utter_show_menu")
        elif select_menu == "delete":
            return_values.append(FollowupAction("delete_appointment_form"))
        elif select_menu == "update":
            return_values.append(FollowupAction("update_appointment_form"))
        return return_values
