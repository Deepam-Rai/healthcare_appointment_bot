
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
