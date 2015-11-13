from django import forms

from models import ThreadCategory, Thread, Post
from utils.models import Tag


class ThreadCategoryForm(forms.ModelForm):
    description = forms.CharField(required=False,
                                  widget=forms.Textarea)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          required=False)

    class Meta:
        model = ThreadCategory
        fields = (
            'name',
            'description',
            'tags'
        )


class ThreadForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          required=False)

    class Meta:
        model = Thread
        fields = (
            'title',
            'tags'
        )


class PostForm(forms.ModelForm):
    file = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          required=False)

    class Meta:
        model = Post
        fields = (
            'text_content',
            'file'
        )
