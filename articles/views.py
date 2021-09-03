from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.http import Http404
from django.shortcuts import render

from .models import Article
from .forms import ArticleForm

# Create your views here.
def article_search_view(request):
    query_dict = request.GET # this is a dictionary
    try:
        query = int(query_dict.get("query")) # <input type='text' name='query' />
    except:
        query = None
    article_obj = None
    if query is not None:
        article_obj = Article.objects.get(id=query)
    context = {
        "object": article_obj
    }
    return render(request, "articles/search.html", context=context)


@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None) # with None is a GET
    context= {
        "form": form
    }
    if form.is_valid():
        article_object = form.save() # with ModelForms only, otherwise get all fields and create
        context['form'] = ArticleForm() # to leave empty form        
        # context['object'] = article_object
        # context['created'] = True 
    return render(request, "articles/create.html", context=context)


# def article_create_view(request):
#     form = ArticleForm()
#     print(dir(form)) # to inspect all possible methods of the form
#     context= {
#         "form": form
#     }
#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         context['form'] = form # to show validation error
#         if form.is_valid():
#             title = form.cleaned_data.get("title")
#             content = form.cleaned_data.get("content")
#             print(f"title: {title}, content: {content}")
#             article_object = Article.objects.create(title=title, content=content)
#             context['object'] = article_object
#             context['created'] = True 
#     return render(request, "articles/create.html", context=context)


def article_detail_view(request, slug=None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first() 
        except:
            raise Http404
    context = {'object': article_obj}
    return render(request, "articles/detail.html", context=context)