import cPickle

from django.db import models
from backends.email import EmailBackend

class EnqueuedEmailNotice(models.Model):
    # This is not in the same database as users : we identify users by emails
    sent = models.BooleanField()
    context = models.TextField()
    content = models.TextField()

    @staticmethod
    def queue(receiver, notification_content_provider, notification_context_provider):
        receiver_info = {
            'receiver': {
                'email': receiver.email,
                'first_name': receiver.first_name,
                'last_name': receiver.last_name,
                'username': receiver.username
            }
        }
        notification_context = notification_context_provider.get_context()
        notification_context.update(receiver_info)
        nq_notice = EnqueuedEmailNotice(sent=False,
                                        context=cPickle.dumps(notification_context),
                                        content=notification_content_provider.get_content()
                                        )
        nq_notice.save()

        print cPickle.loads(nq_notice.context)

        return nq_notice

    @staticmethod
    def send_all_and_forget():
        email_backend = EmailBackend(1)
        for email_notice in EnqueuedEmailNotice.objects.all():
            context = cPickle.loads(email_notice.context.__str__())
            context['content'] = email_notice.content
            nb_sent = email_backend.deliver(recipient=context['receiver']['email'],
                                            sender=context['emitter']['email'],
                                            notice_label=context['notice_type'],
                                            extra_context=context)
            if nb_sent > 0:
                email_notice.delete()


class EnqueuedAppNotice(models.Model):
    seen = models.BooleanField()
    context = models.TextField()
    content = models.TextField()