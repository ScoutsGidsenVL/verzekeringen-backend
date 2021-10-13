# from django.db import models

# from inuits.models import BaseModel, ListField
from inuits.files import FileService


class EmailAttachment:
    file_path: str = None
    file_service: FileService = None

    def __init__(self, file_path: str, file_service: FileService = None):
        self.file_path = file_path
        self.file_service = file_service
    
    def as_attachment(self, file_dest_path: str = None):
        if self.file_service and file_dest_path:
            return self.file_service.as_attachment(self.file_path)
        
        return self.file_path


class Email:

    subject: str = ""
    body: str = ""
    from_email: str = None
    to: list = []
    cc: list = []
    bcc: list = []
    reply_to: str = None
    attachment_paths: list = []
    template_id: str = None
    attachments = []

    def __init__(
        self,
        subject: str = "",
        body: str = "",
        from_email: str = None,
        to: list = [],
        cc: list = [],
        bcc: list = [],
        reply_to: str = None,
        attachment_paths: list = [],
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
    
    def add_attachment(self, attachment: EmailAttachment):
        self.attachments.append(attachment)
    
    def has_attachments(self) -> bool:
        return len(self.attachments) > 0


# class Mail(BaseModel):

#     subject = models.CharField()
#     body = models.TextField()
#     from_email = models.CharField()
#     to = ListField()
#     cc = ListField()
#     bcc = ListField()
#     reply_to = models.CharField
#     attachment_paths = ListField()
#     template_id = models.CharField()

#     def __init__(
#         self,
#         subject: str = "",
#         body: str = "",
#         from_email: str = None,
#         to: list = None,
#         cc: list = None,
#         bcc: list = None,
#         reply_to: str = None,
#         attachment_paths: list = None,
#         template_id=None,
#     ):
#         self.subject = subject
#         self.body = body
#         self.from_email = from_email
#         self.to = to
#         self.cc = cc
#         self.bcc = bcc
#         self.reply_to = reply_to
#         self.attachment_paths = attachment_paths
#         self.template_id = template_id

