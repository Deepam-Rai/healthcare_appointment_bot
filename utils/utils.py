import os
import smtplib
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid
import math
import random
import logging
from pathlib import Path
from datetime import datetime
from dateutil.rrule import rrule, MINUTELY, HOURLY
logger = logging.getLogger(__name__)


def send_email(subject, recipient_email):
    message_data = EmailMessage()
    message_data["Subject"] = subject
    username = os.environ["EMAIL"]
    password = os.environ["PASS"]
    message_data["From"] = username
    message_data["To"] = recipient_email
    image_cid = make_msgid(domain="xyz.com")
    otp = generate_otp()
    # otp = 123456
    print(otp)
    this_path = Path(os.path.realpath(__file__))
    content = get_html_data(f"{this_path.parent.parent}\\utils\\user_mail.html")
    message_data.add_alternative(content.format(otp=otp, image_cid=image_cid), subtype="html")
    # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
    #     smtp_server.login(username, password)
    #     smtp_server.send_message(message_data)
    return True, otp


def get_image_data(filepath:str):
    with open(filepath, "rb") as image_data:
        maintype, subtype = mimetypes.guess_type(image_data.name)[0].split("/")
        return image_data.read(), maintype, subtype


def get_html_data(filepath:str):
    with open(filepath, "r") as html_data:
        return html_data.read()


def generate_otp():
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    return otp


def get_timestamp():
    return f"{datetime.fromtimestamp(datetime.timestamp(datetime.now())).isoformat()}"


def get_timeslots(slots, start_time, end_time):
    start_datetime = datetime.strptime(start_time, "%H:%M")
    end_datetime = datetime.strptime(end_time, "%H:%M")
    duration = (end_datetime - start_datetime) / slots
    time_slots = list(rrule(HOURLY, dtstart=start_datetime, until=end_datetime, interval=duration))
    result = [[slot.strftime("%H:%M"), (slot + duration).strftime("%H:%M")] for slot in time_slots]
    return result


def get_time_interval(doc_free_slots, booked_appointment_slots):
    doc_slots, doc_start_time, doc_end_time = doc_free_slots
    all_doc_slots = get_timeslots(doc_slots, doc_start_time, doc_end_time)
