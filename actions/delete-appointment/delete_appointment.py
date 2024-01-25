from typing import Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from utils.utils import *
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
        return "action_ask_delete_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot(EMAIL)
        is_sent, gen_otp = send_email("One-time Password(OTP)", email)
        dispatcher.utter_message(response='utter_delete_appointment_otp_response')
        return [SlotSet(GENERATED_OTP, gen_otp)]


class ActionSubmitDeleteAppointmentForm(Action):
    def name(self) -> Text:
        return "action_submit_delete_appointment_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        select_appointment = int(tracker.get_slot(SELECT_APPOINTMENT))
        delete_status = delete_row(APPOINTMENT_DETAILS, where_condition={ID: select_appointment})
        logger.debug(delete_status)
        if delete_status == True:
            dispatcher.utter_message(response="utter_row_deleted_response")
        else:
            dispatcher.utter_message(response="utter_row_not_deleted_response")
        dispatcher.utter_message(text="Please choose an option to proceed:")
        dispatcher.utter_message(response="utter_show_menu")
        return []
