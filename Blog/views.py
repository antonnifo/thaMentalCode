from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import Category, Comment, Post


OBJECT_LIST = Post.published.all()


def index(request):

    context = {
                'posts': OBJECT_LIST[:8],
                'tags' : Post.tags.most_common()[:10],
                'featured' : OBJECT_LIST.filter(featured=True),
                'categories' : Category.objects.all()[:5],
                'popular_posts' : OBJECT_LIST.order_by('-hit_count_generic__hits')[:3]
    }
 
    return render (request, 'site/index.html' ,context=context)

   
