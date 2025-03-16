from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger


def send_otp_email(email, otp):
    subject = _("Your otp code for Login")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "otp": otp,
        "expiry_time": settings.OTP_EXPIRATION,
        "site_name": settings.SITE_NAME
    }
    html_email = render_to_string("emails/otp_email.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(
        subject, plain_email, from_email, recipient_list)
    email.attatch_alternatives(html_email, "text/html")

    try:
        email.send()
        logger.info(f"OTP email sent to {email} successfully")

    except Exception as e:
        logger.error(f"failed to send OTP email to {email}: Error str(e) ")


def send_account_locked_email(self):
    subject = _("Your account has been locked")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [self.email]
    context = {
        "User": self,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        "site_name": settings.SITE_NAME
    }
    html_email = render_to_string("emails/account_locked.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(
        subject, plain_email, from_email, recipient_list)
    email.attatch_alternatives(html_email, "text/html")

    try:
        email.send()
        logger.info(f"Account Locked enail sent to {self.email} successfully")

    except Exception as e:
        logger.error(
            f"failed to send Account locked email to {self.email}: Error str(e) ")
