from django.http import HttpResponse, response
from django.template.loader import render_to_string

from articles.models import Article



def home_view(request):
    """
    Take in a request and ...
    """
    article_qs = Article.objects.all()


    context = {
        "object_list": article_qs,
    }
    HTML_STRING = render_to_string("home-view.html", context=context)
    # response = f"""
    # <h1>{title} ({id})</h1>
    # <h2>{content}</h2>
    # """.format(**context)
        
    return HttpResponse(HTML_STRING) 