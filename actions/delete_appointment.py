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


class ActionAskDeleteReason(Action):
    def name(self) -> Text:
        return "action_ask_delete_reason"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_delete_reason")
        return []


class ActionAskDeleteOtp(Action):
    def name(self) -> Text:
        return "action_ask_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot(EMAIL)
        is_sent, gen_otp = send_email("One-time Password(OTP)", email)
        dispatcher.utter_message(response='utter_delete_appointment_otp_response')
        return [SlotSet("generated_otp", gen_otp)]


class ActionSubmitDeleteAppointmentForm(Action):
    def name(self) -> Text:
        return "action_submit_delete_appointment_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        select_appointment = int(tracker.get_slot("select_appointment"))
        delete_status = delete_row("appointment_details", )
        return []
