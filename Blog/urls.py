from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
     path('', views.index, name='home'),
     path('<int:year>/<int:month>/<int:day>/<slug:post>/',
                views.post_detail, name='post_detail'),
     path('tag/<slug:tag_slug>/',
            views.list_category, name='post_list_by_tag'),   
     path('category/<slug:category_slug>/',
                      views.list_category, name='post_list_by_category'), 
     path('results/', views.post_search,name='search'),                                 
]
