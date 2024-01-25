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


class ValidateGetAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_get_appointment_form"

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Text]:
        select_menu = tracker.get_slot("select_menu")
        slots = domain_slots.copy()
        if select_menu == "add_details":
            return ['appointment_details'] + slots
        return slots
