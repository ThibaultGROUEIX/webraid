# coding=UTF-8

from email.mime.image import MIMEImage
import os

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from webraid import settings

from .base import BaseBackend


class EmailBackend(BaseBackend):
    HEADER_IMAGE = os.path.join(settings.BASE_DIR, 'static/images/banner_mail_600.png')
    spam_sensitivity = 2

    def deliver(self, recipient, sender, notice_label, extra_context):
        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender
        })
        context.update(extra_context)
        print "notice label :" + notice_label

        subject = ""
        html_body = ""

        if notice_label == "post_new":
            subject, html_body = render_new_post_body(extra_context)

        print subject

        msg = EmailMultiAlternatives(subject,
                                     extra_context['content'],
                                     settings.EMAIL_HOST_USER,
                                     [recipient])

        msg.attach_alternative(html_body, mimetype='text/html')

        # Header image of email
        msg.mixed_subtype = 'related'
        fp = open(self.HEADER_IMAGE, 'rb')

        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<banner>')
        msg.attach(msg_img)

        return msg.send()


def render_new_post_body(context):
    rendering_context = {
        'recipient_first_name': context['receiver']['first_name'],
        'recipient_last_name': context['receiver']['last_name'],
        'emitter_first_name': context['emitter']['first_name'],
        'emitter_last_name': context['emitter']['last_name'],
        'content': context['content'],
        'date': context['date']
    }

    body = render_to_string(
        'email/notifications/new_post.html',
        rendering_context)

    subject = context['emitter']['first_name'] + u" a posté dans " + context['parent']['name']

    return subject, body
