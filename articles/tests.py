from django.test import TestCase
from django.utils.text import slugify

from .utils import slugify_instance_title

# Create your tests here.
from .models import Article

class ArticleTestCase(TestCase):    
    # you need to set a testDB this is created in setUp
    def setUp(self):
        self.num_entries = 500
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

    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for _ in range(25):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_slugify_instance_title_redux(self):
        slug_list = Article.objects.all().values_list('slug', flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_slug_list))

    #this is not created and return 0 ... check it
    # def test_user_added_slug_unique(self):
    #     obj = Article.objects.create(title='hello world', content="whatever")
    #     print(f"obj.slug is {obj.slug}")
    #     slug = obj.slug
    #     qs = Article.objects.filter(slug__exact=slug)
    #     self.assertEquals(qs.count(), 1)

    def test_article_search_manager(self):
        qs = Article.objects.search(query='hello world')
        self.assertEqual(qs.count(), self.num_entries)
        qs = Article.objects.search(query='hello')
        self.assertEqual(qs.count(), self.num_entries)
        qs = Article.objects.search(query='wonderfull')
        self.assertEqual(qs.count(), self.num_entries)