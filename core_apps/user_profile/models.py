from django.db import models
from typing import Any
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel
from django.conf import settings
User = get_user_model()

# Create your models here.


class Profile(TimeStampedModel):
    class Salutations(models.TextChoices):
        MR = ("mr", _("Mr"),)
        MRS = ("mrs", _("Mrs"),)
        MS = ("ms", _("Ms"),)

    class Gender(models.TextChoices):
        MALE = ("male", _("Male"),)
        FEMALE = ("female", _("Female"),)
        OTHER = ("other", _("Other"),)

    class MaritalStatus(models.TextChoices):
        SINGLE = ("single", _("Single"),)
        MARRIED = ("married", _("Married"),)
        DIVORCED = ("divorced", _("Divorced"),)
        WIDOWED = ("widowed", _("Widowed"),)
        SEPARATED = ("separated", _("Separated"),)
        UNKNOWN = ("unknown", _("Unknown"),)

    class IdentificationMeans(models.TextChoices):
        NATIONAL_ID = ("national_id", _("National ID"),)
        PASSPORT = ("passport", _("Passport"),)
        DRIVER_LICENSE = ("drivers_license", _("Drivers License"),)

    class EmploymentStatus(models.TextChoices):
        EMPLOYED = ("employed", _("Employed"),)
        UNEMPLOYED = ("unemployed", _("Unemployed"),)
        SELF_EMPLOYED = ("self_employed", _("Self Employed"),)
        RETIRED = ("retired", _("Retired"),)
        STUDENT = ("student", _("Student"),)
        OTHER = ("other", _("Other"),)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    title = models.CharField(
        _("Salutation"), choices=Salutations.choices, default=Salutations.MR, max_length=5)
    gender = models.CharField(
        _("Gender"), choices=Gender.choices, default=Gender.MALE, max_length=10)
    date_of_birth = models.DateTimeField(
        _("Date of Birth"), default=settings.DEFAULT_BIRTH_DATE)

    country_of_birth = CountryField(
        _("Country of Birth"), default=settings.DEFAULT_COUNTRY, blank=True, null=True
    )
    place_of_birth = models.CharField(
        _("Place of Birth"), max_length=100, blank=True, null=True
    )
    marital_status = models.CharField(
        _("Marital Status"), default=MaritalStatus.UNKNOWN, max_length=20
    )
    means_of_identification = models.CharField(
        _("Means of Identification"),
        choices=IdentificationMeans.choices,
        default=IdentificationMeans.NATIONAL_ID,
        max_length=20,
    )
    id_issue_date = models.DateField(
        _("ID or passport Issue Date"), default=settings.DEFAULT_DATE
    )
    id_expiry_date = models.DateField(
        _("ID or passport Expiry Date"), default=settings.DEFAULT_EXPIRY_DATE
    )
    passport_number = models.CharField(
        _("Passport Number"), max_length=20, blank=True, null=True
    )
    nationality = models.CharField(
        _("Nationality"), max_length=30, default="Unkown"
    )
    phone_number = PhoneNumberField(
        _("Phone Number"),
        default=settings.DEFAULT_PHONE_NUMBER,
        max_length=20,
        region=settings.DEFAULT_COUNTRY
    )
    address = models.CharField(
        _("Address"), max_length=255, default="Unknown Address"
    )
    city = models.CharField(
        _("City"), max_length=100, default="Unknown City"
    )
    country = CountryField(_("Country"), default=settings.DEFAULT_COUNTRY)
    employment_status = models.CharField(
        _("Employment Status"), choices=EmploymentStatus.choices, default=EmploymentStatus.SELF_EMPLOYED, max_length=20)
    employer_name = models.CharField(
        _("Employer Name"), max_length=100, blank=True, null=True)
    annual_income = models.DecimalField(
        _("Annual Income"), max_digits=12, decimal_places=2, default=0.00)
    date_of_employment = models.DateField(
        _("Date of Employment"), default=settings.DEFAULT_DATE)
    employer_address = models.CharField(
        _("Employer Address"), max_length=255, blank=True, null=True)
    employer_city = models.CharField(
        _("Employer City"), max_length=100, blank=True, null=True)
    employer_country = CountryField(
        _("Employer Country"), default=settings.DEFAULT_COUNTRY, blank=True, null=True
    )
    employer_phone_number = PhoneNumberField(
        _("Employer Phone Number"),
        max_length=20,
        blank=True,
        null=True,
        region=settings.DEFAULT_COUNTRY
    )
    photo = CloudinaryField(
        "photo",
        blank=True,
        null=True
    )
    photo_url = models.URLField(
        _("Photo URL"), blank=True, null=True, max_length=255)

    id_photo = CloudinaryField(
        "ID Photo",
        blank=True,
        null=True
    )
    id_photo_url = models.URLField(
        _("ID Photo URL"), blank=True, null=True, max_length=255)
    signature_photo = CloudinaryField(
        "Signature Photo",
        blank=True,
        null=True
    )
    signature_photo_url = models.URLField(
        _("Signature Photo URL"), blank=True, null=True, max_length=255)

    def clean(self) -> None:
        super().clean()
        if self.id_issue_date and self.id_expiry_date:
            if self.id_expiry_date <= self.id_issue_date:
                raise ValidationError(
                    _("ID issue date must be before the expiry date."))

    def save(self, *args: Any, **Kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **Kwargs)

    def is_complete_with_next_of_kin(self):
        required_fields = [
            self.title,
            self.gender,
            self.date_of_birth,
            self.country_of_birth,
            self.place_of_birth,
            self.marital_status,
            self.means_of_identification,
            self.id_issue_date,
            self.id_expiry_date,
            self.nationality,
            self.phone_number,
            self.address,
            self.city,
            self.country,
            self.employment_status,
            self.photo,
            self.id_photo,
            self.signature_photo,
        ]

        return all(required_fields) and self.next_of_kin.exists()

    def __str__(self) -> str:
        return f"{self.title} {self.user.first_name}'s Profile"


