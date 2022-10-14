from django.contrib import admin

from  .models import Post, Comment, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'author','featured', 'publish',
                    'status')
    list_filter   = ('status', 'category', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields       = ('author',)
    date_hierarchy      = 'publish'
    list_per_page       = 10
    list_editable       = ('featured','status') 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug','publish']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'post', 'created', 'active')
    list_filter   = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    list_per_page = 20
    list_editable = ('active',) 