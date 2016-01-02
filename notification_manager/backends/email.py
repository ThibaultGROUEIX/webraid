# coding=UTF-8

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

        subject = ""
        body = ""
        if notice_label is 'new_post':
            subject, body = render_new_post_body(context)

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])


def render_new_post_body(context):
    body = render_to_string(
        'email/notifications/new_post.html',
        {
            'recipient_first_name': context.recipient.first_name,
            'recipient_last_name': context.recipient.last_name,
            'emitter_first_name': context.emitter.first_name,
            'emitter_last_name': context.emitter.last_name,
            'content': context.content,
            'date': context.date
        }
    )
    subject = context.sender_fullname + u" a posté dans " + context.thread_name

    return subject, body
