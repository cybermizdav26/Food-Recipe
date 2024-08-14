from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from apps.user.models import User
from apps.user.utils import generate_code


@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    code = generate_code()
    cache.set(f"{instance.pk}", code, timeout=90)
    redirect_url = f"http://127.0.0.1:8000/api/v0/user/verify-code?code={code}&user_id={instance.pk}"

    subject = "Verify your email!"
    message = f"Verify code: {code} url: {redirect_url}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [instance.email]

    send_mail(subject, message, from_email, recipient_list)