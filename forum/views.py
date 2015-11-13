from django.views.generic import ListView, FormView
from django.http import Http404
from django.shortcuts import redirect, render
from django.forms.models import model_to_dict

from profiles.models import UserProfile
from models import ThreadCategory, Thread, Post
from forms import ThreadCategoryForm, ThreadForm, PostForm


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


def thread_category_detail(request, slug):
    try:
        thread_category = ThreadCategory.objects.get(slug=slug)
        thread_list = Thread.objects.filter(category=thread_category.pk)
    except ThreadCategory.DoesNotExist:
        raise Http404("Thread category does not exist!")

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.category = thread_category
            thread.save()

            return redirect(thread_category.get_absolute_url())
        else:
            return render(request,
                          'thread_category.html',
                          {
                              'thread_category': thread_category,
                              'thread_list': thread_list,
                              'form': form,
                              'slug': slug,
                          })

    form = ThreadForm()
    return render(request,
                  'thread_category.html',
                  {
                      'thread_category': thread_category,
                      'thread_list': thread_list,
                      'form': form,
                      'slug': slug,
                  })


def thread_detail(request, category_slug, slug, pk=None):
    if pk is not None:
        edit_post = Post.objects.get(pk=pk)
    else:
        edit_post = None

    try:
        thread = Thread.objects.get(slug=slug)
        post_list = Post.objects.filter(thread=thread.pk)
    except Thread.DoesNotExist:
        raise Http404("Thread does not exist!")

    if request.method == 'POST':

        if 'edit-post' in request.POST:
            edit_post_form = PostForm(request.POST, instance=edit_post)

            if edit_post_form.is_valid():
                edit_post_form.save()
                return redirect(thread.get_absolute_url())
            else:
                return render(request,
                              'thread.html',
                              {
                                  'thread': thread,
                                  'post_list': post_list,
                                  'edit_post_form': edit_post_form,
                                  'category_slug': category_slug,
                                  'slug': slug,
                                  'pk': edit_post.pk,
                                  'edit_post': edit_post,
                              })

        elif 'new-post' in request.POST:
            form = PostForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.author = UserProfile.objects.get(user=request.user)
                post.thread = thread
                post.save()

                return redirect(thread.get_absolute_url())
            else:
                return render(request,
                              'thread.html',
                              {
                                  'thread': thread,
                                  'post_list': post_list,
                                  'form': form,
                                  'slug': slug,
                                  'category_slug': category_slug,
                                  'edit_post': edit_post,
                              })

    if edit_post is not None:
        edit_post_form = PostForm(instance=edit_post)

        return render(request,
                      'thread.html',
                      {
                          'thread': thread,
                          'post_list': post_list,
                          'form': PostForm(),
                          'slug': slug,
                          'category_slug': category_slug,
                          'pk': edit_post.pk,
                          'edit_post': edit_post,
                          'edit_post_form': edit_post_form,
                      })
    else:
        return render(request,
                      'thread.html',
                      {
                          'thread': thread,
                          'post_list': post_list,
                          'form': PostForm(),
                          'slug': slug,
                          'category_slug': category_slug,
                      })
