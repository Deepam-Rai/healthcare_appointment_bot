import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


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
        user_otp = str(tracker.get_slot(USER_OTP))
        generated_otp = str(tracker.get_slot(GENERATED_OTP))
        logger.debug(f'user: {user_otp}    gen: {generated_otp}')
        if user_otp != generated_otp:
            dispatcher.utter_message(response="utter_wrong_otp")
            return_values += [FollowupAction(ACTION_LOGIN_REGISTER)]
        else:
            dispatcher.utter_message(response="utter_logged_in")
        return return_values + [
            SlotSet(USER_OTP, None),
            SlotSet(GENERATED_OTP, None)
        ]