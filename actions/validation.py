from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


class ValidateLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return []


class ValidateRegisterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_register_form"

    async def validate_otp(self, value: Text,
                           dispatcher: "CollectingDispatcher",
                           tracker: "Tracker",
                           domain: "DomainDict") -> Dict[str, str]:
        gen_otp = tracker.get_slot("generated_otp")
        if value == gen_otp:
            return {"otp": value}
        else:
            dispatcher.utter_message(response="utter_incorrect_otp_response")
            return {"requested_slot": "otp"}


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


class ValidateDeleteAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_delete_appointment_form"

    async def validate_delete_otp(self, value: Text,
                                  dispatcher: "CollectingDispatcher",
                                  tracker: "Tracker",
                                  domain: "DomainDict") -> Dict[str, str]:
        gen_otp = tracker.get_slot("generated_otp")
        if value == gen_otp:
            return {"otp": value}
        else:
            dispatcher.utter_message(response="utter_incorrect_otp_response")
            return {"requested_slot": "otp"}
