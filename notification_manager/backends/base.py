from django.template import Context
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from webraid import settings


class BaseBackend(object):
    """
    The base backend.
    """

    def __init__(self, medium_id, spam_sensitivity=None):
        self.medium_id = medium_id
        if spam_sensitivity is not None:
            self.spam_sensitivity = spam_sensitivity

    def deliver(self, recipient, sender, notice_label, extra_context):
        """
        Deliver a notification to the given recipient.
        """
        raise NotImplementedError()

    @staticmethod
    def get_formatted_messages(formats, label, context):
        """
        Returns a dictionary with the format identifier as the key. The values are
        are fully rendered templates with the given context.
        """
        format_templates = {}
        for fmt in formats:
            # conditionally turn off autoescaping for .txt extensions in format
            if fmt.endswith(".txt"):
                context.autoescape = False
            format_templates[fmt] = render_to_string((
                "pinax/notifications/{0}/{1}".format(label, fmt),
                "pinax/notifications/{0}".format(fmt)), context)
        return format_templates

    @staticmethod
    def default_context():
        use_ssl = getattr(settings, "PINAX_USE_SSL", False)
        default_http_protocol = "https" if use_ssl else "http"
        current_site = Site.objects.get_current()
        base_url = "{0}://{1}".format(default_http_protocol, current_site.domain)
        return Context({
            "default_http_protocol": default_http_protocol,
            "current_site": current_site,
            "base_url": base_url
        })
