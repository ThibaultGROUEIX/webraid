from django.views.generic import ListView, FormView
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from profiles.models import UserProfile
from models import ThreadCategory, Thread, Post, UserTag, PostTag
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


def thread_category_detail(request, slug, pk=None):
    if pk is not None:
        edit_thread = Thread.objects.get(pk=pk)
    else:
        edit_thread = None

    try:
        thread_category = ThreadCategory.objects.get(slug=slug)
        thread_list = Thread.objects.filter(category=thread_category.pk)
    except ThreadCategory.DoesNotExist:
        raise Http404("Thread category does not exist!")

    data = {
        'thread_category': thread_category,
        'thread_list': thread_list,
        'form': ThreadForm(),
        'slug': slug,
    }

    if request.method == 'POST':
        if 'new-thread' in request.POST:
            form = ThreadForm(request.POST)
            if form.is_valid():
                thread = form.save(commit=False)
                thread.category = thread_category
                thread.save()

                return redirect(thread_category.get_absolute_url())
            else:
                data.update({'form': form})
                return render(request,
                              'thread_category.html',
                              data)

        elif 'edit-thread' in request.POST:
            edit_thread_form = ThreadForm(request.POST, instance=edit_thread)
            if edit_thread_form.is_valid():
                edit_thread_form.save()

                return redirect(thread_category.get_absolute_url())
            else:
                data.update({
                    'pk': edit_thread.pk,
                    'edit_thread_form': edit_thread_form,
                })
                return render(request,
                              'thread_category.html',
                              data)

    if edit_thread is not None:
        edit_thread_form = ThreadForm(instance=edit_thread)

        data['pk'] = edit_thread.pk
        data['edit_thread_form'] = edit_thread_form
        data['edit_thread'] = edit_thread

    return render(request, 'thread_category.html', data)


def thread_detail(request, category_slug, slug, pk=None):
    if pk is not None:
        edit_post = Post.objects.get(pk=pk)
        if edit_post.author.user != request.user:
            raise PermissionDenied
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
    data = {
        'thread': thread,
        'post_list': post_list,
        'form': PostForm(),
        'slug': slug,
        'category_slug': category_slug,
    }

    if edit_post is not None:
        edit_post_form = PostForm(instance=edit_post)
        data['edit_post_form'] = edit_post_form
        data['pk'] = edit_post.pk
        data['edit_post'] = edit_post
        return render(request, 'thread.html', data)
    else:
        return render(request, 'thread.html', data)

def thread_delete(request, slug):
    if request.user.is_superuser:
        thread = Thread.objects.get(slug=slug)
        thread.delete_with_posts()
    return redirect(request.META.get('HTTP_REFERER'))


def category_delete(request, slug):
    if request.user.is_superuser:
        category = ThreadCategory.objects.get(slug=slug)
        category.delete_recursive()
    return redirect(request.META.get('HTTP_REFERER'))


def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    parent = post.thread
    if request.user == post.author.user:
        post.delete()
        UserTag.objects.filter(post=post).delete()
        PostTag.objects.filter(post=post).delete()

    else:
        raise PermissionDenied

    return redirect(parent.get_absolute_url())
