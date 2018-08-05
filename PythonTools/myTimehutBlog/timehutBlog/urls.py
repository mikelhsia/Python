"""
urls.py for this application
"""

from django.urls import path
from . import views

# Generating Card feed format
from .feeds import LatestCollectionsFeed

app_name = 'timehutBlog'
urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('collection/', views.collection_list, name='collection_list'),
	# path('collection/', views.CollectionView.as_view(), name='post_list'),
	path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),
	path('collection/<int:collection_id>/share/', views.collection_share, name='collection_share'),
	path('feed/', LatestCollectionsFeed(), name='collection_feed'),
]
