from django.urls import path
from site_module import views


urlpatterns = [
    path('', views.SearchListView.as_view(), name='search_result_page'),
]