
# OTP mail
OTP_SUBJECT = "OTP for Life HealthCare"

# actions
ACTION_LOGIN_REGISTER = "action_login_register"
ACTION_ALL_OPTIONS = "action_all_options"

# generally used terms
TRUE = "true"
FALSE = "false"
DETAILS = "details"
UPDATE = "update"
INVALID = "invalid"
TIME = "time"
DATE = "date"

# Commonly used slots
GENERATED_OTP = "generated_otp"
USER_OTP = "user_otp"
DELETE = "delete"
REQUESTED_SLOT = "requested_slot"

# register form slots
EMAIL = "email"
NAME = "name"
PHONE_NO = "phone_no"

# book_form slots
BOOK_DOCTOR = "book_doctor"
BOOK_DATE = "book_date"
BOOK_TIME = "book_time"
BOOK_CONFIRM = "book_confirm"
BOOK_FORM_SLOTS = [
    BOOK_DOCTOR,
    BOOK_DATE,
    BOOK_TIME,
    BOOK_CONFIRM
]

# get_details form slots
DET_DOCTOR = "det_doctor"
DET_APPT = "det_appt"
DET_CHOICE = "det_choice"
GET_DETAILS_FORM_SLOTS = [
    DET_DOCTOR,
    DET_APPT,
    DET_CHOICE
]

# delete_appt_form slots
DEL_DOC = "del_doc"
DEL_APPT = "del_appt"
DEL_REASON = "del_reason"
DELETE_APPT_FORM_SLOTS = [
    DEL_DOC,
    DEL_APPT,
    DEL_REASON
]

# update_form slots
UPDATE_DOC = "update_doc"
UPDATE_APPT = "update_appt"
UPDATE_REASON = "update_reason"
UPDATE_DOC_NEW = "update_doc_new"
UPDATE_DATE_NEW = "update_date_new"
UPDATE_TIME_NEW = "update_time_new"
UPDATE_CONFIRM = "update_confirm"
UPDATE_FORM_SLOTS = [
    UPDATE_DOC,
    UPDATE_APPT,
    UPDATE_REASON,
    UPDATE_DOC_NEW,
    UPDATE_DATE_NEW,
    UPDATE_TIME_NEW,
    UPDATE_CONFIRM
]

# table names
USER_DETAILS = "user_details"
DOCTOR_DETAILS = "doctor_details"
APPOINTMENT = "appointment"

# commonly used column names
ID = "id"

# doctor_details table columns
DOCTOR_NAME = "doctor_name"
START_TIME = "start_time"
INTERVAL = "interval"
SLOTS = "slots"

# apoointment table columns
USER_MAIL = "user_mail"
