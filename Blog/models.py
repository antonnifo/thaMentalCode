from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from hitcount.models import HitCount
from taggit.managers import TaggableManager


class BaseContent(models.Model):
  
    publish  = models.DateTimeField(default=timezone.now)            
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    
    class Meta:
        abstract = True

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
        self).get_queryset().filter(status='published')


class Category(BaseContent):
        name = models.CharField(max_length=200)
        slug = models.SlugField(max_length=200,
                    unique=True)
                   
        class Meta:
            ordering = ('updated',)
            verbose_name = 'category'
            verbose_name_plural = 'categories'

        def __str__(self):
            return self.name

        def get_absolute_url(self):
            return reverse('blog:post_list_by_category',
               args=[self.slug])

class Post(BaseContent):
    
    published = PublishedManager() # custom manager.
    tags = TaggableManager()
    
    STATUS_CHOICES = (
                    ('draft', 'Draft'),
                    ('published', 'Published'),
                )

    title   = models.CharField(max_length=250)
    slug    = models.SlugField(max_length=250, unique_for_date='publish', help_text='Should auto fill as you add title text')
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body    = RichTextUploadingField()
    photo   = models.ImageField(upload_to='photos')
    category       = models.ForeignKey(Category,
                        related_name='posts',
                                on_delete=models.CASCADE) 
    status   = models.CharField(max_length=10, choices =STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                    related_query_name='hit_count_generic_relation')
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):

        return reverse('blog:post_detail',
                args=[self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug])


class Comment(BaseContent):

    post    = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name    = models.CharField(max_length=80)
    email   = models.EmailField()
    body    = models.TextField()
    active  = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)