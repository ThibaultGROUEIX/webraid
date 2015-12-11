from django.db import models
from django.core.urlresolvers import reverse

from utils.snippets.slugifiers import unique_slugify
from profiles.models import UserProfile
from utils.models import Tag


# Create your models here.

class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum.views.thread_category_detail', args=[self.slug])

    def save(self, **kwargs):
        unique_slugify(self, self.name)
        super(ThreadCategory, self).save(**kwargs)


class Thread(models.Model):
    category = models.ForeignKey(ThreadCategory)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        slug_category = self.category.slug
        return reverse('forum.views.thread_detail', args=[slug_category, self.slug])

    def save(self, **kwargs):
        unique_slugify(self, self.title)
        super(Thread, self).save(**kwargs)

    @staticmethod
    def get_last_threads_posted_in(limit=1):
        thread_with_last_posted_date = []
        for thread in Thread.objects.all():
            last_post = Post.objects.filter(thread=thread).order_by('-posted_date')[:1]
            if last_post is not None:
                thread_with_last_posted_date.append(
                    {
                        'thread': thread,
                        'last_posted_date': last_post[0].posted_date
                    }
                )
        thread_with_last_posted_date.sort(key=lambda x: x['last_posted_date'], reverse=True)
        return thread_with_last_posted_date[:limit]

    @staticmethod
    def get_last_threads_posted_in_with_posts(threads_limit=1, posts_limit=1):
        thread_with_last_posted_date = []
        for thread in Thread.objects.all():
            last_posts = Post.objects.filter(thread=thread).order_by('-posted_date')
            lp_len = last_posts.__len__()
            if (last_posts is not None) and (lp_len > 0):
                thread_with_last_posted_date.append(
                    {
                        'thread': thread,
                        'last_posted_date': last_posts[1].posted_date,
                        'first_posts': last_posts[(lp_len - posts_limit):lp_len]
                    }
                )
        thread_with_last_posted_date.sort(key=lambda x: x['last_posted_date'], reverse=True)
        return thread_with_last_posted_date[:threads_limit]


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    # Contenu
    text_content = models.TextField()
    author = models.ForeignKey(UserProfile)
    posted_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    # File uploads
    file = models.FileField()

    @staticmethod
    def get_last_posts_by_author_with_answers(user, posts_limit=1, answers_limit=0):
        post_and_answers = []
        posts_retrieved = 0
        for thread in Thread.objects.all():
            for post in Post.objects.filter(thread=thread, author=user.user_profile).order_by('-posted_date')[:1]:
                answers = Post.objects \
                              .filter(thread=post.thread).exclude(author=user.user_profile) \
                              .filter(posted_date__gte=post.posted_date).order_by('posted_date')[:answers_limit]
                post_and_answers.append({'date': post.posted_date, 'post': post, 'answers': answers})
                posts_retrieved += 1
                if posts_limit == posts_retrieved:
                    post_and_answers.sort(key=lambda x: x['date'], reverse=True)
                    return post_and_answers

        post_and_answers.sort(key=lambda x: x['date'], reverse=True)
        return post_and_answers

    @staticmethod
    def get_last_posts(last_posts_no=1):
        return Post.objects.all().order_by('-posted_date')[:last_posts_no]
