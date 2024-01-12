from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


######################################################################################
# Action Name: action_login_register
# Description: Gives user option for login and register.
######################################################################################


class ActionLoginRegister(Action):
    def name(self) -> Text:
        return "action_login_register"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_login_register")
        return []


######################################################################################
# Action Name: action_all_options
# Description: Gives options to user - book, delete, update, etc for appointment.
######################################################################################


class ActionAllOptions(Action):
    def name(self) -> Text:
        return "action_all_options"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_all_options")
        return []