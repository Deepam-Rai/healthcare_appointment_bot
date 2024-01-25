from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from datetime import datetime
from rasa_sdk.types import DomainDict
from utils.database_utils import *
import logging
logger = logging.getLogger(__name__)


class ValidateLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    async def validate_email(self, value: Text,
                           dispatcher: "CollectingDispatcher",
                           tracker: "Tracker",
                           domain: "DomainDict") -> Dict[str, str]:
        email = get_values(USER_DETAILS,
                           column_names=[ID],
                           where_condition={ID: value}
                           )
        if email:
            return {EMAIL: value}
        else:
            dispatcher.utter_message(response="utter_no_existing_user_response")
            return {REQUESTED_SLOT: EMAIL}

    async def validate_otp(self, value: Text,
                           dispatcher: "CollectingDispatcher",
                           tracker: "Tracker",
                           domain: "DomainDict") -> Dict[str, str]:
        gen_otp = tracker.get_slot(GENERATED_OTP)
        if value == gen_otp:
            return {OTP: value}
        else:
            dispatcher.utter_message(response="utter_incorrect_otp_response")
            return {REQUESTED_SLOT: OTP}


class ValidateRegisterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_register_form"

    async def validate_otp(self, value: Text,
                           dispatcher: "CollectingDispatcher",
                           tracker: "Tracker",
                           domain: "DomainDict") -> Dict[str, str]:
        gen_otp = tracker.get_slot(GENERATED_OTP)
        if value == gen_otp:
            return {OTP: value}
        else:
            dispatcher.utter_message(response="utter_incorrect_otp_response")
            return {REQUESTED_SLOT: OTP}

    async def validate_email(self, value: Text,
                             dispatcher: "CollectingDispatcher",
                             tracker: "Tracker",
                             domain: "DomainDict") -> Dict[str, str]:
        email = get_values(USER_DETAILS,
                           column_names=[ID],
                           where_condition={ID: value}
                          )
        if email == []:
            return {EMAIL: value}
        else:
            dispatcher.utter_message(response="utter_existing_user_response")
            return {REQUESTED_SLOT: EMAIL}
