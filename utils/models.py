import json

from django.db import models


# Create your models here.
DEFAULT_TAG_LIST_FILE = "tags.json"


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

    def raw(self):
        return self.tag.strip().replace(" ", "_")

    def populate_from_json(json_file):
        with open(json_file, 'r') as data_file:
            data = json.load(data_file)

        for tag_name in data:
            Tag(tag=tag_name).save()


