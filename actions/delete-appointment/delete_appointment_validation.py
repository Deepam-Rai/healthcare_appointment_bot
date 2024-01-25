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


class ValidateDeleteAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_delete_appointment_form"

    async def validate_delete_otp(self, value: Text,
                                  dispatcher: "CollectingDispatcher",
                                  tracker: "Tracker",
                                  domain: "DomainDict") -> Dict[str, str]:
        gen_otp = tracker.get_slot(GENERATED_OTP)
        if value == gen_otp:
            return {DELETE_OTP: value}
        else:
            dispatcher.utter_message(response="utter_incorrect_otp_response")
            return {REQUESTED_SLOT: DELETE_OTP}
