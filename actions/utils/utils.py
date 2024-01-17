import logging
import mimetypes
import random
import smtplib
import traceback
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import make_msgid
from actions.constants import *
import os
from pathlib import Path
from dateutil.rrule import rrule, MINUTELY

from actions.utils.database_utils import get_values

logger = logging.getLogger(__name__)


def generate_otp():
    """Generates a random 4 digit number"""
    otp = random.randint(1000, 9999)
    return otp


def send_otp(otp, user_mail):
    """Sends OTP to the user's mail"""
    try:
        message_data = EmailMessage()
        message_data["Subject"] = OTP_SUBJECT
        username = os.environ["EMAIL"]
        password = os.environ["PASS"]
        logger.debug(f'email: {username}    pass: {password}')
        message_data["From"] = username
        message_data["To"] = user_mail
        image_cid = make_msgid(domain="life.com")
        this_path = Path(os.path.realpath(__file__))
        content = get_html_data(f"{this_path.parent}\\user_mail.html")
        content = content.replace("<gen-otp></gen-otp>", f'<gen-otp>{otp}</gen-otp>')
        message_data.add_alternative(content.format(image_cid=image_cid), subtype="html")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.send_message(message_data)
        return True
    except Exception as error:
        logger.error(f'Error: {error}')
        logger.info(traceback.print_exc())
        return False


def get_html_data(filepath:str):
    with open(filepath, "r") as html_data:
        return html_data.read()


def get_slot_timings(start_time, interval, slot_count):
    """start_time: type datetime
        interval: type integer; interval time in minutes
        slot_count: type integer; how many slots are wanted
    Gets "slot_count" many time intervals, each "interval" time long, starting from "start_time".
    And returns the start time of each interval."""
    intervals = list(rrule(freq=MINUTELY, interval=interval, count=slot_count, dtstart=start_time))
    return intervals


def get_free_slots(doctor, date):
    """Returns free slots for the doctor on that date.
    Format: [(start_time, end_time), (start_time, end_time),...]"""
    start_time, interval, slot_count = get_values(
        DOCTOR_DETAILS,
        column_names=[START_TIME, INTERVAL, SLOTS],
        where_condition={
            NAME: doctor
        }
    )[0]
    start_time = datetime.strptime(start_time, '%H:%M:%S')
    all_slots = get_slot_timings(start_time=start_time, interval=interval, slot_count=slot_count)
    all_slots = [str(x.time()) for x in all_slots]
    booked_slots = get_values(
        APPOINTMENT,
        column_names=[f'{APPOINTMENT}.{TIME}'],
        where_condition={
            DOCTOR_NAME: doctor,
            DATE: date
        }
    )
    booked_slots = sum(booked_slots, [])
    logger.debug(all_slots)
    logger.debug(booked_slots)
    free_slots_start = list(set(all_slots)-set(booked_slots))
    free_slots_start = [datetime.strptime(x, '%H:%M:%S') for x in free_slots_start]
    logger.debug(free_slots_start)
    free_slots_end = [x + timedelta(minutes=interval) for x in free_slots_start]
    free_slots_end = [x.time() for x in free_slots_end]
    free_slots_start = [x.time() for x in free_slots_start]
    free_slots = list(zip(free_slots_start, free_slots_end))
    return free_slots

