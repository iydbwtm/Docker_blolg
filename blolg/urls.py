from django.urls import path
from .views import post_list, PostListView, post_detail

app_name = 'blolg'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
]