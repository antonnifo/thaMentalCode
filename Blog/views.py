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
    }
 
    return render (request, 'site/index.html' ,context)

def post_detail(request, year, month, day, post):
    
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    

    latest_comments = Comment.objects.filter(active=True)[:2]
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':

        name  = request.POST['name']
        email = request.POST['email']
        body  = request.POST['message']

        new_comment = Comment(name=name, email=email,body=body)
        
        # Assign the current post to the comment
        new_comment.post = post
        
        new_comment.save()
        
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                        .exclude(id=post.id)

    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]
   
    context =   {   'post'  : post,
                    'comments': comments,
                    'new_comment': new_comment,
                    'similar_posts': similar_posts,
                    'latest_comments': latest_comments,                  
                }


    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    return render(request,
                    'site/blog-detail.html', context
                 )   

def list_category(request,tag_slug=None, category_slug=None):


    category   = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        post = OBJECT_LIST.filter(category=category)
    
    tag = None
    if tag_slug:
        tag  = get_object_or_404(Tag, slug=tag_slug)
        post = OBJECT_LIST.filter(tags__in=[tag])

    paginator = Paginator(post, 5)
    page = request.GET.get('page')

    try:

        posts = paginator.page(page)

    except PageNotAnInteger:

        # If page is not an integer deliver the first page
        posts = paginator.page(1)

    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request,
                    'site/category.html',
                    {'posts'    : posts,
                     'category' : category,
                     'page'     : page,
                     'tag'      : tag,
                    })  

def post_search(request):

    query    = None
    results = []
    
    if 's' in request.GET:

        query   = request.GET['s'] 

        search_vector = SearchVector('title', weight='A') + SearchVector('body',weight='B')
        search_query = SearchQuery(query)
                    
        results = OBJECT_LIST.annotate(
                        rank=SearchRank(search_vector, search_query)
                        ).filter(rank__gte=0.3).order_by('-rank')

        paginator = Paginator(results, 6)
        page = request.GET.get('page', 1)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:

        # If page is not an integer deliver the first page
        results = paginator.page(1)

    except EmptyPage:
        # If page is out of range deliver last page of results
        results = paginator.page(paginator.num_pages)
                
    return render(request,
                    'site/search_results.html',
                    {
                        'query': query,
                        'results': results,
                        'page': page,            
                    })