from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from utils.constants import *
from utils.utils import *
from pathlib import Path
from utils.database_utils import *


class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_greet_response_1")
        dispatcher.utter_message(response="utter_greet_response_2")
        return []


class ActionAskOtp(Action):
    def name(self) -> Text:
        return "action_ask_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot(EMAIL)
        name = tracker.get_slot(NAME)
        this_path = Path(os.path.realpath(__file__))
        gen_otp = generate_otp()
        print(gen_otp)
        user_content = get_html_data(f"{this_path.parent.parent}\\utils\\user_mail.html")
        user_content.format(otp=gen_otp, name=name)
        print(user_content)
        send_email("One-time Password(OTP)", email, user_content)
        dispatcher.utter_message(response='utter_otp_response')
        return [SlotSet("generated_otp", gen_otp)]


class ActionSubmitLoginForm(Action):
    def name(self) -> Text:
        return "action_submit_login_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_register_confirmation_response")
        return []


class ActionSubmitRegisterForm(Action):
    def name(self) -> Text:
        return "action_submit_register_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_register_confirmation_response")
        return []

#
# class ActionAskWhichDoctor(Action):
#     def name(self) -> Text:
#         return "action_ask_which_doctor"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # fetch doctor list from db
#         # fetch slots from db
#         # show doctor and slots to user
#         values = get_values(table="doctor_details", column_names=['name', 'start_time', 'end_time', 'slots'])
#         doctors_name = values['name']
#         # doctors_start_time = values['start_time']
#         # doctors_end_time = values['end_time']
#         # doctors_total_slots = values['slots']
#         # values = get_values(table = "appointment_details", columns = ['start_ts', 'end_ts', 'doctor_name'])
#         # appointment_start_ts = values['start_ts']
#         # appointment_end_ts = values['end_ts']
#         # appointment_docs_name = values['doctor_name']
#         buttons = [
#             {
#                 "title": doc,
#                 "payload": f'/appointment_intent{{"which_doctor":"{doc}"}}',
#             } for doc in doctors_name
#         ]
#         dispatcher.utter_message(response="utter_which_doctor", buttons=buttons)
#         return []
#
#
# class ActionAskAppointmentDate(Action):
#     def name(self) -> Text:
#         return "action_ask_appointment_date"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(response="utter_appointment_date")
#         return []
#
#
# class ActionAskAppointmentTime(Action):
#     def name(self) -> Text:
#         return "action_ask_appointment_time"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         values = get_values(table="appointment_details", column_names = ['start_ts', 'end_ts', 'doctor_name'])
#         appointment_start_ts = values['start_ts']
#         appointment_end_ts = values['end_ts']
#         appointment_docs_name = values['doctor_name']
#         return []
#
#
# class ActionAskConfirmDetails(Action):
#     def name(self) -> Text:
#         return "action_ask_confirm_details"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(response="utter_confirm_appointment_details")
#         return []
