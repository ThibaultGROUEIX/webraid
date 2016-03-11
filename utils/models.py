import json
import re

from django.db import models
from django.core.urlresolvers import reverse

DEFAULT_TAG_LIST_FILE = "tags.json"


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('show_tag', args=[self.tag])

    def normalized_save(self):
        self.tag = self.tag.strip().replace(" ", "_")
        self.save()
        return self

    @staticmethod
    def extract(text_content):
        tags = []
        for word in re.findall(r"#(\w+)", text_content):
            try:
                tags.append(Tag.objects.get(tag=word))
            except Tag.DoesNotExist:
                tags.append(Tag(tag=word).normalized_save())
        return tags

    @staticmethod
    def populate_from_json(json_file):
        with open(json_file, 'r') as data_file:
            data = json.load(data_file)

        for tag_name in data:
            Tag(tag=tag_name).save()

