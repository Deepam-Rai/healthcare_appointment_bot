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


class ValidateUpdateAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_update_appointment_form"

    async def validate_update_otp(self, value: Text,
                                  dispatcher: "CollectingDispatcher",
                                  tracker: "Tracker",
                                  domain: "DomainDict") -> Dict[str, str]:
        gen_otp = tracker.get_slot("generated_otp")
        logger.error(gen_otp)
        logger.error(value)
        if value == gen_otp:
            return {"update_otp": value}
        else:
            dispatcher.utter_message(response="utter_incorrect_otp_response")
            return {"requested_slot": "update_otp"}

    async def validate_new_appointment_date(self, value: Text,
                                            dispatcher: "CollectingDispatcher",
                                            tracker: "Tracker",
                                            domain: "DomainDict") -> Dict[str, str]:
        parsed_date = datetime.strptime(value, "%d/%m/%Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return {"new_appointment_date": formatted_date}
