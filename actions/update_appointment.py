# from typing import Any, Dict, List, Text
# from rasa_sdk import Action, Tracker
# from rasa_sdk.events import FollowupAction, SlotSet
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormValidationAction
# from rasa_sdk.types import DomainDict
# from utils.constants import *
# from utils.utils import *
# from pathlib import Path
# import logging
# from utils.database_utils import *
# logger = logging.getLogger(__name__)
#
#
# class ActionAskUpdateReason(Action):
#     def name(self) -> Text:
#         return "action_ask_update_reason"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(text="Please enter the reason for you modifying the appointment: ")
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
#         values = get_values("appointment_details",
#                             column_names=['start_ts', 'end_ts', 'doctor_name', 'user_id'],
#                             group_by=['doctor_name']
#                             )
#         which_doctor = tracker.get_slot("which_doctor")
#         logger.error(values)
#         if values is None:
#             doctor_slots = get_values("doctor_details",
#                                       column_names=["slots", "start_time", "end_time"],
#                                       where_condition={'name': which_doctor}
#                                       )
#             logger.debug(doctor_slots)
#         #
#         #
#         # buttons = [
#         #     {
#         #         "title": doc[0],
#         #         "payload": f'/appointment_intent{{"which_doctor":"{doc[0]}"}}',
#         #     } for doc in doctors_name
#         # ]
#         return []
