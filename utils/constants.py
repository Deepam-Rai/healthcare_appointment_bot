# constants

# database
USERNAME = "postgres"
PASSWORD = "root"
LOCAL_DB_SERVER = "http://localhost:35000/"
ANALYTICS_CONN_PARAMETERS_LOCAL = {
    "host": "localhost",
    "user": "postgres",
    "password": "root",
    "database": "appointment_app_db",
}

# table names
USER_DETAILS = "user_details"
APPOINTMENT_DETAILS = "appointment_details"
DOCTOR_DETAILS = "doctor_details"

# slots
EMAIL = "email"
NAME = "name"
PHNO = "phno"
GENDER = "gender"
OTP = "otp"
GENERATED_OTP = "generated_otp"
FULLY_BOOKED_DOCS = "fully_booked_docs"
IS_DOC_FULL = "is_doc_full"
WHICH_DOCTOR = "which_doctor"
APPOINTMENT_DATE = "appointment_date"
APPOINTMENT_TIME = "appointment_time"
IS_DOCTOR_FULL = 'is_doctor_full'
SELECT_APPOINTMENT = "select_appointment"
DELETE_OTP = "delete_otp"
SHOW_DOCTOR = "show_doctor"
SELECT_MENU = "select_menu"
NEW_WHICH_DOCTOR = "new_which_doctor"
NEW_APPOINTMENT_DATE = "new_appointment_date"
NEW_APPOINTMENT_TIME = "new_appointment_time"
UPDATE_OTP = "update_otp"


# db column names
ID = "id"
SLOTS = "slots"
START_TIME = "start_time"
END_TIME = "end_time"
DOCTOR_NAME = "doctor_name"
USER_ID = "user_id"
DATE = "date"
DETAILS = "details"

# misc
EMAIL_SUBJECT = "One-time Password(OTP)"
REQUESTED_SLOT = "requested_slot"
ADD_DETAILS = "add_details"
DELETE = "delete"
UPDATE = "update"






