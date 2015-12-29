from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .base import BaseBackend


class EmailBackend(BaseBackend):
    spam_sensitivity = 2

    def deliver(self, recipient, sender, notice_label, extra_context):
        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender
        })
        context.update(extra_context)

        messages = self.get_formatted_messages((
            "short.txt",
            "full.txt"
        ), notice_label, context)

        subject = "".join(render_to_string('email/notification_subject.txt', context).splitlines())

        body = render_to_string("email/notification.html", {
            "message": messages["full.txt"],
        }, context)

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
