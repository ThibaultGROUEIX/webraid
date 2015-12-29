import cPickle
import base64

from django.db import models

from .backends.email import EmailBackend


class EnqueuedEmailNotice(models.Model):
    # This is not in the same database as users : we identify users by emails
    sent = models.BooleanField()
    context = models.TextField()
    content = models.TextField()
    extra_context = models.TextField()

    @staticmethod
    def queue(send_to_user, sender_user, notice_label, content, extra_context):
        context = {
            'recipient_email': send_to_user.email,
            'recipient_username': send_to_user.username,
            'recipient_fullname': " ".join([send_to_user.firstname, send_to_user.lastname]),
            'sender_fullname': " ".join([sender_user.firstname, sender_user.lastname]),
            'notice_label': notice_label
        }
        EnqueuedEmailNotice(sent=False,
                            context=base64.b64encode(cPickle.dumps(context)),
                            content=content,
                            extra_context=base64.b64decode(cPickle.dumps(extra_context))
                            ).save()

    @staticmethod
    def send_all_and_forget():
        email_backend = EmailBackend(1)
        for email_notice in EnqueuedEmailNotice.objects.all():
            context = cPickle.loads(base64.b64decode(email_notice.context))
            extra_context = cPickle.loads(base64.b64decode(email_notice.extra_context))
            context_copy = context.copy()
            extras = extra_context.update(context_copy)
            nb_sent = email_backend.deliver(recipient=context['recipient_email'],
                                            sender=context['sender_email'],
                                            notice_label=context['notice_label'],
                                            extra_context=extras)
            if nb_sent > 0:
                email_notice.delete()


class EnqueuedAppNotice(models.Model):
    seen = models.BooleanField()
    content = models.TextField()
