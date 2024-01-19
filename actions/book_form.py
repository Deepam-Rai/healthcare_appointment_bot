import logging
from datetime import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils.database_utils import insert_row, get_values
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


######################################################################################
# Action Name: action_ask_book_doctor
# Description: Gives list of doctors to users to choose from.
######################################################################################

class ActionAskBookDoctor(Action):
    def name(self) -> Text:
        return "action_ask_book_doctor"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        doctors = get_values(
            DOCTOR_DETAILS,
            column_names=[NAME, ID],
        )
        buttons = [
            {
                "title": doc[0],
                "payload": f'/general_intent{{"book_doctor":"{doc[1]}", "book_doctor_name":"{doc[0]}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_select_doc", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_book_date
# Description: Asks user to choose an appointment date.
######################################################################################

class ActionAskBookDate(Action):
    def name(self) -> Text:
        return "action_ask_book_date"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_select_book_date")
        return []


######################################################################################
# Action Name: action_ask_book_time
# Description: Asks user to choose an appointment time.
######################################################################################

class ActionAskBookTime(Action):
    def name(self) -> Text:
        return "action_ask_book_time"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        doctor = tracker.get_slot(BOOK_DOCTOR)
        date = tracker.get_slot(BOOK_DATE)
        free_slots_time = get_free_slots(doctor=doctor, date=date)
        logger.debug(free_slots_time)
        free_slots = [(a.strftime("%H:%M:%S"), b.strftime("%H:%M:%S")) for a, b in free_slots_time]
        free_slots = [(':'.join(str(a).split(':')[:-1]), ':'.join(str(b).split(':')[:-1])) for a, b in free_slots]
        btn_titles = [f'{a} - {b}' for a, b in free_slots]
        logger.debug(btn_titles)
        buttons = [
            {
                "title": btn_titles[i],
                "payload": f'/general_intent{{"book_time":"{free_slots_time[i][0]}"}}'
            } for i in range(0, len(free_slots))
        ]
        dispatcher.utter_message(response="utter_select_book_time", buttons=buttons)
        return []


#############################################################################################
# action: action_submit_book_form
# description: Submits book form.
#############################################################################################

class ActionSubmitBookForm(Action):
    def name(self) -> Text:
        return "action_submit_book_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return_values = []
        slot_sets = [SlotSet(x, None) for x in BOOK_FORM_SLOTS]
        confirm = tracker.get_slot(BOOK_CONFIRM)
        if confirm == FALSE:
            dispatcher.utter_message(response="utter_booking_cancelled")
        else:
            is_inserted, id = insert_row(
                APPOINTMENT,
                doctor_id=tracker.get_slot(BOOK_DOCTOR),
                doctor_name=tracker.get_slot(BOOK_DOCTOR_NAME),
                date=tracker.get_slot(BOOK_DATE),
                time=tracker.get_slot(BOOK_TIME),
                user_mail=tracker.get_slot(EMAIL)
            )
            logger.debug(f'id" {id}')
            logger.debug(
                f"is inserted: {is_inserted}\n" f"table-name: {USER_DETAILS}"
            )
            if is_inserted is False:
                dispatcher.utter_message(response="utter_booking_failed")
                dispatcher.utter_message(response="utter_try_again")
                return [FollowupAction(ACTION_ALL_OPTIONS)]
            else:
                dispatcher.utter_message(response="utter_booking_done")
        return slot_sets + return_values
