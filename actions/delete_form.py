import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils.database_utils import delete_row
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


######################################################################################
# Action Name: action_ask_del_doc
# Description: Gives list of doctors to users to choose from for deleting appointment.
######################################################################################

class ActionAskDelDoc(Action):
    def name(self) -> Text:
        return "action_ask_del_doc"

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
                "payload": f'/general_intent{{"del_doc":"{doc[0]}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_del_doctor", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_del_appt
# Description: Gives list of appointments to users to choose from for deletion.
######################################################################################

class ActionAskDelAppt(Action):
    def name(self) -> Text:
        return "action_ask_del_appt"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_mail = tracker.get_slot(EMAIL)
        doctor = tracker.get_slot(DEL_DOC)
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
                "payload": f'/general_intent{{"del_appt":"{x[0]}"}}'
            } for x in booked_slots
        ]
        dispatcher.utter_message(response="utter_del_appt", buttons=buttons)
        return []


#############################################################################################
# action: action_submit_delete_appt_form
# description: Verifies OTP and deletes the appointment.
#############################################################################################


class ActionSubmitDeleteApptForm(Action):
    def name(self) -> Text:
        return "action_submit_delete_appt_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return_values = []
        slot_sets = [SlotSet(x, None) for x in DELETE_APPT_FORM_SLOTS]
        user_otp = str(tracker.get_slot(USER_OTP))
        generated_otp = str(tracker.get_slot(GENERATED_OTP))
        if user_otp != generated_otp:
            dispatcher.utter_message(response="utter_wrong_otp")
            return_values += slot_sets + [
                SlotSet(GENERATED_OTP, None),
                SlotSet(USER_OTP, None)
            ]
        else:
            deleted = delete_row(
                APPOINTMENT,
                where_condition={
                    ID: tracker.get_slot(DEL_APPT)
                }
            )
            if deleted is True:
                dispatcher.utter_message(response="utter_appt_deleted")
            else:
                dispatcher.utter_message(response="utter_appt_deleted_fail")
            return_values += slot_sets + [
                SlotSet(GENERATED_OTP, None),
                SlotSet(USER_OTP, None)
            ]
        return return_values
