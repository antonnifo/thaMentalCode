import markdown
from django import template
from django.utils.safestring import mark_safe
from Blog.models import Post, Category
from taggit.models import Tag



register = template.Library()


OBJECT_LIST = Post.published.all()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.inclusion_tag('site/sidebar.html')
def show_sidebar(count=5):
    return {
            'tags' : Post.tags.most_common()[:10],
            'featured' : OBJECT_LIST.filter(featured=True),
            'categories' : Category.objects.all()[:count],
            'popular_posts' : OBJECT_LIST.order_by('-hit_count_generic__hits')[:3]          
    }