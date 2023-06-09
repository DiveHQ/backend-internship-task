from django.conf import settings
from django.core.mail import EmailMessage


def send_email(
    user, template_id: str, dynamic_template_data: dict = None, fail_silently=True
):
    """
    Helper to send emails system wide.
    Special consideration made for sendgrid's dynamic templating.

    https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates
    """
    msg = EmailMessage(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )
    msg.template_id = template_id

    if dynamic_template_data:
        msg.dynamic_template_data = dynamic_template_data

    return msg.send(fail_silently=fail_silently)
