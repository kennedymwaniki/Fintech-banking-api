from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .emails import send_account_locked_email
from .managers import UserManager

# Create your models here.


class User(AbstractUser):
    class SecurityQuestions(models.TextChoices):
        MAIDEN_NAME = (
            "maiden_name",
            _("what is your mother's maiden name?")
        )
        FAVORITE_COLOR = (
            "favorite_color",
            _("what is favorite color?")
        )
        BIRTH_CITY = (
            "birth_city",
            _("what is the name of the city you were born?")
        )
        CHILDHOOD_FRIEND = (
            "childhood_frient",
            _("what is the name of your childhood friend?")
        )

    class AccountStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        Locked = "locked", _("locked")

    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        ACCOUNT_EXECUTIVE = "account_executive", _("Account Executive")
        TELLER = "teller", _("Teller")
        BRANCH_MANAGER = "branch_manager", _("Branch Manager")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("Username"), max_length=150, unique=True)
    security_questions = models.Charfield(
        _("Security Questions"),
        max_length=30,
        choices=SecurityQuestions.choices,
    )
    security_answer = models.CharField(_("Security Answer"), max_length=20)
    email = models.EmailField(_("email"), unique=True, db_index=True)
    first_name = models.CharField(_("First Name"), max_length=30)
    middle_name = models.CharField(_("Middle Name"), max_length=30, blank=True)
    lat_name = models.CharField(_("Last Name"), max_length=30)
    id_number = models.CharField(_("ID Number"), unique=True)
    account_status = models.CharField(
        _("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE

    )
    role = models.CharField(_("Role"), max_length=30,
                            choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    otp = models.CharField(_('OTP'), max_length=6, blank=True)
    otp_expiry_time = models.DateTimeField(
        _("OTP Expiry Time"), null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        'first_name',
        "last_name",
        "id_no"
        "security_question",
        "security_answer"
    ]

    def det_otp(self, otp: str) -> None:
        self.otp = otp
        self.otp_expiry_time = timezone.mow() + settings.OTP_EXPIRATION
        self.save()

    def verify_otp(self, otp: str) -> bool:
        # check if otp is correct and has not expired
        if self.otp == otp and self.otp_expiry_time > timezone.now():
            # once used it is cleared
            self.otp = ""
            self.otp_expiry_time = None
            self.save()
            return True
        return False
