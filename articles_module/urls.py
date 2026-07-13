from django.urls import path
from articles_module import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles_page'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('like/', views.like_comment, name='like_comment'),
    path('tag/<str:tag>/', views.ArticleListView.as_view(), name='article_tag_page'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail_page'),
]