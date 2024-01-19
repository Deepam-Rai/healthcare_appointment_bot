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
            column_names=[NAME, ID],
        )
        buttons = [
            {
                "title": doc[0],
                "payload": f'/general_intent{{"del_doc":"{doc[1]}", "del_doc_name":"{doc[0]}"}}'
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
        doctor_name = tracker.get_slot(DEL_DOC_NAME)
        booked_slots = get_values(
            APPOINTMENT,
            column_names=[ID, TIME, DATE],
            where_condition={
                DOCTOR_ID: doctor,
                USER_MAIL: user_mail
            }
        )
        if len(booked_slots) == 0:
            logger.debug(f"Booked appointments: {booked_slots}")
            dispatcher.utter_message(response="utter_no_appt", doctor=doctor_name)
            return [
                SlotSet(DEL_APPT, INVALID_APPT),
                SlotSet(REQUESTED_SLOT, None)
            ]
        else:
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
        otp_resets = [
            SlotSet(GENERATED_OTP, None),
            SlotSet(USER_OTP, None)
        ]
        user_otp = str(tracker.get_slot(USER_OTP))
        generated_otp = str(tracker.get_slot(GENERATED_OTP))
        appt = tracker.get_slot(DEL_APPT)
        if appt != INVALID_APPT:
            if user_otp != generated_otp:
                dispatcher.utter_message(response="utter_wrong_otp")
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
        return return_values + slot_sets + otp_resets


######################################################################################
# Action Name: validate_delete_appt_form
# Description:
######################################################################################


class ValidateGetDeleteApptForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_delete_appt_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        slots = domain_slots.copy()
        appt = tracker.get_slot(DEL_APPT)
        if appt is not None and appt != INVALID_APPT:
            slots = [DEL_REASON, USER_OTP] + slots
        return slots
