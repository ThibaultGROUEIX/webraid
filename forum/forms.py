from django import forms

from models import ThreadCategory, Thread, Post


class ThreadCategoryForm(forms.ModelForm):
    description = forms.CharField(required=False,
                                  widget=forms.Textarea)

    class Meta:
        model = ThreadCategory
        fields = (
            'name',
            'description',
            'tags'
        )


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = (
            'title',
            'tags'
        )


class PostForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = (
            'text_content',
            'file'
        )
