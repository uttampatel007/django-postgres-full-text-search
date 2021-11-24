from django.contrib.postgres import search
from django.shortcuts import render
from example.models import Video
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
# Create your views here.


def index(request):

    q = request.GET.get("q")
    
    videos = Video.objects.all()
    
    # search = Video.objects.filter(title__search=q)
    
    """ in vector we can add one or multiple fields"""
    vector = SearchVector('title', 'description')
    query = SearchQuery(q)
    
    # search_results = Video.objects.annotate(search=vector).filter(search=query)

    """search rank will return all objects after ranking them [not just search]"""
    # search_results = Video.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")

    """for not returning all objects we can add filter"""
    """to not miss little relevance 0.001"""
    # search_results = Video.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by("-rank")

    """search headline - something like small description of search"""
    search_headline = SearchHeadline('description', query)
    search_results = Video.objects.annotate(
        rank=SearchRank(vector, query)
    ).annotate(
        headline=search_headline
    ).filter(rank__gte=0.001).order_by("-rank")

    context = {"videos":videos, "search":search_results}
    return render(request, 'example/index.html', context)