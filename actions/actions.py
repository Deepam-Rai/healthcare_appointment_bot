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

        is_sent, gen_otp = send_email(EMAIL_SUBJECT, email)
        if name is None:
            name = get_values(USER_DETAILS,
                              column_names=[NAME],
                              where_condition={ID: email}
                              )
            if name is None:
                return [SlotSet(OTP, -1)]
            dispatcher.utter_message(response='utter_login_otp_response', name=name[0][0])
        else:
            dispatcher.utter_message(response='utter_register_otp_response')
        return [SlotSet(GENERATED_OTP, gen_otp)]


class ActionSubmitLoginForm(Action):
    def name(self) -> Text:
        return "action_submit_login_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot(EMAIL)
        otp = tracker.get_slot(OTP)
        if otp != -1:
            values = get_values(USER_DETAILS,
                                column_names=[NAME, PHNO, GENDER] ,
                                where_condition={ID: email}
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
        name = tracker.get_slot(NAME)
        email = tracker.get_slot(EMAIL)
        phno = tracker.get_slot(PHNO)
        gender = tracker.get_slot(GENDER)
        is_inserted, id = insert_row(
            USER_DETAILS,
            name=name,
            id=email,
            phno=phno,
            gender=gender,
        )
        logger.error(is_inserted)
        dispatcher.utter_message(response="utter_register_confirmation_response")
        dispatcher.utter_message(response="utter_show_menu")
        return []
