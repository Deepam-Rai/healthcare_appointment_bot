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


class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_greet_response_1")
        dispatcher.utter_message(response="utter_greet_response_2")
        return []


class ActionAskOtp(Action):
    def name(self) -> Text:
        return "action_ask_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot(EMAIL)
        name = tracker.get_slot(NAME)
        is_sent, gen_otp = send_email("One-time Password(OTP)", email)
        if name is None:
            name = get_values("user_details",
                              column_names=['name'],
                              where_condition={"id": email}
                              )
            if name is None:
                return [SlotSet("otp", -1)]
            dispatcher.utter_message(response='utter_login_otp_response', name=name[0][0])
        else:
            dispatcher.utter_message(response='utter_register_otp_response')
        return [SlotSet("generated_otp", gen_otp)]


class ActionSubmitLoginForm(Action):
    def name(self) -> Text:
        return "action_submit_login_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot('email')
        otp = tracker.get_slot('otp')
        if otp != -1:
            values = get_values("user_details",
                                column_names=['name', 'phno', 'gender'] ,
                                where_condition={"id": email}
                          )
            dispatcher.utter_message(response="utter_login_confirmation_response")
            dispatcher.utter_message(response="utter_show_menu")
        else:
            dispatcher.utter_message(response="utter_invalid_user_response")
        return []


class ActionSubmitRegisterForm(Action):
    def name(self) -> Text:
        return "action_submit_register_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        phno = tracker.get_slot('phno')
        gender = tracker.get_slot('gender')
        is_inserted, id = insert_row(
            "user_details",
            name=name,
            id=email,
            phno=phno,
            gender=gender,
        )
        logger.error(is_inserted)
        dispatcher.utter_message(response="utter_register_confirmation_response")
        dispatcher.utter_message(response="utter_show_menu")
        return []
