import base64
import cPickle

from django.db import models

from backends.email_backend import EmailBackend


class EnqueuedEmailNotice(models.Model):
    # This is not in the same database as users : we identify users by emails
    sent = models.BooleanField()
    async_rt = models.BooleanField()
    in_daily_digest = models.BooleanField()
    in_weekly_digest = models.BooleanField()
    context = models.TextField()
    content = models.TextField()

    @staticmethod
    def enqueue(receiver, notification_context_provider,
              in_rt, in_daily_digest, in_weekly_digest):
        """
        Enqueue an email notice in the notification database for further handling
        :param receiver:
        :param notification_context_provider: an instance of a class extending the
            NotificationContextProviderMixin
        :param in_rt: boolean, if notice should be sent asap
        :param in_daily_digest: if notice should be included in daily digest
        :param in_weekly_digest: if notice should be included in weekly digest
        """
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
                                        context=base64.b64encode(cPickle.dumps(notification_context)),
                                        content=notification_context_provider.get_content(),
                                        async_rt=in_rt,
                                        in_daily_digest=in_daily_digest,
                                        in_weekly_digest=in_weekly_digest
                                        )
        print nq_notice.context

        nq_notice.save()

        return nq_notice

    @staticmethod
    def send_all_immediate():
        email_backend = EmailBackend(1)
        for email_notice in EnqueuedEmailNotice.objects.all():
            context = cPickle.loads(base64.b64decode(email_notice.context.__str__()))
            context['content'] = email_notice.content
            nb_sent = email_backend.deliver(recipient=context['receiver']['email'],
                                            sender=context['emitter']['email'],
                                            notice_label=context['notice_type'],
                                            extra_context=context)

            print "Messages snt :" + str(nb_sent)
            if nb_sent > 0:
                email_notice.sent = True
                if not (email_notice.in_daily_digest or email_notice.in_weekly_digest):
                    email_notice.delete()

    @staticmethod
    def send_daily_digest():
        pass

    @staticmethod
    def send_weekly_digest():
        pass


class EnqueuedAppNotice(models.Model):
    seen = models.BooleanField()
    context = models.TextField()
    content = models.TextField()
