import logging
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)


class MailService:
    # Example method that might be handy when sending send in blue emails
    # Not tested but should work
    def send_template_email(self, *, receivers: list, template_id: int, data: dict = {}, file: str = None):
        message = EmailMessage(to=receivers)
        message.template_id = template_id  # use Sendinblue template
        message.from_email = None  # to use the template's default sender
        message.merge_global_data = data

        if file:
            message.attach_file(file)

        try:
            logger.debug("Sending mail to (%s)", ", ".join(receivers))
            message.send()
        except Exception as e:
            print(e)
            # Actually do something when this fails
            print("Mail could not be sent")
