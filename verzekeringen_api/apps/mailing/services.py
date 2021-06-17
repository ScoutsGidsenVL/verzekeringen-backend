from django.core.mail import EmailMessage

# Example method that might be handy when sending send in blue emails
# Not tested but should work
def sendTemplateEmail(*, receivers: list, template_id: int, data: dict = {}):
    message = EmailMessage(to=receivers)
    message.template_id = template_id  # use Sendinblue template
    message.from_email = None  # to use the template's default sender
    message.merge_global_data = data

    try:
        message.send()
    except:
        # Actually do something when this fails
        print("Mail could not be sent")
