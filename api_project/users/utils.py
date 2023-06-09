from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from api_project.common.email import send_email
from api_project.common.utils import encode_uid


def send_welcome_email(user):
    """
    Send a welcome email to a new user
    """

    # Example template id and dynamic data for sendgrid
    # https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates
    template_id = "d-5ae50cec5e064a6693674ca85edc3ddb"
    dynamic_template_data = {
        "fullname": user.name,
    }
    return send_email(user, template_id, dynamic_template_data)


def send_password_reset(user):
    """
    Send password reset
    """

    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)

    # Example template id and dynamic data for sendgrid
    # https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates
    template_id = "d-277b429b15e3459cb2cb668f5b9374a3"
    dynamic_template_data = {
        "url": f"{settings.PASSWORD_RESET_FRONTEND_URL}#{uid}/{token}",
        "fullname": user.name,
    }
    return send_email(user, template_id, dynamic_template_data)