class NextOfKin(TimeStampedModel):
    class Salutation(models.TextChoices):
        MR = (
            "mr",
            _("Mr"),
        )
        MRS = (
            "mrs",
            _("Mrs"),
        )
        MISS = (
            "miss",
            _("Miss"),
        )

    class Gender(models.TextChoices):
        MALE = (
            "male",
            _("Male"),
        )
        FEMALE = (
            "female",
            _("Female"),
        )

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="next_of_kin"
    )
    title = models.CharField(
        _("Salutation"), max_length=5, choices=Salutation.choices)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    other_names = models.CharField(
        _("Other Names"), max_length=50, blank=True, null=True
    )
    date_of_birth = models.DateField(_("Date of Birth"))
    gender = models.CharField(
        _("Gender"), max_length=8, choices=Gender.choices)
    relationship = models.CharField(_("Relationship"), max_length=50)
    email_address = models.EmailField(_("Email Address"), db_index=True)
    phone_number = PhoneNumberField(_("Phone Number"))
    address = models.CharField(_("Address"), max_length=100)
    city = models.CharField(_("City"), max_length=50)
    country = CountryField(_("Country"))
    is_primary = models.BooleanField(
        _("Is Primary Next of Kin"), default=False)

    # ensure there is only one primary next of kin per profile
    def clean(self) -> None:
        super().clean()
        if self.is_primary:
            primary_kin = NextOfKin.objects.filter(
                profile=self.profile, is_primary=True
            ).exclude(pk=self.pk)
            if primary_kin.exists():
                raise ValidationError(
                    _("There can only be one primary next of kin."))

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - Next of Kin for {self.profile.user.full_name}"

#    # Meta class to ensure unique primary next of kin per profile
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "is_primary"],
                condition=models.Q(is_primary=True),
                name="unique_primary_next_of_kin",
            )
        ]
