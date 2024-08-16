from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.user.tasks import send_verification_email
from apps.notification.models import Notification
from apps.user.models import User, Follow
from apps.user.utils import generate_code
from food_recipe import settings


@receiver(post_save, sender=Follow)
def create_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.following,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            title='New Follower',
            message=f"You have been followed by {instance.following.username}",
        )


@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    if created:
        code = generate_code()
        cache.set(f"{instance.pk}", code, timeout=300)  # Store the code in Redis
        redirect_url = f"http://127.0.0.1:8000/api/v0/user/verify-code?code={code}&user_id={instance.pk}"

        subject = "Verify your email!"
        message = f"Verify code: {code}\nURL: {redirect_url}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]

        send_verification_email.delay(subject, message, from_email, recipient_list)
