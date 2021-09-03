from django.test import TestCase

from .utils import slugify

# Create your tests here.
from .models import Article

class ArticleTestCase(TestCase):    
    # you need to set a testDB this is created in setUp
    def setUp(self):
        self.num_entries = 5
        for _ in range(self.num_entries):
            Article.objects.create(title='hello world', content='wonderfull')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.num_entries)

    def test_hello_world_slug(self):
        obj = Article.objects.all().order_by("id").first()
        title = obj.title
        slugified_title = slugify(title)
        slug = obj.slug
        self.assertEqual(slug, slugified_title)

    def test_hello_world_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            title = obj.title
            slugified_title = slugify(title)
            slug = obj.slug
            self.assertNotEqual(slug, slugified_title)        
