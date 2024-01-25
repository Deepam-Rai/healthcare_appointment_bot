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
        show_doctor = tracker.get_slot(SHOW_DOCTOR)
        email = tracker.get_slot(EMAIL)
        values = get_values(APPOINTMENT_DETAILS,
                            column_names=[ID, DOCTOR_NAME, DATE, START_TIME, END_TIME],
                            where_condition={USER_ID: email}
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
        select_menu = tracker.get_slot(SELECT_MENU)
        return_values = []
        if select_menu == ADD_DETAILS:
            app_id = tracker.get_slot(SELECT_APPOINTMENT)
            details = tracker.get_slot(APPOINTMENT_DETAILS)
            if details:
                is_updated = update_row(
                    APPOINTMENT_DETAILS,
                    conditions={ID: app_id},
                    update_fields={DETAILS: details},
                )
                logger.error(is_updated)
                dispatcher.utter_message(text="Your details have been saved successfully!")
            dispatcher.utter_message(text="Please choose an option to proceed:")
            dispatcher.utter_message(response="utter_show_menu")
        elif select_menu == DELETE:
            return_values.append(FollowupAction("delete_appointment_form"))
        elif select_menu == UPDATE:
            return_values.append(FollowupAction("update_appointment_form"))
        return return_values
