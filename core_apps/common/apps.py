from django.apps import AppConfig
# the line below is used as a translation service should i decide my app will support or be availbale in various countries
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.common"
    verbose_name = _("Common")
