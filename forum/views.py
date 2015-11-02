from django.views.generic import ListView, FormView
from django.http import Http404
from django.shortcuts import render_to_response, redirect

from models import ThreadCategory, Thread, Post
from forms import ThreadCategoryForm, ThreadForm


class ThreadCategoryListView(ListView):
    model = ThreadCategory
    template_name = "forum.html"


class AddThreadCategoryView(FormView):
    template_name = 'forms/thread_category_form.html'
    form_class = ThreadCategoryForm
    success_url = '/forum/'

    def form_valid(self, form):
        form.save()
        return super(AddThreadCategoryView, self).form_valid(form)


class AddThreadView(FormView):
    template_name = 'forms/thread_form.html'
    form_class = ThreadForm
    success_url = '/forum/'

    def form_valid(self, form):
        thread = form.save()
        super(AddThreadView, self).form_valid(form)

        return redirect(thread.get_absolute_url())



def thread_category_detail(request, slug):
    try:
        thread_category = ThreadCategory.objects.get(slug=slug)
        thread_list = Thread.objects.filter(category=thread_category.pk)
    except ThreadCategory.DoesNotExist:
        raise Http404("Thread category does not exist!")
    return render_to_response('thread_category.html',
                              {
                                  'thread_category': thread_category,
                                  'thread_list': thread_list
                              }
                              )


def thread_detail(request, slug):
    try:
        thread = Thread.objects.get(slug=slug)
        post_list = Post.objects.filter(thread=thread.pk)
    except Thread.DoesNotExist:
        raise Http404("Thread does not exist!")
    return render_to_response('thread.html',
                              {
                                  'thread': thread,
                                  'post_list': post_list
                              })
