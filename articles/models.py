from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, \
                # default=timezone.now, \
                null=True, blank=True) # top allow empty values

    def save(self, *args, **kwargs):
        # if self.slug is None:
        #     self.slug = slugify(self.title) # beware of nonunique titles!
        super().save(*args, **kwargs)
        # super().save(*args, **kwargs) is equivalent to:
        # obj = Article.object.get(id=1)
        # obj.save()
    
def article_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    print(sender, instance)
    if instance.slug is None:
        instance.slug = slugify(instance.title)

pre_save.connect(article_pre_save, sender=Article)
# alternatively with the reveiver decorator

def article_post_save(sender, instance, created, *args, **kwargs):
    print('post_save')
    print(args, kwargs)
    if created: # we need a bool like this to stop recursively & endlessly calling
        instance.slug = "this is my slug"
        instance.save()


post_save.connect(article_post_save, sender=Article)