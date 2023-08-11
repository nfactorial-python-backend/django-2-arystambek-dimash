from django.urls import path
from . import views
app_name = 'news'


urlpatterns = [
    path('',views.home,name = "home"),
    path('news/', views.news, name="news"),
    path('news/<int:news_id>/',views.detail, name="detail"),
    path('news/<int:news_id>/comment/',views.comment,name="comment"),
    path('news/post/',views.news_post,name="post_news")

]