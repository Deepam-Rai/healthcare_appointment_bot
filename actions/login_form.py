import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils.database_utils import exists_in_col
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


######################################################################################
# Action Name: action_ask_user_otp
# Description: Sends an OTP to user via mail and ask user to enter it in the chat.
######################################################################################

class ActionAskUserOtp(Action):
    def name(self) -> Text:
        return "action_ask_user_otp"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return_values = []
        user_mail = tracker.get_slot(EMAIL)
        if user_mail == INVALID:
            return [
                SlotSet(USER_OTP, None),
                SlotSet(REQUESTED_SLOT, None)
            ]
        otp = generate_otp()
        otp_sent = send_otp(otp, user_mail)
        logger.debug(f'OTP sent status: {otp_sent}')
        if otp_sent:
            dispatcher.utter_message(response="utter_ask_otp")
            return_values.append(SlotSet(GENERATED_OTP, otp))
        else:
            dispatcher.utter_message(response="utter_otp_not_sent")
            return_values.append(FollowupAction(ACTION_LOGIN_REGISTER))
        return return_values


#############################################################################################
# Action Name: validate_login_form
# Description: Validates if user has given correct input for login
#############################################################################################

class ValidateLoginForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_login_form"

    def validate_email(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            if exists_in_col(USER_DETAILS, EMAIL, value):
                return {"email": value}
            return {"email": INVALID}
        else:
            return {"requested_slot": EMAIL}

    def validate_user_otp(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict"
    ) -> Dict[str, str]:
        if value is not None:
            return {"user_otp": value}
        else:
            return {"requested_slot": USER_OTP}


#############################################################################################
# action: action_submit_login_form
# description: Submits login after OTP verification
#############################################################################################

class ActionSubmitLoginForm(Action):
    def name(self) -> Text:
        return "action_submit_login_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return_values = [
            SlotSet(USER_OTP, None),
            SlotSet(GENERATED_OTP, None)
        ]
        user_mail = tracker.get_slot(EMAIL)
        if user_mail == INVALID:
            dispatcher.utter_message(response="utter_unregistered_email", email=user_mail)
            dispatcher.utter_message(response="utter_request_register")
            return return_values + [
                FollowupAction(ACTION_LOGIN_REGISTER),
                SlotSet(EMAIL, None)
            ]
        else:
            user_otp = str(tracker.get_slot(USER_OTP))
            generated_otp = str(tracker.get_slot(GENERATED_OTP))
            logger.debug(f'user: {user_otp}    gen: {generated_otp}')
            if user_otp != generated_otp:
                dispatcher.utter_message(response="utter_wrong_otp")
                return return_values + [FollowupAction(ACTION_LOGIN_REGISTER)]
            else:
                dispatcher.utter_message(response="utter_logged_in")
        return return_values
