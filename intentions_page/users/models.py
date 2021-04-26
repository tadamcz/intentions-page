from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save

class User(AbstractUser):
    """Default user for intentions page."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    '''
    https://stackoverflow.com/a/27458036/
    '''
    user_email = instance.email
    username = user_email

    n = 1
    while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        n += 1
        username = user_email + '-' + str(n)

    instance.username = username
