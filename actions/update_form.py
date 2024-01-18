import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils.database_utils import delete_row, update_row
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


######################################################################################
# Action Name: action_ask_update_doc
# Description: Asks user which doctor's appointment to update.
######################################################################################

class ActionAskUpdateDoc(Action):
    def name(self) -> Text:
        return "action_ask_update_doc"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        doctors = get_values(
            DOCTOR_DETAILS,
            column_names=[NAME],
        )
        buttons = [
            {
                "title": doc[0],
                "payload": f'/general_intent{{"{UPDATE_DOC}":"{doc[0]}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_update_doc", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_update_appt
# Description: Asks user which appointment to update.
######################################################################################

class ActionAskUpdateAppt(Action):
    def name(self) -> Text:
        return "action_ask_update_appt"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_mail = tracker.get_slot(EMAIL)
        doctor = tracker.get_slot(UPDATE_DOC)
        booked_slots = get_values(
            APPOINTMENT,
            column_names=[ID, TIME, DATE],
            where_condition={
                DOCTOR_NAME: doctor,
                USER_MAIL: user_mail
            }
        )
        buttons = [
            {
                "title": f'{x[2]} - {remove_seconds_str(x[1])}',
                "payload": f'/general_intent{{"{UPDATE_APPT}":"{x[0]}"}}'
            } for x in booked_slots
        ]
        dispatcher.utter_message(response="utter_update_appt", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_update_doc_new
# Description: Asks user which new doctor for whom appointment is to be made.
######################################################################################

class ActionAskUpdateDocNew(Action):
    def name(self) -> Text:
        return "action_ask_update_doc_new"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        doctors = get_values(
            DOCTOR_DETAILS,
            column_names=[NAME],
        )
        buttons = [
            {
                "title": doc[0],
                "payload": f'/general_intent{{"{UPDATE_DOC_NEW}":"{doc[0]}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_update_doc_new", buttons=buttons)
        return []



######################################################################################
# Action Name: action_ask_update_date_new
# Description: Asks user new appointment date.
######################################################################################

class ActionAskUpdateDateNew(Action):
    def name(self) -> Text:
        return "action_ask_update_date_new"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_select_update_date")
        return []



######################################################################################
# Action Name: action_ask_update_time_new
# Description: Asks user new appointment time.
######################################################################################

class ActionAskUpdateTimeNew(Action):
    def name(self) -> Text:
        return "action_ask_update_time_new"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        doctor = tracker.get_slot(UPDATE_DOC_NEW)
        date = tracker.get_slot(UPDATE_DATE_NEW)
        free_slots_time = get_free_slots(doctor=doctor, date=date)
        logger.debug(free_slots_time)
        free_slots = [(a.strftime("%H:%M:%S"), b.strftime("%H:%M:%S")) for a, b in free_slots_time]
        free_slots = [(':'.join(str(a).split(':')[:-1]), ':'.join(str(b).split(':')[:-1])) for a, b in free_slots]
        btn_titles = [f'{a} - {b}' for a, b in free_slots]
        logger.debug(btn_titles)
        buttons = [
            {
                "title": btn_titles[i],
                "payload": f'/general_intent{{"{UPDATE_TIME_NEW}":"{free_slots_time[i][0]}"}}'
            } for i in range(0, len(free_slots))
        ]
        dispatcher.utter_message(response="utter_select_update_time", buttons=buttons)
        return []


#############################################################################################
# action: action_submit_update_form
# description: Verifies OTP and updates the appointment.
#############################################################################################


class ActionSubmitUpdateForm(Action):
    def name(self) -> Text:
        return "action_submit_update_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return_values = []
        slot_sets = [SlotSet(x, None) for x in UPDATE_FORM_SLOTS]
        otp_resets = [
            SlotSet(GENERATED_OTP, None),
            SlotSet(USER_OTP, None)
        ]
        user_otp = str(tracker.get_slot(USER_OTP))
        generated_otp = str(tracker.get_slot(GENERATED_OTP))
        if user_otp != generated_otp:
            dispatcher.utter_message(response="utter_wrong_otp")
            return_values += slot_sets
        else:
            updated = update_row(
                APPOINTMENT,
                conditions={
                    ID: tracker.get_slot(UPDATE_APPT)
                },
                update_fields={
                    DOCTOR_NAME: tracker.get_slot(UPDATE_DOC_NEW),
                    DATE: tracker.get_slot(UPDATE_DATE_NEW),
                    TIME: tracker.get_slot(UPDATE_TIME_NEW)
                },
            )
            logger.debug(f"is data updated: {updated}")
            if updated is True:
                dispatcher.utter_message(response="utter_appt_updated")
            else:
                dispatcher.utter_message(response="utter_update_fail")
                dispatcher.utter_message(response="utter_try_again_later")
            return_values += slot_sets
        return return_values + otp_resets
