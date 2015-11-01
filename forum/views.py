from django.views.generic import ListView

from models import ThreadCategory


class ThreadCategoryListView(ListView):
    model = ThreadCategory
    template_name = "forum.html"
