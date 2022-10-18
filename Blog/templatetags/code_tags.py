import markdown
from django import template
from django.utils.safestring import mark_safe
from Blog.models import Post, Category


register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


# @register.inclusion_tag('blog/blog_sidebar.html')
# def show_sidebar(count=5):
#     popular_posts = Post.objects.all().order_by('-hit_count_generic__hits')[:3]
#     return {
#         'popular_posts' : popular_posts,
#         'categories': Category.objects.order_by('-name')[:count],
#         'tags': Post.tags.most_common()[:10],
    
    
#     }