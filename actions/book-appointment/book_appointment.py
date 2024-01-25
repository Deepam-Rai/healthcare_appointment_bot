from typing import Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from utils.utils import *
import logging
from utils.database_utils import *

logger = logging.getLogger(__name__)


class ActionAskWhichDoctor(Action):
    def name(self) -> Text:
        return "action_ask_which_doctor"

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
                    "payload": f'/appointment_intent{{"which_doctor":"{doc[0]}"}}',
                } for doc in doctors_name if doc[0] not in fully_booked_docs
            ]
        else:
            buttons = [
                {
                    "title": doc[0],
                    "payload": f'/appointment_intent{{"which_doctor":"{doc[0]}"}}',
                } for doc in doctors_name if doc[0]
            ]
        dispatcher.utter_message(response="utter_which_doctor", buttons=buttons)
        return [SlotSet(IS_DOC_FULL, False)]


class ActionAskAppointmentDate(Action):
    def name(self) -> Text:
        return "action_ask_appointment_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_appointment_date")
        return []


class ActionAskAppointmentTime(Action):
    def name(self) -> Text:
        return "action_ask_appointment_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        which_doctor = tracker.get_slot(WHICH_DOCTOR)
        fully_booked_docs = tracker.get_slot(FULLY_BOOKED_DOCS)
        appointment_date = tracker.get_slot(APPOINTMENT_DATE)
        doctor_free_slots = get_values(DOCTOR_DETAILS,
                                       column_names=[SLOTS, START_TIME, END_TIME],
                                       where_condition={NAME: which_doctor}
                                       )[0]
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
                    SlotSet(WHICH_DOCTOR, None),
                    SlotSet(APPOINTMENT_DATE, None),
                    SlotSet(APPOINTMENT_TIME, None),
                    ]

        buttons = [
            {
                "title": f"{slot[0]}-{slot[1]}",
                "payload": f'/appointment_intent{{"appointment_time":"{slot[0]}-{slot[1]}"}}',
            } for slot in free_slots
        ]
        dispatcher.utter_message(response="utter_appointment_time", buttons=buttons)
        return []


class ActionSubmitBookAppointmentForm(Action):
    def name(self) -> Text:
        return "action_submit_book_appointment_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        start_time, end_time = tracker.get_slot(APPOINTMENT_TIME).split('-')
        doctor_name = tracker.get_slot(WHICH_DOCTOR)
        user_id = tracker.get_slot(EMAIL)
        date = tracker.get_slot(APPOINTMENT_DATE)
        is_inserted, id = insert_row(
            APPOINTMENT_DETAILS,
            start_time=start_time,
            end_time=end_time,
            doctor_name=doctor_name,
            user_id=user_id,
            date=date
        )
        logger.debug(f'is_inserted : {is_inserted}, ID : {id}')
        dispatcher.utter_message(response="utter_success_appointment_booking_response",
                                 start_time=start_time, end_time=end_time,
                                 doctor_name=doctor_name,
                                 date=date
                                 )
        dispatcher.utter_message(text="Please choose an option to proceed:")
        dispatcher.utter_message(response="utter_show_menu")
        return []
