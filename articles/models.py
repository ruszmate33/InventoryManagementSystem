from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone

from .utils import slugify_instance_title

# Create your models here.

User = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    # if we want to be able to do e.g.: qs = Article.objects.filter(title__icontains='t').search(query=query)
    # we need to define its own custom QS like this
    def search(self, query=None):
        if query is None or query == "":
            return self.none() # []
       
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, \
                # default=timezone.now, \
                null=True, blank=True) # top allow empty values

    objects = ArticleManager()

    def get_absolute_url(self):
        # return f'/articles/{self.slug}/'
        return reverse("article-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # if self.slug is None:
        #     self.slug = slugify(self.title) # beware of nonunique titles!
        # if self.slug is None:
        #     slugify_instance_title(self, save=False)
        super().save(*args, **kwargs)
        # super().save(*args, **kwargs) is equivalent to:
        # obj = Article.object.get(id=1)
        # obj.save()
   
def article_pre_save(sender, instance, *args, **kwargs):
    # print('pre_save')
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)
# alternatively with the reveiver decorator

def article_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    if created: # we need a bool like this to stop recursively & endlessly calling
        slugify_instance_title(instance, save=True)


post_save.connect(article_post_save, sender=Article)