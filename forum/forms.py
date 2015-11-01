from django import forms
from django.utils.text import slugify

from models import ThreadCategory, Thread, Post


class AddThreadCategoryForm(forms.ModelForm):
    class Meta:
        model = ThreadCategory
        fields = (
            'name',
            'description',
            'tags'
        )

    # This form can be used for editing and creating ThreadCategory
    # If editing, we already have an instance, we don't modify the slug
    def save(self, commit=True):
        if self.instance.pk:
            return super(AddThreadCategoryForm, self).save()

        instance = super(AddThreadCategoryForm, self).save(commit=False)
        instance.slug = slugify(instance.name)
        instance.save()

        return instance


class AddThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = (
            'title',
            'tags',
            'category'
        )

    def save(self, commit=True):
        if self.instance.pk:
            return super(AddThreadForm, self).save()

        instance = super(AddThreadForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        instance.save()

        return instance


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'text_content',
            'file',
            'thread'
        )

    def save(self, commit=True):
        instance = super(AddPostForm, self).save(commit=False)
