from django.db import models

from inuits.models import BaseModel, ListField


class Mail(BaseModel):

    subject = models.CharField()
    body = models.TextField()
    from_email = models.CharField()
    to = ListField()
    cc = ListField()
    bcc = ListField()
    reply_to = models.CharField
    attachment_paths = ListField()
    template_id = models.CharField()

    def __init__(
        self,
        subject: str = "",
        body: str = "",
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
        template_id=None,
    ):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to
        self.attachment_paths = attachment_paths
        self.template_id = template_id
