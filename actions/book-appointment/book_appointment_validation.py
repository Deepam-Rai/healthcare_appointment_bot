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


class ValidateBookAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_book_appointment_form"

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Text]:
        is_doc_full = tracker.get_slot("is_doc_full")
        slots = domain_slots.copy()
        if is_doc_full == True:
            return ["which_doctor", "appointment_date", "appointment_time"] + slots
        return slots

    async def validate_appointment_date(self, value: Text,
                                        dispatcher: "CollectingDispatcher",
                                        tracker: "Tracker",
                                        domain: "DomainDict") -> Dict[str, str]:
        parsed_date = datetime.strptime(value, "%d/%m/%Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return {"appointment_date": formatted_date}
