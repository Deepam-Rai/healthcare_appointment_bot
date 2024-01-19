import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.utils.utils import *
from actions.constants import *


logger = logging.getLogger(__name__)


######################################################################################
# Action Name: action_ask_det_doctor
# Description: Gives list of doctors to users to choose from.
######################################################################################

class ActionAskDetDoctor(Action):
    def name(self) -> Text:
        return "action_ask_det_doctor"

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
                "payload": f'/general_intent{{"det_doctor":"{doc[1]}", "det_doctor_name":"{doc[0]}"}}'
            } for doc in doctors
        ]
        dispatcher.utter_message(response="utter_det_doctor", buttons=buttons)
        return [SlotSet(DET_APPT, None)]


######################################################################################
# Action Name: action_ask_det_appt
# Description: Gives list of appointments to users to choose from.
######################################################################################

class ActionAskDetAppt(Action):
    def name(self) -> Text:
        return "action_ask_det_appt"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_mail = tracker.get_slot(EMAIL)
        doctor = tracker.get_slot(DET_DOCTOR)
        doctor_name = tracker.get_slot(DET_DOCTOR_NAME)
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
                SlotSet(DET_APPT, INVALID_APPT),
                SlotSet(REQUESTED_SLOT, None)
            ]
        else:
            buttons = [
                {
                    "title": f'{x[2]} - {remove_seconds_str(x[1])}',
                    "payload": f'/general_intent{{"det_appt":"{x[0]}"}}'
                } for x in booked_slots
            ]
            dispatcher.utter_message(response="utter_det_appt", buttons=buttons)
        return []


######################################################################################
# Action Name: action_ask_det_choice
# Description: Ask user if they want to see details or update or delete appointment.
######################################################################################

class ActionAskDetChoice(Action):
    def name(self) -> Text:
        return "action_ask_det_choice"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return []



#############################################################################################
# action: action_submit_get_details_form
# description: Submits form and routes as required.
#############################################################################################

class ActionSubmitGetDetailsForm(Action):
    def name(self) -> Text:
        return "action_submit_get_details_form"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return_values = []
        slot_sets = [SlotSet(x, None) for x in GET_DETAILS_FORM_SLOTS]
        doctor = tracker.get_slot(DET_DOCTOR)
        det_appt = tracker.get_slot(DET_APPT)
        choice = tracker.get_slot(DET_CHOICE)
        if det_appt != INVALID_APPT:
            if choice == UPDATE:
                return_values += [
                    SlotSet(UPDATE_DOC, doctor),
                    SlotSet(UPDATE_APPT, det_appt),
                    FollowupAction(UPDATE_FORM)
                ]
            elif choice == DELETE:
                return_values += [
                    SlotSet(DEL_DOC, doctor),
                    SlotSet(DEL_APPT, det_appt),
                    FollowupAction(DELETE_APPT_FORM)
                ]
            else:
                details = get_values(
                    APPOINTMENT,
                    column_names=[TIME, DATE],
                    where_condition={
                        ID: tracker.get_slot(DET_APPT)
                    }
                )
                date, time = details[0]
                doctor = tracker.get_slot(DET_DOCTOR_NAME)
                dispatcher.utter_message(response="utter_appt_details", doctor=doctor, date=date, time=time)
        return return_values + slot_sets


######################################################################################
# Action Name: validate_get_details_form
# Description: validates get details form.
######################################################################################


class ValidateGetDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_get_details_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        slots = domain_slots.copy()
        appt = tracker.get_slot(DET_APPT)
        if appt is not None and appt != INVALID_APPT:
            slots.insert(0, DET_CHOICE)
        return slots
