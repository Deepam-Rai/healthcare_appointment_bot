import logging
import mimetypes
import random
import smtplib
import traceback
from email.message import EmailMessage
from email.utils import make_msgid
from actions.constants import *
import os
from pathlib import Path


logger = logging.getLogger(__name__)


os.environ["EMAIL"] = "deepam@chatowl.com"
os.environ["PASS"] = "ghrh fbxp zqwo srqa"


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
