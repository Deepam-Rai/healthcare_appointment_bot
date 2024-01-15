import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils.database_utils import insert_row, exists_in_col
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)



######################################################################################
# Action Name: action_ask_user_phone_no
# Description: Aks phone no and checks if given email already registered.
######################################################################################

class ActionAskPhoneNo(Action):
    def name(self) -> Text:
        return "action_ask_PhoneNo"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot(PHONE_NO)
        if email == INVALID:
            return [
                SlotSet(PHONE_NO, None),
                SlotSet(USER_OTP, None)
            ]
        dispatcher.utter_message(response="utter_ask_phone_no")


#############################################################################################
# Action Name: validate_register_form
# Description: Validates if user has given correct input for registration
#############################################################################################

class ValidateRegisterForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_register_form"

    def validate_email(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            if exists_in_col(USER_DETAILS, EMAIL, value):
                return {"email": INVALID}
            return {"email": value}
        else:
            return {"requested_slot": EMAIL}


#############################################################################################
# action: action_submit_register_form
# description: Verifies OTP and submits form.
#############################################################################################

class ActionSubmitRegisterForm(Action):
    def name(self) -> Text:
        return "action_submit_register_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return_values = []
        email = tracker.get_slot(EMAIL)
        if email == INVALID:
            dispatcher.utter_message(response="utter_registered_email")
            dispatcher.utter_message(response="utter_request_login")
            return_values += [
                SlotSet(EMAIL, None),
                FollowupAction(ACTION_LOGIN_REGISTER)
            ]
        else:
            user_otp = str(tracker.get_slot(USER_OTP))
            generated_otp = str(tracker.get_slot(GENERATED_OTP))
            logger.debug(f'user: {user_otp}    gen: {generated_otp}')
            if user_otp != generated_otp:
                dispatcher.utter_message(response="utter_wrong_otp")
                return_values += [FollowupAction(ACTION_LOGIN_REGISTER)]
            else:
                dispatcher.utter_message(response="utter_logged_in")
                email = tracker.get_slot(EMAIL)
                name = tracker.get_slot(NAME)
                phone_no = tracker.get_slot(PHONE_NO)
                is_inserted, id = insert_row(
                    USER_DETAILS,
                    email=email,
                    name=name,
                    phone_no=phone_no
                )
                logger.debug(
                    f"is inserted: {is_inserted}\n" f"table-name: {USER_DETAILS}"
                )
                logger.debug(f"id: {id}")
        return return_values + [
            SlotSet(USER_OTP, None),
            SlotSet(GENERATED_OTP, None)
        ]