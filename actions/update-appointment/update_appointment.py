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


class ActionAskUpdateReason(Action):
    def name(self) -> Text:
        return "action_ask_update_reason"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_update_reason")
        return []


class ActionAskNewWhichDoctor(Action):
    def name(self) -> Text:
        return "action_ask_new_which_doctor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        values = get_values(DOCTOR_DETAILS,
                            column_names=[NAME])
        logger.debug(values)
        fully_booked_docs = tracker.get_slot(FULLY_BOOKED_DOCS)
        doctors_name = values
        if fully_booked_docs:
            buttons = [
                {
                    "title": doc[0],
                    "payload": f'/update_appointment_intent{{"new_which_doctor":"{doc[0]}"}}',
                } for doc in doctors_name if doc[0] not in fully_booked_docs
            ]
        else:
            buttons = [
                {
                    "title": doc[0],
                    "payload": f'/update_appointment_intent{{"new_which_doctor":"{doc[0]}"}}',
                } for doc in doctors_name if doc[0]
            ]
        dispatcher.utter_message(response="utter_which_doctor", buttons=buttons)
        return [SlotSet(IS_DOC_FULL, False)]


class ActionAskNewAppointmentDate(Action):
    def name(self) -> Text:
        return "action_ask_new_appointment_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_appointment_date")
        return []


class ActionAskNewAppointmentTime(Action):
    def name(self) -> Text:
        return "action_ask_new_appointment_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        which_doctor = tracker.get_slot(NEW_WHICH_DOCTOR)
        fully_booked_docs = tracker.get_slot(FULLY_BOOKED_DOCS)
        appointment_date = tracker.get_slot(NEW_APPOINTMENT_DATE)
        doctor_free_slots = get_values(DOCTOR_DETAILS,
                                       column_names=[SLOTS, START_TIME, END_TIME],
                                       where_condition={NAME: which_doctor}
                                       )[0]
        logger.error(appointment_date)
        logger.error(which_doctor)
        booked_appointment_slots = get_values(APPOINTMENT_DETAILS,
                                              column_names=[START_TIME, END_TIME, DOCTOR_NAME, USER_ID, DATE],
                                              where_condition={DATE: appointment_date, DOCTOR_NAME: which_doctor},
                                              group_by=[DOCTOR_NAME]
                                              )

        free_slots = get_time_interval(doctor_free_slots, booked_appointment_slots)

        if free_slots == None:
            dispatcher.utter_message(response="utter_doctor_occupied_response")
            fully_booked_docs = fully_booked_docs.append(which_doctor) if fully_booked_docs else [which_doctor]
            return [SlotSet(IS_DOCTOR_FULL, True),
                    SlotSet(FULLY_BOOKED_DOCS, fully_booked_docs),
                    SlotSet(NEW_WHICH_DOCTOR, None),
                    SlotSet(NEW_APPOINTMENT_DATE, None),
                    SlotSet(NEW_APPOINTMENT_TIME, None),
                    ]

        buttons = [
            {
                "title": f"{slot[0]}-{slot[1]}",
                "payload": f'/update_appointment_intent{{"new_appointment_time":"{slot[0]}-{slot[1]}"}}',
            } for slot in free_slots
        ]
        dispatcher.utter_message(response="utter_appointment_time", buttons=buttons)
        return []


class ActionAskUpdateOtp(Action):
    def name(self) -> Text:
        return "action_ask_update_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot(EMAIL)
        is_sent, gen_otp = send_email("One-time Password(OTP)", email)
        dispatcher.utter_message(response='utter_update_appointment_otp_response')
        return [SlotSet(GENERATED_OTP, gen_otp)]


class ActionSubmitBookAppointmentForm(Action):
    def name(self) -> Text:
        return "action_submit_update_appointment_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        start_time, end_time = tracker.get_slot(NEW_APPOINTMENT_TIME).split('-')
        appointment_id = tracker.get_slot(SELECT_APPOINTMENT)
        doctor_name = tracker.get_slot(NEW_WHICH_DOCTOR)
        date = tracker.get_slot(NEW_APPOINTMENT_DATE)
        is_updated = update_row(
            APPOINTMENT_DETAILS,
            conditions={ID: appointment_id},
            update_fields={
                START_TIME: start_time,
                END_TIME: end_time,
                DOCTOR_NAME: doctor_name,
                DATE: date
            }
        )
        logger.debug(f'is_updated : {is_updated}')
        dispatcher.utter_message(response="utter_success_update_response",
                                 start_time=start_time, end_time=end_time,
                                 doctor_name=doctor_name,
                                 date=date
                                 )
        dispatcher.utter_message(text="Please choose an option to proceed:")
        dispatcher.utter_message(response="utter_show_menu")
        return []
