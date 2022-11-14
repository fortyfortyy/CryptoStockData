from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site

#  imports needed for email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import UserProfile
from users.utils import account_token, send_html_mail
# from users.utils import send_html_mail

from templated_email import get_templated_mail


@receiver(post_save, sender=UserProfile)
def send_activate_link_account(sender, instance, created, **kwargs) -> None:
    """
    Send activation account link to the given user's email.
    """
    profile = instance
    if not profile.is_active and created:
        current_domain = Site.objects.get_current().domain
        email_template = get_templated_mail(
            template_name='activate_account_email.html',
            from_email=settings.EMAIL_HOST_USER,
            to=[profile.email],
            context={
                'profile': profile,
                'domain': current_domain,
                'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
                'token': account_token.make_token(profile),
            },
            template_prefix="emails/",
            template_suffix="html",
        )
        send_html_mail(email_template)
